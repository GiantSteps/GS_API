from GSPattern import GSPattern

class GSStyle(object):
	""" base class for defining a style

	such class needs to provide following functions :
		generateStyle(self, PatternClasses) : compute inner state of style based on list of patterns
		getDistanceFromStyle(self,Pattern) : return a normalized value representing the "styliness" of a pattern 1 being farthest from style
		getClosestPattern(self,Pattern,seed=0) : return the closest pattern in this style
		getInterpolated(self,PatternA,PatternB,distanceFromA,seed=0) : interpolate between two pattern given this style constraints
		getInternalState(self): should return a dict representing current internal state
		loadInternalState(self,internalStateDict): load internal state from a given dict


	"""
	def __init__():
		self.type = "None"

	def generateStyle(self, PatternClasses):
		raise NotImplementedError( "Should have implemented this" )

	def getDistanceFromStyle(self,Pattern):
		raise NotImplementedError( "Should have implemented this" )

	def getClosestPattern(self,Pattern,seed=0):
		raise NotImplementedError( "Should have implemented this" )

	def getInterpolated(self,PatternA,PatternB,distanceFromA,seed=0):
		raise NotImplementedError( "Should have implemented this" )

	def getInternalState(self):
		raise NotImplementedError( "Should have implemented this" )

	def loadInternalState(self,internalStateDict):
		raise NotImplementedError( "Should have implemented this" )	

	def saveToJSON(self, filePath):
		import json
		state = self.getInternalState();
		with open(filePath,'w') as f:
			json.dump(f,state)


	def loadFromJSON(self,filePath):
		import json
		
		with open(filePath,'r') as f:
			state = json.loads(f)
		if state:
			self.setInternalState(state);


	def saveToPickle(self,filePath):
		import cPickle
		cPickle.dump(self,filePath)
	def loadFromPickle(self,filePath):
		import cPickle
		self = cPickle.load(filePath)