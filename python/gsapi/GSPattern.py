import math
import copy
import logging
from MidiMap import *
from GSPatternUtils import *

patternLog = logging.getLogger("gsapi.GSPattern")

"""Documentation for GSPattern module.

GSPattern
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
        self.tags = tags

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

    def __repr__(self):
        return "%s %i %f %f"%(self.tags,
                              self.pitch,
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

    def transpose(self, transposition_interval):

        for e in self.events:
            e.pitch += transposition_interval
            e.tags = [pitchToName(e.pitch, defaultPitchNames)]
        return self

    def toMIDI(self, midiMap=None, path="output/", name="test"):
        """ Function to write GSPattern instance to MIDI.

        Args:
            midiMap: mapping used to translate tags to MIDI pitch
            path: folder where MIDI file is stored
            name: name of the file
        """

        #Import the library
        from midiutil.MidiFile import MIDIFile

        # Create the MIDIFile Object with 1 track
        MyMIDI = MIDIFile(1, adjust_origin=False)

        # Tracks are numbered from zero. Times are measured in beats.
        track = 0
        time = 0

        # Add track name and tempo.
        MyMIDI.addTrackName(track, time, "Sample Track")
        MyMIDI.addTempo(track, time, self.bpm)

        # Add a note. addNote expects the following information:
        track = 0
        channel = 0

        # Now add the note.
        for e in self.events:
            if midiMap is None:
                MyMIDI.addNote(track, channel, e.pitch, e.startTime, e.duration, e.velocity)
            else:
                MyMIDI.addNote(track, channel, midiMap[e.tags[0]], e.startTime, e.duration, e.velocity)

        # And write it to disk.
        binfile = open(path + name + ".mid", 'wb')
        MyMIDI.writeFile(binfile)
        binfile.close()

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

    def addEvent(self, GSPatternEvent):
        """Add an event increasing duration if needed.

        Args:
            GSPatternEvent: the event to be added
        """
        self.events += [GSPatternEvent]
        self.setDurationFromLastEvent()

    def quantize(self, beatDivision):
        """ Quantize events.

        Args:
            beatDivision: the fraction of beat that we want to quantize to
        """
        for e in self.events:
            e.startTime = int(e.startTime * beatDivision) * 1.0 / beatDivision

    def timeStretch(self, ratio):
        """Time-stretch a pattern.

        Args:
            ratio: the ratio used for time stretching
        """
        for e in self.events:
            e.startTime *= ratio
            e.duration *= ratio
        self.duration  *= ratio

    def getStartingEventsAtTime(self, time, tolerance=0):
        """ Get all events activating at a givent time.

        Args:
            time: time asked for
            tolerance: admited deviation of start time
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
            if(time - e.startTime >= 0 and time - e.startTime <= e.duration):
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
                if not t in tags:
                    tags+=[t]
        return tags

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
                boolFunction = lambda inTags: tags in inTags
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
                ea.duration = stepSize
                newEvents+=[ea]
        self.events = newEvents
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
            overLappedEv =[]
            for i in range(idx + 1, len(self.events)):
                ee = self.events[i]
                if usePitchValues:
                    equals = (ee.pitch == e.pitch)
                else:
                    equals = (ee.tags==e.tags)
                if equals:
                    if (ee.startTime >= e.startTime) and (ee.startTime < e.startTime + e.duration):
                        found = True
                        if ee.startTime - e.startTime>0:
                            e.duration = ee.startTime - e.startTime
                            newList += [e]
                            overLappedEv += [ee]
                        else:
                            patternLog.warning("strict overlapping of start times %s with %s"%(e, ee))

                if ee.startTime > (e.startTime + e.duration):
                    break
            if not found:
                newList+=[e]
            else:
                patternLog.info("remove overlapping %s with %s"%(e,overLappedEv))
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

    def fillWithSilences(self, maxSilenceTime=0, perTag=False, silenceTag ='silence'):
        """Fill empty (i.e no event ) spaces with silence event.

        Args:
            maxSilenceTime: if positive value is given, will add multiple silence of maxSilenceTime for empty time larger than maxSilenceTime
            perTag: fill silence for each Tag
            silenceTag: tag that will be used when inserting the silence event
        """
        self.reorderEvents()

        def _fillListWithSilence(list, silenceTag):
            lastOff = 0
            newEvents = []
            for e in self.events:
                if e.startTime > lastOff:
                    if maxSilenceTime > 0:
                        while e.startTime - lastOff > maxSilenceTime:
                            newEvents += [GSPatternEvent(lastOff, maxSilenceTime, 0, 0, [silenceTag])]
                            lastOff += maxSilenceTime
                    newEvents += [GSPatternEvent(lastOff, e.startTime - lastOff, 0, 0, [silenceTag])]
                newEvents += [e]
                lastOff = max(lastOff, e.startTime + e.duration)
            if lastOff < self.duration:
                if maxSilenceTime > 0:
                    while lastOff < self.duration - maxSilenceTime:
                        newEvents += [GSPatternEvent(lastOff, maxSilenceTime, 0, 0, [silenceTag])]
                        lastOff += maxSilenceTime
                newEvents += [GSPatternEvent(lastOff, self.duration - lastOff, 0, 0, [silenceTag])]
            return newEvents
        if not perTag:
            self.events = _fillListWithSilence(self.events, silenceTag)
        else:
            allEvents = []
            for t in self.getAllTags():
                allEvents += _fillListWithSilence(self.getPatternWithTags(tags=[t], exactSearch=False, copy=False), silenceTag)
            self.events = allEvents

    def getPatternForTimeSlice(self, startTime, length, trimEnd=True):
        """ Returns a pattern within given timeslice.

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
        s = "GSPattern %s\n"%(self.name)
        for e in self.events:
            s += str(e) + "\n"
        return s

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
            res+=[patterns[p]]

        return res
