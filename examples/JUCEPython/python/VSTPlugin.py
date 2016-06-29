
from gsapi import *
import random

""" this example generates random notes to demonstrate passing GSPattern to C++ plugin
"""

def setup():
    pass

def onNewTime(time):
	""" called when user press generate new
	Returns:
 		the new GSpattern to be played
	"""
	pass



def onGenerateNew():
	""" called when user press generate new
	Returns:
	 the new GSpattern to be played
	"""
	pattern = GSPattern();
	
	for i in range(32):
		pattern.addEvent(GSPatternEvent(i/4.0,.25,random.randint(60,60+i),127,["lala"]));
	
	transformPattern(pattern)
	return pattern


def transformPattern(patt):
	i = 0;
	j=1
	for e in patt.events:
		e.startTime+=(random.random()*2.0 - 1)*.4
		e.duration=max(0.1,e.duration+(random.random()*2.0-1)*.4)

		
	
	return patt




if __name__ =='__main__':
	patt = onGenerateNew();
	print patt.__dict__
	for i in patt.events:
		print i.duration