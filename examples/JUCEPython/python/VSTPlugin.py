
from gsapi import *


def test(s):
	return s+"kklolo"


def setup():
    pass

def onNewTime(time):
    pass

def onGenerateNew():
	pattern = GSPattern();
	pattern.addEvent(GSPatternEvent(0,1,60,100,["lala"]));
	pattern.addEvent(GSPatternEvent(2,2,60,100,["lala"]));

	transformPattern(pattern)
	return pattern

def transformPattern(patt):
	i = 0;
	
	l =list(patt.events)
	for e in l:
		print patt

	patt.events = l
		
	
	return patt

if __name__ =='__main__':
	patt = onGenerateNew();
	
	for i in patt.events:
		print i
		print i.length