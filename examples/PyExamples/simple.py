import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir,"python")))

from gsapi import *


# choose base folder to crawl
defaultMidiFolder = "../../corpus/drums"
# generate a dataset from all midi files in defaultMidiFolder
# all events will have tags corresponding to generalMIDI mapping see generalMidiMap
dataset = GSDataset(midiFolder=defaultMidiFolder,midiGlob="*.mid",midiMap=GSPatternUtils.generalMidiMap,checkForOverlapped = True)

# GSDataset is nothing more than a class containing a list of datasets
# let say we want to retrieve every 16 beat long slice from this dataset
allPatternsSliced = []
sizeOfSlice = 16
for midiPattern in dataset.patterns:
	for sliced in midiPattern.splitInEqualLengthPatterns(4):
		allPatternsSliced+=[sliced]

# 
markovStyle = GSStyles.GSMarkovStyle(order=3,numSteps=32,loopDuration=sizeOfSlice);
markovStyle.generateStyle(allPatternsSliced)
newPattern = markovStyle.generatePattern()

allTags = allPatternsSliced[0].getAllTags()
tagToSearch =  allTags[0]

densityDescriptor = GSDescriptors.GSDescriptorDensity();
for p in allPatternsSliced:
	p = p.getPatternWithTags(tags="kick")
	densityDescriptor.getDescriptorForPattern(p)
		





exit()


for p in self.dataset.patterns:
	allTags = p.getAllTags()
	density = descriptor.getDescriptorForPattern(p);

