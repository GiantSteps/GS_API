from gsapi import GSStyle
import random
import numpy as np
from numpy.random import random_sample
import copy

class GSMarkovStyle(GSStyle):
	""" compute sa style based on markov chains

	Args:
		order: order used for markov computation
		numSteps: number of steps to consider (binarization of pattern)

	Attributes:
		order: order used for markov computation
		numSteps: number of steps to consider (binarization of pattern)

	"""
	def __init__(self,order,numSteps):
		super(GSStyle,self).__init__()
		self.type = "None"
		self.order = order;
		self.numSteps = numSteps;


	def generateStyle(self, PatternClasses):
		""" generate style based on list of GSPattern
		Args:
			PatternClasses :  list of GSPatterns
		"""
		if not isinstance(PatternClasses,list):
			print "style need a list"
			return False
		else:
			self.originPatterns = PatternClasses;
			self.buildStyle();


	def buildStyle(self):
		""" builds transisiont table for the previously given list of GSPattern
		"""
		self.transitionTable = [{} for f in range(self.numSteps)]

		self.binarizedPatterns = copy.deepcopy(self.originPatterns)
		for p in self.binarizedPatterns:
			self.formatPattern(p)
			for e in p.events :
				lastEvents = self.getLastEvents(p,e,self.order,1)
				curDic = self.transitionTable[int(e.startTime)]
				combinationName = self._buildNameForEvents(lastEvents)

				
				if combinationName not in curDic:
					curDic[combinationName] = {}
				for n in e.tags:
					if n not in curDic[combinationName]:
						curDic[combinationName][n] = 1
					else:
						curDic[combinationName][n] += 1
				# print e.tags , [ x.tags  for t in lastEvents for x in t]
		print self.transitionTable
		def _normalize():
			for t in self.transitionTable:
				for d in t:
					sum= 0
					for pe in t[d]:
						sum+= t[d][pe]
					
					for pe in t[d]:
						t[d][pe]/=1.0*sum
		_normalize()
		print self.transitionTable

	def generatePattern(self,seed = None):
		""" generate a new pattern
		Args:
			seed: seed used for random initialisation of pattern (value of None generates a new one)
		"""
		random.seed(seed)
		potentialStartEvent = []

		def _getAvailableAtStep(step):
			res = []
			if step < 0 : step+=len(self.transitionTable)
			for n in self.transitionTable[step]:
				for t in self.transitionTable[step][n]:
					res+=[t]
			return res

		def _isValidState(step,previousTags):
			d = self.transitionTable[step]
			return previousTags in d

		def _generateEventAtStep(step,previousTags):
			if not previousTags in self.transitionTable[step] : return None
			d = self.transitionTable[step][previousTags]
			bins = np.cumsum([d[x] for x in d])
			chosenIdx = np.digitize(random.random(), bins);
			
			return d.keys()[chosenIdx]
			
			
			


		
		cIdx = self.order
		startHypothesis =[]
		for n in range (self.order):
			startHypothesis+=[random.choice(_getAvailableAtStep(n))]
		while not _isValidState(cIdx,','.join(startHypothesis)):
			startHypothesis =[]
			for n in range (self.order):
				startHypothesis+=[random.choice(_getAvailableAtStep(n))]

		print startHypothesis
		events = startHypothesis
		i = self.order
		while i <self.numSteps:
			print "ii"+str(i)
			print events[i-self.order:i]
			newEv =  _generateEventAtStep(i,','.join(events[i-self.order:i]))
			if newEv:
				events+=[newEv]
				i+=1
			



		


	def _buildNameForEvents(self,events):
		res = ""
		for n in events:
			for s in n:
				s.tags.sort()
				res+='/'.join(s.tags)+'/'
			res = res[:-1]
			res+=','
		res = res[:-1]
		return res

	def formatPattern(self,p):
		p.quantize(8,8);
		p.discretize(1)
		p.fillWithSilences(32);
		p.discretize(1)
		print "len" + str(len(p.events))
		

	def getLastEvents(self,pattern,event,num,stepSize):
		events = []
		for i  in range(1,num+1):
			idx = event.startTime - i*stepSize;
			if idx < 0 :
				idx+=pattern.duration
				print idx
			events += [pattern.getStartingEventsAtTime(idx,stepSize)]
		return events




	def getDistanceFromStyle(self,Pattern):
		raise NotImplementedError( "Should have implemented this" )

	def getClosestPattern(self,Pattern,seed=0):
		raise NotImplementedError( "Should have implemented this" )

	def getInterpolated(self,PatternA,PatternB,distanceFromA,seed=0):
		raise NotImplementedError( "Should have implemented this" )




if __name__ == '__main__':

	import glob,json
	from GSPattern import GSPattern
	searchPath = "../../test/slicedMidi/*.json"
	s = GSMarkovStyle(2,32)
	patterns = []
	for f in glob.glob(searchPath):
		with open(f) as j:
			d = json.load(j)
			p = GSPattern();
			p.fromJSONDict(d);
			p = p.getPatternForTimeSlice(0,4);
			print p.duration
			patterns+=[p]

	s.generateStyle(patterns)
	s.generatePattern()