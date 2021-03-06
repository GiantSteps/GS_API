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

print "Script initialized"

try:
    print "Script arguments: ", sys.argv
except:
    print "Couldn't load arguments"

# Set GS_API verbose level:
GSIO.gsiolog.setLevel(level=logging.ERROR)


def GSPatternToList(gspattern):
    list_of_events = []
    for event in gspattern.events:
        list_of_events.append(str(event.tags))
        list_of_events.append(event.pitch)
        list_of_events.append(event.startTime)
        list_of_events.append(event.duration)
    return list_of_events


def normalize_to_c4(midi_file):
    my_pattern = GSIO.fromMidi(str(midi_file), "pitchNames")
    start_event = my_pattern.events[0].startTime
    first_chord = my_pattern.getStartingEventsAtTime(start_event)
    first_notes = []
    for e in first_chord:
        first_notes.append(e.pitch)
    first_notes.sort()
    first_root = first_notes[0]
    transposition_interval = 60 - first_root
    my_pattern.removeOverlapped(usePitchValues=True)
    my_pattern.reorderEvents()
    my_pattern.transpose(transposition_interval)
    my_pattern.quantize(0.25)
    my_pattern.fillWithPreviousEvent()
    my_pattern.fillWithSilences()
    return GSPatternToList(my_pattern)
