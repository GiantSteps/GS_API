from GSBasePatternTransformer import *
from gsapi.GSPattern import *


class GSChord(GSPatternEvent):
    """Represents an event of a GSPattern.
    An event has a startTime, duration, pitch, velocity and associated tags.

    Class variables:
        startTime: startTime of event
        duration: duration of event
        pitch: pitches of event
        velocity: velocity of event
        tags: list of tags representing the event
    """

    def __init__(self, startTime=0, duration=1.0, components=[], tags=[], label="chord"):
        self.duration = duration
        if not isinstance(tags, list):
            tags = [tags]
        self.startTime = startTime
        self.components = components
        self.tags = tags
        self.label = label

    def __repr__(self):
        return "%s %s %s %05.2f %05.2f" % (self.label,
                                           self.tags,
                                           str(self.components),
                                           self.startTime,
                                           self.duration)


class Chordify(GSBasePatternTransformer):
    """Makes vertical slices of a pattern."""
    def __init__(self, pattern):
        self.originPattern = pattern
        self.currentPattern = self.transformPattern()
        self.duration = self.currentPattern.duration
        self.events = self.currentPattern.events
        self.numChords = len(self.currentPattern.events)

    def configure(self, paramDict):
        """Configure current transformer based on implementation
        specific parameters passed in paramDict argument.

        Args:
            paramDict: a dictionary with configuration values.
        """
        raise NotImplementedError("Should have implemented this")

    def transformPattern(self, pattern):
        """Return a transformed GSPattern

        Args:
            pattern: the GSPattern to be transformed.
        """
        self.currentPattern = self.originPattern.getACopyWithoutEvents()
        p = -1
        for e in self.originPattern:
            if e.startTime != p:
                new_chord = GSChord(startTime=e.startTime, duration=e.duration)
                activePattern = GSPattern(self.originPattern.getActiveEventsAtTime(e.startTime))

                print activePattern
                for ee in activePattern:
                    print ee
                    new_chord.components.append((ee.pitch, ee.velocity))
                #self.currentPattern.events.append(new_chord)
                # print new_chord
            p = e.startTime
        return self.currentPattern


    #for e in self.events:
    #    e.pitch += interval
    #    e.tags = [pitch2name(e.pitch, defaultPitchNames)]
    # return self
