from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import numpy as np
import copy,os
import random
import json
from . import GSPattern,GSPatternEvent
from . import GSBassmineUtils


def normalize(a):
	"""
	Normalize matrix by rows

	Args:
	    a: matrix (2D)

	Returns:
		a: normalized matrix
	"""
	c = 0
	for row in a:
		factor = sum(row)
		if factor > 0:
			a[c, :] = row / factor
		c += 1
	return a


def indices(a, func):
	"""
	Return indices in an array matching to a given function

	Examples: indices(array, lambda x: x <= 1)

	Args:
		a: array, list
		func: lambda function

	Returns:
		Indices of 'a' matching lambda function
	"""
	return [i for (i, val) in enumerate(a) if func(val)]


def pdf_sampling(n):  # variable argument list

	x = random.random()
	f = 0
	for i in range(1, len(n)):
		if x < sum(n[0:i]):
			f = i - 1
			break
	return f


class MarkovModel:
	"""
	Class to operate with markov models. Internal function used by GSBassmineAnalysis module.

	Attributes:
	    model_size: Dictionary size of the model
	    normalized: Boolean to control if the model has been normalized

	    support_temporal: internal matrix to compute markov model
	    support_initial: internal matrix to compute markov model
	    support_interlocking: internal matrix to compute markov model

	    initial_model: matrix to store initial MTM
	    temporal_model: matrix to store temporal MTM
	    interlocking_model: matrix to store interlocking MTM

	"""
	def __init__(self, model_size, order=1):
		"""
		Constructor

		Args:
			model_size: Dictionary size of the model
			order: default = 1 (not implemented for other orders yet...)
		Returns:
			instance of MarkovModel
		"""
		if type(model_size) == tuple:
			if len(model_size) == 2:
				self.model_size = model_size
			else:
				raise NameError("Model size must be an integer or a tuple of the form (x,y)")
		elif type(model_size) == int:
			self.model_size = (model_size, model_size)
		else:
			raise NameError("Model size must be an integer or a tuple of the form (x,y)")

		# Model state
		self.normalized = False

		# Temporal model
		self.support_temporal = np.zeros(self.model_size, dtype=float)
		self.support_initial = np.zeros(self.model_size[0], dtype=float)
		# Interlocking model
		self.support_interlocking = np.zeros(self.model_size, dtype=float)
		# Normalized model
		self.initial_model = []
		self.temporal_model = []
		self.interlocking_model = []
		# Pattern dictionary. Used for generation (table index -> onset pattern)
		self.model_dictionary = createMarkovGenerationDictionary()

	def add_temporal(self, pattern):
		"""
		Create markov transition matrix given a sequence

		First element counts are stored in self.initial_model
		Rest of elements feed the transition matrix (no time-series)

		Args:
			pattern: list or array with idx of the state dictionary
		"""
		count = 0
		for p in pattern:
			if count == 0:
				self.update_initial(p)
			elif 0 < count < len(pattern) - 1:
				self.update_temporal(pattern[count - 1], p)
			elif count == len(pattern) - 1:
				self.update_temporal(pattern[count], pattern[0])
			count += 1

	def add_interlocking(self, patt_kick, patt_bass):
		"""
		Create interlocking (concurrency) markov matrix given two sequences

		Args:
			patt_kick: kick drum pattern (anchor)
			patt_bass: bassline pattern
		"""

		l = min(len(patt_kick), len(patt_bass))

		for i in range(l):
			self.update_interlocking(patt_kick[i], patt_bass[i])

	def update_interlocking(self, x, y):
		"""
		internal function to update interlocking matrix

		Args:
			x: row (anchor)
			y: col (bass)
		"""
		self.support_interlocking[int(x), int(y)] += 1.

	def update_temporal(self, x, y):
		"""
		internal function to update temporal matrix

		Args:
		 x: row (past)
		 y: col (present)
		"""
		self.support_temporal[int(x), int(y)] += 1.

	def update_initial(self, x):
		"""
		internal function to update initial probabilites

		Args:
			x: row (probabilities)
		"""
		self.support_initial[int(x)] += 1.

	def normalize_model(self):
		"""
		Normalize matrices
		"""
		self.initial_model = self.support_initial / sum(self.support_initial)
		self.temporal_model = normalize(self.support_temporal)
		self.interlocking_model = normalize(self.support_interlocking)
		self.normalized = True

	def get_initial(self):
		"""
		Get initial probabilites

		Returns:
			initial_model: list
		"""
		return self.initial_model

	def get_temporal(self):
		"""
		Get temporal model

		Returns:
			temporal_model: 2D matrix
		"""
		return self.temporal_model

	def get_interlocking(self):
		"""
		Get interlocking model

		Returns:
			interlocking_model: 2D matrix
		"""
		return self.interlocking_model

	def rhythm_model(self, _path="output/"):

		path = _path

		init_set = markov_tm_2dict(self.initial_model)
		#print( self.initial_model)
		init = []

		init_dict = {}
		init_dict['initial'] = {}
		init_dict['initial']['pattern'] = [int(r) for r in init_set]
		init_dict['initial']['prob'] = [self.initial_model[i] for i in init_dict['initial']['pattern']]
		#print( "init\n", init_dict)

		rhythm_temporal_model = markov_tm_2dict(self.get_temporal())
		rhythm_dict = dict()
		#print((pitch_temporal_model))
		## Temporal model
		for key,val in rhythm_temporal_model.items():
			rhythm_dict[key] = {}
			#print( key # parent)
			#print( list(val) # child)
			tmp = [] # child
			for v in val:
				tmp.append(self.get_temporal()[key, int(v)])
			#print( list(tmp/sum(tmp)))
			rhythm_dict[key]['pattern'] = [int(r) for r in rhythm_temporal_model[key]]
			rhythm_dict[key]['probs'] = list(tmp/sum(tmp))

		ePath = os.path.abspath(os.path.join(path,'HModel.json'))
		with open( ePath  , 'w') as outfile:
			json.dump(rhythm_dict, outfile)
			outfile.close()

		with open( path + 'HModel_init.json', 'w') as outfile:
			json.dump(init_dict, outfile)
			outfile.close()
		#print( "Rhythm model computed\n", rhythm_dict)
		return [init_dict, rhythm_dict]


	def pitch_model(self):
		"""
		Build pitch model

		[work in progress...]

		Takes first note an assume it as root note. Other notes are represented as intervals relative to root (first note)

		Returns:
			dictionary{0: {'interval': , 'probs'}, {},{},...}
		"""
		pitch_temporal_model = markov_tm_2dict(self.get_temporal())
		pitch_dict = dict()
		#print((pitch_temporal_model))
		## Temporal model
		for key,val in pitch_temporal_model.items():
			pitch_dict[key-12] = {}
			#print( key # parent)
			#print( list(val) # child)
			tmp = [] # child
			for v in val:
				tmp.append(self.get_temporal()[key, int(v)])
			#print( list(tmp/sum(tmp)))
			pitch_dict[key-12]['interval'] = [int(x)-12 for x in val]
			pitch_dict[key-12]['probs'] = list(tmp/sum(tmp))

		print( "Pitch model computed\n", pitch_dict)
		return pitch_dict


def constrainMM(markov_model, target, _path="output/"):
	"""

	Compute non-homogeneuous markov model (NHMM) based on interlocking constraint.
	Given a target pattern it constraint the original model and ensure arc-consistency

	This function is also implemented as a pyext class.

	Args:
		markov_model: MarkovModel instance (output from GSBassmineUtils.corpus_analysis())
		target: Target pattern for interlocking (kick) represented by its pattern ids.
		_path: Path to where the Markov models will be stored

	Returns:
		Interlocking model as dictionary in JSON format

	"""
	path = _path

	b0 = copy.copy(markov_model.get_initial())
	b = copy.copy(markov_model.get_temporal())
	inter = copy.copy(markov_model.get_interlocking())

	# b and inter are converted to dictionaries {row>0 : (idx columns>0)}
	# Domains
	Dom_init = markov_tm_2dict(b0)
	Dom_B = markov_tm_2dict(b)
	Dom_I = markov_tm_2dict(inter)

	#print( "Initial dict ", Dom_init)
	#print( "Temporal dict ", Dom_B)
	#print( "Interlocking dict ", Dom_I)

	## Representation of target kick pattern as variable domain
	target = GSBassmineUtils.translate_rhythm(GSBassmineUtils.binaryBeatPattern([e.startTime for e in target.events],target.duration))

	target_setlist = []
	for t in target:
		# RELAXATION RULE: if the target kick is not in the model consider metronome pulse as kick
		if t in Dom_I:
			target_setlist.append(Dom_I[t])
		else:
			target_setlist.append(Dom_I[8])
			print( "Kick pattern mistmatch")
	#print( target_setlist)

	## V store the domain of patterns at each step
	V = []

	filter_init = Dom_init.intersection(target_setlist[0])
	#print( list(filter_init))
	## Look for possible continuations of filter_init in Dom_B, constrained to target_list[1]
	V.append(dict())
	tmp = []
	for f in filter_init:
	#	print( "Possible intital continuations",f, Dom_B[int(f)])
	#	print( "Kick constrain", target_setlist[1])
	#	print( "Intersection", Dom_B[int(f)].intersection(target_setlist[1]))

		if len(Dom_B[int(f)].intersection(target_setlist[1])) > 0:
			V[0][int(f)] = Dom_B[int(f)].intersection(target_setlist[1])
			tmp.append(f)
	#	print( "\n\n")
	#print( "Kick constr", list(target_setlist[0]))
	#print( "V0", V[0])
	#print( "V1", V[1].keys()	# Domain for step 1 / rows  of transition matrix)
	#print( V[1])

	## Create rest of V
	##############################################
	## Make backtrack free Non-Homogeneuous Markov Model ordr 1
	##############################################
	for step in range(1, len(target)-1):
		V.append(dict())
		#print( "Kick constr", list(target_setlist[step]))
		# for each v in V[step] keep continuations that match interlocking with step+1
		for t in target_setlist[step]:
			if len(Dom_B[int(t)].intersection(target_setlist[step+1])):
				V[step][int(t)] =  Dom_B[int(t)].intersection(target_setlist[step+1])
		#print( "check\n")
		#print( "V", step, V[step].keys())

	## Delete values from each key in V[i] that are not in V[i+1]
	val_del = dict()
	## Font-propagation
	for step in range(1,len(target)-1):
		val_del_temp = []
		next_key = set([str(x) for x in V[step].keys()])
		#print( next_key)
		for key, value in V[step-1].items():
			#print( key, value)
			tmp_int = value.intersection(next_key)
			#if len(tmp_int) > 0:
			V[step-1][key] = tmp_int
			if len(tmp_int) == 0:
				val_del_temp.append(key)
		val_del[step] = val_del_temp
	#print( val_del)
	## Back-propagation
	for step, value in val_del.items():
		if len(value) > 0:
			for v in value:
				## Delete key
				V[step-1].pop(v, None)
			## Delete in previous continuations
			#print( V[step-2])
			for idx in V[step-2].keys():
				V[step-2][idx] = set([str(x) for x in V[step-1].keys()]).intersection(V[step-2][idx])
	# BUILD FINAL DICTIONARY
	#print( "\nFinal Model:")
	out_Model = {}
	init = []
	init_dict = dict()
	for key in V[0]:
		init.append(b0[key])
	init_dict['initial'] = dict()
	init_dict['initial']['prob'] = list(init/sum(init))
	init_dict['initial']['pattern'] = V[0].keys()
	#print( init_dict)
	for i in range(len(V)):
		out_Model[i] = {}
		#print( "step:",i)
		for key,val in V[i].items():
			out_Model[i][key] = {}
			#print( key # parent)
			#print( list(val) # child)
			tmp = [] # child
			for v in val:
				tmp.append(b[key, int(v)])
			#print( list(tmp/sum(tmp)))
			out_Model[i][key]['pattern'] = [int(x) for x in val]
			out_Model[i][key]['probs'] = list(tmp/sum(tmp))
	#print( out_Model)
	with open( path + 'NHModel.json', 'w') as outfile:
		json.dump(out_Model, outfile)
		outfile.close()

	with open( path + 'Model_init.json', 'w') as outfile:
		json.dump(init_dict, outfile)
		outfile.close()

	#print(("Interlocking model build!"))

	return [init_dict, out_Model]


def variationMM(markov_model, target, _path="output/"):

	"""
	Compute non-homogeneuous markov model (NHMM) based on variation constraint.
	Given a target Variation Mask(VM) it constraint the original model and ensure arc-consistency

	Examples:
	    VM should be a list representing a pattern (id formatted) with negative numbers on those frames to variate.
	    Positive values will be preserved.

	Args:
		markov_model: MarkovModel instance (output from GSBassmineUtils.corpus_analysis())
		target: Variation Mask (list with negative numbers indicating variation of that time frame)
		_path: Path to where the Markov models will be stored

	Returns:
	    Variation model as a dictionary in JSON format

	"""
	path = _path

	b = copy.copy(markov_model.get_temporal())

	## Domains
	#Dom_init = markov_tm_2dict(b0)
	Dom_B = markov_tm_2dict(b)
	#Dom_I = markov_tm_2dict(inter)

	#print( "Initial dict ", Dom_init)
	#print( "Temporal dict ", Dom_B)
	#print( "Interlocking dict ", Dom_I)

	# target
	#target = [8,8,4,-2,2,0,4,-2,8]

	# Create V : variable domain for transitions
	V = []
	# target
	#target = [8,8,4,14,4,10,8,2,8]

	V.append(dict())

	if target[1] >= 0:
		V[0][target[0]] = {str(target[1])}
	else:
		V[0][target[0]] = Dom_B[target[0]]


	for i in range(1,len(target)-1):

		V.append(dict())

		if target[i] >= 0:  # Current beat don't vary

			for key, value in V[i-1].items():

				# store keys that match target[i]
				tmp_key = value.intersection({str(target[i])})
				if len(tmp_key) > 0:
					V[i][int(list(tmp_key)[0])] = Dom_B[int(list(tmp_key)[0])]
				#V[i][target[i-1]] = set([str(target[i])])

		else:  # Current beat varies

			#Check possible continuations from V[i-1] as Key candidates in V[i]
			for key, value in V[i-1].items():

				for v in value:
					V[i][int(v)] = Dom_B[int(v)]

			#print( "h")


	#V.append(dict())

	#V[len(target)-1][target[len(target)-1]] = set([str(target[len(target)-1])])

	#print( V)


	## Delete values from each key in V[i] that are not in V[i+1]
	val_del = dict()
	## Font-propagation
	for step in range(1,len(target)-1):
		val_del_temp = []
		next_key = set([str(x) for x in V[step].keys()])
		#print( next_key)
		for key, value in V[step-1].items():
			#print( key, value)
			tmp_int = value.intersection(next_key)
			#if len(tmp_int) > 0:
			V[step-1][key] = tmp_int
			if len(tmp_int) == 0:
				val_del_temp.append(key)
		val_del[step] = val_del_temp
	#print( val_del)
	## Back-propagation
	for step, value in val_del.items():
		if len(value) > 0:
			for v in value:
				## Delete key
				V[step-1].pop(v, None)
			## Delete in previous continuations
			#print( V[step-2])
			for idx in V[step-2].keys():
				V[step-2][idx] = set([str(x) for x in V[step-1].keys()]).intersection(V[step-2][idx])
	# BUILD FINAL DICTIONARY
	#print( "\nFinal Model:")

	for key,val in V[len(V)-1].items():
		tmp_val  = val.intersection({str(target[len(target) - 1])})
		#print( tmp_val)
		if len(tmp_val)>0:
			V[len(V)-1][key] = tmp_val

	#for v in V:
	#	print( v)
	#	print( "\n")

	out_Model = {}
	# Force last beat
	#init = []
	init_dict = dict()
	#for key in V[0]:
	#	init.append(b0[key])
	init_dict['initial'] = dict()
	init_dict['initial']['prob'] = 1.00
	init_dict['initial']['pattern'] = target[0]
	#print( init_dict)

	for i in range(len(V)):
		out_Model[i] = {}
		#print( "step:",i)
		for key,val in V[i].items():
			out_Model[i][key] = {}
			#print( key # parent)
			#print( list(val) # child)
			tmp = [] # child
			for v in val:
				tmp.append(b[key, int(v)])
			#print( list(tmp/sum(tmp)))
			#print( tmp)
			out_Model[i][key]['pattern'] = [int(x) for x in val]
			out_Model[i][key]['probs'] = list(tmp/sum(tmp))
	#print( out_Model)
	with open( path + 'NHModel_var.json', 'w') as outfile:
		json.dump(out_Model, outfile)
		outfile.close()

	with open( path + 'Model_init_var.json', 'w') as outfile:
		json.dump(init_dict, outfile)
		outfile.close()

	print(("Variation model build!"))
	return [init_dict, out_Model]


def markov_tm_2dict(a):
	"""
	Convert markov transition matrix to dictionary of sets.
	Compact representation to avoid sparse matrices and better performance in the constrain model

	Args:
		a: MarkovModel temporal/interlocking/pitch matrix

	Returns:
		dictionary{}
	"""
	out = dict()
	key = 0

	if len(a.shape) == 2:
		for row in a:
			value = 0
			tmp_dom = []
			if sum(row) > 0:
				for col in row:
					if col > 0:
						tmp_dom.append(str(value))
					value += 1
				out[key] = set(tmp_dom)
			key += 1
		return out
	elif len(a.shape) == 1:
		tmp_dom = []
		value = 0
		for col in a:
			if col > 0:
				tmp_dom.append(str(value))
			value += 1

		return set(tmp_dom)
	else:
		print( "Wrong size")


def createMarkovGenerationDictionary(toJSON=False, _path="output/"):
	"""
	Internal function to build a dictionary relating binarized patterns into start times (in beats)
	Args:
	    toJSON: boolean. If true it exports to JSON
	    _path: path to store the dictionary as JSON

	Returns: Pattern dictionary

	"""
	start_times = [0,0.25,0.5,0.75]

	out = dict()

	out['patterns'] = dict()

	for p in range(16):
		# Binary pattern
		binpatt = format(p, '04b')
		st = []
		for i in range(len(start_times)):
			if binpatt[i] == '1':
				st.append((start_times[i]))
		val = st
		out['patterns'][p] = val


	#print( out)

	path = _path
	name = 'pattern_dict'
	data = out

	if toJSON:
		with open(path + name + '.json', 'w') as outfile:
				json.dump(data, outfile)

	return data


def generateBassRhythm(markov_model, beat_length=8, target=[]):
	"""
	Function to generate a rhythmic bassline. If no target given the system assume no constraints and uses the regular
	Markov model (computed by MarkovModel.rhythm_model()).
	If target given it is assumed as target constraint for interlocking model.
	Args:
	    markov_model: output from  MarkovModel.rhythm_model()
	    beat_length: desired length of the generated pattern
	    target: Pattern used as constraint in Interlocking Model.

	Returns:
	    bassline: GSPattern containing bassline onset pattern

	"""
	bassline = GSPattern()
	pattern_idx = []

	if len(target) == 0:  # no constraints

		HMM = markov_model.rhythm_model()

		pattern_idx.append(np.random.choice(HMM[0]['initial']['pattern'], p=HMM[0]['initial']['prob']))

		for beat in range(beat_length-1):
			pattern_idx.append(np.random.choice(HMM[1][pattern_idx[beat]]['pattern'],
			                                    p=HMM[1][pattern_idx[beat]]['probs']))

	else: # use constrained model

		if len(target) < beat_length:
			beat_length = len(target)

		NHMM = constrainMM(markov_model, target)
		pattern_idx.append(np.random.choice(NHMM[0]['initial']['pattern'], p=NHMM[0]['initial']['prob']))

		for beat in range(beat_length-1):
			pattern_idx.append(np.random.choice(NHMM[1][beat][pattern_idx[beat]]['pattern'],
			                                    p=NHMM[1][beat][pattern_idx[beat]]['probs']))

	bassline.duration = len(pattern_idx)

	start_times = []
	beat_count = 0
	for idx in pattern_idx:
		st = markov_model.model_dictionary['patterns'][idx]
		if len(st)>0:
			for s in st:
				bassline.events.append(GSPatternEvent(s + beat_count,0.25,36,velocity=110,tag="bass"))
		beat_count += 1

	return bassline

def _generateBassRhythm(markov_model, beat_length=8, target=[]):
	"""
	Function to generate a rhythmic bassline. If no target given the system assume no constraints and uses the regular
	Markov model (computed by MarkovModel.rhythm_model()).
	If target given it is assumed as target constraint for interlocking model.
	Args:
	    markov_model: output from  MarkovModel.rhythm_model()
	    beat_length: desired length of the generated pattern
	    target: Pattern used as constraint in Interlocking Model.

	Returns:
	    bassline: GSPattern containing bassline onset pattern

	"""
	bassline = GSPattern()
	pattern_idx = []

	markovDict = createMarkovGenerationDictionary()

	pattern_idx.append(np.random.choice(markov_model[0]['initial']['pattern'], p=markov_model[0]['initial']['prob']))

	for beat in range(beat_length-1):
		pattern_idx.append(np.random.choice(markov_model[1][beat][pattern_idx[beat]]['pattern'],
		                                    p=markov_model[1][beat][pattern_idx[beat]]['probs']))

	bassline.duration = len(pattern_idx)

	start_times = []
	beat_count = 0
	for idx in pattern_idx:
		st = markovDict['patterns'][idx]
		if len(st)>0:
			for s in st:
				bassline.events.append(GSPatternEvent(s + beat_count,0.25,36,velocity=110,tag="bass"))
		beat_count += 1

	return bassline


def generateBassRhythmVariation(markov_model, target_pattern, variation_mask):
	"""
	Function that implements a variation model given an already generated pattern. Based on the variation mask it creates
	a Markov model that preserve desired beat measures while it models "variation" beats to be stylistically consistent.
	Args:
	    markov_model: output from  MarkovModel.rhythm_model()
	    target_pattern: GSPattern, for instance output from generateBassRhythm()
	    variation_mask: List of the same length of the target_pattern(in beats). Positions with value 1 will be preserved,
	    those with -1 will vary.

	Returns:
		bassline: generated GSPattern
	"""

	bassline = GSPattern()
	pattern_idx = []

	if len(variation_mask) < target_pattern.duration:
		print( "Variation mask must be same length as target_pattern (in beats)")
		return
	else:
		#Convert target pattern to markov dictionary
		onset_target = [x.startTime for x in target_pattern.events]
		target_rhythm = GSBassmineUtils.binaryBeatPattern(onset_target, target_pattern.duration)
		target_id = GSBassmineUtils.translate_rhythm(target_rhythm)
		#Mask formatted pattern
		masked_target = [target_id[i] * variation_mask[i] for i in range(len(variation_mask) - 1)]

		#Build variation model
		NHMM = variationMM(markov_model, masked_target)
		#Generate GSPattern
		pattern_idx.append(target_id[0])

		for beat in range(len(masked_target) - 1):
			pattern_idx.append(np.random.choice(NHMM[1][beat][pattern_idx[beat]]['pattern'],
			                                    p=NHMM[1][beat][pattern_idx[beat]]['probs']))

		bassline.duration = len(pattern_idx)

		beat_count = 0
		for idx in pattern_idx:
			st = markov_model.model_dictionary['patterns'][idx]
			if len(st)>0:
				for s in st:
					bassline.events.append(GSPatternEvent(s + beat_count,0.25,36,velocity=110,tag=("bass")))
			beat_count += 1

		return bassline



