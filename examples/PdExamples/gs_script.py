# py/pyext - python script objects for PD and MaxMSP
#
# Copyright (c) 2002-2005 Thomas Grill (gr@grrrr.org)
# For information on usage and redistribution, and for a DISCLAIMER OF ALL
# WARRANTIES, see the file, "license.txt," in this distribution.  
#

"""Several functions to show the py script functionality"""

import sys
import logging
from gsapi import *
from music21 import *

print "Script initialized"

try:
    print "Script arguments: ", sys.argv
except:
    print "couldn't load arguments"


def test_gsio():
    my_pattern = GSIO.fromMidi("/Users/angeluni/Git/GS_API/corpus/harmony/I-VIIm7.mid", "pitchNames")
    # print myPattern

    # get start time of first event in the pattern:
    start_event = my_pattern.events[0].startTime

    # get all vertical components at start time:
    first_chord = my_pattern.getStartingEventsAtTime(start_event)

    # get the midi note numbers of the first chord:
    first_notes = []
    for e in first_chord:
        first_notes.append(e.pitch)

    # we sort them in ascending order and take the lowest as root:
    # (afterwards we could check if the agregate is a chord and if it is in root position)
    first_notes.sort()
    first_root = first_notes[0]

    # find a transposition factor and transpose the progression to middle C:
    transposition_interval = 60 - first_root
    my_pattern.transpose(transposition_interval)
    my_pattern.fillWithSilences()  # adds silences when needed!
    return my_pattern.events

#