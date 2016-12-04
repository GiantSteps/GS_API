if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, "python")))

import logging
from gsapi import *
from music21 import *

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
myPattern.fillWithPreviousEvent()
myPattern.fillWithSilences()
print myPattern

aa = myPattern.getACopyWithoutEvents()
aa.events = myPattern.getActiveEventsAtTime(0)
print aa



#GSIO.toMIDI(myPattern, path='./', name='test')
#s = converter.parse('./test.mid')
# s.duration = duration.Duration(myPattern.duration)
#s.show()

# It would be good to create a simple script to load
# midi files and rewrite them properly, perfectly aligned and quantized and so on...


p = GSPattern(8.0)
print p.timeSignature
print p.bpm
print p.duration
print p.key
