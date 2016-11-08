from gsapi import *
from music21 import *

midiFile    = "../../corpus/harmony/I5-IV.mid"
myPattern = GSIO.fromMidi("../../corpus/harmony/I5-IV.mid", "pitchNames")

print myPattern

a = myPattern.transpose(-2)

a.fillWithSilences()

print myPattern

#   a.quantize(1)
# b = a.splitInEqualLengthPatterns(2)

# a.alignOnGrid(2)

# print a.duration

a.toMIDI(path='./', name='test')
s = converter.parse('./test.mid')
s.show()
