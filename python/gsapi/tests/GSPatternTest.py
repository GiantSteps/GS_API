import unittest,os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

	


from gsapi import *
import random,glob
from GSPatternTestUtils import *

class GSPatternTest(GSPatternTestUtils):
	
	
	


	def test_Import(self):
		dataSet = GSDataset(midiGlob="*.mid",midiMap="pitchNames",checkForOverlapped=True)
		for p in dataSet.patterns:
			
			self.assertTrue(p!=None, 'cant import midi file %s'%p.name)
			self.assertTrue(p.duration>0, 'cant import midi file %s: no duration'%p.name)
			self.assertTrue(p.events!=[], 'cant import midi file %s: no events'%p.name)
			self.checkPatternValid(p,msg='import Pattern %s failed'%p.name)
			p = p.getPatternForTimeSlice(0,4)
			self.checkPatternValid(p,msg='slicing pattern failed')
			ps = p.splitInEqualLengthPatterns(4,copy=False)
			for p in ps:
				self.checkPatternValid(p,msg='spit in equalLength failed')

	def test_Silences(self):
		dataSet = GSDataset(midiGlob="*.mid",midiMap="pitchNames",checkForOverlapped=True)
		for p in dataSet.patterns:
			pattern1 = p.getFilledWithSilences(perTag=True)
			pattern2 = p.getFilledWithSilences(perTag=False)
			self.checkPatternValid(pattern1,checkForDoublons = False,checkOverlap = False,msg='fill with silence per tag failed')
			self.checkPatternValid(pattern2,checkForDoublons = False,checkOverlap = False,msg='fill with silence failed')
	def test_stretch(self):
		dataSet = GSDataset(midiGlob="*.mid",midiMap="pitchNames",checkForOverlapped=True)
		for p in dataSet.patterns:
			originPattern = p.copy()
			p = p.getPatternForTimeSlice(0,4)
			p.timeStretch(32/4.0)
			p.alignOnGrid(1)
			# p.removeOverlapped()
			p.fillWithSilences(maxSilenceTime = 1);
			p.setDurationFromLastEvent(False)

			self.assertTrue(p.events[-1].startTime == 31)
			self.checkPatternValid(p,msg='stretch failed \n\n%s \n\n%s'%(originPattern,p))

	def test_legato(self):
		dataSet = GSDataset(midiGlob="*.mid",midiMap="pitchNames",checkForOverlapped=True)
		patternList = dataSet[0].splitInEqualLengthPatterns(4,copy=False)
		for p in patternList:
			p.applyLegato()
			self.checkPatternValid(p,msg='legato failed')


			





if __name__=='__main__':
	
	runTest(profile = True,getStat = False)


