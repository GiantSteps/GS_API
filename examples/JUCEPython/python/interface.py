import VSTPlugin
import JUCEAPI
from UIParameter import *



class Dummy(object):
	def __init__(self,value):
		self.value = value
	def fun(self):
		print self.value


dummy = Dummy(8)
test4 = EnumParameter(choicesList={"lala":dummy.fun,"lolo":{"fesse":["loulou"]}},name="list")



def createLayout():
	area = Rectangle(0,0,100,100)
	firstStack = area.removeFromLeft(30)
	VSTPlugin.loopDuration.setBoundsRect(firstStack.removeFromTop(50))
	VSTPlugin.numSteps.setBoundsRect(firstStack)

	VSTPlugin.eachBarIsNew.setBoundsRect(area.removeFromLeft(20))
	VSTPlugin.generateNewP.setBoundsRect(area.removeFromLeft(20))

	test4.setBoundsRect(area)

def configureParams():
	VSTPlugin.loopDuration.setMinMax(1,8).setCallbackFunction(VSTPlugin.generateStyleIfNeeded,forceParamUpdate=True)
	VSTPlugin.numSteps.setMinMax(32,64).setCallbackFunction(VSTPlugin.generateStyleIfNeeded,forceParamUpdate=True)
	VSTPlugin.generateNewP.setCallbackFunction(VSTPlugin.generatePattern)
	# add others ..
	test4.onChange = updateList

def getAllParameters():
	""" gets caled when parameters are built in VST host
	should return a list of UIParams
	"""
	
	
	configureParams()
	createLayout()
	# add existing 
	res = []
	res+=[VSTPlugin.loopDuration]
	res+=[VSTPlugin.numSteps]
	res+=[VSTPlugin.eachBarIsNew]
	res+=[VSTPlugin.generateNewP]
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
	print 'running main'
	import sys
	print sys.executable
	print getAllParameters()

	VSTPlugin.generateNewP.addListener('tst',dummy.fun)
	VSTPlugin.numSteps.value = 32
	VSTPlugin.generateNewP.setValueFrom('tst', 1)

	
	

