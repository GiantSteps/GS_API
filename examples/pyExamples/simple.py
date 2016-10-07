import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import *



defaultMidiFolder = "/Users/mhermant/Documents/Work/Dev/GS_API/test/midiDatasets"


dataset = GSDataSet(midiFolder=defaultMidiFolder,midiGlob="*.mid",midiMap=GSIO.generalMidiMap,checkForOverlapped = True)


allPatternsSliced = []
for midiPattern in dataset.patterns:
	for sliced in midiPattern.splitInEqualLengthPatterns(4):
		allPatternsSliced+=[sliced]

markovStyle = GSMarkovStyle(order=3,numSteps=32,loopDuration=16);
markovStyle.generateStyle(allPatternsSliced)
newPattern = markovStyle.generatePattern()

allTags = allPatternsSliced[0].getAllTags()
tagToSearch =  allTags[0]

densityDescriptor = GSDescriptorDensity();
for p in allPatternsSliced:
	p = p.getPatternWithTags(tags="kick")
	densityDescriptor.getDescriptorForPattern(p)
		



print totalDensity



exit()


for p in self.dataset.patterns:
	allTags = p.getAllTags()
	density = descriptor.getDescriptorForPattern(p);

