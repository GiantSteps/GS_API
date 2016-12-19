from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def GSPatternToList(GSPattern):
    """Converts a GSPattern to a regular python list."""
    list_of_events = []
    for event in GSPattern.events:
        list_of_events.append([event.pitch,
                               event.startTime,
                               event.duration])
    return list_of_events


# ==============================
# DEFAULT DICTIONARY DEFINITIONS
# ==============================

simpleDrumMap = {"Kick": 36,
                 "Rimshot": 37,
                 "Snare": 38,
                 "Clap": 39,
                 "Clave": 40,
                 "LowTom": 41,
                 "ClosedHH": 42,
                 "MidTom": 43,
                 "Shake": 44,
                 "HiTom": 45,
                 "OpenHH": 46,
                 "LowConga": 47,
                 "HiConga": 48,
                 "Cymbal": 49,
                 "Conga": 50,
                 "CowBell": 51
                 }


verySimpleDrumMap = {"Kick": 36,
                 "Snare": 38,
                 "ClosedHH": 42,
                 "OpenHH": 46,
                 }

generalMidiMap = {"Acoustic Bass Drum": 35,
                  "Bass Drum 1": 36,
                  "Side Stick": 37,
                  "Acoustic Snare": 38,
                  "Hand Clap": 39,
                  "Electric Snare": 40,
                  "Low Floor Tom": 41,
                  "Closed Hi Hat": 42,
                  "High Floor Tom": 43,
                  "Pedal Hi-Hat": 44,
                  "Low Tom": 45,
                  "Open Hi-Hat": 46,
                  "Low-Mid Tom": 47,
                  "Hi-Mid Tom": 48,
                  "Crash Cymbal 1": 49,
                  "High Tom": 50,
                  "Ride Cymbal 1": 51,
                  "Chinese Cymbal": 52,
                  "Ride Bell": 53,
                  "Tambourine": 54,
                  "Splash Cymbal": 55,
                  "Cowbell": 56,
                  "Crash Cymbal 2": 57,
                  "Vibraslap": 58,
                  "Ride Cymbal 2": 59,
                  "Hi Bongo": 60,
                  "Low Bongo": 61,
                  "Mute Hi Conga": 62,
                  "Open Hi Conga": 63,
                  "Low Conga": 64,
                  "High Timbale": 65,
                  "Low Timbale": 66,
                  "High Agogo": 67,
                  "Low Agogo": 68,
                  "Cabasa": 69,
                  "Maracas": 70,
                  "Short Whistle": 71,
                  "Long Whistle": 72,
                  "Short Guiro": 73,
                  "Long Guiro": 74,
                  "Claves": 75,
                  "Hi Wood Block": 76,
                  "Low Wood Block": 77,
                  "Mute Cuica": 78,
                  "Open Cuica": 79,
                  "Mute Triangle": 80,
                  "Open Triangle": 81
                  }

chordTypes = {"0":          [0],
              "5":          [0, 7],
              "maj(omit5)": [0, 4],
              "min(omit5)": [0, 3],
              "d5":         [0, 6],
              "maj":        [0, 4, 7],
              "min":        [0, 3, 7],
              "aug":        [0, 4, 8],
              "dim":        [0, 3, 6],
              "sus4":       [0, 5, 7],
              "sus2":       [0, 2, 7],
              "7":          [0, 4, 7, 10],
              "maj7":       [0, 4, 7, 11],
              "min7":       [0, 3, 7, 10],  # inversion (rotation) of 6
              "min(maj7)":  [0, 3, 7, 11],
              "min7(b5)":   [0, 3, 6, 10],  # inversion (rotation) of min6
              "dim7":       [0, 3, 6, 9],
              "6":          [0, 4, 7, 9],   # inversion (rotation) of min7
              "min6":       [0, 3, 7, 9],   # inversion (rotation) of min7(b5)
              "add9":       [0, 4, 7, 14],
              "min(add9)":  [0, 3, 7, 14],
              "7sus4":      [0, 5, 7, 10],
              "add11":      [0, 4, 7, 17],
              "min(add11)": [0, 3, 7, 16],
              "9":          [0, 4, 7, 10, 14],
              "b9":          [0, 4, 7, 10, 13],
              "maj9":       [0, 4, 7, 11, 14],
              "min9":       [0, 3, 7, 10, 14],
              "11":         [0, 4, 7, 10, 14, 17],
              "maj11":      [0, 4, 7, 11, 14, 17],
              "min11":      [0, 3, 7, 10, 14, 17],
              "13":         [0, 4, 7, 10, 14, 17,21], # TODO i've read 5th 9th an 11th weren't usualy played

              }

chordIntervals = {"0":           [],
                  "5":           [23],
                  "maj(omit5)":  [12],
                  "min(omit5)":  [11],
                  "d5":          [22],
                  "maj":         [12, 11],
                  "min":         [11, 12],
                  "aug":         [12, 12],
                  "dim":         [11, 11],
                  "sus4":        [17, 6],
                  "sus2":        [6, 17],
                  "7":           [12, 11, 11],
                  "7sus4":       [17, 6, 11],
                  "maj7":        [12, 11, 12],
                  "min7":        [11, 12, 11],  # inversion (rotation) of 6
                  "min(maj7)":   [11, 12, 12],
                  "min7(b5)":    [11, 11, 12],  # inversion (rotation) of min6
                  "dim7":        [11, 11, 11],
                  "6":           [12, 11, 6],   # inversion (rotation) of min7
                  "min6":        [11, 12, 6],   # inversion (rotation) of min7(b5)
                  "add9":        [12, 11, 23],
                  "min(add9)":   [11, 12, 23],
                  "add11":       [12, 11, 34],
                  "min(add11)":  [11, 12, 34],
                  "add#11":      [12, 11, 35],
                  "min(add#11)": [11, 12, 35],
                  "9":           [12, 11, 11, 12],
                  "maj9":        [12, 11, 12, 11],
                  "min9":        [11, 12, 11, 11],
                  "11":          [12, 11, 11, 12, 11],
                  "maj11":       [12, 11, 12, 11, 11],
                  "min11":       [11, 12, 11, 12, 11],
                  "#11":         [12, 11, 11, 12, 12],
                  "maj#11":      [12, 11, 11, 12, 12],
                  "min#11":      [11, 12, 11, 12, 12],
                  }


if __name__ == '__main__':
    # check chord rotations (for duplicates!)

    def getConsecutiveIntervalList(l):
        res = []
        lmod = map(lambda x: x % 12, l)
        lmod.sort()
        for i in range(1, len(l)):
            res.append(lmod[i] - lmod[i-1])
        res.append(12-lmod[-1])
        return res


    def hasCommonRotation(l1, l2):
        length = len(l1)
        for start in range(length):
            isEqual = True
        for i in range(length):
            isEqual &= (l1[(-start + i + length) % length] == l2[i])
        if isEqual:
            return start
        return None


    chords = {}
    for k, v in chordTypes.items():
        numElem = len(v)
        if numElem not in chords:
            chords[numElem] = {}
        chords[numElem][k] = v

    for n, c in chords.items():
        if int(n) > 1:
            for k, v in c.items():
                for k2, v2 in c.items():
                    if k != k2:
                        cR = hasCommonRotation(getConsecutiveIntervalList(v),
                                               getConsecutiveIntervalList(v2))
                        if cR:
                            print ('commonRotation', k, k2, cR)
