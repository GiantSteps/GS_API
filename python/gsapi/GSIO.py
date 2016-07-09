import glob
import os


import gsapi
import math
from gsapi import *




def fromMidi(midiPath,NoteToTagsMap,TagsFromTrackNameEvents=False):
	""" loads a midi file as a pattern

	Args:
		midiPath: midi filePath
		NoteToTagsMap: dictionary converting pitches to tags 
			noteMapping maps classes to a list of possible Mappings, a mapping can be:
			a tuple of (note, channel) if one of those doesnt matter it canbe replaced by '*' character
			an integer if only pitch matters
			for simplicity one can pass only one integer (i.e not a list) for one to one mappings
			if midi track contain the name of one element of mapping, it'll be choosed without anyother consideration

		TagsFromTrackNameEvents: use only track names to resolve mapping, useful for midi contained named tracks
	"""

	def findTimeInfoFromMidi(pattern,midiFile):
		
		foundTimeSignatureEvent = False
		foundTempo = False
		for tracks in midiFile:
			for e in tracks:
				if midi.MetaEvent.is_event(e.statusmsg):
					if e.metacommand == midi.TimeSignatureEvent.metacommand :
						if foundTimeSignatureEvent: print "multiple time signature found, not supported" ; exit(-1)
						foundTimeSignatureEvent = True;
						pattern.timeSignature = [e.numerator, e.denominator]
						#  e.metronome = e.thirtyseconds ::  do we need that ???
					elif e.metacommand == midi.SetTempoEvent.metacommand :
						if foundTempo: print "multiple bpm found, not supported"; exit(-1)
						foundTempo = True;
						pattern.bpm = e.bpm

			if foundTimeSignatureEvent: break;
		if not foundTimeSignatureEvent: print "no time event found"
		


	def findTagsFromName(name,noteMapping):
		res =[]
		for l in noteMapping:
			if l in name: res+=[l];
		return res

	def findTagsFromPitchAndChannel(pitch,channel,noteMapping):
		res = [];
		for l in noteMapping:
			cMap = noteMapping[l] ; listToCheck  = []

			if isinstance(cMap,int) or isinstance(cMap,tuple): listToCheck = [cMap]
			elif isinstance(cMap,list): listToCheck = cMap;
			else: print "wrongMapping : "+str(cMap)
			
			for le in listToCheck:
				if isinstance(le, int) and ( le == pitch): res+=[l]; continue;
				elif isinstance(le, tuple) and le[0] in {'*',pitch} and le[1] in {'*',channel}: res+=[l]; continue;
			
		return res

	import midi
	import os
	globalMidi = midi.read_midifile(midiPath)
	globalMidi.make_ticks_abs();
	pattern = GSPattern();
	pattern.name = os.path.splitext(os.path.basename(midiPath))[0];


	# first get signature
	findTimeInfoFromMidi(pattern,globalMidi);

	tick2quarterNote = 1.0/(globalMidi.resolution) ;

	pattern.events=[]
	lastNoteOff = 0;

	notFoundTags = []
	for tracks in globalMidi:
		for e in tracks:
			noteTags = []
			
			if midi.MetaEvent.is_event(e.statusmsg):
				if e.metacommand==midi.TrackNameEvent.metacommand:
					noteTags = findTagsFromName(e.text,NoteToTagsMap)

			if(midi.NoteOnEvent.is_event(e.statusmsg) or midi.NoteOffEvent.is_event(e.statusmsg) ):
				if noteTags == []:
					if TagsFromTrackNameEvents:
						continue
					noteTags = findTagsFromPitchAndChannel(e.pitch,e.channel,NoteToTagsMap)
				if noteTags ==[] and ([e.channel,e.pitch] not in notFoundTags):
					print "no tags found for "+str(e.channel) +" "+str(e.pitch)
					notFoundTags+=[[e.channel,e.pitch]]
					continue;

				
				if midi.NoteOnEvent.is_event(e.statusmsg):
					pattern.events+=[GSPatternEvent(e.tick*tick2quarterNote,-1,e.pitch,e.velocity,noteTags)]
					
					
				# we forbid overlapping of two consecutive note of the same pitch
				if midi.NoteOnEvent.is_event(e.statusmsg) or midi.NoteOffEvent.is_event(e.statusmsg):
					foundNoteOn = False
					
					for i in reversed(pattern.events):
						
						if (i.pitch == e.pitch) and (i.tags==noteTags) and e.tick*tick2quarterNote > i.startTime and i.duration<0:
							foundNoteOn = True
							i.duration = e.tick*tick2quarterNote - i.startTime
							lastNoteOff = max(e.tick*tick2quarterNote,lastNoteOff);
							break;
					# if not foundNoteOn and midi.NoteOffEvent.is_event(e.statusmsg):
						# print "not found note on "+str(e)+str(pattern.events[-1])
						# exit()
					



	for e in pattern.events:
		if e.startTime<0:
			print 'midi file not valid'
			exit();
	elementSize = 4.0/pattern.timeSignature[1]
	barSize = pattern.timeSignature[0]*elementSize;
	lastBarPos = math.ceil(lastNoteOff*1.0/barSize)*barSize;
	pattern.duration = lastBarPos

	return pattern





def fromMidiCollection(midiGlobPath,NoteToTagsMap,TagsFromTrackNameEvents=False,desiredLength = 0):
	""" loads a midi collection

	Args:
		midiGlobPath: midi filePath in glob naming convention (e.g '/folder/To/Crawl/*.mid')
		NoteToTagsMap: dictionary converting pitches to tags  (see :py:func:`gsapi.GSIO.fromMidi` function)
		TagsFromTrackNameEvents: use only track names to resolve mapping, useful for midi contained named tracks
		desiredLength: optionally cut patterns in equal length
	Returns:
		a list of GSPattern build from Midi folder
	"""


	res = []
	print glob.glob(midiGlobPath)
	for f in glob.glob(midiGlobPath):
		name =  os.path.splitext(os.path.basename(f))[0]
		print "getting "+name
		p = fromMidi(f,NoteToTagsMap,TagsFromTrackNameEvents=TagsFromTrackNameEvents);
		
		if desiredLength>0:
			res+= p.splitInEqualLengthPatterns(desiredLength,copy=False);
		else:
			res+=[p];
	return res;





def PatternFromJSONFile(filePath):
	""" load a pattern to internal JSON Format

	Args:
		filePath:filePath where to load it
	"""
	with open(filePath,'r') as f:
		return GSPattern().fromJSONDict(json.load(f))

def PatternToJSONFile(pattern,filePath):
	""" save a pattern to internal JSON Format

	Args:
		filePath:filePath where to save it
	"""
	with open(filePath,'w') as f:
		return json.dump(pattern.toJSONDict(),f)

