from __future__ import absolute_import,division,print_function

import math
import copy
import logging
import collections
from .GSPitchSpelling import *

# logger for pattern related operations
patternLog = logging.getLogger("gsapi.GSPattern")


class GSPatternEvent(object):
    """Represent an event of a GSPattern with startTime, duration, pitch,
    velocity and tag variables.

    Class variables:
        startTime: startTime of event
        duration: duration of event
        pitch: pitch of event
        velocity: velocity of event
        tag: any hashable object representing the event , i.e strings, tuples, objects (but not lists) 
        originPattern : keeps track of origin pattern for events generated from pattern, example a chord event can still access to its individual components via originPattern (see GSPattern.generateViewpoints)
    """
    def __init__(self, startTime=0, duration=1, pitch=60, velocity=80, tag=None,originPattern=None):
        self.duration = duration
        self.startTime = startTime

        self.originPattern = originPattern 
        if not tag: 
            self.tag = ()
        elif isinstance(tag,list):
            patternLog.error("tag cannot be list, converting to tuple")
            self.tag = tuple(tag)

        elif not isinstance(tag, collections.Hashable):
            patternLog.error("tag has to be hashable, trying conversion to tuple")
            self.tag = (tag,)
        else:
            self.tag = tag

        
        self.pitch = pitch
        self.velocity = velocity
        

    def __repr__(self):
        return "%s %i %i %05.4f %05.4f" % (self.tag,
                                           self.pitch,
                                           self.velocity,
                                           self.startTime,
                                           self.duration)

    def __eq__(self, other):
        if isinstance(other, GSPatternEvent):
            return (self.startTime == other.startTime) and (self.pitch == other.pitch) and (self.velocity==other.velocity) and (self.duration==other.duration) and (self.tag==other.tag)
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result


    
    def hasOneCommonTagWith(self, event):
        """Compare tags between events.

        Args:
            event: event to compare with
        Returns:
            True if at least one tag is equal
        """
        # if type(self.tag)!=type(event.tag):
        #     return False
        return self.hasOneOfTags(event.tag)

    def hasOneOfTags(self, tags):
        """Compare this event's tags with a list of possible tag.

        Args:
            tags: list of tags to compare with
        Returns:
            True if at least one tag is equal
        """
        for t in tags:
            if (t==self.tag) or (t in self.tag):
                return True
        return False

    def tagIs(self, tag):
        """Compare this event's tag with a a given tag.

        Args:
            tag: tag to compare with
        Returns:
            True if all event tag is equal to given tag
        """
        return self.tag == tag

    def allTagsAreEqualWith(self, event):
        """Compare this event's tag with an other event.

        Args:
            event: event to compare with
        Returns:
            True if tags are equal
        """
        self.tagIs(event.tag)

    def getEndTime(self):
        """Return the time when this events ends

        Returns:
            The time when this event ends
        """
        return self.startTime + self.duration

    def copy(self):
        """ Copy an event.

        Returns:
            A deep copy of this event to be manipulated without changing
            original.
        """
        return copy.deepcopy(self)

    def cutInSteps(self, stepSize):
        """ Cut an event in steps of stepsize length.

        Args:
            stepSize: the desired size of each produced events
        Returns:
            a list of events of length `stepSize`
        """
        res = []
        num = max(1, int(self.duration / stepSize))  # if smaller still take it
        for i in range(num):
            newE = self.copy()
            newE.startTime = self.startTime + i * stepSize
            newE.duration = stepSize
            res += [newE]
        return res


    def containsTime(self, time):
        """Return true if event is active at given time

        Args:
            time: time to compare with
        """
        return (time >= self.startTime) and (time < self.startTime + self.duration)




# ============================
# GSPattern Class Declaration
# ============================


class GSPattern(object):
    """Class representing a pattern made of GSPatternEvent.
    Holds a list of GSEvents and provide basic manipulation function.

    Class Variables:
        duration: length of pattern. Usually in beats, but time scale is up to
         the user (it can be useful if working on 32th note steps).
        events: list of GSPatternEvent for this pattern.
        bpm: initial tempo in beats per minute for this pattern (default: 120).
        timeSignature: list of integers representing the time signature,
         i.e [numerator, denominator].
         startTime : startTimeof pattern (useful when splitting in sub patterns)
         viewPoints: dict of GSViewPoint
    """
    def __init__(self,
                 duration=0,
                 events=None,
                 bpm=120,
                 timeSignature=(4, 4),  # changed list to tuple.
                 key="C",
                 originFilePath="",
                 name=""):
        self.duration = duration
        if events:
            self.events = events
        else:
            self.events = []
        self.viewpoints = {}
        self.bpm = bpm
        self.timeSignature = timeSignature
        self.key = key
        self.originFilePath = originFilePath
        self.name = name
        self.startTime =0
        self.originPattern = None

    def __repr__(self):
        """Nicely print out the list of events.
        Each line represents an event formatted as "[tag] pitch velocity startTime duration"
        """
        s = "GSPattern %s : duration: %.2f,bpm: %.2f,time signature: %d/%d\n" % (self.name,self.duration,self.bpm,self.timeSignature[0],self.timeSignature[1])
        for e in self.events:
            s += str(e) + "\n"
        return s

    def __len__(self):
        return len(self.events)

    def __getitem__(self, index):
        """Utility to access events as list member: GSPattern[idx] = GSPattern.events[idx]
        """
        return self.events[index]

    def __eq__(self, other):
        if isinstance(other, GSPattern):
            return (self.events == other.events) and (self.duration == other.duration) and (self.timeSignature==other.timeSignature) and (self.startTime==other.startTime)
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __setitem__(self, index, item):
        self.events[index] = item

    def applyLegato(self, usePitchValues=False):
        """ this function supress the possible silences in this pattern by stretching consecutive identical events
         (i.e identical tags or pitch values)
        Args:
            usePitchValues: should we consider pitch numbers instead of tags (bit faster)
        """

        def _perVoiceLegato(pattern):
            
            pattern.reorderEvents()
            if len(pattern) == 0:
                patternLog.warning("try to apply legato on an empty voice")

                return
            for idx in range(1, len(pattern)):
                
                diff = pattern[idx].startTime - pattern[idx-1].getEndTime()
                if diff > 0:
                    pattern[idx-1].duration += diff

            diff = pattern.duration - pattern[-1].getEndTime()
            if diff > 0:
                pattern[-1].duration += diff

        if usePitchValues:
            for p in self.getAllPitches():
                voice = self.getPatternWithPitch(p)
                _perVoiceLegato(voice)
        for t in self.getAllTags():
            voice = self.getPatternWithTags(tagToLookFor=t, exactSearch=False, makeCopy=False)
            _perVoiceLegato(voice)

    def transpose(self, interval):
        """Transposes a GSPattern to the desired interval

                Args:
                    interval: transposition factor in semitones
                    (it can be a positive or negative int)
                """
        for e in self.events:
            e.pitch += interval
            e.tag = [pitch2name(e.pitch, defaultPitchNames)]
        # return self

    def setDurationFromLastEvent(self, onlyIfBigger=True):
        """Sets duration to last event NoteOff

        Args:
            onlyIfBigger: update duration only if last Note off is bigger
        if inner events have a bigger time span than self.duration, increase duration to fit
        """
        total = self.getLastNoteOff()
        if total and (total > self.duration or not onlyIfBigger):
            self.duration = total

    def reorderEvents(self):
        """Ensure than our internal event list `events` is time sorted.
        It can be useful for time sensitive events iteration.
        """
        self.events.sort(key=lambda x: x.startTime, reverse=False)

    def getLastNoteOff(self):
        """Gets last event end time

        Returns:
            lastNoteOff, i.e the time corresponding to the end of the last event
        """
        if len(self.events):
            self.reorderEvents()
            return self.events[-1].duration + self.events[-1].startTime
        else:
            return None

    def addEvent(self, event):
        """Add an event increasing duration if needed.

        Args:
            event: the GSPatternEvent to be added
        """
        self.events += [event]
        self.setDurationFromLastEvent()

    def removeEvent(self, event):
        """remove given event
        Args:
            event: the GSPatternEvent to be added
        """
        idxToRemove = []
        idx = 0
        for e in self.events:
            if event == e :
                idxToRemove += [idx]
            idx += 1

        for i in idxToRemove:
            del self.events[i]

    def removeByTags(self, tags):
        """Remove all event(s) in a pattern with specified tag(s).

        Args:
            tags: list of tag(s)
        """
        for e in self.events:
            if e.hasOneOfTags(tuple(tags)):
                self.removeEvent(e)

    def quantize(self, stepSize, quantizeStartTime=True, quantizeDuration=True):
        """ Quantize events.

        Args:
            stepSize: the duration that we want to quantize to
            quantizeDuration: do we quantize duration?
            quantizeStartTime: do we quantize startTimes
        """
        beatDivision = 1.0 / stepSize
        if quantizeStartTime and quantizeDuration:
            for e in self.events:
                e.startTime = int(e.startTime * beatDivision) * 1.0 / beatDivision
                e.duration = int(e.duration * beatDivision) * 1.0 / beatDivision
        elif quantizeStartTime:
            for e in self.events:
                e.startTime = int(e.startTime * beatDivision) * 1.0 / beatDivision
        elif quantizeDuration:
            for e in self.events:
                e.duration = int(e.duration * beatDivision) * 1.0 / beatDivision

    def timeStretch(self, ratio):
        """Time-stretch a pattern.

        Args:
            ratio: the ratio used for time stretching
        """
        for e in self.events:
            e.startTime *= ratio
            e.duration *= ratio
        self.duration *= ratio

    def getStartingEventsAtTime(self, time, tolerance=0):
        """ Get all events activating at a given time.

        Args:
            time: time asked for
            tolerance: allowed deviation of start time
        Returns:
            list of events
        """
        res = []
        for e in self.events:
            if(time - e.startTime >= 0 and time - e.startTime <= tolerance):
                res += [e]
        return res

    def getActiveEventsAtTime(self, time, tolerance=0):  # todo: either implement or remove tolerance
        """ Get all events currently active at a givent time.

        Args:
            time: time asked for
            tolerance: admited deviation of start time
        Returns:
            list of events
        """
        res = []
        for e in self.events:
            if(time - e.startTime >= 0 and time - e.startTime < e.duration):
                res += [e]
        return res

    def copy(self):
        """Deepcopy a pattern
        """
        return copy.deepcopy(self)

    def getACopyWithoutEvents(self):
        """Copy all fields but events.
            Useful for creating patterns from patterns.
        """
        p = GSPattern()
        p.duration = self.duration
        p.bpm = self.bpm
        p.timeSignature = self.timeSignature
        p.originFilePath = self.originFilePath
        p.name = self.name
        return p

    def getAllTags(self):
        """ Returns all used tags in this pattern.

        Returns:
            set of tags composed of all possible tags
        """
        tagsList = []
        for e in self.events:
            tagsList += [e.tag]
        tagsList = set(tagsList)
        return tagsList

    def getAllPitches(self):
        """ Returns all used pitch in this pattern.

        Returns:
            list of integers composed of all pitches present in this pattern
        """
        pitchs = []
        for e in self.events:
            pitchs += [e.pitch]
        pitchs = list(set(pitchs))
        return pitchs

    def getPatternWithTags(self, tagToLookFor, exactSearch=True, makeCopy=True):
        """Returns a sub-pattern with the given tags.

        Args:
            tagToLookFor: tag,tags list or lambda  expression (return boolean based on tag input): tags to be checked for
            exactSearch: bool: if True the tags argument can be an element of tag to look for, example : if we set tags='maj',an element with tag ('C','maj') will be valid
            makeCopy: do we return a copy of original events (avoid modifying originating events when modifying the returned subpattern)
        Returns:
            a GSPattern with only events that tags corresponds to given tagToLookFor
        """
        if isinstance(tagToLookFor, list):
            if exactSearch:
                patternLog.error("cannot search exactly with a list of elements")
            boolFunction = lambda inTags:len(inTags)>0 and inTags in tagToLookFor
        elif callable(tagToLookFor):
            boolFunction = tagToLookFor
        else:
            # tuple / string or any hashable object
            if exactSearch:
                boolFunction = lambda inTags: inTags == tagToLookFor
            else:
                boolFunction = lambda inTags: (inTags == tagToLookFor) or (len(inTags)>0 and tagToLookFor in inTags)

        res = self.getACopyWithoutEvents()
        for e in self.events:
            found = boolFunction(e.tag)
            if found:
                newEv = e if not makeCopy else e.copy()
                res.events += [newEv]
        return res

    def getPatternWithPitch(self, pitch, makeCopy=True):
        """Returns a sub-pattern with the given pitch.

        Args:
            pitch: pitch to look for
            makeCopy: do we return a copy of original events (avoid modifying originating events when modifying the returned subpattern)
        Returns:
            a GSPattern with only events that pitch corresponds to given pitch
        """
        res = self.getACopyWithoutEvents()
        for e in self.events:
            found = (e.pitch == pitch)
            if found:
                newEv = e if not makeCopy else e.copy()
                res.events += [newEv]

        return res

    def getPatternWithoutTags(self, tagToLookFor, exactSearch=False, makeCopy=True):
        """Returns a sub-pattern without the given tags.

        Args:
            tagToLookFor: tag or tag list: tags to be checked for
            exactSearch: bool: if True the tags have to be exactly the same as tagToLookFor, else they can be included in events tag
            makeCopy: do we return a copy of original events (avoid modifying originating events when modifying the returned subpattern)

        Returns:
            a GSPattern with events without given tags
        """

        if isinstance(tagToLookFor, list):
            if exactSearch:
                patternLog.error("cannot search exactly with a list of elements")
            boolFunction = lambda inTags:len(inTags)>0 and inTags in tagToLookFor
        elif callable(tagToLookFor):
            boolFunction = tagToLookFor
        else:
            # tuple / string or any hashable object
            if exactSearch:
                boolFunction = lambda inTags: inTags == tagToLookFor
            else:
                boolFunction = lambda inTags: (inTags == tagToLookFor) or (len(inTags)>0 and tagToLookFor in inTags)

        res = self.getACopyWithoutEvents()
        for e in self.events:
            needToExclude = boolFunction(e.tag)
            if not needToExclude :
                newEv = e if not makeCopy else e.copy()
                res.events += [newEv]
        return res

    def alignOnGrid(self, stepSize, repeatibleTags=['silence']):
        """Align this pattern on a temporal grid.
        Very useful to deal with step-sequenced pattern:
        - all events durations are shortened to stepsize
        - all events startTimes are quantified to stepsize

        RepeatibleTags allow to deal with `silences type` of events:
        - if a silence spread over more than one stepsize, we generate an event for each stepSize

        Thus each step is ensured to be filled with one distinct event at least.

        Args:
            stepSize: temporal definition of the grid
            repeatibleTags: tags
        """
        newEvents = []
        for e in self.events:
            if e.tagIs(repeatibleTags):
                evToAdd = e.cutInSteps(stepSize)
            else:
                evToAdd = [e]
            for ea in evToAdd:
                ea.startTime = int(ea.startTime / stepSize + 0.5) * stepSize
                # avoid adding last event out of duration range
                if ea.startTime < self.duration:
                    ea.duration = stepSize
                    newEvents += [ea]

        self.events = newEvents
        self.removeOverlapped()
        return self

    def removeOverlapped(self, usePitchValues=False):
        """Remove overlapped elements.

            Args:
                usePitchValues: use pitch to discriminate events
        """
        self.reorderEvents()
        newList = []
        idx = 0
        for e in self.events:
            found = False
            overLappedEv = []
            for i in range(idx + 1, len(self.events)):
                ee = self.events[i]
                if usePitchValues:
                    equals = (ee.pitch == e.pitch)
                else:
                    equals = (ee.tag == e.tag)
                if equals:
                    if (ee.startTime >= e.startTime) and (ee.startTime < e.startTime + e.duration):
                        found = True
                        if ee.startTime - e.startTime > 0:
                            e.duration = ee.startTime - e.startTime
                            newList += [e]
                            overLappedEv += [ee]
                        else:
                            patternLog.info("strict overlapping of start times %s with %s" % (e, ee))

                if ee.startTime > (e.startTime + e.duration):
                    break
            if not found:
                newList += [e]
            else:
                patternLog.info("remove overlapping %s with %s" % (e, overLappedEv))
            idx += 1
        self.events = newList
        # return self

    def getAllIdenticalEvents(self, event, allTagsMustBeEquals=True):
        """Get a list of event with same tags.

        Args:
            event:event to compare with
            allTagsMustBeEquals: shall we get exact tags equality or be fine with one common tag (valable if tags are tuple)

        Returns:
            list of events that have all or one tags in common
        """
        res = []
        for e in self.events:
            equals = False
            equals = event.allTagsAreEqualWith(e) if allTagsMustBeEquals else event.hasOneCommonTagWith(e)
            if equals:
                res += [e]

    def getFilledWithSilences(self, maxSilenceTime=0, perTag=False, silenceTag='silence'):
        pattern = self.copy()
        pattern.fillWithSilences(maxSilenceTime=maxSilenceTime, perTag=perTag, silenceTag=silenceTag)
        return pattern

    def fillWithSilences(self, maxSilenceTime=0, perTag=False, silenceTag='silence', silencePitch=0):
        """Fill empty time intervals (i.e no event) with silence event.

        Args:
            maxSilenceTime: if positive value is given, will add multiple silence of maxSilenceTime for empty time larger than maxSilenceTime
            perTag: fill silence for each Tag
            silenceTag: tag that will be used when inserting the silence event
            silencePitch : the desired pitch of new silences events
        """
        self.reorderEvents()

        def _fillListWithSilence(pattern, silenceTag, silencePitch=-1):
            lastOff = 0
            newEvents = []

            for e in pattern.events:
                if e.startTime > lastOff:
                    if maxSilenceTime > 0:
                        while e.startTime - lastOff > maxSilenceTime:
                            newEvents += [GSPatternEvent(lastOff, maxSilenceTime, silencePitch, 0, silenceTag)]
                            lastOff += maxSilenceTime
                    newEvents += [GSPatternEvent(lastOff, e.startTime - lastOff, silencePitch, 0, silenceTag)]
                newEvents += [e]
                lastOff = max(lastOff, e.startTime + e.duration)

            if lastOff < pattern.duration:
                if maxSilenceTime > 0:
                    while lastOff < pattern.duration - maxSilenceTime:
                        newEvents += [GSPatternEvent(lastOff, maxSilenceTime, silencePitch, 0, silenceTag)]
                        lastOff += maxSilenceTime
                newEvents += [GSPatternEvent(lastOff, pattern.duration - lastOff, silencePitch, 0, silenceTag)]
            return newEvents

        if not perTag:
            self.events = _fillListWithSilence(self, silenceTag,silencePitch)
        else:
            allEvents = []
            for t in self.getAllTags():
                allEvents += _fillListWithSilence(self.getPatternWithTags(tagToLookFor=t, exactSearch=False, makeCopy=False), silenceTag, silencePitch)
            self.events = allEvents

    def fillWithPreviousEvent(self):
        """
        Fill gaps between onsets making longer the duration of the previous event.
        """
        onsets = []
        for e in self.events:
           if e.startTime not in onsets:
               onsets.append(e.startTime)
        onsets.append(self.duration)

        for e in self.events:
           e.duration = onsets[onsets.index(e.startTime) + 1] - e.startTime

    def getPatternForTimeSlice(self, startTime, length, trimEnd=True):
        """Returns a pattern within given timeslice.

        Args:
            startTime: start time for time slice
            length: length of time slice
            trimEnd: cut any events that ends after startTime + length
        Returns:
            a new GSpattern within time slice
        """
        p = self.getACopyWithoutEvents()
        p.startTime = startTime
        p.duration = length
        for e in self.events:
            if 0 <= (e.startTime - startTime) < length:
                newEv = e.copy()
                newEv.startTime -= startTime
                p.events += [newEv]
        if trimEnd:
            for e in p.events:
                toCrop = e.startTime + e.duration - length
                if toCrop > 0:
                    e.duration -= toCrop
        return p

    def toJSONDict(self,useTagIndexing=True):
        """Gives a standard dict for json output.
        Args:
        useTagIndexing: if true, tags are stored as indexes from a list of all tags (reduce size of json files)
        """
        res = {}
        self.setDurationFromLastEvent()
        res['name'] = self.name
        if self.originPattern : res['originPattern'] = self.originPattern.name
        res['timeInfo'] = {'duration': self.duration, 'bpm': self.bpm,'timeSignature':self.timeSignature}
        res['eventList'] = []
        res['viewpoints'] = {k: v.toJSONDict(useTagIndexing) for k, v in self.viewpoints.items()}
        if useTagIndexing:
            allTags = self.getAllTags()
            res['eventTags'] = allTags
            def findIdxforTags(tags, allTags):
                return [allTags.index(x) for x in tags]
            for e in self.events:
                res['eventList'] += [{'on': e.startTime,
                                      'duration': e.duration,
                                      'pitch': e.pitch,
                                      'velocity': e.velocity,
                                      'tagIdx': findIdxforTags(e.tag, allTags)
                                      }]
        else:
            for e in self.events:
                res['eventList'] += [{'on': e.startTime,
                                      'duration': e.duration,
                                      'pitch': e.pitch,
                                      'velocity': e.velocity,
                                      'tag': e.tag
                                      }]

        return res

    def fromJSONDict(self, json,parentPattern=None):
        """Loads a json API dict object to this pattern

        Args:
            json: a dict created from reading json file with GS API JSON format
        """
        self.name = json['name']
        self.duration = json['timeInfo']['duration']
        self.bpm = json['timeInfo']['bpm']
        self.timeSignature = tuple(json['timeInfo']['timeSignature'])
        if 'originPattern' in json:
            def findOriginPatternInParent(name):
                if not name:
                    return None
                checkedPattern = parentPattern
                while( checkedPattern):
                    if checkedPattern.name==name:
                        return checkedPattern
                    checkedPattern = checkedPattern.originPattern

                assert False, "no origin pattern found"

            self.originPattern = findOriginPatternInParent(json['originPattern'])

        hasIndexedTags = 'eventTags' in json.keys()
        if hasIndexedTags:
            tags = json['eventTags']
            for e in json['eventList']:
                self.events += [GSPatternEvent(startTime = e['on'],
                                               duration = e['duration'],
                                               pitch = e['pitch'],
                                               velocity = e['velocity'],
                                               tag = tuple([tags[f] for f in e['tagsIdx']])
                                               )]
        else:
            for e in json['eventList']:
                self.events += [GSPatternEvent(startTime = e['on'],
                                               duration = e['duration'],
                                               pitch = e['pitch'],
                                               velocity =e['velocity'],
                                               tag = e['tag']
                                               )]

        self.viewpoints = {k: GSPattern().fromJSONDict(v,parentPattern=self) for k, v in json['viewpoints'].items()}
        self.setDurationFromLastEvent()

        return self

    def splitInEqualLengthPatterns(self, desiredLength,viewpointName=None ,makeCopy=True,supressEmptyPattern=True):
        """Splits a pattern in consecutive equal length cuts.

        Args:
            desiredLength: length desired for each pattern
            viewpointName : if given, slice the underneath viewpoint instead
            makeCopy: returns a distint copy of original pattern events, if you don't need original pattern anymore setting it to False will increase speed

        Returns:
            a list of patterns of length desiredLength
        """
        def _handleEvent(e,patterns,makeCopy):
          p = int(math.floor(e.startTime * 1.0 / desiredLength))
          numPattern = str(p)
          if numPattern not in patterns:
              patterns[numPattern] = patternToSlice.getACopyWithoutEvents()
              patterns[numPattern].startTime = p*desiredLength
              patterns[numPattern].duration = desiredLength
              patterns[numPattern].name = patternToSlice.name + "_" + numPattern
          newEv = e if not makeCopy else e.copy()
          
          if (newEv.startTime + newEv.duration > (p+1)*desiredLength):
              remainingEvent = e.copy()
              newOnset = (p+1) * desiredLength
              remainingEvent.duration = remainingEvent.getEndTime() - newOnset
              remainingEvent.startTime = newOnset
              _handleEvent(remainingEvent,patterns,makeCopy)
              newEv.duration = (p+1)*desiredLength - e.startTime

          newEv.startTime -= p*desiredLength
          patterns[numPattern].events += [newEv]
        patterns = {}

        patternToSlice = self.viewpoints[viewpointName] if viewpointName else self
        for e in patternToSlice.events:
            _handleEvent(e,patterns,makeCopy)
        res = []
        maxListLen = int(math.ceil(patternToSlice.duration*1.0/desiredLength))
        for p in range(maxListLen):
            pName = str(p)
            if pName in patterns:
                curPattern = patterns[pName]
                curPattern.setDurationFromLastEvent()
            else:
                curPattern = None
            if (not supressEmptyPattern )or curPattern:
                res += [curPattern]
        return res

    def generateViewpoint(self,name,descriptor=None,sliceType=None):
        """
        generate viewpoints in this GSPattern
        Args:
            name: name of the viewpoint generated , if name is one of ["chords",] it will generate the default descriptor
            descriptor : if given it's the descriptor used
            sliceType: type of slicing to compute viewPoint: 
                if integer its duration based see:splitInEqualLengthPatterns
                if "perEvent" generates new pattern every new events startTime, 
                if "all" get the whole pattern (generate one and only viewPoint value)
        """

        def _computeViewpoint(originPattern,descriptor,name,sliceType=1): 
            """
            Internal function for computing viewPoint
                
            """
            viewpoint = originPattern.getACopyWithoutEvents()
            viewpoint.name = name
            viewpoint.originPattern=originPattern


            if isinstance(sliceType,int):
                step = sliceType
                patternsList = originPattern.splitInEqualLengthPatterns(step)

            elif sliceType=="perEvent":
                originPattern.reorderEvents()
                lastTime = -1
                patternsList=[]
                for consideredEvent in originPattern:
                    if lastTime < consideredEvent.startTime: # group all identical startTimeEvents
                        pattern = originPattern.getACopyWithoutEvents()
                        pattern.startTime = consideredEvent.startTime
                        pattern.events = originPattern.getActiveEventsAtTime(consideredEvent.startTime)
                        pattern.duration = 0


                        for se in pattern.events:
                        # TODO do we need to trim to beginning? 
                        # some events can have negative startTimes and each GSpattern.duration corresponds to difference between consideredEvent.startTime and lastEvent.startTime (if some events were existing before start of consideredEvent)
                        #     se.startTime-=consideredEvent.startTime 
                            eT = se.getEndTime() - pattern.startTime
                            if eT>pattern.duration:
                                pattern.duration = eT
                        lastTime = consideredEvent.startTime

                        patternsList+=[pattern]

            elif sliceType== "all":
                patternsList = [originPattern]
            else:
                patternLog.error("sliceType %s not valid"%(sliceType))
                assert False


            for subPattern in patternsList:
                if subPattern:
                    viewpoint.events+=[GSPatternEvent(duration=subPattern.duration,startTime=subPattern.startTime,tag = descriptor.getDescriptorForPattern(subPattern),originPattern=subPattern)]

            return viewpoint




        if descriptor :
            self.viewpoints[name]=_computeViewpoint(originPattern=self,descriptor=descriptor,sliceType=sliceType,name=name)
        else:
            if name == "chords":
                from .GSDescriptors.GSDescriptorChord import GSDescriptorChord
                self.viewpoints[name] = _computeViewpoint(originPattern=self,descriptor=GSDescriptorChord(),sliceType=4,name=name)

        # can use it as a return value 
        return self.viewpoints[name]





    def printASCIIGrid(self, blockSize=1):
        def __areSilenceEvts(l):
            if len(l) > 0:
                for e in l:
                    if 'silence' not in e.tag:
                        return False
            return True

        for t in self.getAllTags():
            noteOnASCII = '|'
            sustainASCII = '>'
            silenceASCII = '-'
            out = "["
            p = self.getPatternWithTags(t, makeCopy=True)  #.alignOnGrid(blockSize);
            # p.fillWithSilences(maxSilenceTime = blockSize)
            isSilence = __areSilenceEvts(p.getActiveEventsAtTime(0))
            inited = False
            lastActiveEvent = p.events[0]
            numSteps = int(self.duration * 1.0 / blockSize)

            for i in range(numSteps):
                time = i * 1.0 * blockSize
                el = p.getActiveEventsAtTime(time)
                newSilenceState = __areSilenceEvts(el)
                if newSilenceState != isSilence:
                    if newSilenceState:
                        out += silenceASCII
                    else:
                        out += noteOnASCII
                        lastActiveEvent = el[0]
                elif newSilenceState:
                    out += silenceASCII
                elif not newSilenceState:
                    if el[0].startTime == lastActiveEvent.startTime:
                        out += sustainASCII
                    else:
                        out += noteOnASCII
                        lastActiveEvent = el[0]

                isSilence = newSilenceState
                inited = True

            out += "]: " + t
            print (out)

