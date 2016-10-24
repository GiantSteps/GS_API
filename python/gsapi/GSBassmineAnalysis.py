# Read Midi Folders from style
import madmom
import numpy as np
import utility_functions as uf
import markov
import pickle


def write2pickle(name,data, path='../../models/'):
	"""
	Export numpy array to pickle
	:param name: filename
	:param data: allowed pickle data
	:param path: output folder
	:return:
	"""
	#path = 'rhythmic_analysis/graph_models/pickle/'

	with open(path + name + '.pickle', 'wb') as f:
		# Pickle the 'data' dictionary using the highest protocol available.
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def quantize_pattern(pattern):
	"""
	Quantize array of note start times to 1/16 bar resolution
	Loop lengthn is quantized to multiples of whole bars

	:param pattern: array of start times in beats
	:return: array of binary onsets
	"""
	RES = 4

	noBeats_bass = uf.numberOfBeats(pattern)  # Bass files length set the global length of analysis
	print '\n# of beats: ', noBeats_bass
	#beat_subdiv = np.arange(start=0, step=0.25, stop=(noBeats_bass * RES) - 1)
	subdiv_aux = np.array([0., 0.25, 0.5, 0.75])
	# Matrix to store the binary representation of the midi files
	# Basslines -> 1 matrix
	rhythm = np.zeros((noBeats_bass, RES), dtype=int)

	for o in pattern:
		# quantize to the closest subdivision
		i, d = divmod(o, 1)  # i = row(beat number) , d = column (beat subdivision)
		d_ = (abs(subdiv_aux - d)).argmin()
		if i < noBeats_bass:
			rhythm[int(i), d_] = 1
	return rhythm


def translate_rhythm(rhythm):
	"""
	Translate binary rhythm to markov variables dictionary

	:param rhythm: array of binary onsets.(output of quantize_pattern())
	:return: array of beat pattern ids
	"""
	id = []

	for beat in rhythm:
		id.append((beat[0] * 8) + (beat[1] * 4) + (beat[2] * 2) + beat[3])
	return id


def corpus_analysis(bass_path, drum_path):
	"""
	Compute rhtyhmic model (temporal + interlocking)  and pitch model (intervals)

	Input files must match their names : i.e. bass_[trackname].mid , drums_[trackname].mid

	:param bass_path: folder with bass midi files
	:param drum_path: folder with drums midi files
	:return: rhythmic and pitch Markov Models , Kick patterns
	"""

	bass_files = madmom.utils.search_files(bass_path, '.mid')
	drum_files = madmom.utils.search_files(drum_path, '.mid')

	bass_names = []
	drum_names = []

	print "Bass Files"
	for bf in bass_files:
		bass_names.append(bf[len(bass_path) + 1:-len('.mid')])
	print "\nNumber of files: ", len(bass_files)

	print "\nDrums Files"
	for df in drum_files:
		drum_names.append(df[len(drum_path) + 1:-len('.mid')])
	print "\nNumber of files: ", len(drum_files)


	# File counter
	file_it = 0

	# Markov analysis test
	rhythm_model = markov.MarkovModel(16)
	kick_patterns = []

	# Pitch Model
	pitch_model = markov.MarkovModel(25);
	pitch_contours = []
	# LOOP THROUGH THE DIFFERENT MIDI INSTANCES
	for f in range(len(drum_files)):
		# for f in range(0,2):
		match = str(madmom.utils.match_file('drums' + bass_names[f][4:], drum_names))
		match_file = drum_path + '/' + match[2:-2] + '.mid'

		print ('Bass file: '), bass_files[f]
		print ('Drum file: '), match_file
		print bass_names[f][5:-3]
		"""
		BASSLINE
		"""
		# Read Bassline files
		bass_midi = madmom.utils.midi.MIDIFile.from_file(bass_files[f])
		bass_midi.note_time_unit = 'b'
		onset_bass = bass_midi.notes[:, 0]
		print bass_midi.notes[:,1] - bass_midi.notes[0,1] + 12
		# Pitch Contour
		# compute diff
		pitch_contours.append(bass_midi.notes[:,1] - (bass_midi.notes[0,1] + 12))
		#pitch_contours.append(np.diff(bass_midi.notes[:, 1]))

		# Quantize rhythm
		bass_rhythm = quantize_pattern(onset_bass)
		#print(bass_rhythm)
		bass_id = translate_rhythm(bass_rhythm)
		rhythm_model.add_temporal(bass_id)

		pitch_model.add_temporal(pitch_contours[f])
		# Read Drum files
		#
		drum_midi = madmom.utils.midi.MIDIFile.from_file(match_file)
		drum_midi.note_time_unit = 'b'
		# Filter kick notes
		onset_kick = []
		kick = 36
		for event in drum_midi.notes:
			#print event
			if int(event[1]) == kick:
				onset_kick.append(event[0])
		# Quantize
		kick_rhythm = quantize_pattern(onset_kick)
		#print kick_rhythm
		# Translate
		kick_id = translate_rhythm(kick_rhythm)
		kick_patterns.append(kick_id)
		# Update interlocking model
		rhythm_model.add_interlocking(kick_id, bass_id)

		# Update file counter
		file_it += 1

	return rhythm_model, kick_patterns, pitch_model

