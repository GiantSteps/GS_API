import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir,"python")))


from gsapi import *

import gsapi.GSBassmineAnalysis as bassmine
import gsapi.GSBassmineMarkov as markov
# import gsapi.GSDescriptors

import matplotlib.pyplot as plt
import json
import csv
import random



# STYLE DICTIONARY
style = {1: 'booka_shade', 2: 'mr_scruff'}

# SELECT STYLE
style_id = 2

bass_path = os.path.abspath('../../corpus/bassmine/' + style[style_id] + '/bass')
drum_path = os.path.abspath('../../corpus/bassmine/' + style[style_id] + '/drums')

# Output folder (to use with Max this folder should be Bassmine-master/models/)
_path = 'output/'

# Analyse corpus and build Markov model
MM, kick_patterns = bassmine.corpus_analysis(bass_path, drum_path)
# Normalize transition matrices
MM.normalize_model()

# Compute Rhythm Homogeneous MM and export to JSON
HModel = MM.rhythm_model(_path)

#  Uncomment to create models and export to pickle. REQUIRED to add new collections and use them in Max app.
# Export to pickle files
bassmine.write2pickle('initial', MM.get_initial(), _path + style[style_id] + '/')
bassmine.write2pickle('temporal', MM.get_temporal(), _path + style[style_id] + '/')
bassmine.write2pickle('interlocking', MM.get_interlocking(), _path + style[style_id] + '/')

# EXAMPLES OF MARKOV INTERLOCKING CONSTRAINED MODEL
# Given a Kick pattern generate a NHMM with interlocking constraint
target_kick = kick_patterns[random.randint(0,len(kick_patterns)-1)]
# print target_kick
#target = [8,8,8,9,8,8,9,0]
#NHMinter = markov.constrainMM(MM, target_kick, _path)

"""
# Create variation model
target_bass = [5,5,-5,5,5,-5,5,5]
NHMvariation = markov.variationMM(MM, target_bass, _path)
"""
# Generation examples
#patt_dict = markov.createMarkovGenerationDictionary(toJSON=True)
#print patt_dict
pattern = markov.generateBassRhythm(MM)

GSIO.toMidi(pattern, name='regular')

inter_pattern = markov.generateBassRhythm(MM, target=target_kick)
# Write pattern to MIDI
GSIO.toMidi(inter_pattern, name='interlock')

var_mask = [1, 1, 1, -1, 1, 1, -1, 1]
variation_pattern = markov.generateBassRhythmVariation(MM, inter_pattern, var_mask)
GSIO.toMidi(variation_pattern,name='variation')
#########################################
#  DEBUG



# syncDescriptor = GSDescriptors.GSDescriptorSyncopation()
# densDescriptor = GSDescriptors.GSDescriptorDensity()


# experiment paramters
it_values = [500]


# print "Interlocking"
# print MM.get_interlocking()

"""
##########################################
#  EXPORT TO CSV
"""
with open('initial.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(MM.get_initial())

with open('temporal.csv', 'wb') as f:
    writer = csv.writer(f)
    temp = MM.get_temporal()
    for row in temp:
        writer.writerow(row)

with open('interlocking.csv', 'wb') as f:
    writer = csv.writer(f)
    temp = MM.get_interlocking()
    for row in temp:
        writer.writerow(row)
"""
=======
patternDict = {}
idp = 0
#Kick patterns loop
t_id = 0

aux_sum = []
for target_kick in kick_patterns:
	print "New kick: "
	total_bass = []
	total_nodes = []

	patt_stack = {}

	target_kick = bassmine.translate_rhythm(bassmine.binaryBeatPattern([e.startTime for e in target_kick.events],8))
	NHMinter = markov.constrainMM(MM, target_kick, _path)

	for n in it_values:
		num_bass_patterns = 0
		#patt_stack = {}

		for i in range(n):
			xx = []
			yy = []
			#pattern = markov.generateBassRhythm(MM)
			pattern = markov._generateBassRhythm(NHMinter)
			#GSIO.toMIDI(pattern,name='regular')

			#print pattern
			_x = densDescriptor.getDescriptorForPattern(pattern)/pattern.duration
			_y = syncDescriptor.getDescriptorForPattern(pattern)
			#x.append(_x)
			#y.append(_y)

			if (_x,_y) not in patt_stack:
				xx.append(_x)
				yy.append(_y)
				# Add key o dictionary
				patt_stack[(_x,_y)] = {}
				patt_stack[(_x,_y)]['count'] = 1
				patt_stack[(_x,_y)]['patterns'] = {}
				# Use pattern.events[].startTime as dict key
				sT = tuple([x.startTime for x in pattern.events])
				patt_stack[(_x,_y)]['patterns'][sT] = 1

				num_bass_patterns += 1

			else:
				# Check if pattern already exist (avoid duplicate tuple: density,sync value)
				patt_stack[(_x,_y)]['count'] += 1
				# Use pattern.events[].startTime as dict key
				sT = tuple([x.startTime for x in pattern.events])

				if sT not in patt_stack[(_x,_y)]['patterns']:
					#patt_stack[(_x,_y)]['patterns'].append(pattern)
					patt_stack[(_x,_y)]['patterns'][sT] = 1
					num_bass_patterns += 1
				else:
					patt_stack[(_x,_y)]['patterns'][sT] += 1

			_sT = str(tuple([x.startTime for x in pattern.events]))
			if _sT not in patternDict:
				patternDict[_sT] = {}
				patternDict[_sT]['sync'] = _y
				patternDict[_sT]['density'] = _x
				patternDict[_sT]['midi_name'] = 'exp_' + str(idp)
				patternDict[_sT]['kick'] = [t_id]
				patternDict[_sT]['id'] = idp
				patternDict[_sT]['pattern'] = pattern.toJSONDict()
				#GSIO.toMIDI(pattern,path=_path+'midi_gen/',name='exp_' + str(idp))
				idp += 1
				#print idp
			else:
				#print "fumar"
				if t_id not in patternDict[_sT]['kick']:
					patternDict[_sT]['kick'].append(t_id)


		print len(patt_stack.keys())
		aux_sum.append(len(patt_stack.keys()))
		#print patt_stack
		#print patt_stack.keys()
		#print num_bass_patterns
		total_bass.append(num_bass_patterns)
		total_nodes.append(len(patt_stack.keys()))

	t_id +=1
	#plt.plot(it_values, total_nodes)
#plt.xlabel("Number of iterations")
#plt.ylabel("Number of unique generated rhythm nodes")
#plt.show()

# Output all patterns to midi and json file

with open('output/midi_gen/generated_patterns.json', 'w') as fp:
	json.dump(patternDict, fp, indent=4)

print len(patternDict.keys())
print sum(aux_sum)
"""
