import sys, os
from gsapi import *


midiFile    = "../../corpus/harmony/I5-IV.mid"
myPattern = GSIO.fromMidi("../../corpus/harmony/I5-IV.mid", "pitchNames")

print myPattern
print myPattern.getStartingEventsAtTime(4)
