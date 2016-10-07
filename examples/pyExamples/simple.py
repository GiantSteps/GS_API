import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir,"python")))

from gsapi import *

defaultMidiFolder = "../../test/midiDatasets"

GSDataset.log

dataset = GSDataset(midiFolder=defaultMidiFolder,midiGlob="*.mid",midiMap=GSIO.generalMidiMap,checkForOverlapped = True)


allPatternsSliced = []

sizeOfSlice = 16
for midiPattern in dataset.patterns:
	for sliced in midiPattern.splitInEqualLengthPatterns(4):
		allPatternsSliced+=[sliced]

markovStyle = GSMarkovStyle(order=3,numSteps=32,loopDuration=sizeOfSlice);
markovStyle.generateStyle(allPatternsSliced)
newPattern = markovStyle.generatePattern()

allTags = allPatternsSliced[0].getAllTags()
tagToSearch =  allTags[0]

densityDescriptor = GSDescriptorDensity();
for p in allPatternsSliced:
	p = p.getPatternWithTags(tags="kick")
	densityDescriptor.getDescriptorForPattern(p)
		





exit()


for p in self.dataset.patterns:
	allTags = p.getAllTags()
	density = descriptor.getDescriptorForPattern(p);

