import unittest,os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

	


from gsapi import *
import random,glob
from GSPatternTestUtils import *

class GSPatternTest(GSPatternTestUtils):

	dataSet = GSDataSet(midiGlob="corpus-harmony/*.mid",midiMap="pitchNames")
	


	def test_Import(self):
		for p in self.dataSet.patterns:
			self.assertTrue(p!=None, 'cant import midi file')
			self.assertTrue(p.duration>0, 'cant import midi file : no duration')
			self.assertTrue(p.events!=[], 'cant import midi file : no events')
			self.checkPatternValid(p,msg='import Pattern failed')
			p = p.getPatternForTimeSlice(0,4)
			self.checkPatternValid(p,msg='slicing pattern failed')
			ps = p.splitInEqualLengthPatterns(4,copy=False)
			for p in ps:
				self.checkPatternValid(p,msg='spit in equalLength failed')

	def test_Silences(self):
		for p in self.dataSet.patterns:
			p.fillWithSilences(perTag=True)
			self.checkPatternValid(p,checkForDoublons = False,checkOverlap = False,msg='fill with silence per tag failed')

	def test_stretch(self):
		for p in self.dataSet.patterns:
			
			
			p = p.getPatternForTimeSlice(0,4)
			p.timeStretch(32/4.0)
			p.alignOnGrid(1)
			p.removeOverlapped()
			p.fillWithSilences(maxSilenceTime = 1);
			p.setDurationFromLastEvent(False)

			self.assertTrue(p.events[-1].startTime == 31)
			self.checkPatternValid(p,msg='stretch failed')
			





if __name__=='__main__':
	runTest(profile = True,getStat = False)


