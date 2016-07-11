Example using JUCE library
=====
this VST Plugin is for testing purpose only .

this VST loads a python file (python/VSTPlugin.py) and implement a basic API for :
* display and play a GSPattern
* calling python functions from VST UI


###Interface
a basic interface allow to show python file being processed, reloading it and autowatch the file(reload each time the file is modified)
the file is in the VST bundle, under Resources/python

you need to install python gsapi first see GS_API readme


### Dependencies

Cython, numpy,python-midi



Known Bugs
-
work in pretty much all DAWs (Bitwig,JUCEAudiopluginHostDemo ...) but does not work in ableton Live !