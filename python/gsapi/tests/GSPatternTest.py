import unittest,os
if __name__=='__main__':
	import sys
	pathToAdd = os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir))
	sys.path.insert(1,pathToAdd)
	


from gsapi import *


class GSPatternTest(unittest.TestCase):

	midiMap = {"Kick":36,"Rimshot":37,"Snare":38,"Clap":39,"Clave":40,"LowTom":41,"ClosedHH":42,"MidTom":43,"Shake":44,"HiTom":45,"OpenHH":46,"LowConga":47,"HiConga":48,"Cymbal":49,"Conga":50,"CowBell":51}
	midiFolder = os.path.abspath("../../../test/midiDatasets/")
	defaultFile = 'funkyfresh.mid'

	def importMIDI(self):
		return GSIO.fromMidi(os.path.join(self.midiFolder,self.defaultFile),self.midiMap)

	def checkPatternValid(self,pattern,msg=None):
		self.assertTrue(len(pattern.events)>0,msg)
		for e in pattern.events:
			self.assertTrue(e.duration>0,msg)
			self.assertTrue(e.startTime>=0,msg)
		self.checkNoTagsOverlaps(pattern,msg)

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
		self.checkPatternValid(p,'import Pattern failed')
		p = p.getPatternForTimeSlice(0,4)
		self.checkPatternValid(p,'slicing pattern failed')
		ps = p.splitInEqualLengthPatterns(4,copy=False)
		for p in ps:
			self.checkPatternValid(p,'spit in equalLength failed')

	def test_Silences(self):
		p = self.importMIDI()
		
		p.fillWithSilences(p.duration)
		self.checkPatternValid(p,'fill with silence failed')



if __name__=='__main__':
		unittest.main()

# if __name__=='__main__':

# 	crawledFolder = "../test/midi/*.mid"
# 	customNoteMapping = {"Kick":36,"Rimshot":37,"Snare":38,"Clap":39,"Clave":40,"LowTom":41,"ClosedHH":42,"MidTom":43,"Shake":44,"HiTom":45,"OpenHH":46,"LowConga":47,"HiConga":48,"Cymbal":49,"Conga":50,"CowBell":51}

# 	profile =True
# 	if profile:
# 		import cProfile
# 		import re
# 		cProfile.run('patterns = fromMidiCollection(crawledFolder,customNoteMapping,TagsFromTrackNameEvents=False,desiredLength=4)',filename='profiled')
# 		patterns = fromMidiCollection(crawledFolder,customNoteMapping,TagsFromTrackNameEvents=False,desiredLength=4)
# 		print patterns
# 		for p in patterns:
# 			p.printEvents()
# 	else:
# 		import pstats
# 		p = pstats.Stats('profiled')
# 		p.strip_dirs().sort_stats(1).print_stats()