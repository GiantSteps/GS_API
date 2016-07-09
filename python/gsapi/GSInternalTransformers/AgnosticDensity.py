from gsapi import GSPattern,GSPatternEvent
from gsapi.GSPatternTransformer import GSPatternTransformer
class AgnosticDensity(GSPatternTransformer):

	""" Agnostic transformation algorithm
	"""
	def __init__(self):
		self.globalDensity=1
		self.individualdensities = {}

	def configure(self, paramDict):
		pass

	def TransformPattern(self,pattern,paramDict):
		raise NotImplementedError( "Should have implemented this" )