if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, "python")))

import logging
from gsapi import *
from music21 import *

gsiolog.setLevel(level=logging.ERROR)

myPattern = GSIO.fromMidi("../../corpus/harmony/Im7-Vm9.mid", "pitchNames")
print myPattern

# get start time of first event in the pattern:
start_event = myPattern.events[0].startTime

# get all vertical components at start time:
first_chord = myPattern.getStartingEventsAtTime(start_event)

# get the midi note numbers of the first chord:
first_notes = []
for e in first_chord:
    first_notes.append(e.pitch)

# we sort them in ascending order:
# (afterwards we could check if the agregate is a chord and if it is in root position)
first_notes.sort()
first_root = first_notes[0]

# find a transposition factor and transpose the progression to middle C:
transposition_interval = 60 - first_root
myPattern.transpose(transposition_interval)

# in the example of transposition we could make that minor chords transpose automatically to A minor
# and major chords to C...


#myPattern.quantize(1)  # I need to experiment with the quantization factor..0
#print myPattern
myPattern.fillWithSilences()  # adds silences when needed!
print myPattern

# b = a.splitInEqualLengthPatterns(2)

# a.alignOnGrid(2)

# print a.duration

GSIO.toMIDI(myPattern, path='./', name='test')
# s = converter.parse('./test.mid')
# s.duration = duration.Duration(myPattern.duration)
# s.show()

