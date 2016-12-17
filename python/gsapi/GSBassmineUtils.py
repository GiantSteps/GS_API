import numpy as np
def translate_rhythm(rhythm):
	"""
	Translate binary represented rhythms (from binaryBeatPattern()) to markov variables dictionary.
	Each binarized pattern is presented as it's decimal representation.
	Example: [1,0,1,0] = 10, [0,0,0,1] = 1 and so on

	Args:
	    rhythm: 2D formatted list containing binary representation of pattern. Output from binaryBeatPattern()

	Returns:
	    id: decimal representation of binary onset pattern. This ids are used as dictionary for Markov operations.
	"""
	id = []

	for beat in rhythm:
		id.append((beat[0] * 8) + (beat[1] * 4) + (beat[2] * 2) + beat[3])
	return id




def binaryBeatPattern(pattern, noBeats_bass, resolution=4):
	"""
	Quantize array of note start times to specified resolution
	Loop length is quantized to multiples of whole bars

	Args:
	    pattern: list of start times (in beats)
	    noBeats_bass: number of beats of the sequence
	    resolution: quantization resolution (1/resolution beats). For 1/16 note resoltuion set resolution = 4, for 1/8
	        set resolution= 2, and so on
	Returns:
	    rhythm: 2D list with binary representation of a pattern. Each row is a beat measure (i.e rhythm[n] gives beat 'n' binary representation)

	"""
	# resolution = 4
	# noBeats_bass = uf.numberOfBeats(pattern)  # Bass files length set the global length of analysis
	print( '\n# of beats: ', noBeats_bass)
	# beat_subdiv = np.arange(start=0, step=0.25, stop=(noBeats_bass * RES) - 1)
	subdiv_aux = np.array([0., 0.25, 0.5, 0.75])
	# Matrix to store the binary representation of the midi files
	# Basslines -> 1 matrix
	rhythm = np.zeros((noBeats_bass, resolution), dtype=int)

	for o in pattern:
		# quantize to the closest subdivision
		i, d = divmod(o, 1)  # i = row(beat number) , d = column (beat subdivision)
		d_ = (abs(subdiv_aux - d)).argmin()
		if i < noBeats_bass:
			rhythm[int(i), d_] = 1
	return rhythm