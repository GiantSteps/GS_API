from GSPattern import GSPattern

class GSStyle(object):
	""" base class for defining a style

	such class needs to provide following functions :
		generateStyle(self, PatternClasses) : compute inner state of style based on list of patterns
		generatePattern(self,seed=None): generate a new random pattern using seed if not None (idealy same seeds should lead to same patterns...)
		getDistanceFromStyle(self,Pattern) : return a normalized value representing the "styliness" of a pattern 1 being farthest from style
		getClosestPattern(self,Pattern,seed=0None) : return the closest pattern in this style
		getInterpolated(self,PatternA,PatternB,distanceFromA,seed=None) : interpolate between two pattern given this style constraints
		getInternalState(self): should return a dict representing current internal state
		loadInternalState(self,internalStateDict): load internal state from a given dict
		isBuilt(self):returns true if style hasbeen correctly build


	"""
	def __init__():
		self.type = "None"

	def generateStyle(self, PatternClasses):
		"""compute inner state of style based on list of patterns
		"""
		raise NotImplementedError( "Should have implemented this" )

	def generatePattern(self,seed=None):
		"""generate a new random pattern using seed if not None (idealy same seeds should lead to same patterns...)
		"""
		raise NotImplementedError( "Should have implemented this" )

	def getDistanceFromStyle(self,Pattern):
		"""return a normalized value representing the "styliness" of a pattern 1 being farthest from style
		"""
		raise NotImplementedError( "Should have implemented this" )

	def getClosestPattern(self,Pattern,seed=None):
		"""return the closest pattern in this style
		"""
		raise NotImplementedError( "Should have implemented this" )

	def getInterpolated(self,PatternA,PatternB,distanceFromA,seed=0):
		""" interpolate between two pattern given this style constraints
		"""
		raise NotImplementedError( "Should have implemented this" )

	def getInternalState(self):
		"""should return a dict representing current internal state
		"""
		raise NotImplementedError( "Should have implemented this" )

	def setInternalState(self,internalStateDict):
		"""load internal state from a given dict
		"""
		raise NotImplementedError( "Should have implemented this" )	

	def isBuilt(self):
		"""returns true if style hasbeen correctly build
		"""
		raise NotImplementedError( "Should have implemented this" )

	def saveToJSON(self, filePath):
		import json
		state = self.getInternalState();
		with open(filePath,'w') as f:
			json.dump(state,f)


	def loadFromJSON(self,filePath):
		import json
		with open(filePath,'r') as f:
			state = json.load(f)
		if state:
			self.setInternalState(state);


	def saveToPickle(self,filePath):
		import cPickle
		cPickle.dump(self,filePath)
	def loadFromPickle(self,filePath):
		import cPickle
		self = cPickle.load(filePath)