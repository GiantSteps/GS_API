from GSPattern import GSPattern

class GSStyle(object):
	""" base class for defining a style

	such class needs to provide following functions :
		generateStyle(self, PatternClasses) : compute inner state of style based on list of patterns
		getDistanceFromStyle(self,Pattern) : return a normalized value representing the "styliness" of a pattern 1 being farthest from style
		getClosestPattern(self,Pattern,seed=0) : return the closest pattern in this style
		getInterpolated(self,PatternA,PatternB,distanceFromA,seed=0) : interpolate between two pattern given this style constraints

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