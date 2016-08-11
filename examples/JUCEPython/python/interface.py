import VSTPlugin
import JUCEAPI
from UIParameter import *



class Dummy(object):
	def __init__(self,value):
		self.value = value
	def fun(self):
		print self.value




def getAllParameters():
	""" gets caled when parameters are built in VST host
	should return a list of UIParams
	"""
	res = []
	# add existing 
	area = Rectangle(0,0,100,100)
	firstStack = area.removeFromLeft(30)
	res+=[VSTPlugin.loopDuration.setBoundsRect(firstStack.removeFromTop(50)).setMinMax(32,64)]
	res+=[VSTPlugin.numSteps.setBoundsRect(firstStack).setMinMax(1,8)]
	res+=[VSTPlugin.eachBarIsNew.setBoundsRect(area.removeFromLeft(20))]
	res+=[VSTPlugin.generateNew.setBoundsRect(area.removeFromLeft(20))]

# add others ..
	dummy = Dummy(8)
	test4 = EnumParameter(choicesList={"lala":dummy.fun,"lolo":{"fesse":["loulou"]}},name="list").setBoundsRect(area)
	test4.onChange = updateList
	res+=[test4]

	return res


def updateTest(param):
	print "pyrcv"


def updateTog(param):
	if param.value != None:
		print "upTog2 " + str(param.value)
	else:
		print "eventTrig"
	JUCEAPI.vst.setPattern(VSTPlugin.mapMidi(VSTPlugin.style.generatePattern()))

def updateList(param):
	if(callable(param.value)):
		print "calling",param.value
		param.value()
		

	


if __name__ == '__main__':
	import sys
	print sys.executable
	dummy = Dummy(8)
	f = EnumParameter({"lala":dummy.fun,"lolo":"lulu"})
	VSTPlugin.numSteps.value = 32
	f.onChange = updateList
	print getAllParameters()
	f.value = ["lala"]
	

