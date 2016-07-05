
from gsapi import *
from gsapi.GSInternalStyles import *
import json
import glob
import random
import os


""" this example generates random notes to demonstrate passing GSPattern to C++ plugin
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

def setup():
	print "settingUp"
	

def onTimeChanged(time):
	""" called when user press generate new
	Returns:
 		the new GSpattern to be played if needed
	"""
	print time
	return None



def onGenerateNew():
	""" called when user press generate new
	Returns:
	 the new GSpattern to be played
	"""
	searchPath = os.path.abspath(os.path.join(__file__,os.path.pardir))
	searchPath = os.path.join(searchPath,"funkyfresh_style/*.json");
	print "startGenerating for "+searchPath+" : "+str(glob.glob(searchPath))
	s = GSMarkovStyle(2,32,4)
	patterns = []
	for f in glob.glob(searchPath):
		with open(f) as j:
			d = json.load(j)
			p = GSPattern();
			p.fromJSONDict(d);
			loopLength = 4;
			for i in range(int(p.duration/loopLength)):
				p = p.getPatternForTimeSlice(i*loopLength,loopLength); # the current dataset can be splitted in loops of 4
				
				patterns+=[p]

	s.generateStyle(patterns)
	print "start generating pattern"
	pattern = s.generatePattern();
	print "mapMidi"
	mapMidi(pattern)


	print "ended"
	return pattern

def mapMidi(pattern):
	for e in pattern.events:
		if len(e.tags) > 0 and (e.tags[0] in midiMap):
			e.pitch = midiMap[e.tags[0]]



def transformPattern(patt):
	i = 0;
	j=1
	for e in patt.events:
		e.startTime+=(random.random()*2.0 - 1)*.4
		e.duration=max(0.1,e.duration+(random.random()*2.0-1)*.4)
	return patt


print __dict__

if __name__ =='__main__':
	patt = onGenerateNew();
	# patt.printEvents()