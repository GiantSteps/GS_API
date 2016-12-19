from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from .GSBaseDescriptor import *
import math

class GSDescriptorSyncopation(GSBaseDescriptor):
	""" computes the syncopation value from a pattern : 
	"""
	
	def __init__(self):
		GSBaseDescriptor.__init__(self)
		self.weights = []
		self.noteGrid = []
		self.duration = 1

	def getDescriptorForPattern(self,pattern):
		self.duration = int(math.ceil(pattern.duration))
		if not self.weights or ( self.duration!= len(self.weights) ) :
			self.buildSyncopationWeight()
		syncopation =0

		self.buildBinarizedGrid(pattern)
		for t in range(self.duration):
			nextT = (t+1)%self.duration
			if  self.noteGrid[t] and not self.noteGrid[nextT] :
				syncopation+=abs(self.weights[nextT] - self.weights[t])

		return syncopation

		

	def buildSyncopationWeight(self):
		depth = 1
		self.weights = [0] * int(self.duration)
		thresh  =0
		
		stepWidth = int((self.duration)*1.0/depth)
		while(stepWidth>thresh):
			for s in range(depth):
				self.weights[s*stepWidth]+=1
			depth=depth*2
			stepWidth = int(self.duration*1.0/depth)

	def buildBinarizedGrid(self,pattern):
		
		self.noteGrid = [0] * self.duration
		for i in range(self.duration):
			self.noteGrid[i] = len(pattern.getActiveEventsAtTime(i))


