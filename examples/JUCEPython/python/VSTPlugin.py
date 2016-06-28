
from gsapi import *
import random



def setup():
    pass

def onNewTime(time):
    pass

def onGenerateNew():
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


def test(s):
	return s+"kklolo"


if __name__ =='__main__':
	patt = onGenerateNew();
	print patt.__dict__
	for i in patt.events:
		print i.duration