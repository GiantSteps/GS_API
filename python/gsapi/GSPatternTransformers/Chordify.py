from GSBasePatternTransformer import *
from gsapi.GSPattern import *


class GSPatternEventChord(GSPatternEvent):
    """Represents an event of a GSPattern.
    An event has a startTime, duration, pitch, velocity and associated tags.

    Class variables:
        startTime: startTime of event
        duration: duration of event
        pitch: pitches of event
        velocity: velocity of event
        tags: list of tags representing the event
    """

    def __init__(self, startTime=0, duration=1.0, components=None, tags=None, label="chord"):
        self.duration = duration
        if not isinstance(tags, list):
            tags = [tags]
        self.startTime = startTime
        self.components = components or []
        self.tags = tags or []
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
        self.inputPattern = pattern
        self.outputPattern = self.transformPattern()
        self.duration = self.outputPattern.duration
        self.events = self.outputPattern.events
        self.numChords = len(self.outputPattern.events)

    def configure(self, paramDict):
        """Configure current transformer based on implementation
        specific parameters passed in paramDict argument.

        Args:
            paramDict: a dictionary with configuration values.
        """
        raise NotImplementedError("Should have implemented this")

    def transformPattern(self):
        """Return a transformed GSPattern"""
        self.outputPattern = self.inputPattern.getACopyWithoutEvents()
        p = -1
        for e in self.inputPattern:
            if e.startTime != p:
                new_chord = GSPatternEventChord(startTime=e.startTime, duration=e.duration, components=[], tags=[])
                for ee in self.inputPattern.getActiveEventsAtTime(e.startTime):
                    new_chord.components.append((ee.pitch, ee.velocity))
                    for tag in ee.tags:
                        new_chord.tags.append(tag)
                self.outputPattern.addEvent(new_chord)
            p = e.startTime
        return self.outputPattern
