""" empty file emulating (and referencing) accessible function from within vst host
"""
class API(object):

	def setPattern(pattern):
		""" set the current pattern being played
		"""
		assert isinstance(pattern,GSPattern)


""" use instance of the class vst to access to function
"""
vst = API()