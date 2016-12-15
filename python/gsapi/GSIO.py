import logging
import glob
from GSPitchSpelling import *
from GSPattern import *
from GSPatternUtils import *
import GSPitchSpelling
import os
import json  # todo: check if we need to import this library

gsiolog = logging.getLogger("gsapi.GSIO")
# gsiolog.setLevel(level=logging.INFO)


def fromMidi(midiPath,
             NoteToTagsMap="pitchNames",
             tracksToGet=None,
             TagsFromTrackNameEvents=False,
             filterOutNotMapped=True,
             checkForOverlapped=False):
    """Loads a midi file as a pattern.

    Args:
        midiPath: midi filePath
        NoteToTagsMap: dictionary converting pitches to tags
            if only interested in pitch, you can set this to "pitchNames",
            or optionally set the value to the list of string for pitches from C
            noteMapping maps classes to a list of possible mappings,
            a mapping can be either:

            * a tuple of (note, channel):
                if one of those doesnt matter it canbe replaced by '*' character
            * an integer:
                if only pitch matters

            for simplicity, one can pass only one integer (i.e not a list) for
            one to one mappings if midi track contains the name of one element
            of mapping, it'll be choosed without anyother consideration

        TagsFromTrackNameEvents: use only track names to resolve mapping,
            useful for midi containing named tracks
        filterOutNotMapped: if set to true, don't add event not represented by `NoteToTagsMap`
        tracksToGet: if not empty, specifies Midi tracks wanted either by name or index
        checkForOverlapped: if true will check that two consecutiveEvents with
            exactly same MidiNote are not overlapping
    """
    _NoteToTagsMap = __formatNoteToTags(NoteToTagsMap)
    return __fromMidiFormatted(midiPath=midiPath,
                               NoteToTagsMap=_NoteToTagsMap,
                               tracksToGet=tracksToGet,
                               TagsFromTrackNameEvents=TagsFromTrackNameEvents,
                               filterOutNotMapped=filterOutNotMapped,
                               checkForOverlapped=checkForOverlapped)


def fromMidiCollection(midiGlobPath,
                       NoteToTagsMap=defaultPitchNames,
                       tracksToGet=None,
                       TagsFromTrackNameEvents=False,
                       filterOutNotMapped=True,
                       desiredLength=0):
    """Loads a midi collection.

    Args:
        midiGlobPath: midi filePath in glob naming convention (e.g. '/folder/To/Crawl/\*.mid')
        NoteToTagsMap:
        tracksToGet:
        TagsFromTrackNameEvents:
        filterOutNotMapped:
        desiredLength: optionally cut patterns in equal length

    Returns:
        a list of GSPattern build from Midi folder
    """
    res = []
    _NoteToTagsMap = __formatNoteToTags(NoteToTagsMap)
    for f in glob.glob(midiGlobPath):
        name = os.path.splitext(os.path.basename(f))[0]
        gsiolog.info("getting " + name)
        p = fromMidi(f,
                     _NoteToTagsMap,
                     TagsFromTrackNameEvents=TagsFromTrackNameEvents,
                     filterOutNotMapped=filterOutNotMapped)
        if desiredLength > 0:
            res += p.splitInEqualLengthPatterns(desiredLength, makeCopy=False)
        else:
            res += [p]
    return res


def fromJSONFile(filePath):
    """Load a pattern to internal JSON Format.

    Args:
        filePath: filePath where to load it
    """
    with open(filePath, 'r') as f:
        return GSPattern().fromJSONDict(json.load(f))


def toJSONFile(pattern, folderPath,nameSuffix=None):
    """Save a pattern to internal JSON Format.

    Args:
        pattern: a GSPattern
        folderPath: folder where to save it, fileName will be pattern.name+nameSuffix+".json"
    """
    filePath = os.path.join(folderPath,pattern.name+(nameSuffix or "")+".json")
    if(not os.path.exists(folderPath)) : 
        os.makedirs(folderPath)
    with open(filePath, 'w') as f:
        json.dump(pattern.toJSONDict(), f,indent=1)
    return os.path.abspath(filePath)


def __formatNoteToTags(_NoteToTags):
    """Internal conversion for consistent NoteTagMap structure."""

    import copy
    NoteToTags = copy.copy(_NoteToTags)
    if NoteToTags == "pitchNames":
        NoteToTags = {"pitchNames": ""}
    for n in NoteToTags:
        if n == "pitchNames":
            if not NoteToTags["pitchNames"]:
                NoteToTags["pitchNames"] = defaultPitchNames
        else:
            if not isinstance(NoteToTags[n], list):
                NoteToTags[n] = [NoteToTags[n]]
            for i in range(len(NoteToTags[n])):
                if isinstance(NoteToTags[n][i], int):
                    NoteToTags[n][i] = (NoteToTags[n][i], "*")
    return NoteToTags


def __fromMidiFormatted(midiPath,
                        NoteToTagsMap,
                        tracksToGet=None,
                        TagsFromTrackNameEvents=False,
                        filterOutNotMapped=True,
                        checkForOverlapped=False):
    """
    Internal function that accepts only consistent NoteTagMap
    structure as created by __formatNoteToTags.
    """
    import math
    import midi
    import os

    globalMidi = midi.read_midifile(midiPath)
    
    globalMidi.make_ticks_abs()
    pattern = GSPattern()
    pattern.resolution = globalMidi.resolution # hide it in pattern to be able to retrieve it when exporting
    pattern.name = os.path.basename(midiPath)

        # boolean to avoid useless string creation
    extremeLog = gsiolog.getEffectiveLevel()<=logging.DEBUG

    # get time signature first
    gsiolog.info("start processing %s" % pattern.name)
    __findTimeInfoFromMidi(pattern, globalMidi)

    tick_to_quarter_note = 1.0 / globalMidi.resolution

    pattern.events = []
    lastNoteOff = 0
    notFoundTags = []
    trackIdx = 0

    for tracks in globalMidi:
        shouldSkipTrack = False
        lastPitch = -1
        lastTick = -1
        for e in tracks:
            if shouldSkipTrack:
                continue

            if not TagsFromTrackNameEvents:
                noteTags = []

            if midi.MetaEvent.is_event(e.statusmsg):
                if e.metacommand == midi.TrackNameEvent.metacommand:
                    if tracksToGet and not((e.text in tracksToGet) or (trackIdx in tracksToGet)):
                        gsiolog.info("skipping track: %i %s" % (trackIdx, e.text))
                        shouldSkipTrack = True
                        continue
                    else:
                        gsiolog.info(pattern.name + ": getting track: %i %s" % (trackIdx, e.text))

                    if TagsFromTrackNameEvents:
                        noteTags = __findTagsFromName(e.text, NoteToTagsMap)

            isNoteOn = midi.NoteOnEvent.is_event(e.statusmsg)
            isNoteOff = midi.NoteOffEvent.is_event(e.statusmsg)

            if isNoteOn or isNoteOff:
                pitch = e.pitch  # optimize pitch property access
                tick = e.tick
                velocity = e.get_velocity()
                if velocity==0:
                    isNoteOff =True
                    isNoteOn = False

                curBeat = tick * 1.0 * tick_to_quarter_note
                if noteTags == []:
                    if TagsFromTrackNameEvents:
                        continue
                    noteTags = __findTagsFromPitchAndChannel(pitch, e.channel, NoteToTagsMap)

                if noteTags == []:
                    if [e.channel, pitch] not in notFoundTags:
                        gsiolog.info(pattern.name + ": no tags found for "
                                                    "pitch %d on channel %d" % (pitch, e.channel))
                        notFoundTags += [[e.channel, pitch]]
                    if filterOutNotMapped:
                        continue

                if isNoteOn:
                    # ignore duplicated events (can't have 2 simultaneous NoteOn for the same pitch)
                    
                    if pitch == lastPitch and tick == lastTick:
                        gsiolog.info(pattern.name + ": skip duplicated event: %i %f" % (pitch, curBeat))
                        continue
                    lastPitch = pitch
                    lastTick = tick
                    if extremeLog : gsiolog.debug("on %d %f"%(pitch, curBeat))
                    pattern.events += [GSPatternEvent(startTime=curBeat,
                                                      duration=-1,
                                                      pitch=pitch,
                                                      velocity=velocity,
                                                      tags=noteTags)]

                if isNoteOff:
                    if extremeLog: gsiolog.debug( "off %d %f"%(pitch,curBeat))
                    foundNoteOn = False
                    for i in reversed(pattern.events):

                        if (i.pitch == pitch) and (i.tags==noteTags) and ((isNoteOff and(curBeat >= i.startTime))or curBeat>i.startTime) and i.duration<=0.0001:
                            foundNoteOn = True

                            i.duration = max(0.0001,curBeat - i.startTime)
                            lastNoteOff = max(curBeat,lastNoteOff)
                            gsiolog.info("set duration %f at start %f "%(i.duration,i.startTime))
                            break
                    if not foundNoteOn and midi.NoteOffEvent.is_event(e.statusmsg):
                        gsiolog.warning(pattern.name + ": not found note on " + str(e) + str(pattern.events[-1]))
        trackIdx += 1

    elementSize = 4.0 / pattern.timeSignature[1]
    barSize = pattern.timeSignature[0] * elementSize
    lastBarPos = math.ceil(lastNoteOff*1.0/barSize) * barSize
    pattern.duration = lastBarPos
    if checkForOverlapped:
        pattern.removeOverlapped(usePitchValues=True)

    return pattern


def __findTimeInfoFromMidi(pattern, midiFile):

    import midi

    foundTimeSignatureEvent = False
    foundTempo = False
    pattern.timeSignature = (4, 4)
    pattern.bpm = 60

    for tracks in midiFile:
        for e in tracks:
            
            if midi.MetaEvent.is_event(e.statusmsg):
                if e.metacommand == midi.TimeSignatureEvent.metacommand:
                    if foundTimeSignatureEvent and (pattern.timeSignature != (e.numerator, e.denominator)):
                        gsiolog.error(pattern.name + ": multiple time "
                                                     "signature found, not supported, "
                                                     "result can be alterated")
                    foundTimeSignatureEvent = True
                    pattern.timeSignature = (e.numerator, e.denominator)
                    #  e.metronome = e.thirtyseconds ::  do we need that ???
                elif e.metacommand == midi.SetTempoEvent.metacommand:
                    if foundTempo:
                        gsiolog.error(pattern.name+": multiple bpm found, not supported")
                    foundTempo = True
                    pattern.bpm = e.bpm

        if foundTimeSignatureEvent:
            # pass
            break
    if not foundTimeSignatureEvent:
        gsiolog.warning(pattern.name + ": no time signature event found")


def __findTagsFromName(name, noteMapping):
    res = []
    for l in noteMapping:
        if l in name:
            res += [l]
    return res


def __findTagsFromPitchAndChannel(pitch, channel, noteMapping):
    """
    def pitchToName(pitch, pitchNames):
        octaveLength = len(pitchNames)
        # octave  = (pitch / octaveLength) - 2  # 0 is C-2
        octave = (pitch / octaveLength) - 1  # 0 is C-1
        note = pitch % octaveLength
        # return  pitchNames[note] + "_" + str(octave) martin NOTATION
        return  pitchNames[note] + str(octave) # STANDARD NOTATION (ANGEL)
        """
    if "pitchNames" in noteMapping.keys():
        return [pitch2name(pitch, noteMapping["pitchNames"])]

    res = []
    for l in noteMapping:
        for le in noteMapping[l]:
            if (le[0] in {"*", pitch}) and (le[1] in {"*", channel}):
                res += [l]
    return res


def toMidi(gspattern, midiMap=None, folderPath="output/", name="test"):
    """ Function to write GSPattern instance to MIDI.

    Args:
        midiMap: mapping used to translate tags to MIDI pitch
        folderPath: folder where MIDI file is stored
        name: name of the file
    """

    import midi 
    # Instantiate a MIDI Pattern (contains a list of tracks)
    pattern = midi.Pattern(tick_relative=False,format=1)
    pattern.resolution=gspattern.resolution or 960
    # Instantiate a MIDI Track (contains a list of MIDI events)
    track = midi.Track(tick_relative=False)
    
    
    track.append(midi.TimeSignatureEvent(numerator = gspattern.timeSignature[0],denominator=gspattern.timeSignature[1]))
    # obscure events
    # timeSignatureEvent.set_metronome(32)
    # timeSignatureEvent.set_thirtyseconds(4)
    
    track.append(midi.TrackNameEvent(text= gspattern.name))

    track.append(midi.SetTempoEvent(bpm=gspattern.bpm))

    # Append the track to the pattern
    pattern.append(track)
    beatToTick = pattern.resolution 
    for e in gspattern.events:

        startTick = int(beatToTick  * e.startTime)
        endTick   = int(beatToTick  * e.getEndTime()) 
        pitch = e.pitch
        channel=1
        if midiMap:
            pitch = midiMap[e.tags[0]]
        if midiMap is None:
            track.append(midi.NoteOnEvent(tick=startTick, velocity=e.velocity, pitch=pitch,channel=channel))
            track.append(midi.NoteOffEvent(tick=endTick, velocity=e.velocity, pitch=pitch,channel=channel))

    track.append(midi.EndOfTrackEvent(tick=int(gspattern.duration * beatToTick)))



    # make tick relatives
    track.sort(key=lambda e:e.tick)
    track.make_ticks_rel()

    # Save the pattern to disk

    if(not os.path.exists(folderPath)) : 
        os.makedirs(folderPath)
    if not ".mid" in name:
        name+=".mid"
    exportedPath = os.path.join(folderPath,name)
    
    midi.write_midifile(exportedPath, pattern)
    return exportedPath

"""
    # Import the library
    from midiutil.MidiFile import MIDIFile

    # Create the MIDIFile Object with 1 track
    MyMIDI = MIDIFile(1, adjust_origin=False)

    # Tracks are numbered from zero. Times are measured in beats.
    track = 0
    time = 0

    # Add track name and tempo.
    MyMIDI.addTrackName(track, time, "Sample Track")

    MyMIDI.addTempo(track, time, gspattern.bpm)

    # Add a note. addNote expects the following information:
    track = 0
    channel = 0

    # Now add the note.
    for e in gspattern.events:
        if midiMap is None:
            MyMIDI.addNote(track, channel, e.pitch, e.startTime, e.duration, e.velocity)
        else:
            MyMIDI.addNote(track, channel, midiMap[e.tags[0]], e.startTime, e.duration, e.velocity)

    # And write it to disk.
    binfile = open(path + name + ".mid", 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()

    """
