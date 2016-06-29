from gsapi import GSStyle,GSPattern,GSPatternEvent
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
	def __init__(self,order,numSteps,loopDuration):
		super(GSStyle,self).__init__()
		self.type = "None"
		self.order = order;
		self.numSteps = numSteps;
		self.loopDuration = loopDuration


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
			self.checkSilences(p)
			print p.duration
			for step in range(p.duration):
				l = [p.getStartingEventsAtTime(step)];
				self.checkSilenceInList(l)
				curEvent = self._buildNameForEvents(l);
				combinationName = self._buildNameForEvents(self.getLastEvents(p,step,self.order,1));
				curDic = self.transitionTable[int(step)]
				

				
				if combinationName not in curDic:
					curDic[combinationName] = {}
				
				if curEvent not in curDic[combinationName]:
					curDic[combinationName][curEvent] = 1
				else:
					curDic[combinationName][curEvent] += 1
				# print e.tags , [ x.tags  for t in lastEvents for x in t]
		
		def _normalize():
			for t in self.transitionTable:
				for d in t:
					sum= 0
					for pe in t[d]:
						sum+= t[d][pe]
					
					for pe in t[d]:
						t[d][pe]/=1.0*sum
		_normalize()
		

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
			print d,previousTags
			return previousTags in d

		def _generateEventAtStep(step,previousTags):
			
			if not previousTags in self.transitionTable[step] :  return None
			d = self.transitionTable[step][previousTags]

			chosenIdx = 0
			if len(d)>1:
				bins = np.cumsum([d[x] for x in d])
				r = random.random()
				for i in range(1,len(bins)):
					if bins[i-1]<=r and bins[i]>r:
						chosenIdx = i-1
						break;
				print chosenIdx
				
			return d.keys()[chosenIdx]


			
			


		
		cIdx = self.order
		startHypothesis =[]
		for n in range (self.order):
			startHypothesis+=[random.choice(_getAvailableAtStep(n))]
		startHypothesis.sort()
		while not _isValidState(cIdx,','.join(startHypothesis)):
			startHypothesis =[]
			for n in range (self.order):
				startHypothesis+=[random.choice(_getAvailableAtStep(n))]

		print startHypothesis
		events = startHypothesis
		i = self.order
		print self.transitionTable
		while i <self.numSteps:
			newPast =  events[i-self.order:i]
			newPast.sort();
			print newPast , i , self.numSteps,','.join(newPast)
			newEv =  _generateEventAtStep(i,','.join(newPast))
			print newEv
			if newEv:
				print i,newEv
				events+=[newEv]
				i+=1
			else:
				print "not found combination", ','.join(newPast) ,self.transitionTable[i] ;
		

		pattern = GSPattern()
		idx = 0;
		for el in events:
			l = el.split("/")
			for e in l:
				pattern.events+=[GSPatternEvent(idx*1.0*self.loopDuration/self.numSteps,1,100,127,e)]
			idx+=1
		return pattern

	def checkSilences(self,p):
		for i in range(p.duration):
			c = p.getStartingEventsAtTime(i)
			if len(c)>1 and( 'silence' in c):
				print "wrong silence"
				exit()
	def checkSilenceInList(self,c):
		if len(c)>1 and( 'silence' in c):
			print "wrong silence"
			exit()



	def _buildNameForEvents(self,events):
		res = []
		for n in events:
			curL = []
			for s in n:
				for t in s.tags:
					if t not in curL : curL+=[t]
			curL.sort()
			res+=[curL]
		res.sort()
		out = ""
		for l in res:
			out+='/'.join(l)
			out+=","
		out = out[:-1]
			
		return out

	def formatPattern(self,p):
		p.quantize(self.numSteps*1.0/self.loopDuration,self.numSteps*1.0/self.loopDuration);
		p.discretize(1)
		p.fillWithSilences(self.numSteps);
		p.discretize(1)
		p.checkDuration()
		



	def getLastEvents(self,pattern,step,num,stepSize):
		events = []
		for i  in range(1,num+1):
			idx = step - i*stepSize;
			if idx < 0 :
				idx+=pattern.duration
			events += [pattern.getStartingEventsAtTime(idx)]
		return events




	def getDistanceFromStyle(self,Pattern):
		raise NotImplementedError( "Should have implemented this" )

	def getClosestPattern(self,Pattern,seed=0):
		raise NotImplementedError( "Should have implemented this" )

	def getInterpolated(self,PatternA,PatternB,distanceFromA,seed=0):
		raise NotImplementedError( "Should have implemented this" )




if __name__ == '__main__':

	import glob,json
	
	searchPath = "../../test/slicedMidi/*.json"
	s = GSMarkovStyle(2,32,4)
	patterns = []
	for f in glob.glob(searchPath):
		with open(f) as j:
			d = json.load(j)
			p = GSPattern();
			p.fromJSONDict(d);
			loopLength = 4;
			for i in range(int(p.duration/loopLength)):
				p = p.getPatternForTimeSlice(i*loopLength,loopLength); # the current dataset can be splitted in loops of 4
				
				patterns+=[p]

	s.generateStyle(patterns)
	print s.transitionTable
	p = s.generatePattern()

	p.printEvents()