
from gsapi.gsapi import *


def test(s):
	return s+"kklolo"


def setup():
    pass

def onNewTime(time):
    pass

def onGenerateNew():
	pattern = GSPattern();
	
	for i in range(32):
		pattern.addEvent(GSPatternEvent(i/4.0,.25,60+i,100,["lala"]));
	
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
	print patt.__dict__
	
	for i in patt.events:
		print i
		print i.length