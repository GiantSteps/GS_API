import os
from gsapi import *

desiredPatternLength = 4

midi_file = os.path.abspath(__file__ +
                             "../../../../test/midiDatasets/corpus-harmony/I5-IV.mid")

pattern = GSIO.fromMidi(midi_file,
                        NoteToTagsMap=midiPitchMap,
                        filterOutNotMapped=True,
                        TagsFromTrackNameEvents=False)

print pattern

	
print pattern.duration