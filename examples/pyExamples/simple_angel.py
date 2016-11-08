if __name__ == '__main__':
    import sys,os
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, "python")))

import logging
from gsapi import *
from music21 import *

gsiolog.setLevel(level=logging.ERROR)


midiFile    = "../../corpus/harmony/I5-IV.mid"
myPattern = GSIO.fromMidi("../../corpus/harmony/I5-IV.mid", "pitchNames")

print myPattern

myPattern.transpose(-2)
print myPattern
myPattern.quantize(1)
myPattern.fillWithSilences()
print myPattern


# b = a.splitInEqualLengthPatterns(2)

# a.alignOnGrid(2)

# print a.duration

GSIO.toMIDI(myPattern, path='./', name='test')
s = converter.parse('./test.mid')
s.duration = duration.Duration(myPattern.duration)
s.show()
