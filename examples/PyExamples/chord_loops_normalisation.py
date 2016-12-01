if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, "python")))

import logging
from gsapi import *

GSIO.gsiolog.setLevel(level=logging.ERROR)

myPattern = GSIO.fromMidi("../../corpus/harmony/I5-IV.mid", "pitchNames")

# get start time of first event in the pattern:
start_event = myPattern.events[0].startTime

# get all vertical components at start time:
first_chord = myPattern.getStartingEventsAtTime(start_event)

# get the midi note numbers of the first chord:
first_notes = []
for e in first_chord:
    first_notes.append(e.pitch)

# we sort them in ascending order:
# (afterwards we could check if the aggregate is a chord and if it is in root position)
first_notes.sort()
first_root = first_notes[0]

# find a transposition factor and transpose the progression to middle C:
transposition_interval = 60 - first_root
myPattern.transpose(transposition_interval)

# POSIBLY USEFUL FUNCTIONS
myPattern.removeOverlapped(usePitchValues=True)
myPattern.reorderEvents()
myPattern.quantize(0.25)
myPattern.fillWithPreviousEvent()
myPattern.fillWithSilences()  # fills empty time intervals with silences
print myPattern

GSIO.toMIDI(myPattern, path='./', name='test')
