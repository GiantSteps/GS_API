if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, "python")))

import logging
from gsapi import *

GSIO.gsiolog.setLevel(level=logging.ERROR)

myPattern = GSIO.fromMidi("../../corpus/harmony/I5-IV.mid", "pitchNames")
start_event = myPattern.events[0].startTime
first_chord = myPattern.getStartingEventsAtTime(start_event)

first_notes = []
for e in first_chord:
    first_notes.append(e.pitch)

first_notes.sort()
first_root = first_notes[0]
transposition_interval = 60 - first_root
myPattern.removeOverlapped(usePitchValues=True)
myPattern.reorderEvents()
myPattern.transpose(transposition_interval)
myPattern.quantize(0.25)
print myPattern
myPattern.removeByTags(["silence"])
print myPattern
myPattern.fillWithPreviousEvent()
myPattern.fillWithSilences()
print myPattern


# GSIO.toMIDI(myPattern, path='./', name='test')
