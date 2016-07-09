import glob
import os


import gsapi
import math
from gsapi import *




def fromMidi(midiPath,NoteToTagsMap,tracksToGet = [],TagsFromTrackNameEvents=False,filterOutNotMapped=True):
	""" loads a midi file as a pattern

	Args:
		midiPath: midi filePath
		NoteToTagsMap: dictionary converting pitches to tags 
			noteMapping maps classes to a list of possible Mappings, a mapping can be:
			a tuple of (note, channel) if one of those doesnt matter it canbe replaced by '*' character
			an integer if only pitch matters
			for simplicity one can pass only one integer (i.e not a list) for one to one mappings
			if midi track contain the name of one element of mapping, it'll be choosed without anyother consideration

		TagsFromTrackNameEvents: use only track names to resolve mapping, useful for midi containing named tracks
		filterOutNotMapped: if set to true, don't add event not represented by `NoteToTagsMap`
		tracksToGet: if not empty, specifies tracks wanted either by name or index
	"""
	def formatNoteToTags(NoteToTags):
		for n in NoteToTags:
			if not isinstance(NoteToTags[n],list): NoteToTags[n] = [NoteToTags[n]]
			for i in range(len(NoteToTags[n])):
				if isinstance(NoteToTags[n][i],int):NoteToTags[n][i] = (NoteToTags[n][i],'*')

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
			for le in noteMapping[l]:
				if (le[0] in {'*',pitch}) and (le[1] in {'*',channel}): res+=[l]; 
			
		return res

	import midi
	import os
	globalMidi = midi.read_midifile(midiPath)
	globalMidi.make_ticks_abs();
	pattern = GSPattern();
	pattern.name = os.path.splitext(os.path.basename(midiPath))[0];

	formatNoteToTags(NoteToTagsMap)

	# first get signature
	findTimeInfoFromMidi(pattern,globalMidi);

	tick2quarterNote = 1.0/(globalMidi.resolution) ;

	pattern.events=[]
	lastNoteOff = 0;
	lastPitch = -1;
	lastTick = -1;
	notFoundTags = []
	trackIdx = 0;
	for tracks in globalMidi:
		shouldSkipTrack = False;
		for e in tracks:
			if(shouldSkipTrack):continue
			
			noteTags = []
			
			if midi.MetaEvent.is_event(e.statusmsg):
				if e.metacommand==midi.TrackNameEvent.metacommand:
					if tracksToGet!=[] and not((e.text in tracksToGet) or (trackIdx in tracksToGet)): 
						print 'skipping track :',trackIdx,e.text;
						shouldSkipTrack = True;
						continue ;
					else: 
						print 'getting track :',trackIdx,e.text

					if TagsFromTrackNameEvents : noteTags = findTagsFromName(e.text,NoteToTagsMap)

			isNoteOn = midi.NoteOnEvent.is_event(e.statusmsg)
			isNoteOff =midi.NoteOffEvent.is_event(e.statusmsg);
			if(isNoteOn or isNoteOff  ):
				pitch = e.pitch # optimize pitch property access
				tick = e.tick
				if noteTags == []:
					if TagsFromTrackNameEvents:continue
					noteTags = findTagsFromPitchAndChannel(pitch,e.channel,NoteToTagsMap)

				if noteTags ==[] :
					if ([e.channel,pitch] not in notFoundTags):
						print "no tags found for pitch %d on channel %d"%(pitch,e.channel)
						notFoundTags+=[[e.channel,pitch]]
					if filterOutNotMapped:
						continue;



				if isNoteOn:
					# ignore duplicated events (can't have 2 simultaneous NoteOn for the same pitch)
					if  pitch == lastPitch and tick == lastTick:
						# print 'skip duplicated event :', pitch,tick
						continue;
					lastPitch = pitch
					lastTick = tick
					pattern.events+=[GSPatternEvent(tick*tick2quarterNote,-1,pitch,e.velocity,noteTags)]

					
					
				
				if isNoteOn or isNoteOff:
					foundNoteOn = False
					for i in reversed(pattern.events):
						
						if (i.pitch == pitch) and (i.tags==noteTags) and tick*tick2quarterNote >= i.startTime and i.duration<0:
							foundNoteOn = True
							i.duration = max(0.001,tick*tick2quarterNote - i.startTime)
							lastNoteOff = max(e.tick*tick2quarterNote,lastNoteOff);
							break;
					# if not foundNoteOn and midi.NoteOffEvent.is_event(e.statusmsg):
						# print "not found note on "+str(e)+str(pattern.events[-1])
						# exit()
		trackIdx+=1



	elementSize = 4.0/pattern.timeSignature[1]
	barSize = pattern.timeSignature[0]*elementSize;
	lastBarPos = math.ceil(lastNoteOff*1.0/barSize)*barSize;
	pattern.duration = lastBarPos

	return pattern





def fromMidiCollection(midiGlobPath,NoteToTagsMap,tracksToGet = [],TagsFromTrackNameEvents=False,filterOutNotMapped = True,desiredLength = 0):
	""" loads a midi collection

	Args:
		midiGlobPath: midi filePath in glob naming convention (e.g '/folder/To/Crawl/*.mid')
		desiredLength: optionally cut patterns in equal length
		otherArguments: are defined in :py:func:`fromMidi`
	Returns:
		a list of GSPattern build from Midi folder
	"""


	res = []
	print glob.glob(midiGlobPath)
	for f in glob.glob(midiGlobPath):
		name =  os.path.splitext(os.path.basename(f))[0]
		print "getting "+name
		p = fromMidi(f,NoteToTagsMap,TagsFromTrackNameEvents=TagsFromTrackNameEvents,filterOutNotMapped =filterOutNotMapped);
		
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

