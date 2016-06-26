from GSStyle import GSStyle
import random
import copy

class GSMarkovStyle(GSStyle):

	def __init__(self,order,numSteps):
		super(GSStyle,self).__init__()
		self.type = "None"
		self.order = order;
		self.numSteps = numSteps;


	def generateStyle(self, PatternClasses):
		if not isinstance(PatternClasses,list):
			print "style need a list"
			return False
		else:
			self.originPatterns = PatternClasses;

			self.buildStyle();


	def buildStyle(self):
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

	def generatePattern(self,seed = None):
		random.seed(seed)
		potentialStartEvent = []

		def getAvailableAtStep(step):
			res = []
			for n in self.transitionTable[step]:
				for t in self.transitionTable[step][n]:
					res+=[t]
			return res

		def isValidState(step,previousTags):
			d = self.transitionTable[step]
			return previousTags in d

		
		
		cIdx = self.order
		startHypothesis =[]
		for n in range (self.order):
			startHypothesis+=[random.choice(getAvailableAtStep(n))]
		while not isValidState(cIdx,','.join(startHypothesis)):
			startHypothesis =[]
			for n in range (self.order):
				startHypothesis+=[random.choice(getAvailableAtStep(n))]
			
		eventTags = startHypothesis
		print startHypothesis

		


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
	searchPath = "../test/slicedMidi/*.json"
	s = GSMarkovStyle(2,32)
	patterns = []
	for f in glob.glob(searchPath):
		with open(f) as j:
			d = json.load(j)
			p = GSPattern.GSPattern();
			p.fromJSONDict(d);
			p = p.getPatternForTimeSlice(0,4);
			print p.duration
			patterns+=[p]

	s.generateStyle(patterns)
	s.generatePattern()