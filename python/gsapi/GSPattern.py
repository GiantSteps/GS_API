import GSPatternEvent
import os
import json

class GSPattern(object):

	def __init__(self,**kwargs):
		self.originBPM = -1
		self.originBPM = -1
		self.originBPM = -1
		self.originBPM = -1
		
		
		for k in kwargs:
			if k=='originBPM':
				self.originBPM = kwargs[k]
			



	def saveToJSON(self,path):

		if os.path.exists(path):
			print " no valid file for "+path
			return 
		json.




if __name__ == "__main__":
	p = GSPattern();
	print p.__dict__;