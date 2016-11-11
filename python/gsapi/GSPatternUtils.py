

def pitchToName(pitch, pitchNames):
    octaveLength = len(pitchNames)
    octave = (pitch / octaveLength) - 1
    note = pitch % octaveLength
    return pitchNames[note] + str(octave)



defaultPitchNames = ["C",  # default pitch names for pitch class
                     "C#",
                     "D",
                     "Eb",
                     "E",
                     "F",
                     "F#",
                     "G",
                     "Ab",
                     "A",
                     "Bb",
                     "B"]


simpleDrumMap = {"Kick": 36,
                          "Rimshot": 37,
                          "Snare": 38,
                          "Clap":39,
                          "Clave":40,
                          "LowTom":41,
                          "ClosedHH":42,
                          "MidTom":43,
                          "Shake":44,
                          "HiTom":45,
                          "OpenHH":46,
                          "LowConga":47,
                          "HiConga":48,
                          "Cymbal":49,
                          "Conga":50,
                          "CowBell":51
                          }


generalMidiMap = {"Acoustic Bass Drum":35, #  from General Midi Specification
                  "Bass Drum 1":36,
                  "Side Stick":37,
                  "Acoustic Snare":38,
                  "Hand Clap":39,
                  "Electric Snare":40,
                  "Low Floor Tom":41,
                  "Closed Hi Hat":42,
                  "High Floor Tom":43,
                  "Pedal Hi-Hat":44,
                  "Low Tom":45,
                  "Open Hi-Hat":46,
                  "Low-Mid Tom":47,
                  "Hi-Mid Tom":48,
                  "Crash Cymbal 1":49,
                  "High Tom":50,
                  "Ride Cymbal 1":51,
                  "Chinese Cymbal":52,
                  "Ride Bell":53,
                  "Tambourine":54,
                  "Splash Cymbal":55,
                  "Cowbell":56,
                  "Crash Cymbal 2":57,
                  "Vibraslap":58,
                  "Ride Cymbal 2":59,
                  "Hi Bongo":60,
                  "Low Bongo":61,
                  "Mute Hi Conga":62,
                  "Open Hi Conga":63,
                  "Low Conga":64,
                  "High Timbale":65,
                  "Low Timbale":66,
                  "High Agogo":67,
                  "Low Agogo":68,
                  "Cabasa":69,
                  "Maracas":70,
                  "Short Whistle":71,
                  "Long Whistle":72,
                  "Short Guiro":73,
                  "Long Guiro":74,
                  "Claves":75,
                  "Hi Wood Block":76,
                  "Low Wood Block":77,
                  "Mute Cuica":78,
                  "Open Cuica":79,
                  "Mute Triangle":80,
                  "Open Triangle":81
                  }
