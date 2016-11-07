import logging
import glob
import os
from gsapi import *
import math
from MidiMap import *

gsiolog = logging.getLogger("gsapi.GSIO")
gsiolog.setLevel(level=logging.INFO)

def fromMidi(midiPath,
             NoteToTagsMap=defaultPitchNames, # find out if midimap is better!
             tracksToGet=[],  #TODO: unnecessary parameter??
             TagsFromTrackNameEvents=False,
             filterOutNotMapped=True,
             checkForOverlapped=False):
    """Loads a midi file as a pattern.

    Args:
        midiPath: midi filePath
        NoteToTagsMap: dictionary converting pitches to tags
            if only interested in pitch, you can set this to "pitchNames",
            or optionaly set the value to the list of string for pitches from C.
            noteMapping maps classes to a list of possible Mappings,
            a mapping can be:
            a tuple of (note, channel)
                if one of those doesnt matter it canbe replaced by '*' character
            an integer
                if only pitch matters
            for simplicity, one can pass only one integer (i.e not a list) for one to one mappings
            if midi track contains the name of one element of mapping,
            it'll be choosed without anyother consideration

        TagsFromTrackNameEvents: use only track names to resolve mapping,
            useful for midi containing named tracks
        filterOutNotMapped: if set to true, don't add event not represented by `NoteToTagsMap`
        tracksToGet: if not empty, specifies tracks wanted either by name or index
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
                       tracksToGet=[],
                       TagsFromTrackNameEvents=False,
                       filterOutNotMapped=True,
                       desiredLength=0):
    """Loads a midi collection.

    Args:
        midiGlobPath: midi filePath in glob naming convention (e.g. '/folder/To/Crawl/*.mid')
        desiredLength: optionally cut patterns in equal length
        otherArguments: as defined in :py:func:`fromMidi`

    Returns:
        a list of GSPattern build from Midi folder
    """
    res = []
    _NoteToTagsMap = __formatNoteToTags(NoteToTagsMap)
    for f in glob.glob(midiGlobPath):
        name = os.path.splitext(os.path.basename(f))[0]
        gsiolog.info( "getting " + name)
        p = fromMidi(f,
                     _NoteToTagsMap,
                     TagsFromTrackNameEvents=TagsFromTrackNameEvents,
                     filterOutNotMapped=filterOutNotMapped)
        if desiredLength > 0:
            res += p.splitInEqualLengthPatterns(desiredLength, copy=False)
        else:
            res += [p]
    return res

def PatternFromJSONFile(filePath):
    """Load a pattern to internal JSON Format

    Args:
        filePath: filePath where to load it
    """
    with open(filePath, 'r') as f:
        return GSPattern().fromJSONDict(json.load(f))

def PatternToJSONFile(pattern, filePath):
    """Save a pattern to internal JSON Format.

    Args:
        filePath: filePath where to save it
    """
    with open(filePath,'w') as f:
        return json.dump(pattern.toJSONDict(),f)

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
                if isinstance(NoteToTags[n][i],int):
                    NoteToTags[n][i] = (NoteToTags[n][i], '*')
    return NoteToTags

def __fromMidiFormatted(midiPath,
                        NoteToTagsMap,
                        tracksToGet=[],
                        TagsFromTrackNameEvents=False,
                        filterOutNotMapped=True,
                        checkForOverlapped=False):
    """
    Internal function that accept only consistent NoteTagMap structure as
    created by __formatNoteToTags.
    """
    import midi
    import os

    globalMidi = midi.read_midifile(midiPath)
    globalMidi.make_ticks_abs()
    pattern = GSPattern()
    pattern.name = os.path.basename(midiPath)

    # get time signature first
    gsiolog.info("start processing %s" % pattern.name)
    __findTimeInfoFromMidi(pattern, globalMidi)

    tick_to_quarter_note = 1.0 / (globalMidi.resolution)

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
                    if tracksToGet != [] and not((e.text in tracksToGet) or (
                                trackIdx in tracksToGet)):
                        gsiolog.info('skipping track: %i %s' % (trackIdx,
                                                               e.text))
                        shouldSkipTrack = True
                        continue
                    else:
                        gsiolog.info(pattern.name + ' : getting track : %i '
                                                   '%s' % (trackIdx,e.text))

                    if TagsFromTrackNameEvents:
                        noteTags = __findTagsFromName(e.text, NoteToTagsMap)

            isNoteOn = midi.NoteOnEvent.is_event(e.statusmsg)
            isNoteOff =midi.NoteOffEvent.is_event(e.statusmsg)

            if isNoteOn or isNoteOff:
                pitch = e.pitch # optimize pitch property access
                tick = e.tick
                curBeat = tick * 1.0 * tick_to_quarter_note
                if noteTags == []:
                    if TagsFromTrackNameEvents:
                        continue
                    noteTags = __findTagsFromPitchAndChannel(pitch,
                                                             e.channel,
                                                             NoteToTagsMap)

                if noteTags == []:
                    if ([e.channel, pitch] not in notFoundTags):
                        gsiolog.info(pattern.name + ": no tags found for "
                                                   "pitch %d on channel %d"
                                      %(pitch,
                                        e.channel))
                        notFoundTags += [[e.channel, pitch]]
                    if filterOutNotMapped:
                        continue

                if isNoteOn:
                    # ignore duplicated events (can't have 2 simultaneous NoteOn for the same pitch)
                    if  pitch == lastPitch and tick == lastTick:
                        gsiolog.info(pattern.name + ': skip duplicated event: '
                                                   '%i %f' % (pitch, curBeat))
                        continue
                    lastPitch = pitch
                    lastTick = tick
                    # print "on"+str(pitch)+":"+str( tick*1.0*tick_to_quarter_note)
                    pattern.events += [GSPatternEvent(startTime=curBeat,
                                                      duration=-1,
                                                      pitch=pitch,
                                                      velocity=127,
                                                      tags=noteTags)]

                if isNoteOn or isNoteOff:
                    # print "off"+str(pitch)+":"+str( tick*1.0*tick_to_quarter_note)
                    foundNoteOn = False
                    for i in reversed(pattern.events):

                        if (i.pitch == pitch) and (i.tags==noteTags) and curBeat >= i.startTime and i.duration<=0.0001:
                            foundNoteOn = True

                            i.duration = max(0.0001,curBeat - i.startTime)
                            lastNoteOff = max(curBeat,lastNoteOff)
                            # print "set duration "+str(i.duration) + "at start " + str(i.startTime)
                            break
                    if not foundNoteOn and midi.NoteOffEvent.is_event(e.statusmsg):
                        gsiolog.warning(pattern.name + ": not found note on " + str(e) + str(pattern.events[-1]))
        trackIdx+=1

    elementSize = 4.0 / pattern.timeSignature[1]
    barSize = pattern.timeSignature[0] * elementSize
    lastBarPos = math.ceil(lastNoteOff*1.0/barSize) * barSize
    pattern.duration = lastBarPos

    if(checkForOverlapped):
        pattern.removeOverlapped(usePitchValues=True)

    return pattern


def __findTimeInfoFromMidi(pattern, midiFile):

    import midi

    foundTimeSignatureEvent = False
    foundTempo = False
    pattern.timeSignature = [4, 4]
    pattern.bpm = 60

    for tracks in midiFile:
        for e in tracks:
            if midi.MetaEvent.is_event(e.statusmsg):
                if e.metacommand == midi.TimeSignatureEvent.metacommand:
                    if foundTimeSignatureEvent and (pattern.timeSignature != [e.numerator, e.denominator]):
                        gsiolog.error(pattern.name + ": multiple time "
                                                    "signature found, not supported, result can be alterated")
                    foundTimeSignatureEvent = True
                    pattern.timeSignature = [e.numerator, e.denominator]
                    #  e.metronome = e.thirtyseconds ::  do we need that ???
                elif e.metacommand == midi.SetTempoEvent.metacommand:
                    if foundTempo:
                        gsiolog.error(pattern.name+": multiple bpm found, not supported")
                    foundTempo = True
                    pattern.bpm = e.bpm

        if foundTimeSignatureEvent:
            break
    if not foundTimeSignatureEvent:
        gsiolog.warning(pattern.name + ": no time signature event found")


def __findTagsFromName(name, noteMapping):

    res =[]
    for l in noteMapping:
        if l in name: res += [l];
    return res


def __findTagsFromPitchAndChannel(pitch, channel, noteMapping):

    def pitchToName(pitch, pitchNames):
        octaveLength = len(pitchNames)
        # octave  = (pitch / octaveLength) - 2  # 0 is C-2
        octave = (pitch / octaveLength) - 1  # 0 is C-1
        note = pitch % octaveLength
        # return  pitchNames[note] + "_" + str(octave) martin NOTATION
        return  pitchNames[note] + str(octave) # STANDARD NOTATION (ANGEL)

    if "pitchNames" in noteMapping.keys():
        return [pitchToName(pitch, noteMapping["pitchNames"])]

    res = []
    for l in noteMapping:
        for le in noteMapping[l]:
            if (le[0] in {'*', pitch}) and (le[1] in {'*', channel}):
                res += [l]
    return res
