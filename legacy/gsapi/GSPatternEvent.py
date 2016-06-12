class GSPatternEvent(object):



	def __init__(self):
		self.tags={}
		self.start = -1
		self.length = -1
		self.pitch = -1
		self.velocity = -1

	def isTimeValid(self):
		return 	(self.start != -1) and (self.length != -1) 
