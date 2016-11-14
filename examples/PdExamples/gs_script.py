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


def numargs(*args):   # variable argument list
    """Return the number of arguments"""
    return len(args)


def strlen(arg):   
    """Return the string length"""
    # we must convert to string first (it's a symbol type most likely)
    return len(str(arg))


def strcat(*args):
    """Concatenate several symbols"""
    return reduce(lambda a, b: a+str(b), args,"")


def addall(*args):   # variable argument list
    """Add a couple of numbers"""
    return reduce(lambda a,b: a+b, args,0)


def ret1():
    return 1, 2, 3, 4


def ret2():
    return "sd", "lk", "ki"


def ret3():
    return ["sd", "lk", "ki"]


def test_gsio():
    my_pattern = GSIO.fromMidi("../../corpus/harmony/Im7-Vm9.mid", "pitchNames")
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
    return my_pattern
