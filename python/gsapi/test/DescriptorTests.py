import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import *

from GSPatternTestUtils import *

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
		descriptor = GSDescriptors.GSDescriptorChord(forceMajMin=False)
		harmonyDataset = GSDataset(midiGlob="*.mid",midiFolder = self.getLocalCorpusPath('harmony'),midiMap="pitchNames",checkForOverlapped = True)

		for  p in harmonyDataset:
			print p.name
			sliced = p.splitInEqualLengthPatterns(4);
			for s in sliced:
				# s.printASCIIGrid(1);
				chord = descriptor.getDescriptorForPattern(s)
				print chord


if __name__=='__main__':
	runTest(profile = True,getStat = False)