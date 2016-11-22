import logging
from gsapi import GSPattern


class GSBaseDescriptor(object):

	def __init__(self):
		pass

	def getDescriptorForPattern(self,pattern):
		"""Compute a unique value for a given pattern (can be a sliced part of a bigger one)
		"""
		raise NotImplementedError( "Should have implemented this" )

	def configure(self,paramDict):
		"""configure current descriptor mapping dict to parameters 
		"""
		raise NotImplementedError( "Should have implemented this" )


