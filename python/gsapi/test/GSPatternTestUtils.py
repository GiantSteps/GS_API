
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


class singleTonDataset(GSDataset):
	def __init__(self,**kwargs):
		self.creationArgs = kwargs
		self.dataset = None

	def get():
		if not self.dataset:
			self.dataset = GSDataset(**self.creationArgs)
		return dataset

class GSTestBase(unittest.TestCase):
	"""
	helper function for test classes
	"""


	__cachedDataset = None
	@property
	def cachedDataset(self):
		if not self.__cachedDataset:
			self.__cachedDataset = self.generateCachedDataset()
		return self.__cachedDataset
		

	# sub class can override that to load a cached dataset only once per session (not per test)
	#  default will crawl all midiTests Folder
	def generateCachedDataset(self):
		raise GSDataset(midiGlob="*.mid",midiFolder = self.getLocalCorpusPath('midiTests'),midiMap="pitchNames",checkForOverlapped = True)

	# helper to get local corpus path
	def getLocalCorpusPath(self,toAppend=""):
		import os
		return os.path.abspath(__file__ + "../../../../../corpus/"+toAppend)


	def checkNoTagsOverlaps(self,pattern,msg=None):
		tags = pattern.getAllTags();
		for t in tags:
			lastTimeOff = 0
			for e in pattern.events:
				if t in e.tags:
					self.assertTrue(e.startTime>=lastTimeOff,"%s : (%f<%f) tag : %s"%(msg,e.startTime,lastTimeOff,t));
					lastTimeOff = e.getEndTime()

	def checkPatternValid(self,pattern,checkForDoublons =True,checkOverlap = True,msg=""):
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


	def setUp(self):
		print '-------------------------------------'
		print "Starting test : ", self._testMethodName
		print '-------------------------------------'