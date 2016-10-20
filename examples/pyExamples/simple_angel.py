import sys
from gsapi import *

if __name__=='__main__':
	sys.path.insert(1, os.path.abspath(os.path.join(__file__,
                                                    os.pardir,
                                                    os.pardir,
                                                    os.pardir,
                                                    "python")))

defaultMidiFolder = "../../test/midiDatasets/corpus-harmony"
dataset = GSDataset(midiFolder=defaultMidiFolder,
                    midiGlob="*.mid",
                    midiMap=GSIO.defaultPitchNames,
                    checkForOverlapped=True)


all_patterns_sliced = []
slice_size = 16

for midiPattern in dataset.patterns:
	for sliced in midiPattern.splitInEqualLengthPatterns(4):
		all_patterns_sliced += [sliced]

"""
markovStyle = GSMarkovStyle(order=3, numSteps=32, loopDuration=slice_size)
markovStyle.generateStyle(all_patterns_sliced)
newPattern = markovStyle.generatePattern()

allTags = all_patterns_sliced[0].getAllTags()
tagToSearch =  allTags[0]

densityDescriptor = GSDescriptorDensity()
for p in all_patterns_sliced:
	p = p.getPatternWithTags(tags="C    ")
	densityDescriptor.getDescriptorForPattern(p)

exit()

for p in self.dataset.patterns:
	allTags = p.getAllTags()
	density = descriptor.getDescriptorForPattern(p)

"""