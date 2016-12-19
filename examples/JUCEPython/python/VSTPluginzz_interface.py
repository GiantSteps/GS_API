import VSTPluginzz as VSTPlugin
import JUCEAPI
from UIParameter import *



class Dummy(object):
	def __init__(self,value):
		self.value = value
	def fun(self):
		print self.value


dummy = Dummy(8)
test4 = EnumParameter(choicesList={"lala":dummy.fun,"lolo":{"fesse":["loulou"]}},name="list")


def updateSlaveSlider(self,sliderToUpdate):
	sliderToUpdate.value = self.value *8.2

slaveSlider = NumParameter(0.0).setMinMax(0,100)
masterSlider = NumParameter(0.0).setMinMax(0,10)
masterSlider.setCallbackFunction(updateSlaveSlider,masterSlider,slaveSlider)



def createLayout():
	area = Rectangle(0,0,100,100)
	header = area.removeFromTop(40);
	VSTPlugin.patternParameter.setBoundsRect(header);
	firstStack = area.removeFromLeft(30)
	VSTPlugin.loopDuration.setBoundsRect(firstStack.removeFromTop(30))
	VSTPlugin.numSteps.setBoundsRect(firstStack)

	secondStack = area.removeFromLeft(10)
	masterSlider.setBoundsRect(secondStack.removeFromTop(50))
	slaveSlider.setBoundsRect(secondStack)

	# VSTPlugin.eachBarIsNew.setBoundsRect(area.removeFromLeft(20))
	# VSTPlugin.generateNewP.setBoundsRect(area.removeFromLeft(20))


	test4.setBoundsRect(area)

def configureParams():
	VSTPlugin.loopDuration.setMinMax(1,16).setCallbackFunction(VSTPlugin.generateStyleIfNeeded,forceParamUpdate=True)
	VSTPlugin.numSteps.setMinMax(4,32).setCallbackFunction(VSTPlugin.generateStyleIfNeeded,forceParamUpdate=True)
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
	# res+=[VSTPlugin.eachBarIsNew]
	# res+=[VSTPlugin.generateNewP]

	res+=[masterSlider]
	res+=[slaveSlider]
	res+=[VSTPlugin.patternParameter]

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
	VSTPlugin.setup()
	print getAllParameters()

	VSTPlugin.generateNewP.addListener('tst',dummy.fun)
	VSTPlugin.numSteps.value = 32
	VSTPlugin.generateNewP.setValueFrom('tst', 1)

	
	

