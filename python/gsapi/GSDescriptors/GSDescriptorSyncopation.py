from GSBaseDescriptor import *

import math

class GSDescriptorSyncopation(GSBaseDescriptor):
	""" computes the syncopation value from a pattern : 
	"""
	
	def __init__(self):
		GSBaseDescriptor.__init__(self)
		self.weights = []
		self.duration  = 16
		self.noteGrid = []

	def getDescriptorForPattern(self,pattern):
		if(pattern.duration!=self.duration):
			print "Syncopation inputing a pattern of duration %f but expected is %f"%(pattern.duration,self.duration)
			pattern = pattern.getPatternForTimeSlice(0,self.duration)
		if not self.weights :
			self.buildSyncopationWeight(pattern.duration)
		syncopation =0

		self.buildBinarizedGrid(pattern)
		for t in range(self.duration):
			nextT = (t+1)%self.duration
			if  self.noteGrid[t] and not self.noteGrid[nextT] :
				syncopation+=abs(self.weights[nextT] - self.weights[t])

		return syncopation

		

	def buildSyncopationWeight(self,duration):
		depth = 1
		# numSteps = int(math.log(duration)/math.log(2)
		self.weights = [0] * int(duration)
		thresh  =0
		
		stepWidth = int((duration)*1.0/depth)
		while(stepWidth>thresh):
			for s in range(depth):
				self.weights[s*stepWidth]+=1
			depth=depth*2
			stepWidth = int(duration*1.0/depth)

	def buildBinarizedGrid(self,pattern):
		self.noteGrid = [0] * self.duration
		for i in range(self.duration):
			self.noteGrid[i] = len(pattern.getActiveEventsAtTime(i))



