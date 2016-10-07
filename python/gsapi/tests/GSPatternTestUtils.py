
import unittest,os,sys,glob,random
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))


from gsapi import *

def runTest(profile=False,getStat=False):
	if profile:
		import cProfile
		import re
		cProfile.run('unittest.main()',filename='profiled')
	if getStat:
		import pstats
		p = pstats.Stats('profiled')
		p.strip_dirs().sort_stats(1).print_stats()
	if not getStat and not profile:
		unittest.main()

class GSPatternTestUtils(unittest.TestCase):
	"""
	helper function for test classes
	"""
	
	# def __init__(self,GSDataset):
	# 	unittest.TestCase.__init__(self,*args)
		



	def checkNoTagsOverlaps(self,pattern,msg=None):
		tags = pattern.getAllTags();
		for t in tags:
			lastTimeOff = 0
			for e in pattern.events:
				if t in e.tags:
					self.assertTrue(e.startTime>=lastTimeOff,"%s : (%f<%f) tag : %s"%(msg,e.startTime,lastTimeOff,t));
					lastTimeOff = e.getEndTime()

	def checkPatternValid(self,pattern,checkForDoublons =True,checkOverlap = True,msg=None):
		self.assertTrue(len(pattern.events)>0,msg)
		i=0
		for e in pattern.events:
			self.assertTrue(e.duration>0,msg + str(e))
			self.assertTrue(e.startTime>=0,msg + str(e))
			i+=1
		
		if(checkForDoublons):
			i = 0 ;
			for e in pattern.events:
				for ii in range(i+1,len(pattern.events)):
					ee = pattern.events[ii]
					self.assertFalse((e.startTime==ee.startTime) and 
						(e.duration==ee.duration) and
						(e.pitch==ee.pitch) and 
						(e.tags == ee.tags),"%s : %s doublons %s // %s"%(pattern.name, msg ,e,ee ))
				i+=1

		if checkOverlap : self.checkNoTagsOverlaps(pattern,msg )