GS_API
===

The GS_API is a Python/C++ library for manipulating musical symbolic data.


Overview
------
The GS_API provides Python/C++ classes and interface for dealing with musical data. The main features are:

* flexible input/output from/to JSON/MIDI
* Rhythm generation, both agnostic and based on styles.
* Style and music-theoretical based harmony progression generation.
* More to come.


Using the Library
-----

**Python**

The python code resides in the **python** folder:

* Build:
```
python setup.py build
```

* Install:
```
python setup.py install
```

*All modules are documented so typing help(GSPattern) provides relevant information.*



* naive example:

```python
from gsapi import *
p = GSPattern()
p.addEvent(GSPatternEvent(startTime=0,duration=1,pitch=64,velocity=127,tags=["Kick"]))
p.addEvent(GSPatternEvent(1,3,62,51,["Snare"]))
```
will fill *GSPattern* p with :
* one event tagged Kick starting at 0 with a duration of 1 a Midi Note Number of 64 and a velocity of 127
* one event tagged Snare starting at 1 with a duration of 3 a Midi Note Number of 62 and a velocity of 51

API Philosophies
------
**JSON and MIDI**

we encourage use of JSON to be able to work with consistent and reusable datasets, as midi files tends to have different MIDI mapping , structures, or even suspicious file format implementations.
Thus we provide flexible MIDI input module *GSIO* for tagging events with respect to their pitch/channel/trackName
Note to tag mapping is reppresented by a dictionnary where key represent a tag and value is a rule such tag has to validate
* rules are either list or single *condition* that are OR'ed
* each condition is either a tuple with expected pitch value and channel value or an integer representing expected pitch value

```python
from gsapi import *
midiGlobPath = '/path/to/midi/*.mid'
NoteToTagsMap = {"Kick":30,"Snare":(32,4),"ClosedHihat":[(33,'*'),45]}
listOfGSPatterns = GSIO.fromMidiCollection(midiGlobPath,NoteToTagsMap)
```


will return a list of *GSPattern* with event being tagged :
* 'Kick' if MIDI pitch is 30 and whatever channel
* 'Snare' if MIDI pitch is 32 and channel is 4
* 'ClosedHihat' if MIDI pitch is 33 on whatever channel or MIDI pitch is 45 on whatever channel





