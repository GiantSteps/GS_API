from GSBasePatternTransformer import *


################
## WIP

class AgnosticDensity(GSBasePatternTransformer):

	""" Agnostic transformation algorithm
	Args:
		numSteps : number of steps to consider
		mode:['random','syncopation'] :  algorithm used 

	Attributes:
		globalDensity: float (0..2) the desired global density ,i.e 0 is an empty pattern, 1 matches the origin pattern, 2 is a pattern with all events
		individualDensities: dict[tag]=density :  a per Tag density, densities should be in the same range as globalDensity
		mode:['random','syncopation'] :  algorithm used 
		originPattern: the origin pattern, e.g : the one given if all densities are equals to 1
	"""
	def __init__(self, mode='random', numSteps = 32):
		self.globalDensity=1
		self.individualdensities = {}
		self.mode='random'
		self.originPattern = None
		self.numSteps = numSteps

	def configure(self, paramDict):
		if 'originPattern' in paramDict:
			buildDensityMap(paramDict['originPattern'])

	def TransformPattern(self,pattern,paramDict):
		if pattern!=None and pattern!=self.originPattern:
			buildDensityMap(pattern);
		if self.originPattern==None:
			print ("no pattern given for agnosticDensity transformation")
			return 

	def buildDensityMap(pattern):
		self.originPattern = pattern.copy();
		self.originPattern.alignOnGrid(1)
		


