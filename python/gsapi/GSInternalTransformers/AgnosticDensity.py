from gsapi import GSPattern,GSPatternEvent
from gsapi.GSPatternTransformer import GSPatternTransformer
class AgnosticDensity(GSPatternTransformer):

	""" Agnostic transformation algorithm
	Args:
		globalDensity: float (0..2) the desired global density ,i.e 0 is an empty pattern, 1 matches the origin pattern, 2 is a pattern with all events
		individualDensities: dict[tag]=density :  a per Tag density, densities should be in the same range as globalDensity
		mode:['random','syncopation'] :  algorithm used 
	"""
	def __init__(self,mode='random'):
		self.globalDensity=1
		self.individualdensities = {}
		self.mode='random'
		self.originPattern = None

	def configure(self, paramDict):
		if 'originPattern' in paramDict:
			buildDensityMap(paramDict['originPattern'])

	def TransformPattern(self,pattern,paramDict):
		if pattern!=None and pattern!=self.originPattern:
			buildDensityMap(pattern);
		if self.originPattern==None:
			print ("no pattern given for agnosticDensity transformation")

		raise NotImplementedError( "Should have implemented this" )

	def buildDensityMap(pattern):
		self.originPattern = pattern;
		# if mode == 'random':
			

