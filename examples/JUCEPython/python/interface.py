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
	test = NumParameter("slider",value = 10,style = "Rotary").setBounds(0,0,20,100).setMinMax(0,10)
	test.onChange = updateTest
	test.value = 11
	res+=[test]
	test2 = BoolParameter("tog").setBounds(20,0,20,100)
	test2.onChange = updateTog
	res+=[test2]
	test3 = EventParameter("ev").setBounds(40,0,20,100)
	test3.onChange = updateTog
	res+=[test3]
	dummy = Dummy(8)
	test4 = EnumParameter(name="list",choicesList={"lala":dummy.fun,"lolo":{"fesse":["loulou"]}}).setBounds(60,0,20,100)
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
	dummy = Dummy(8)
	f = EnumParameter("tst",choicesList={"lala":dummy.fun,"lolo":"lulu"})
	f.onChange = updateList
	print getAllParameters()
	f.value = ["lala"]
	

