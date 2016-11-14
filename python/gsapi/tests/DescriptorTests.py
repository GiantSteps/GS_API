import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import *

from GSPatternTestUtils import *

class DescriptorTests(GSPatternTestUtils):

	dataset = GSDataset(midiGlob="funkyfresh.mid",midiMap="pitchNames",checkForOverlapped = True)

	def test_density_simple(self):
		descriptor = GSDescriptors.GSDescriptorDensity();
		for p in self.dataset.patterns:
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
		for p in self.dataset.patterns:
			# p = p.getPatternWithTags(p.getAllTags()[0])
			sliced = p.splitInEqualLengthPatterns(descriptor.duration)
			print p
			for s in sliced:
				syncopation =  descriptor.getDescriptorForPattern(s);
				
				self.assertTrue(syncopation>=0 , "syncopation value not valid : %f"%(syncopation))


if __name__=='__main__':
	runTest(profile = True,getStat = False)