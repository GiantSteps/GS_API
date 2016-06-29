GS_API
===

GS_API is a Python /C++ library for manipulating musical symbolic data


Overview
==
GS_API provide Python/C++ classes and interface for dealing with musical data, main features are :

* rythm generation ; agnostic and style based
* style based harmony progression generation
* more to come


Using the library
==
Python
-
python code resides in pythonWrap folder:
Building : run python setup.py build
Installing : run python setup.py install

using it :
sample code : 
>>> from gsapi import *
>>> p = GSPattern()
>>> p.addEvent(GSPatternEvent(0,1,64,127,["Kick"]))

all modules are documented so typing help(GSPattern) provides relevent informations



JSON vs MIDI
==
GS_API use JSON format to deal with musical event allowing a more descriptive way to represent patterns than MIDI. mainly by affecting classes or tags to any note event as General MIDI mapping is not so wellspread out there...

Of course there is simple ways to transform midi collections in our JSON format (see scripts folder)



