
from gsapi import GSStyle,GSPattern,GSPatternEvent
import random

class GSDBStyle(GSStyle):
	""" A database based style
	simply generatePatterns from existing patterns

	Args:
		generatePatternOrdering: can be 'indexed','increasing','random' , defining the generatePattern behaviour
	"""
	def __init__(self,generatePatternOrdering = "indexed"):
		self.generatePatternOrdering=generatePatternOrdering
		self.patternList = []
		self.currentIdx = 0;
	def generateStyle(self, PatternClasses):
		self.patternList = PatternClasses;

	def generatePattern(self,seed=None):

		if self.generatePatternOrdering=='increasing':
			p = self.patternList[self.currentIdx]
			self.currentIdx+=1
			print "reading ",self.currentIdx
			return p
		elif self.generatePatternOrdering=='random':
			return self.patternList[int(random.random()*len(self.patternList))]
		elif self.generatePatternOrdering=='indexed':
			return self.patternList[self.currentIdx]


	def getDistanceFromStyle(self,Pattern):
		raise NotImplementedError( "Should have implemented this" )

	def getClosestPattern(self,Pattern,seed=0):
		raise NotImplementedError( "Should have implemented this" )

	def getInterpolated(self,PatternA,PatternB,distanceFromA,seed=0):
		raise NotImplementedError( "Should have implemented this" )

	def getInternalState(self):
		res = {"patternList":[]}
		for e in self.patternList:
			res["patternList"]+=[e.toJSONDict()]
		return res

	def setInternalState(self,internalStateDict):
		self.patternList = []
		for e in internalStateDict["patternList"]:
			p = GSPattern()
			p.fromJSONDict(e);
			self.patternList += [p]

	def isBuilt(self):
		self.patternList!=[]


