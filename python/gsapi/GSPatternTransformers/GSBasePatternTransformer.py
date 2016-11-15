from gsapi.GSPattern import GSPattern

class GSBasePatternTransformer(object):
	""" Base class for defining a transform algorithm

	such class needs to provide following functions :
		- configure(self, dict) : configure current transformer based on implementation specific parameters passed in dict argument
		- TransformPattern(self,GSPattern) : return a transformed version of GSPattern

	"""
	def __init__(self):
		self.type = "None"

	def configure(self, paramDict):
		"""configure current transformer based on implenmentation specific parameters passed in dict argument

		Args:
			paramDict : a dictionnary filed with configuration values
		"""
		raise NotImplementedError( "Should have implemented this" )

	def TransformPattern(self,pattern):
		"""returns a transformed version of GSPattern

		Args:
			pattern : the pattern to be transformed
		"""
		raise NotImplementedError( "Should have implemented this" )
