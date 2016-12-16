GS_API
===
[![Build Status](https://travis-ci.org/GiantSteps/GS_API.svg?branch=master)](https://travis-ci.org/GiantSteps/GS_API)
[![codecov.io](https://codecov.io/github/cainus/codecov.io/coverage.svg?branch=master)](https://codecov.io/github/cainus/codecov.io?branch=master)

The GS_API is a Python/C++ library for manipulating musical symbolic data.


Overview
------
The GS_API provides Python/C++ classes and interface for dealing with musical data. The main features are:

* flexible input/output from/to JSON/MIDI
* Rhythm generation, both agnostic and based on styles.
* Style and music-theoretical based harmony progression generation.
* More to come.


Installing the Library
-----
Installing last stable release can be done via pip
```
pip install gsapi
```

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


* naive use cases example:

```python
from gsapi import *
p = GSPattern()
p.addEvent(GSPatternEvent(startTime=0,duration=1,pitch=64,velocity=127,tags=["Kick"]))
p.addEvent(GSPatternEvent(1,3,62,51,["Snare"]))
```
will fill *GSPattern* p with :
* one event tagged Kick starting at 0 with a duration of 1 a Midi Note Number of 64 and a velocity of 127
* one event tagged Snare starting at 1 with a duration of 3 a Midi Note Number of 62 and a velocity of 51


* get All loops from a dataset
```python
from gsapi import *
dataset = GSDataSet(midiFolder="The/Midi/Folder/To/Crawl",midiGlob="*.mid", midiMap=GSIO.generalMidiMap)
allPatternsSliced = []
for midiPattern in dataset.patterns:
	for sliced in midiPattern.splitInEqualLengthPatterns(16): # split in 16 beat slices
		allPatternsSliced+=[sliced]
print allPatternSliced
```

* descriptors analysis example 
```python
densityDescriptor = GSDescriptorDensity();
for pattern in dataset.patterns:
	kickPattern = pattern.getPatternWithTags(tags="kick")
	densityOfKick = densityDescriptor.getDescriptorForPattern(kickPattern)
```

* style analysis example
```python

markovStyle = GSMarkovStyle(order=3,numSteps=32,loopDuration=16);
markovStyle.generateStyle(allPatternsSliced)
newPattern = markovStyle.generatePattern()
```



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


# GS-API examples


All submodules within API provide help by typing help(Name of the module)


```python
help(GSPattern)
#help(GSBassmineAnalysis)
```

## Drum and bass generative example

### Drums example


```python
from gsapi import *

#Select the folder where the MIDI files for analysis are located

defaultMidiFolder = "../../corpus/midiTests"

#Use 'GSDataset' to extract the MIDI file

dataset = GSDataset(midiFolder=defaultMidiFolder,midiGlob="motown.mid",midiMap=GSIO.generalMidiMap,checkForOverlapped = True)

#use the function'splitInEqualLengthPatterns' to split the 
#contents of the dataset and to set the minimum "grain" or "timeframe" of the analysis
#save each slice as an element in a list called "allPatternsSliced"

allPatternsSliced = []
sizeOfSlice = 16
for midiPattern in dataset.patterns:
    for sliced in midiPattern.splitInEqualLengthPatterns(sizeOfSlice):
        allPatternsSliced+=[sliced]

#set the parameters of the markov style: the order, the number of steps and the final duration of the output
#and create an instance of GSMarkovStyle called "markovstyle"

markovStyle = GSMarkovStyle(order=1,numSteps=16,loopDuration=sizeOfSlice);

#generate a style based on the sliced patterns in the list "allPatternsSliced"
markovStyle.generateStyle(allPatternsSliced)

#Create a pattern simply using the function "generatePattern" of the markovStyle
newPattern = markovStyle.generatePattern()

# Export to MIDI
GSIO.toMIDI(newPattern, name="drums", midiMap=GSPatternUtils.generalMidiMap)

#print the pattern for visualization
print newPattern

#Extract the only the pattern of the kick drum from the complete pattern.
#Using the function "getPatternWithTags" and asking for the 'Acoustic Bass Drum' tag
#makes it easy. To create such list, we should first extract the events as a class called "justkick"
#and then extract each event on the class using justkick.events.


justkick=newPattern.getPatternWithTags('Acoustic Bass Drum', exactSearch=True, copy=True)

kickAsList=[0]*sizeOfSlice
for s,e in enumerate(justkick.events):

    kickAsList[int(e.startTime)]=1

print kickAsList
```

### Bassmine example

Following script commands present examples of Bassline rhythmic analysis for generative processes using GS-API.


```python
import gsapi.GSBassmineAnalysis as bassmine
import gsapi.GSBassmineMarkov as markov
import json
import csv
import random
```

First step is to determine the datasets to use. In this case we need to provide a dataset that contains MIDI clips of basslines and drums in pairs. That means that each bass MIDI file has an associated drum MIDI file. 

The implemented algorithm builds two Markov models.

First, contains the transition probabilities between bass beat patterns (temporal)
Second, contains the concurrency probabilities between kick-drum and bass beat patterns.
Moreover, the initial probabilites of events are computed, used to trigger the generation.



```python
# STYLE DICTIONARY
style = {1: 'booka_shade', 2: 'mr_scruff'}

# SELECT STYLE
style_id = 2

bass_path = '../../corpus/bassmine/' + style[style_id] + '/bass'
drum_path = '../../corpus/bassmine/' + style[style_id] + '/drums'
```

The implemented algorithm in [bassmine.corpus_analysis] builds two Markov models.

- Transition probabilities between bass beat patterns (temporal). 
- Concurrency probabilities between kick-drum and bass beat patterns (interlocking). 

Moreover, the initial probabilites of events are computed, used to trigger the generation.


```python
# Analyse corpus and build Markov model
MM, kick_patterns = bassmine.corpus_analysis(bass_path, drum_path)
# Normalize transition matrices
MM.normalize_model()
```

Once models are computed we can export them.


```python
# Output folder (to use with Max this folder should be Bassmine-master/models/)
_path = 'output/'
#  Uncomment to create models and export to pickle. REQUIRED to add new collections and use them in Max app.
# Export to pickle files
bassmine.write2pickle('initial', MM.get_initial(),_path + style[style_id] + '/')
bassmine.write2pickle('temporal', MM.get_temporal(),_path + style[style_id] + '/')
bassmine.write2pickle('interlocking', MM.get_interlocking(),_path + style[style_id] + '/')
```

#### Stylistic transformations using Markov Models with constraints


```python
# Compute Rhythm Homogeneous MM (HMM) and export to JSON
HModel = MM.rhythm_model(_path)
```


```python
# Given a Kick pattern generate a NHMM with interlocking constraint
# Select a random Kick pattern from the corpus
target_kick = kick_patterns[random.randint(0,len(kick_patterns)-1)]
#print target_kick
#target = [8,8,8,9,8,8,9,0]
NHMinter = markov.constrainMM(MM, target_kick, _path)
```


```python
# Create variation model
target_bass = [5,5,-5,5,5,-5,5,5]
NHMvariation = markov.variationMM(MM, target_bass, _path)
```

#### Generation examples


```python
# Example od generation without constraints. It computes Homogeneous Markov Model (HM)
pattern = markov.generateBassRhythm(MM)
pattern.toMIDI(name='regular')
```


```python
# Example of generation using Interlocking constraint.
inter_pattern = markov.generateBassRhythm(MM, target=target_kick)
# Write pattern to MIDI
inter_pattern.toMIDI(name='interlock')
```


```python
# Example of variation generation
var_mask = [1, 1, 1, -1, 1, 1, -1, 1]
variation_pattern = markov.generateBassRhythmVariation(MM,inter_pattern,var_mask)
variation_pattern.toMIDI(name='variation')
```



