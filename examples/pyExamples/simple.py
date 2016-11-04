import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir,"python")))

from gsapi import *

defaultMidiFolder = "../../corpus/midiTests"



dataset = GSDataset(midiFolder=defaultMidiFolder,midiGlob="hiphop.mid",midiMap=MidiMap.generalMidiMap,checkForOverlapped = True)


allPatternsSliced = []

sizeOfSlice = 32
for midiPattern in dataset.patterns:
	for sliced in midiPattern.splitInEqualLengthPatterns(4):
		allPatternsSliced+=[sliced]

markovStyle = GSMarkovStyle(order=1,numSteps=32,loopDuration=sizeOfSlice);
markovStyle.generateStyle(allPatternsSliced)
newPattern = markovStyle.generatePattern()
print newPattern
newPattern.toMIDI(path="", midiMap=MidiMap.generalMidiMap)

allTags = allPatternsSliced[0].getAllTags()
tagToSearch =  allTags[0]

justkick=newPattern.getPatternWithTags('Acoustic Bass Drum', exactSearch=True, copy=True)

kickAsList=[0]*sizeOfSlice
for s,e in enumerate(justkick.events):

    kickAsList[int(e.startTime)]=1

print kickAsList


"""
densityDescriptor = GSDescriptorDensity();
for p in allPatternsSliced:
	p = p.getPatternWithTags(tags="kick")
	densityDescriptor.getDescriptorForPattern(p)
		





exit()


for p in self.dataset.patterns:
	allTags = p.getAllTags()
	density = descriptor.getDescriptorForPattern(p);
"""
