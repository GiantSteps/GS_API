

def pitchToName(pitch, pitchNames):
    octaveLength = len(pitchNames)
    octave = (pitch / octaveLength) - 1
    note = pitch % octaveLength
    return pitchNames[note] + str(octave)