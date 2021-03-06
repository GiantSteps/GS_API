# inject develop version of gsapi if debugging
if __name__=='__main__':
	import sys,os
	pathToAdd = os.path.abspath(os.path.join(__file__,os.path.pardir,os.path.pardir,os.path.pardir,os.path.pardir,"python"))
	sys.path.insert(1,pathToAdd)
	

from gsapi import *




import json
import glob
import random
import os



import JUCEAPI

from UIParameter import *



""" this example generates stylistic markovian pattern to demonstrate passing GSPattern to C++ plugin
"""
#generalMidiMap

localDirectory = os.path.abspath(os.path.join(__file__,os.path.pardir))

# searchPath = os.path.join(localDirectory,"midi","garagehouse1_snare.mid");
# # searchPath = os.path.join(localDirectory,"midi","daftpunk2.mid");
# searchPath = os.path.join(localDirectory,"midi","motown.mid");
# searchPath = "/Users/Tintamar/Dev/GS_API/corpus/midiTests/miniDaftPunk.mid";
searchPath = os.path.join(localDirectory,"midi")
styleName = 'daftpunk2.mid'
# searchPath = os.path.join(localDirectory,"midi/corpus-harmony","*.mid");
#searchPath = os.path.join(localDirectory,"*.mid");
# midiMap = "pitchNames"
dataSet = GSDataset(midiFolder = searchPath, midiGlob=styleName,midiMap=GSPatternUtils.simpleDrumMap)
# searchPath = os.path.join(localDirectory,"midi","*.mid");

# searchPath =os.path.join(localDirectory,"/Users/Tintamar/Downloads/renamed/*.mid");

styleSavingPath = os.path.join(localDirectory,"DBStyle.json");
numSteps = NumParameter(32)
loopDuration = NumParameter(8)
generateNewP = EventParameter()




style = GSStyles.GSMarkovStyle(order=numSteps.value/(loopDuration.value+1),numSteps=int(numSteps.value),loopDuration=int(loopDuration.value))
patterns = None
# style = GSDBStyle(generatePatternOrdering = "increasing");

#  parameters enable simple UI bindings
eachBarIsNew = BoolParameter()

# this is the main pattern (that will be played)
# changing its value will automagically change the current pattern played in VST (c.f generatePattern())
patternParameter = PatternParameter()

def setup():
	generateStyleIfNeeded(forceRebuild = True,forceParamUpdate = False,loadFromJSON = False)
	generatePattern()
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
	


def tagToPitch(tag):
	split = tag.split('_')

	note = GPatternUtils.defaultPitchNames.index(split[0])
	octave = int(split[1])
	return note+octave*12


def mapMidi(pattern,midiMap):
	if midiMap=="pitchNames" : 
		for e in pattern.events:
			e.pitch = tagToPitch(e.tag)
	else:
		for e in pattern.events:
			if e.tag in midiMap:
				e.pitch = midiMap[e.tag]
			elif len(e.tag) > 0 and (e.tag[0] in midiMap):
				e.pitch = midiMap[e.tag[0]]
			else:
				print "no custom map possible"
	return pattern


def generateStyleIfNeeded(forceRebuild = False,forceParamUpdate = False,loadFromJSON = False):
	

	global style
	global styleSavingPath
	global patterns

	hasStyleSaved = os.path.isfile(styleSavingPath)

	if loadFromJSON:
		if hasStyleSaved :
			style.loadFromJSON(styleSavingPath)
			numSteps.value = style.numSteps
			loopDuration.value = style.loopDuration
		else:
			forceParamUpdate=True 
			forceRebuild=True
			
	if forceRebuild:
		print "startGenerating for "+searchPath+" : "+str(glob.glob(searchPath))
		# patterns = dataSet.patterns#gsapi.GSIO.fromMidiCollection(searchPath,NoteToTagsMap=midiMap,TagsFromTrackNameEvents=False,desiredLength = int(loopDuration.value))
		

	if forceRebuild or forceParamUpdate :
		style = GSStyles.GSMarkovStyle(order=numSteps.value/(loopDuration.value+1),numSteps=int(numSteps.value),loopDuration=int(loopDuration.value))
		patterns = []
		for p in dataSet.patterns:
			patterns += p.splitInEqualLengthPatterns(loopDuration.value);
		if patterns:
			style.generateStyle(patterns)
		else:
			print ("errror, no pattern found")


		
		

def saveStyle():
	style.saveToJSON(styleSavingPath)


def transformPattern(patt):
	i = 0;
	j=1
	for e in patt.events:
		e.startTime+=(random.random()*2.0 - 1)*.4
		e.duration=max(0.1,e.duration+(random.random()*2.0-1)*.4)
	return patt


def generatePattern():

	generateStyleIfNeeded();
	newPattern = style.generatePattern()
	newPattern = mapMidi(newPattern,GSPatternUtils.simpleDrumMap)
	print 'newPattern set'
	patternParameter.value = newPattern
	


if __name__ =='__main__':
	# import interface
	print "runMain"
	setup()
	numSteps.value = 32
	generatePattern()
	# params =  interface.getAllParameters()
	
	
	
	# patt.printEvents()
