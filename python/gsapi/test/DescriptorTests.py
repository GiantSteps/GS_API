import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import *

from GSPatternTestUtils import *
from gsapi.GSPatternUtils import *

class DescriptorTests(GSTestBase):
	


	def generateCachedDataset(self):
		return GSDataset(midiGlob="funkyfresh.mid",midiFolder = self.getLocalCorpusPath('midiTests'),midiMap="pitchNames",checkForOverlapped = True)

	def test_density_simple(self):

		descriptor = GSDescriptors.GSDescriptorDensity();
		for p in self.cachedDataset.patterns:
			allTags = p.getAllTags()
			density = descriptor.getDescriptorForPattern(p);
			p2 = p.getPatternWithTags([allTags[0]])
			density2 = descriptor.getDescriptorForPattern(p2)
			print density,density2,p.duration
			self.assertTrue(density>=0,p.name + " negative density : "+str(density))
			self.assertTrue(density< p.duration * len(allTags),p.name +" density over maximum bound : %f %f %f"%(density,p.duration ,len(allTags)))
			self.assertTrue(density2<=density,"part of the pattern has a bigger density than the whole")




	def test_syncopation(self):
		descriptor = GSDescriptors.GSDescriptorSyncopation();
		for p in self.cachedDataset.patterns:
			# p = p.getPatternWithTags(p.getAllTags()[0])
			sliced = p.splitInEqualLengthPatterns(descriptor.duration)
			print p
			for s in sliced:
				syncopation =  descriptor.getDescriptorForPattern(s);
				
				self.assertTrue(syncopation>=0 , "syncopation value not valid : %f"%(syncopation))

	def test_chords(self):
		descriptor = GSDescriptors.GSDescriptorChord(forceMajMin=False,allowDuplicates=True)
		# GSIO.gsiolog.setLevel('INFO')
		harmonyDataset = GSDataset(midiGlob="Im9-bVIadd9-VIm9-VIm9.mid",midiFolder = self.getLocalCorpusPath('harmony'),midiMap="pitchNames",checkForOverlapped = True)

		for  p in harmonyDataset:
			# print p.name,p.duration,p

			gt = p.name.split('.')[0].split('-')
			groundTruthBase = map(stringToChord,gt)
			# print groundTruthBase
			lengthOfChords = p.duration/len(groundTruthBase)
			# print lengthOfChords
			sliced = p.splitInEqualLengthPatterns(lengthOfChords);
			chords = [] 
			# print sliced
			# exit()
			for s in sliced:
				# s.printASCIIGrid(1);
				chords.append( descriptor.getDescriptorForPattern(s))
				

			print chords



			def checkProposition(root,prop,truth,index):
				res = False
				if index>=len(prop):
					return True
				for p in prop[index]:
					if p == 'silence':
						return False
					if index==0:
						root = defaultPitchNames.index(p[0])
					# print index,truth[index][0],defaultPitchNames.index(p[0])-root
					if truth[index][0]==(defaultPitchNames.index(p[0])-root+12) %12:
						if index < len(truth):
							if checkProposition(root,prop,truth,index+1):
								return True

				return False


			if len(chords)==len(groundTruthBase):
				hasValidProposition =  checkProposition(0,chords,groundTruthBase,0)
				if not hasValidProposition:
					self.assertTrue(False,"proposition not valid :\nproposition: %s\ngroundTruth: %s"%(chords,groundTruthBase))



			else:
				print p
				self.assertTrue(False,'annotation not based on 4beat division or midiFile larger')



def stringToChord(s):
	isFirstPart = True
	allowedChars = 'VI'
	degree = ""
	armature = ""

	degNum = 0
	
	if s[0]=='b':
		degNum-=1
		s = s[1:]
	if s[0]=='#':
		degNum+=1
		s = s[1:]
	for e in s:
		
		if isFirstPart:
			if e not in allowedChars:
				isFirstPart=False

		if isFirstPart:
			degree+=e
		else:
			armature+=e
	
	degrees = {"I":0,"II":2,"III":4,"IV":5,"V":7,"VI":9,"VII":11}


	degNum+=degrees[degree]
	
	if armature=='':
		armature  = 'maj'
	elif armature=='m9':
		armature  = 'min9'
	elif armature=='m7':
		armature  = 'min7'
	


	return (degNum,armature)




if __name__=='__main__':
	runTest(profile = True,getStat = False)