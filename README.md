GS_API
===

The GS_API is a Python /C++ library for manipulating musical symbolic data.


Overview
==
The GS_API provides Python/C++ classes and interface for dealing with musical data. The main features are:

* Rhythm generation, both agnostic and based on styles.
* Style and music-theoretical based harmony progression generation.
* More to come.


Using the Library
==
Python
-
The python code resides in the **python** folder:
Build: run python setup.py build
Install: run python setup.py install

use example:
>>> from gsapi import *
>>> p = GSPattern()
>>> p.addEvent(GSPatternEvent(0,1,64,127,["Kick"]))

All modules are documented so typing help(GSPattern) provides relevant information.



JSON vs MIDI
==
GS_API use JSON format to deal with musical event allowing a more descriptive way to represent patterns than MIDI. mainly by affecting classes or tags to any note event as General MIDI mapping is not so wellspread out there...

Of course there is simple ways to transform midi collections in our JSON format (see scripts folder)



