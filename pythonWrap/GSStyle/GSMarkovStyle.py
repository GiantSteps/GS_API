from GSStyle import GSStyle
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
		transitionTable = [{} for f in range(self.numSteps)]

		self.binarizedPatterns = copy.deepcopy(self.originPatterns)
		for p in self.binarizedPatterns:
			self.formatPattern(p)
			for e in p.events :
				lastEvents = self.getLastEvents(p,e,self.order,1)
				print e.tags , [ x.tags  for t in lastEvents for x in t]

	def formatPattern(self,p):
		p.quantize(8,8);
		p.discretize(1)
		p.fillWithSilences();
		p.discretize(1)
		

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