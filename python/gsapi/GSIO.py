from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import logging
import glob
from .GSPitchSpelling import *
from .GSPattern import *
from .GSPatternUtils import *
from . import GSPitchSpelling
import os,sys
import json  
if sys.version_info >= (3,0):
    import pickle
else:
    import cPickle as pickle
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


def fromJSONFile(filePath,conserveTuple=False):
    """Load a pattern to internal JSON Format.

    Args:
        filePath: filePath where to load it
    """


    def hinted_tuple_hook(obj):
        # print obj
        
        if isinstance(obj, list):return [hinted_tuple_hook(e) for e in obj]
        if isinstance(obj, dict):
            if '__tuple__' in obj:return tuple(obj['items'])
            return {k:hinted_tuple_hook(e) for k,e in obj.items()}
        else:
            return obj

    with open(filePath, 'r') as f:
        return GSPattern().fromJSONDict(json.load(f,object_hook=hinted_tuple_hook if conserveTuple else None))



def toJSONFile(pattern, folderPath,useTagIndexing=True,nameSuffix=None,conserveTuple = False):
    """Save a pattern to internal JSON Format.

    Args:
        pattern: a GSPattern
        folderPath: folder where to save it, fileName will be pattern.name+nameSuffix+".json"
        nameSuffix : string to append to name of the file
        useTagIndexing: if true, tags are stored as indexes from a list of all tags (reduce size of json files)
        ConserveTuple : useful if some tags can be tuple but much slower
    """

    filePath = os.path.join(folderPath,pattern.name+(nameSuffix or "")+".json")
    if(not os.path.exists(folderPath)) : 
        os.makedirs(folderPath)


    class TupleEncoder(json.JSONEncoder):
        """ encoder conserving tuple type info"""
        def checkTuple(self,item):
            if isinstance(item, tuple):return {'__tuple__': True, 'items': item}
            if isinstance(item, list):return [self.checkTuple(e) for e in item]
            if isinstance(item, dict):return {k:self.checkTuple(e) for k,e in item.items()}
            else:return item

        def iterencode(self,item):
            return json.JSONEncoder.iterencode(self, self.checkTuple(item))

    encoderClass =  TupleEncoder if conserveTuple else None;
    with open(filePath, 'w') as f:
        json.dump(pattern.toJSONDict(useTagIndexing=useTagIndexing), f,cls=encoderClass,indent=1,separators=(',', ':'))
    return os.path.abspath(filePath)

def fromPickleFile(filePath):
    """Load a pattern from pickle Format.

    Args:
        filePath: filePath where to load it
    """
    with open(filePath, 'rb') as f:
        return pickle.load(f)

def toPickleFile(pattern,folderPath,nameSuffix=None):
    """Save a pattern to python's pickle Format.

    Args:
        pattern: a GSPattern
        folderPath: folder where to save it, fileName will be pattern.name+nameSuffix+".json"
        nameSuffix : string to append to name of the file
    """
    filePath = os.path.join(folderPath,pattern.name+(nameSuffix or "")+".pickle")
    if(not os.path.exists(folderPath)) : 
        os.makedirs(folderPath)
    with open(filePath, 'wb') as f:
        pickle.dump(pattern, f)
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
    trackDuration = None
    for tracks in globalMidi:
        shouldSkipTrack = False
        for e in tracks:
            if shouldSkipTrack:
                continue

            if not TagsFromTrackNameEvents:
                noteTag = ()

            if midi.MetaEvent.is_event(e.statusmsg):
                if e.metacommand == midi.TrackNameEvent.metacommand:
                    if tracksToGet and not((e.text in tracksToGet) or (trackIdx in tracksToGet)):
                        gsiolog.info("skipping track: %i %s" % (trackIdx, e.text))
                        shouldSkipTrack = True
                        continue
                    else:
                        gsiolog.info(pattern.name + ": getting track: %i %s" % (trackIdx, e.text))

                    if TagsFromTrackNameEvents:
                        noteTag = __findTagsFromName(e.text, NoteToTagsMap)

            if midi.EndOfTrackEvent.is_event(e.statusmsg):
                thisDuration = e.tick * tick_to_quarter_note
                trackDuration = max(trackDuration,thisDuration) if trackDuration else thisDuration
                continue

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
                if not noteTag:
                    if TagsFromTrackNameEvents:
                        continue
                    noteTag = __findTagsFromPitchAndChannel(pitch, e.channel, NoteToTagsMap)

                if not noteTag:
                    if [e.channel, pitch] not in notFoundTags:
                        gsiolog.info(pattern.name + ": no tags found for "
                                                    "pitch %d on channel %d" % (pitch, e.channel))
                        notFoundTags += [[e.channel, pitch]]
                    if filterOutNotMapped:
                        continue

                if isNoteOn:
                    if extremeLog : gsiolog.debug("on %d %f"%(pitch, curBeat))
                    pattern.events += [GSPatternEvent(startTime=curBeat,
                                                      duration=-1,
                                                      pitch=pitch,
                                                      velocity=velocity,
                                                      tag=noteTag)]

                if isNoteOff:
                    if extremeLog: gsiolog.debug( "off %d %f"%(pitch,curBeat))
                    foundNoteOn = False
                    isTrueNoteOff = midi.NoteOffEvent.is_event(e.statusmsg)
                    for i in reversed(pattern.events):

                        if (i.pitch == pitch) and (i.tag==noteTag) and ((isTrueNoteOff and(curBeat >= i.startTime))or curBeat>i.startTime) and i.duration<=0.0001:
                            foundNoteOn = True

                            i.duration = max(0.0001,curBeat - i.startTime)
                            lastNoteOff = max(curBeat,lastNoteOff)
                            gsiolog.info("set duration %f at start %f "%(i.duration,i.startTime))
                            break
                    if not foundNoteOn :

                        gsiolog.warning(pattern.name + ": not found note on\n %s\n%s\n%s , %s "% (e,pattern.events[-1],noteTag,curBeat))
                        
        trackIdx += 1

    elementSize = 4.0 / pattern.timeSignature[1]
    barSize = pattern.timeSignature[0] * elementSize
    lastBarPos = math.ceil(lastNoteOff*1.0/barSize) * barSize
    pattern.duration = trackDuration or lastBarPos
    if checkForOverlapped:
        pattern.removeOverlapped(usePitchValues=True)

    return pattern


def __findTimeInfoFromMidi(pattern, midiFile):

    import midi

    foundTimeSignatureEvent = False
    foundTempo = False
    pattern.timeSignature = (4, 4)
    pattern.bpm = 60
    pattern.resolution = midiFile.resolution # hide it in pattern to be able to retrieve it when exporting

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
        gsiolog.info(pattern.name + ": no time signature event found")


def __findTagsFromName(name, noteMapping):
    res = tuple()
    for l in noteMapping:
        if l in name:
            res += [l]
    return res


def __findTagsFromPitchAndChannel(pitch, channel, noteMapping):
    
    if "pitchNames" in noteMapping.keys():
        return pitch2name(pitch, noteMapping["pitchNames"])

    res = tuple()
    for l in noteMapping:
        for le in noteMapping[l]:
            if (le[0] in {"*", pitch}) and (le[1] in {"*", channel}):
                res += (l,)
    if len(res)==1:
        return res[0]
    return res


def toMidi(gspattern, midiMap=None, folderPath="output/", name=None):
    """ Function to write GSPattern instance to MIDI.

    Args:
        midiMap: mapping used to translate tags to MIDI pitch
        folderPath: folder where MIDI file is stored
        name: name of the file
    """

    import midi 
    # Instantiate a MIDI Pattern (contains a list of tracks)
    pattern = midi.Pattern(tick_relative=False,format=1)
    pattern.resolution=getattr(gspattern,'resolution' , 960)
    
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
            pitch = midiMap[e.tag[0]]
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
    name = name or gspattern.name
    name = name or "test"
    if not ".mid" in name:
        name+=".mid"
    exportedPath = os.path.join(folderPath,name)
    
    midi.write_midifile(exportedPath, pattern)
    return exportedPath

