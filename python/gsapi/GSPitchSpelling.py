from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
GSPitchSpelling - Angel Faraldo, December 2016.

This file implements utilities for the correct spelling of
notes and chords based on a representation by W. B. Hewlett.

|===========================================================|
| INTERVAL            DELTA       INTERVAL            DELTA |
|===========================================================|
| perfect unison      0           perfect octave      40    |
| augmented unison    1           diminished octave   39    |
|                                                           |
| diminished second   4           augmented seventh   36    |
| minor second        5           major seventh       35    |
| major second        6           minor seventh       34    |
| augmented second    7           diminished seventh  33    |
|                                                           |
| diminished third    10          augmented sixth     30    |
| minor third         11          major sixth         29    |
| major third         12          minor sixth         28    |
| augmented third     13          diminished sixth    27    |
|                                                           |
| diminished fourth   16          augmented fifth     24    |
| perfect fourth      17          perfect fifth       23    |
| augmented fourth    18          diminished fifth    22    |
|===========================================================|

- The inversion  of a simple interval is 40 minus that interval.

- Intervals may be computed across the B - C octave boundary
without extra calculations.

- Compound intervals such as tenths are related to intervals by
the difference of an octave (40). A major tenth is 12 + 40 = 52.

- Limitations: Intervals involving notes outside the set,
e.g. with three or more sharps or flats, cannot be computed properly
from this representation. Some unusual intervals will have numbers
which overlap the numbers for the standard intervals given above.
For example,  the quadruple augmented unison between Cbb1 and C##1
has an interval value of 4, which also the number for a diminished
second. These limitations can be removed by using solutions of a
higher order.

Walter B. Hewlett (1992) "A Base-40 Number-line Representation
of Musical Pitch Notation." Musikometrica (4), pp. 1--14
"""

defaultPitchNames = ["C", "C#", "D", "Eb", "E", "F",
                     "F#", "G", "Ab", "A", "Bb", "B"]

pitch40 = ["Cbb", "Cb", "C", "C#", "C##", "",
           "Dbb", "Db", "D", "D#", "D##", "",
           "Ebb", "Eb", "E", "E#", "E##",
           "Fbb", "Fb", "F", "F#", "F##", "",
           "Gbb", "Gb", "G", "G#", "G##", "",
           "Abb", "Ab", "A", "A#", "A##", "",
           "Bbb", "Bb", "B", "B#", "B##"]


def pitch2name(pitch, pitchNames):
    """Converts a midi note number to alphabetic notation with octave index (e.g. "C4", "Db5")"""
    octaveLength = len(pitchNames)
    octave = int(pitch / octaveLength) - 1
    note = pitch % octaveLength
    return pitchNames[note] + str(octave)


def make_chord(root, chord_structure):
    chord_structure = [0] + chord_structure
    for i in range(len(chord_structure)):
        root += chord_structure[i]
        chord_structure[i] = pitch40[root % 40]
    return chord_structure


def pc2note(pitch_class, alt="#"):
    if alt is "#":
        base40 = [2, 3, 8, 9, 14, 19, 20, 25, 26, 31, 32, 37]
    elif alt is "b":
        base40 = [2, 7, 8, 13, 14, 19, 24, 25, 30, 31, 36, 37]
    else:
        raise Exception("alt should be either '#' or 'b'")
    return pitch40[base40[pitch_class % 12]]


def pc2base40(pitch_class, alt="#"):
    if alt is "#":
        base40 = [2, 3, 8, 9, 14, 19, 20, 25, 26, 31, 32, 37]
    elif alt is "b":
        base40 = [2, 7, 8, 13, 14, 19, 24, 25, 30, 31, 36, 37]
    else:
        raise Exception("alt should be either '#' or 'b'")
    return base40[pitch_class % 12]


