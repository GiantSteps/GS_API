from GSPattern import GSPattern

class GSPatternTransformer(object):
	""" base class for defining a transform algorithm

	such class needs to provide following functions :
		configure(self, dict) : configure current transformer based on implenmentation specific parameters passed in dict argument
		TransformPattern(self,GSPattern) : return a transformed version of GSPattern

	"""
	def __init__():
		self.type = "None"

	def configure(self, paramDict):
		"""configure current transformer based on implenmentation specific parameters passed in dict argument
		"""
		raise NotImplementedError( "Should have implemented this" )

	def TransformPattern(self,pattern):
		"""return a transformed version of GSPattern
		"""
		raise NotImplementedError( "Should have implemented this" )
