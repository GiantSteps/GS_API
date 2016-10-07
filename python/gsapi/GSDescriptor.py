import logging


from gsapi import GSPattern

class GSDescriptor(object):

	def __init__(self):
		pass

	def getDescriptorForPattern(self,pattern):
		""" compute a unique value for a given pattern (can be a sliced part of a bigger one)
		"""
		raise NotImplementedError( "Should have implemented this" )

