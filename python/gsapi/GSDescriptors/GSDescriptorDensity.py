import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import GSDescriptor


class GSDescriptorDensity(GSDescriptor):

	def __init__(self):
		GSDescriptor.__init__(self)

	def getDescriptorForPattern(self,pattern):
		density = 0;
		for e in pattern.events:
			if not "silence" in e.tags:
				density+=e.duration
		return density

	