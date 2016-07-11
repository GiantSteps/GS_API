import unittest,os
if __name__=='__main__':
	import sys
	pathToAdd = os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir))
	sys.path.insert(1,pathToAdd)

	


from gsapi import *
import random,glob

class GSPatternTest(unittest.TestCase):

	midiMap = {"Kick":36,"Rimshot":37,"Snare":38,"Clap":39,"Clave":40,"LowTom":41,"ClosedHH":42,"MidTom":43,"Shake":44,"HiTom":45,"OpenHH":46,"LowConga":47,"HiConga":48,"Cymbal":49,"Conga":50,"CowBell":51}
	midiFolder = os.path.abspath("../../../test/midiDatasets/daftpunk.mid")
	f = glob.glob(midiFolder)
	idx = random.randint(0,len(f)-1)

	def importMIDI(self):
		print 'using ' +self.f[self.idx]
		p  = GSIO.fromMidi(self.f[self.idx],self.midiMap,tracksToGet=[1])
		self.assertTrue(p!=None, 'cant import midi file')
		self.assertTrue(p.duration>0, 'cant import midi file : no duration')
		self.assertTrue(p.events!=[], 'cant import midi file : no events')
		return p

	def checkPatternValid(self,pattern,checkForDoublons =True,checkOverlap = True,msg=None):
		self.assertTrue(len(pattern.events)>0,msg)
		eToStr =[]
		for e in pattern.events:
			eToStr+= [self.evToStr(e)];
		i=0
		for e in pattern.events:
			self.assertTrue(e.duration>0,msg + eToStr[i])
			self.assertTrue(e.startTime>=0,msg + eToStr[i])
			i+=1
		
		if(checkForDoublons):
			i = 0 ;
			for e in pattern.events:
				for ii in range(i+1,len(pattern.events)):
					ee = pattern.events[ii]
					self.assertFalse((e.startTime==ee.startTime) and 
						(e.duration==ee.duration) and
						(e.pitch==ee.pitch) and 
						(e.tags == ee.tags),msg + eToStr[i]+'/'+eToStr[ii])
				i+=1

		if checkOverlap : self.checkNoTagsOverlaps(pattern,msg )

	def evToStr(self,e):
		return (', '.join(['%s']*len(e.tags))+' %d %.2f %.2f')%(tuple(e.tags)+(e.pitch,e.startTime,e.duration))


	def checkNoTagsOverlaps(self,pattern,msg=None):
		tags = pattern.getAllTags();
		for t in tags:
			lastTimeOff = 0
			for e in pattern.events:
				if t in e.tags:
					self.assertTrue(e.startTime>=lastTimeOff,msg);
					lastTimeOff = e.getEndTime()

	def test_Import(self):
		p = self.importMIDI()
		self.checkPatternValid(p,msg='import Pattern failed')
		p = p.getPatternForTimeSlice(0,4)
		self.checkPatternValid(p,msg='slicing pattern failed')
		ps = p.splitInEqualLengthPatterns(4,copy=False)
		for p in ps:
			self.checkPatternValid(p,msg='spit in equalLength failed')

	def test_Silences(self):
		p = self.importMIDI()
		p.fillWithSilences(perTag=True)
		self.checkPatternValid(p,checkForDoublons = False,checkOverlap = False,msg='fill with silence per tag failed')

	def test_stretch(self):
		p = self.importMIDI()
		
		p = p.getPatternForTimeSlice(0,4)
		p.timeStretch(32/4.0)
		p.alignOnGrid(1)
		p.removeOverlapped()
		p.fillWithSilences(maxSilenceTime = 1);
		p.setDurationFromLastEvent(False)

		self.assertTrue(p.events[-1].startTime == 31)
		self.checkPatternValid(p,msg='stretch failed')
		



if __name__=='__main__':
	profile =False
	pStat = False
	if profile:
		import cProfile
		import re
		cProfile.run('unittest.main()',filename='profiled')
	if pStat:
		import pstats
		p = pstats.Stats('profiled')
		p.strip_dirs().sort_stats(1).print_stats()
	if not pStat and not profile:
		unittest.main()


