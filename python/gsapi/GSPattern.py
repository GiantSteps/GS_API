
"""GSPattern module holds classes :class:`GSPatternEvent` and :class:`GSPattern`
"""

import math
import copy
import logging
from GSPatternUtils import *



patternLog = logging.getLogger("gsapi.GSPattern")
"""logger for pattern related operations
"""

class GSPatternEvent(object):
    """Represents an event of a GSPattern.
    An event has a startTime, duration, pitch, velocity and associated tags.

    Attributes:
        startTime: startTime of event
        duration: duration of event
        pitch: pitch of event
        velocity: velocity of event
        tags: list of tags representing the event
    """
    def __init__(self, startTime, duration, pitch, velocity=127, tags=[]):
        self.duration = duration
        if not isinstance(tags, list):
            tags = [tags]
        self.tags = tags
        self.startTime = startTime
        self.pitch = pitch
        self.velocity = velocity
        self.tags = tags # TODO check if this is a dupe...

    def hasOneCommonTagWith(self, event):
        """Compare tags between events.

        Args:
            event: event to compare with
        Returns:
            True if at least one tag is equal
        """
        return self.hasOneOfTags(event.tags)

    def hasOneOfTags(self, tags):
        """Compare this event's tags with a list of strings.

        Args:
            tags: list of strings to compare with
        Returns:
            True if at least one tag is equal
        """
        for t in tags:
            if t in self.tags:
                return True
        return False

    def tagsAre(self, tags):
        """Compare this event's tags with a list of strings.

        Args:
            tags: list of strings to compare with
        Returns:
            True if all tags are equal
        """
        return all([x in self.tags for x in tags])

    def allTagsAreEqualWith(self, event):
        """Compare this event's tags with an other event.

        Args:
            event: event to compare with
        Returns:
            True if all tags are equal
        """
        self.tagsAre(event.tags)

    def getEndTime(self):
        """Returns the time when this events ends

        Returns:
            the time when this event ends
        """
        return self.startTime + self.duration

    def copy(self):
        """ Copy an event.

        Returns:
            A deep copy of this event to be manipulated without changing original
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
        # if smaller still take it
        num = max(1, int(self.duration / stepSize))
        for i in range(num):
            newE = self.copy()
            newE.startTime = self.startTime + i * stepSize
            newE.duration = stepSize
            res += [newE]
        return res

    def isSimilarTo(self,event):
        """ helper to compare events that could have be copy of each other (equality compares reference not content...)
        Args:
            event:event to compare wuith
        """
        return (self.startTime == event.startTime) and (self.duration==event.duration) and (self.tags==event.tags) and (self.pitch == event.pitch)

    def containsTime(self,time):
        """return true if event is active at given time
        Args:
            time : time to compare with
        """
        return (time >= self.startTime) and (time < self.startTime+self.duration)

    def __repr__(self):
        return "%s %i %i %05.2f %05.2f" % (self.tags,
                                self.pitch,
                                self.velocity,
                                self.startTime,
                                self.duration)


# ==============================================================================
# *********************** GSPattern Class Declaration **************************
# ==============================================================================

class GSPattern(object):
    """ Class representing a pattern made of GSPatternEvent.
    Holds a list of GSEvents and provide basic manipulation function.

    Args:
        duration: length of pattern. Usually in beats, but time scale is up to
            the user (it can be useful if working on 32th note steps).
        events: list of GSPatternEvent for this pattern.
        bpm: initial tempo in beats per minute for this pattern (default: 120).
        timeSignature: list of integers representing the time signature,
            i.e [numerator, denominator].
    """
    defaultTimeSignature = [4, 4]
    defaultBPM = 120

    def __init__(self):
        self.duration = 0
        self.events = []
        self.bpm = GSPattern.defaultBPM
        self.timeSignature = GSPattern.defaultTimeSignature
        self.originFilePath = ""
        self.name = ""

    def transpose(self, interval):
        """Transposes a GSPattern to the desired interval

                Args:
                    interval: transposition factor in semitones
                    (it can be a positive or negative int)
                """
        for e in self.events:
            e.pitch += interval
            e.tags = [pitchToName(e.pitch, defaultPitchNames)]
        return self

    def setDurationFromLastEvent(self, onlyIfBigger=True):
        """Sets duration to last event NoteOff

        Args:
            onlyIfBigger: update duration only if last Note off is bigger
        if inner events have a bigger time span than self.duration, increase duration to fit
        """
        total = self.getLastNoteOff()
        if (total and (total > self.duration or not onlyIfBigger)):
            # print "resizing : "+str(total) +'old : '+ str(self.duration)
            self.duration = total

    def reorderEvents(self):
        """Ensure than our internal event list `events` is time sorted

            can be useful for time sensitive events iteration
        """
        self.events.sort(key=lambda x: x.startTime, reverse=False)

    def getLastNoteOff(self):
        """Gets last event end time

        Returns:
            lastNoteOff, i.e the time corresponding to the end of the last event
        """

        if(len(self.events)):
            self.reorderEvents()
            return self.events[-1].duration + self.events[-1].startTime
        else:
            return None

    def addEvent(self, event):
        """Add an event increasing duration if needed.

        Args:
            GSPatternEvent: the event to be added
        """
        self.events += [event]
        self.setDurationFromLastEvent()

    def removeEvent(self,event):
        """remove given event
        Args:
            GSPatternEvent: the event to be added
        """
        idxToRemove = []
        idx = 0;
        for e in self.events:
            if event==e or event.isSimilarTo(e):
                idxToRemove+=[idx]
            idx+=1

        for i in idxToRemove:
            del self.events[i]


    def quantize(self, stepSize,quantizeStartTime=True,quantizeDuration = True):
        """ Quantize events.

        Args:
            stepSize: the duration that we want to quantize to
            quantizeDuration : do we quantize duration ?
            quantizeStartTime : do we quantize startTimes
        """
        beatDivision = 1.0/stepSize
        if(quantizeStartTime and quantizeDuration) :
			for e in self.events:
				e.startTime = int(e.startTime * beatDivision) * 1.0 / beatDivision
				e.duration = int(e.duration * beatDivision) * 1.0 / beatDivision
        elif quantizeStartTime :
			for e in self.events:
				e.startTime = int(e.startTime * beatDivision) * 1.0 / beatDivision
        elif quantizeDuration :
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

    def getActiveEventsAtTime(self, time):
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
            list of string composed of all possible tags
        """
        tags = []
        for e in self.events:
            for  t in e.tags:
                tags+=[t]
        tags = list(set(tags))
        return tags

    def getAllPitches(self):
    	""" Returns all used pitch in this pattern.

        Returns:
            list of integers composed of all pitches present in this pattern
        """
        pitchs = []
        for e in self.events:
             pitchs+=[e.pitch]
        pitchs = list(set(pitchs))
        return pitchs

    def getPatternWithTags(self, tags, exactSearch=True, copy=True):
        """Returns a sub-pattern with the given tags.

        Args:
            tags: string list or lambda  expression (return boolean based on tag list input): tags to be checked for
            exactSearch: bool: if True the tags have to be exactly the same, else they can be included in events Tags
            copy: do we return a copy of original events (avoid modifying originating events when modifying the returned subpattern)
        Returns:
            a GSPattern with only events that tags corresponds to given tags
        """

        if isinstance(tags, (list)):
            if exactSearch:
                boolFunction = lambda inTags: inTags == tags
            else:
                boolFunction = lambda inTags: not set(tags).isdisjoint(inTags)
        elif isinstance(tags, (str)):
            if exactSearch:
                boolFunction = lambda inTags: len(inTags) == 1 and inTags[0] == tags
            else:
                boolFunction = lambda inTags: len(inTags)>0 and tags in inTags
        elif callable(tags):
            boolFunction = tags


        res = self.getACopyWithoutEvents()
        for e in self.events:
            found = boolFunction(e.tags)
            if found:
                newEv = e if not copy else e.copy()
                res.events += [newEv]
        return res

    def getPatternWithPitch(self, pitch, copy=True):
        """Returns a sub-pattern with the given tags.

        Args:
            pitch: pitch to look for
            copy: do we return a copy of original events (avoid modifying originating events when modifying the returned subpattern)
        Returns:
            a GSPattern with only events that pitch corresponds to given pitch
        """


        res = self.getACopyWithoutEvents()
        for e in self.events:
            found = (e.pitch == pitch)
            if found:
                newEv = e if not copy else e.copy()
                res.events += [newEv]
        return res

    def getPatternWithoutTags(self, tags, exactSearch=False, copy=True):
        """Returns a sub-pattern without the given tags.

        Args:
            tags: string list: tags to be checked for
            exactSearch: bool: if True the tags have to be exactly the same, else they can be included in events Tags
            copy: do we return a copy of original events (avoid modifying originating events when modifying the returned subpattern)

        Returns:
            a GSPattern with events without given tags
        """
        res = self.getACopyWithoutEvents()
        for e in self.events:
            if  exactSearch and e.tags==tags:
                pass
            elif tags in e.tags:
                newEv = e if not copy else e.copy()
                for tRm in newEv.tags:
                    newEv.tags.remove(tRm)
                res.events+=[newEv]
            else:
                newEv = e if not copy else e.copy()
                res.events+=[newEv]
        return res

    def alignOnGrid(self, stepSize, repeatibleTags = ['silence']):
        """Align this pattern on a temporal grid.
        Very useful to deal with step-sequenced pattern:
        - all events durations are shortened to stepsize
        - all events startTimes are quantified to stepsize

        RepeatibleTags allow to deal with `silences type` of events:
        - if a silence spread over more than one stepsize, we generate an event for each stepSize

        Thus each step is ensured to be filled with one distinct event at least.

        Args:
            stepSize: temporal definition of the grid
        """
        newEvents = []
        for e in self.events:
            if e.tagsAre(repeatibleTags):
                evToAdd = e.cutInSteps(stepSize)
            else:
                evToAdd = [e]
            for ea in evToAdd:
                ea.startTime = int(ea.startTime/stepSize+0.5)*stepSize
                # avoid adding last event out of duration range
                if ea.startTime < self.duration:
                    ea.duration = stepSize
                    newEvents += [ea]

        self.events = newEvents
        self.removeOverlapped()
        return self

    def removeOverlapped(self, usePitchValues=False):
        """remove overlapped elements

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
                    equals = (ee.tags == e.tags)
                if equals:
                    if (ee.startTime >= e.startTime) and (ee.startTime < e.startTime + e.duration):
                        found = True
                        if ee.startTime - e.startTime > 0:
                            e.duration = ee.startTime - e.startTime
                            newList += [e]
                            overLappedEv += [ee]
                        else:
                            patternLog.info("strict overlapping of start times %s with %s"%(e, ee))

                if ee.startTime > (e.startTime + e.duration):
                    break
            if not found:
                newList += [e]
            else:
                patternLog.info("remove overlapping %s with %s"%(e, overLappedEv))
            idx += 1
        self.events = newList
        return self

    def getAllIdenticalEvents(self, event, allTagsMustBeEquals=True):
        """Get a list of event with same tags.

        Args:
            event:event to compare with
            allTagsMustBeEquals: shall we get exact tags equality or be fine with one common tag

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

    def fillWithSilences(self, maxSilenceTime=0, perTag=False, silenceTag ='silence',silencePitch = -1):
        """Fill empty time intervals (i.e no event) with silence event.

        Args:
            maxSilenceTime: if positive value is given, will add multiple silence of maxSilenceTime for empty time larger than maxSilenceTime
            perTag: fill silence for each Tag
            silenceTag: tag that will be used when inserting the silence event
            silencePitch : the desired pitch of new silences events
        """
        self.reorderEvents()

        def _fillListWithSilence(pattern, silenceTag,silencePitch =-1):
            lastOff = 0
            newEvents = []

            for e in pattern.events:
                if e.startTime > lastOff:
                    if maxSilenceTime > 0:
                        while e.startTime - lastOff > maxSilenceTime:
                            newEvents += [GSPatternEvent(lastOff, maxSilenceTime, silencePitch, 0, [silenceTag])]
                            lastOff += maxSilenceTime
                    newEvents += [GSPatternEvent(lastOff, e.startTime - lastOff, silencePitch, 0, [silenceTag])]
                newEvents += [e]
                lastOff = max(lastOff, e.startTime + e.duration)

            if lastOff < pattern.duration:
                if maxSilenceTime > 0:
                    while lastOff < pattern.duration - maxSilenceTime:
                        newEvents += [GSPatternEvent(lastOff, maxSilenceTime, silencePitch, 0, [silenceTag])]
                        lastOff += maxSilenceTime
                newEvents += [GSPatternEvent(lastOff, pattern.duration - lastOff, silencePitch, 0, [silenceTag])]
            return newEvents


        if not perTag:
            self.events = _fillListWithSilence(self, silenceTag,silencePitch)
        else:
            allEvents = []
            for t in self.getAllTags():
                allEvents += _fillListWithSilence(self.getPatternWithTags(tags=[t], exactSearch=False, copy=False), silenceTag,silencePitch)
            self.events = allEvents

    def applyLegato(self,usePitchValues=False):
    	""" this function supress the possible silences in this pattern by stretching consecutive identical events (i.e identical tags or pitch values)
    	Args:
    		usePitchValues: should we consider pitch numbers instead of tags (bit faster)

    	"""

    	def _perVoiceLegato(pattern):
    		pattern.reorderEvents()
    		if(len(pattern)==0) : 
    			patternLog.warning("try to apply legato on an empty voice")
    			return
    		for idx in range(1,len(pattern)):
    			diff =  pattern[idx].startTime-pattern[idx-1].getEndTime()
    			if(diff>0):
    				pattern[idx-1].duration+=diff

    		diff = pattern.duration - pattern[-1].getEndTime()
    		if(diff>0):
    			pattern[-1].duration+=diff
    		

    	if usePitchValues:
    		for p in self.getAllPitches():
    			voice = self.getPatternWithPitch(p)
    			_perVoiceLegato(voice)
    	for t in self.getAllTags():
    		voice = self.getPatternWithTags(tags=[t], exactSearch=False, copy=False)
    		_perVoiceLegato(voice)


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
        p.duration = length
        for e in self.events:
            if e.startTime - startTime >= 0 and e.startTime - startTime < length:
                newEv = e.copy()
                newEv.startTime -= startTime
                p.events += [newEv]
        if trimEnd:
            for e in p.events:
                toCrop = e.startTime + e.duration - length
                if toCrop > 0:
                    e.duration -= toCrop
        return p

    def __repr__(self):
        """Nicely print out the list of events.
        Each line represents an event formatted as: tags pitch startTime duration
        """
        s = "GSPattern %s\n" % self.name
        for e in self.events:
            s += str(e) + "\n"
        return s

    def __getitem__(self, index):
    	"""Utility to access events as list member : GSPattern[idx] = GSPattern.events[idx]
     	"""
    	return self.events[index]

    def __setitem__(self, index, item):
    	self.events[index] = item 

    def __len__(self):
    	return len(self.events)

    def toJSONDict(self):
        """Gives a standard dict for json output.
        """
        res = {}
        self.setDurationFromLastEvent()
        allTags =self.getAllTags()
        res['eventTags'] = allTags
        res['timeInfo'] = {'duration': self.duration, 'BPM': self.bpm}
        res['eventList'] = []

        def findIdxforTags(tags, allTags):
            return [allTags.index(x) for x in tags]
        for e in self.events:
            res['eventList'] += [{'on': e.startTime,
                                  'duration': e.duration,
                                  'pitch': e.pitch,
                                  'velocity': e.velocity,
                                  'tagsIdx': findIdxforTags(e.tags, allTags)
                                  }]
        return res

    def fromJSONDict(self, json):
        """Loads a json API dict object to this pattern

        Args:
            json: a dict created from reading json file with GS API JSON format
        """
        tags = json['eventTags']
        self.duration = json['timeInfo']['duration']
        self.bpm = json['timeInfo']['BPM']
        for e in json['eventList']:
            self.events += [GSPatternEvent(e['on'], e['duration'], e['pitch'], e['velocity'], [tags[f] for f in e['tagsIdx']])]
        self.setDurationFromLastEvent()
        return self

    def splitInEqualLengthPatterns(self, desiredLength, trimEnd=True, copy=True):
        """Splits a pattern in consecutive equal length cuts.

        Args:
            desiredLength: length desired for each pattern
            trimEnd: trim the end to exact desiredLength
            copy: returns a distint copy of original pattern events, if you don't need original pattern anymore setting it to False will increase speed

        Returns:
            a list of patterns of length desiredLength
        """
        patterns = {}
        for e in self.events:
            p = math.floor(e.startTime * 1.0 / desiredLength)
            numPattern = str(p)
            if numPattern not in patterns:
                patterns[numPattern] = self.getACopyWithoutEvents()
                patterns[numPattern].name += "_slice_" + numPattern
                patterns[numPattern].duration = desiredLength
                patterns[numPattern].name = self.name + "_" + numPattern
            newEv = e if not copy else e.copy()
            newEv.startTime -= p * desiredLength
            if trimEnd and (newEv.startTime + newEv.duration > desiredLength):
                newEv.duration = desiredLength - newEv.startTime
            patterns[numPattern].events += [newEv]

        res = []
        for p in patterns:
            patterns[p].setDurationFromLastEvent()
            res += [patterns[p]]

        return res
    def printASCIIGrid(self,blockSize = 1):
        def __areSilenceEvts(l):
            if len(l)>0:
                for e in l:
                    if not 'silence' in e.tags:
                        return False
            return True


        for t in self.getAllTags():
            noteOnASCII = '|'
            sustainASCII = '>'
            silenceASCII = '-' 
            out = "["
            p = self.getPatternWithTags(t,copy=True);#.alignOnGrid(blockSize);
            # p.fillWithSilences(maxSilenceTime = blockSize)
            isSilence = __areSilenceEvts(p.getActiveEventsAtTime(0))
            inited = False
            lastActiveEvent = p.events[0]
            numSteps = int(self.duration*1.0/blockSize)
            
            for i in range(numSteps):
                time = i*1.0*blockSize

                el = p.getActiveEventsAtTime(time)

                newSilenceState = __areSilenceEvts(el)
                
                if newSilenceState!=isSilence :
                    
                    if newSilenceState:
                        out+=silenceASCII
                    else:
                        out+=noteOnASCII
                        lastActiveEvent = el[0]
                elif newSilenceState:
                    out+=silenceASCII
                elif not newSilenceState:
                    if el[0].startTime==lastActiveEvent.startTime:
                        out+=sustainASCII
                    else:
                        out+=noteOnASCII
                        lastActiveEvent = el[0]

                isSilence = newSilenceState
                inited = True


            out+="] : "+t
            print out

        
