import sys, os
from gsapi import *

midiFile    = "../../corpus/harmony/I5-IV.mid"
myPattern = GSIO.fromMidi("../../corpus/harmony/I5-IV.mid", "pitchNames")

print myPattern
a = myPattern.transpose(1)
# a.toMIDI(path='/pyExamples/', name='test')

print a
