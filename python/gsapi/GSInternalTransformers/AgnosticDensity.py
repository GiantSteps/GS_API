from gsapi import GSPatternTransformer,GSPattern,GSPatternEvent

class AgnosticDensity(GSPatternTransformer):
	def __init__():
		self.globalDensity=1
		self.individualdensities = {}

	def configure(self, paramDict):
		raise NotImplementedError( "Should have implemented this" )

	def TransformPattern(self,pattern):
		raise NotImplementedError( "Should have implemented this" )