import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import *


class GSDescriptorNumberOfTags(GSBase.GSDescriptor):

	def __init__(self,ignoredTags = ["silence"],includedTags=[]):
		GSDescriptor.__init__(self)
		self.ignoredTags = ignoredTags
		self.includedTags = includedTags

	def getDescriptorForPattern(self,pattern):
		density = 0;
		_checkedPattern = pattern.getPatternWithoutTags(self.ignoredTags)
		if(self.includedTags) : _checkedPattern = _checkedPattern.getPatternWithTags(self.includedTags,copy=False)
		
		return len(_checkedPattern.getAllTags())

