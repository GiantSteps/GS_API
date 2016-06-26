from GSPattern import GSPattern

class GSStyle(object):
	
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