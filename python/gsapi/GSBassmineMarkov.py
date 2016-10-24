import numpy as np
import copy
import json

def normalize(a):
	"""
	Normalize matrix by rows
	:param a: matrix
	:return: normalized matrix
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
	EX: indices(array, lambda x: x <= 1)
	:param a: array, list
	:param func: lambda function
	:return: indices matching lambda function
	"""
	# UF.
	return [i for (i, val) in enumerate(a) if func(val)]


class MarkovModel:
	"""
	Class to operate with markov models
	"""
	def __init__(self, model_size, order=1):
		"""
		Constructor
		:param model_size: Dictionary size of the model
		:param order: default = 1 (not implemented)
		:return: instance of MarkovModel
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

	def add_temporal(self, pattern):
		"""
		Create markov transition matrix given a sequence

		First element counts are stored in self.initial_model
		Rest of elements feed the transition matrix (no time-series)

		:param pattern: list or array with idx of the state dictionary
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
		Create interlocking markov matrix given two sequences

		:param patt_kick: kick drum pattern (anchor)
		:param patt_bass: bassline pattern
		"""

		l = min(len(patt_kick), len(patt_bass))

		for i in range(l):
			self.update_interlocking(patt_kick[i], patt_bass[i])

	def update_interlocking(self, x, y):
		"""
		internal function to update interlocking matrix
		:param x: row (anchor)
		:param y: col (bass)
		"""
		self.support_interlocking[int(x), int(y)] += 1.

	def update_temporal(self, x, y):
		"""
		internal function to update temporal matrix
		:param x: row (past)
		:param y: col (present)
		"""
		self.support_temporal[int(x), int(y)] += 1.

	def update_initial(self, x):
		"""
		internal function to update initial probabilites
		:param x: row (probabilities)
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
		:return: list
		"""
		return self.initial_model

	def get_temporal(self):
		"""
		Get temporal model
		:return: matrix[][]
		"""
		return self.temporal_model

	def get_interlocking(self):
		"""
		Get interlocking model
		:return:
		"""
		return self.interlocking_model

	def pitch_model(self):
		"""
		Build pitch model

		work in progress...

		Takes first not an assume it as root note. Other notes are represented as intervals relative to root (first note)

		:return: dictionary{0: {'interval': , 'probs'}, {},{},...}
		"""
		pitch_temporal_model = markov_tm_2dict(self.get_temporal())
		pitch_dict = dict()
		#print(pitch_temporal_model)
		## Temporal model
		for key,val in pitch_temporal_model.iteritems():
			pitch_dict[key-12] = {}
			print key # parent
			print list(val) # child
			tmp = [] # child
			for v in val:
				tmp.append(self.get_temporal()[key, int(v)])
			print list(tmp/sum(tmp))
			pitch_dict[key-12]['interval'] = [int(x)-12 for x in val]
			pitch_dict[key-12]['probs'] = list(tmp/sum(tmp))

		print "Pitch model computed\n", pitch_dict
		return pitch_dict


def constrainMM(markov_model, target):
	"""

	Compute non-homogeneuous markov model based on interlocking constraint

	This function is also implemented as a pyext class.

	:param markov_model: MarkovModel instance
	:param target: Target pattern for interlocking (kick) represented by its pattern ids.

	"""
	path = "output/"

	b0 = copy.copy(markov_model.get_initial())
	b = copy.copy(markov_model.get_temporal())
	inter = copy.copy(markov_model.get_interlocking())

	# b and inter are converted to dictionaries {row>0 : (idx columns>0)}
	# Domains
	Dom_init = markov_tm_2dict(b0)
	Dom_B = markov_tm_2dict(b)
	Dom_I = markov_tm_2dict(inter)

	print "Initial dict ", Dom_init
	print "Temporal dict ", Dom_B
	print "Interlocking dict ", Dom_I

	## Representation of target kick pattern as variable domain
	target_setlist = []
	for t in target:
		# RELAXATION RULE: if the target kick is not in the model consider metronome pulse as kick
		if t in Dom_I:
			target_setlist.append(Dom_I[t])
		else:
			target_setlist.append(Dom_I[8])
			print "Kick pattern mistmatch"
	#print target_setlist

	## V store the domain of patterns at each step
	V = []

	filter_init = Dom_init.intersection(target_setlist[0])
	#print list(filter_init)
	## Look for possible continuations of filter_init in Dom_B, constrained to target_list[1]
	V.append(dict())
	tmp = []
	for f in filter_init:
	#	print "Possible intital continuations",f, Dom_B[int(f)]
	#	print "Kick constrain", target_setlist[1]
	#	print "Intersection", Dom_B[int(f)].intersection(target_setlist[1])

		if len(Dom_B[int(f)].intersection(target_setlist[1])) > 0:
			V[0][int(f)] = Dom_B[int(f)].intersection(target_setlist[1])
			tmp.append(f)
	#	print "\n\n"
	#print "Kick constr", list(target_setlist[0])
	#print "V0", V[0]
	#print "V1", V[1].keys()	# Domain for step 1 / rows  of transition matrix
	#print V[1]

	## Create rest of V
	##############################################
	## Make backtrack free Non-Homogeneuous Markov Model ordr 1
	##############################################
	for step in range(1, len(target)-1):
		V.append(dict())
		#print "Kick constr", list(target_setlist[step])
		# for each v in V[step] keep continuations that match interlocking with step+1
		for t in target_setlist[step]:
			if len(Dom_B[int(t)].intersection(target_setlist[step+1])):
				V[step][int(t)] =  Dom_B[int(t)].intersection(target_setlist[step+1])
		#print "check\n"
		#print "V", step, V[step].keys()

	## Delete values from each key in V[i] that are not in V[i+1]
	val_del = dict()
	## Font-propagation
	for step in range(1,len(target)-1):
		val_del_temp = []
		next_key = set([str(x) for x in V[step].keys()])
		#print next_key
		for key, value in V[step-1].iteritems():
			#print key, value
			tmp_int = value.intersection(next_key)
			#if len(tmp_int) > 0:
			V[step-1][key] = tmp_int
			if len(tmp_int) == 0:
				val_del_temp.append(key)
		val_del[step] = val_del_temp
	#print val_del
	## Back-propagation
	for step, value in val_del.iteritems():
		if len(value) > 0:
			for v in value:
				## Delete key
				V[step-1].pop(v, None)
			## Delete in previous continuations
			#print V[step-2]
			for idx in V[step-2].keys():
				V[step-2][idx] = set([str(x) for x in V[step-1].keys()]).intersection(V[step-2][idx])
	# BUILD FINAL DICTIONARY
	#print "\nFinal Model:"
	out_Model = {}
	init = []
	init_dict = dict()
	for key in V[0]:
		init.append(b0[key])
	init_dict['initial'] = dict()
	init_dict['initial']['prob'] = list(init/sum(init))
	init_dict['initial']['pattern'] = V[0].keys()
	#print init_dict
	for i in range(len(V)):
		out_Model[i] = {}
		#print "step:",i
		for key,val in V[i].iteritems():
			out_Model[i][key] = {}
			#print key # parent
			#print list(val) # child
			tmp = [] # child
			for v in val:
				tmp.append(b[key, int(v)])
			#print list(tmp/sum(tmp))
			out_Model[i][key]['pattern'] = [int(x) for x in val]
			out_Model[i][key]['probs'] = list(tmp/sum(tmp))
	#print out_Model
	with open( path + 'NHModel.json', 'w') as outfile:
		json.dump(out_Model, outfile)
		outfile.close()

	with open( path + 'Model_init.json', 'w') as outfile:
		json.dump(init_dict, outfile)
		outfile.close()

	print("Interlocking model build!")

	print len(out_Model)


def variationMM(markov_model, target):

	path =  "output/"

	b = copy.copy(markov_model.get_temporal())

	## Domains
	#Dom_init = markov_tm_2dict(b0)
	Dom_B = markov_tm_2dict(b)
	#Dom_I = markov_tm_2dict(inter)

	#print "Initial dict ", Dom_init
	#print "Temporal dict ", Dom_B
	#print "Interlocking dict ", Dom_I

	# target
	#target = [8,8,4,-2,2,0,4,-2,8]

	# Create V : variable domain for transitions
	V = []
	# target
	#target = [8,8,4,14,4,10,8,2,8]

	V.append(dict())

	if target[1] >= 0:
		V[0][target[0]] = set([str(target[1])])
	else:
		V[0][target[0]] = Dom_B[target[0]]


	for i in range(1,len(target)-1):

		V.append(dict())

		if target[i] >= 0:  # Current beat don't vary

			for key, value in V[i-1].iteritems():

				# store keys that match target[i]
				tmp_key = value.intersection(set([str(target[i])]))
				if len(tmp_key) > 0:
					V[i][int(list(tmp_key)[0])] = Dom_B[int(list(tmp_key)[0])]
				#V[i][target[i-1]] = set([str(target[i])])

		else:  # Current beat varies

			#Check possible continuations from V[i-1] as Key candidates in V[i]
			for key, value in V[i-1].iteritems():

				for v in value:
					V[i][int(v)] = Dom_B[int(v)]

			#print "h"


	#V.append(dict())

	#V[len(target)-1][target[len(target)-1]] = set([str(target[len(target)-1])])

	#print V
	for v in V:
		print v
		print "\n"

	## Delete values from each key in V[i] that are not in V[i+1]
	val_del = dict()
	## Font-propagation
	for step in range(1,len(target)-1):
		val_del_temp = []
		next_key = set([str(x) for x in V[step].keys()])
		#print next_key
		for key, value in V[step-1].iteritems():
			#print key, value
			tmp_int = value.intersection(next_key)
			#if len(tmp_int) > 0:
			V[step-1][key] = tmp_int
			if len(tmp_int) == 0:
				val_del_temp.append(key)
		val_del[step] = val_del_temp
	#print val_del
	## Back-propagation
	for step, value in val_del.iteritems():
		if len(value) > 0:
			for v in value:
				## Delete key
				V[step-1].pop(v, None)
			## Delete in previous continuations
			#print V[step-2]
			for idx in V[step-2].keys():
				V[step-2][idx] = set([str(x) for x in V[step-1].keys()]).intersection(V[step-2][idx])
	# BUILD FINAL DICTIONARY
	#print "\nFinal Model:"

	for key,val in V[len(V)-1].iteritems():
		tmp_val  = val.intersection(set([str(target[len(target)-1])]))
		print tmp_val
		if len(tmp_val)>0:
			V[len(V)-1][key] = tmp_val

	out_Model = {}
	# Force last beat
	#init = []
	init_dict = dict()
	#for key in V[0]:
	#	init.append(b0[key])
	init_dict['initial'] = dict()
	init_dict['initial']['prob'] = 1.00
	init_dict['initial']['pattern'] = target[0]
	#print init_dict

	for i in range(len(V)):
		out_Model[i] = {}
		#print "step:",i
		for key,val in V[i].iteritems():
			out_Model[i][key] = {}
			#print key # parent
			#print list(val) # child
			tmp = [] # child
			for v in val:
				tmp.append(b[key, int(v)])
			#print list(tmp/sum(tmp))
			#print tmp
			out_Model[i][key]['pattern'] = [int(x) for x in val]
			out_Model[i][key]['probs'] = list(tmp/sum(tmp))
	#print out_Model
	with open( path + 'NHModel_var.json', 'w') as outfile:
		json.dump(out_Model, outfile)
		outfile.close()

	with open( path + 'Model_init_var.json', 'w') as outfile:
		json.dump(init_dict, outfile)
		outfile.close()

	print("Variation model build!")

def markov_tm_2dict(a):
	"""
	Convert markov transition matrix to dictionary of sets.
	Compact representation to avoid sparse matrices and better performance in the constrain model

	:param a: MarkovModel temporal/interlocking/pitch matrix

	:return dictionary
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
		print "Wrong size"
