import sys, os
from gsapi import *


defaultMidiFolder = "../../corpus/harmony/"
fil = GSIO.fromMidi(defaultMidiFolder + "/I5-IV.mid", "pitchNames")

print fil

print fil.getStartingEventsAtTime(4)
