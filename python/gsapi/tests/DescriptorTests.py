import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import *

from GSPatternTestUtils import *

class DescriptorTests(GSPatternTestUtils):

	dataset = GSDataSet(midiGlob="corpus-harmony/*.mid",midiMap="pitchNames")

	def test_density_simple(self):
		descriptor = GSDescriptorDensity();
		for p in self.dataset.patterns:
			p.printEvents()
			allTags = p.getAllTags()
			density = descriptor.getDescriptorForPattern(p);
			p2 = p.getPatternWithTags([allTags[0]])
			density2 = descriptor.getDescriptorForPattern(p2)
			print density,density2,p.duration
			self.assertTrue(density>=0,"negative density : "+str(density))
			self.assertTrue(density< p.duration * len(allTags),"density over maximum bound")
			self.assertTrue(density2<=density,"part of the pattern has a bigger density than the whole")



if __name__=='__main__':
	runTest(profile = True,getStat = False)