# inject develop version of gsapi if debugging
# if __name__=='__main__':
# 	import sys,os
# 	pathToAdd = os.path.abspath(os.path.join(__file__,os.path.pardir,os.path.pardir,os.path.pardir,os.path.pardir,"python"))
# 	sys.path.insert(1,pathToAdd)
	

from gsapi import *
from gsapi.GSInternalStyles import *
import json
import glob
import random
import os



import JUCEAPI

from UIParameter import *



""" this example generates stylistic markovian pattern to demonstrate passing GSPattern to C++ plugin
"""
midiMap = {
		"Kick":36,
		"Rimshot":37,
		"Snare":38,
		"Clap":39,
		"Clave":40,
		"LowTom":41,
		"ClosedHH":42,
		"MidTom":43,
		"Shake":44,
		"HiTom":45,
		"OpenHH":46,
		"LowConga":47,
		"HiConga":48,
		"Cymbal":49,
		"Conga":50,
		"CowBell":51
}

localDirectory = os.path.abspath(os.path.join(__file__,os.path.pardir))

searchPath = os.path.join(localDirectory,"midi","garagehouse1_snare.mid");
# searchPath = os.path.join(localDirectory,"midi","daftpunk2.mid");
searchPath = os.path.join(localDirectory,"midi","motown.mid");
# searchPath = os.path.join(localDirectory,"midi","nj-house.mid");
# searchPath = os.path.join(localDirectory,"midi","*.mid");

# searchPath =os.path.join(localDirectory,"/Users/Tintamar/Downloads/renamed/*.mid");

styleSavingPath = os.path.join(localDirectory,"DBStyle.json");
numSteps = NumParameter(32).setCallbackFunction(lambda :generateStyleIfNeeded(True))
loopDuration = NumParameter(4).setCallbackFunction(lambda :generateStyleIfNeeded(True))
def generatePattern():
	generateStyleIfNeeded();
	JUCEAPI.vst.setPattern(mapMidi(style.generatePattern()))
generateNew = EventParameter().setCallbackFunction(generatePattern)
style = GSMarkovStyle(order=numSteps.value/(loopDuration.value+1),numSteps=numSteps.value,loopDuration=loopDuration.value)
# style = GSDBStyle(generatePatternOrdering = "increasing");
needStyleUpdate = False;



#  parameters enable simple UI bindings
eachBarIsNew = BoolParameter()


def setup():
	print "settingThingsUp"
	

def onTimeChanged(time):
	""" called at eacch beat when pattern is playing
	Args:
		a dictionary {'time':timeinBeat}
	Returns:
 		the new GSpattern to be played if needed
	"""

	if eachBarIsNew.value :
		generatePattern()
	




def onGenerateNew():
	""" called when user press generate new
	Returns:
	 the new GSpattern to be played
	"""
	global style
	generateStyleIfNeeded();
	print "start generating pattern"
	pattern = style.generatePattern();
	print "mapMidi"
	mapMidi(pattern)


	print "ended"
	return pattern

def mapMidi(pattern):
	for e in pattern.events:
		if len(e.tags) > 0 and (e.tags[0] in midiMap):
			e.pitch = midiMap[e.tags[0]]
	return pattern


def generateStyleIfNeeded(force = False):
	
	global needStyleUpdate
	global midiMap
	global style
	global styleSavingPath

	if force or not style.isBuilt():
		hasStyleSaved = os.path.isfile(styleSavingPath)
		if(force or (not hasStyleSaved)  or needStyleUpdate ):
			print "startGenerating for "+searchPath+" : "+str(glob.glob(searchPath))
			patterns = gsapi.GSIO.fromMidiCollection(searchPath,NoteToTagsMap=midiMap,TagsFromTrackNameEvents=False,desiredLength = loopDuration.value)
			style.generateStyle(patterns)
			style.saveToJSON(styleSavingPath)
			needStyleUpdate =False
		else:
			style.loadFromJSON(styleSavingPath)
	


def transformPattern(patt):
	i = 0;
	j=1
	for e in patt.events:
		e.startTime+=(random.random()*2.0 - 1)*.4
		e.duration=max(0.1,e.duration+(random.random()*2.0-1)*.4)
	return patt


if __name__ =='__main__':
	import interface
	print "runMain"
	onGenerateNew()
	needStyleUpdate=False
	numSteps.value = 32
	params =  interface.getAllParameters()
	
	
	
	# patt.printEvents()