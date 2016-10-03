import glob
import os


import gsapi
import math
from gsapi import *




defaultPitchNames = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
generalMidiMap = {"Acoustic Bass Drum":35,"Bass Drum 1":36,"Side Stick":37,"Acoustic Snare":38,"Hand Clap":39,"Electric Snare":40,"Low Floor Tom":41,"Closed Hi Hat":42,"High Floor Tom":43,"Pedal Hi-Hat":44,"Low Tom":45,"Open Hi-Hat":46,"Low-Mid Tom":47,"Hi-Mid Tom":48,"Crash Cymbal 1":49,"High Tom":50,"Ride Cymbal 1":51,"Chinese Cymbal":52,"Ride Bell":53,"Tambourine":54,"Splash Cymbal":55,"Cowbell":56,"Crash Cymbal 2":57,"Vibraslap":58,"Ride Cymbal 2":59,"Hi Bongo":60,"Low Bongo":61,"Mute Hi Conga":62,"Open Hi Conga":63,"Low Conga":64,"High Timbale":65,"Low Timbale":66,"High Agogo":67,"Low Agogo":68,"Cabasa":69,"Maracas":70,"Short Whistle":71,"Long Whistle":72,"Short Guiro":73,"Long Guiro":74,"Claves":75,"Hi Wood Block":76,"Low Wood Block":77,"Mute Cuica":78,"Open Cuica":79,"Mute Triangle":80,"Open Triangle":81}
def __formatNoteToTags(_NoteToTags):
	""" internal conversion for consistent NoteTagMap Structure

	"""
	import copy
	NoteToTags = copy.copy(_NoteToTags) 
	if(NoteToTags == "pitchNames"):
		NoteToTags = {"pitchNames":""}
	for n in NoteToTags:
		if n=="pitchNames":
			if not NoteToTags["pitchNames"]:
				NoteToTags["pitchNames"] = defaultPitchNames
		else:	
			if not isinstance(NoteToTags[n],list): NoteToTags[n] = [NoteToTags[n]]
			for i in range(len(NoteToTags[n])):
				if isinstance(NoteToTags[n][i],int):NoteToTags[n][i] = (NoteToTags[n][i],'*')
	return NoteToTags

def __fromMidiFormatted(midiPath,NoteToTagsMap,tracksToGet = [],TagsFromTrackNameEvents=False,filterOutNotMapped=True):
	""" internal function that accept only Consistent NoteTagMap structure as created by __formatNoteToTags
	"""
	def findTimeInfoFromMidi(pattern,midiFile):
		
		foundTimeSignatureEvent = False
		foundTempo = False
		for tracks in midiFile:
			for e in tracks:
				if midi.MetaEvent.is_event(e.statusmsg):
					if e.metacommand == midi.TimeSignatureEvent.metacommand :
						if foundTimeSignatureEvent: print "multiple time signature found, not supported, result can be alterated" 
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
		def pitchToName(pitch,pitchNames):
			octaveLength = len(pitchNames);
			octave  = (pitch/octaveLength) - 2; # 0 is C-2
			note = pitch%octaveLength
			return  pitchNames[note]+"_"+str(octave)

		if "pitchNames" in noteMapping.keys():
			return [pitchToName(pitch,noteMapping["pitchNames"])]
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

	

	# first get signature
	findTimeInfoFromMidi(pattern,globalMidi);

	tickToQNote = 1.0/(globalMidi.resolution) ;

	pattern.events=[]
	lastNoteOff = 0;
	notFoundTags = []
	trackIdx = 0;
	for tracks in globalMidi:
		shouldSkipTrack = False;
		lastPitch = -1;
		lastTick = -1;
		for e in tracks:
			if(shouldSkipTrack):continue
			
			if not TagsFromTrackNameEvents : noteTags = []
			
			if midi.MetaEvent.is_event(e.statusmsg):
				if e.metacommand==midi.TrackNameEvent.metacommand:
					if tracksToGet!=[] and not((e.text in tracksToGet) or (trackIdx in tracksToGet)): 
						print 'skipping track :',trackIdx,e.text;
						shouldSkipTrack = True;
						continue ;
					else: 
						print 'getting track :',trackIdx,e.text

					if TagsFromTrackNameEvents :
						noteTags = findTagsFromName(e.text,NoteToTagsMap)


			isNoteOn = midi.NoteOnEvent.is_event(e.statusmsg)
			isNoteOff =midi.NoteOffEvent.is_event(e.statusmsg);
			if(isNoteOn or isNoteOff  ):

				pitch = e.pitch # optimize pitch property access
				tick = e.tick
				curBeat = tick*1.0*tickToQNote
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
						print 'skip duplicated event :', pitch,tick
						continue;
					lastPitch = pitch
					lastTick = tick
					# print "on"+str(pitch)+":"+str( tick*1.0*tickToQNote)
					pattern.events+=[GSPatternEvent(startTime=curBeat,duration=-1,pitch=pitch,velocity=127,tags=noteTags)]


					
					
				
				if isNoteOn or isNoteOff:
					# print "off"+str(pitch)+":"+str( tick*1.0*tickToQNote)
					foundNoteOn = False
					for i in reversed(pattern.events):
						
						if (i.pitch == pitch) and (i.tags==noteTags) and curBeat >= i.startTime and i.duration<=0.0001:
							foundNoteOn = True

							i.duration = max(0.0001,curBeat - i.startTime)
							lastNoteOff = max(curBeat,lastNoteOff);
							# print "set duration "+str(i.duration) + "at start " + str(i.startTime)
							break;
					if not foundNoteOn and midi.NoteOffEvent.is_event(e.statusmsg):
						print "not found note on "+str(e)+str(pattern.events[-1])
						
		trackIdx+=1



	elementSize = 4.0/pattern.timeSignature[1]
	barSize = pattern.timeSignature[0]*elementSize;
	lastBarPos = math.ceil(lastNoteOff*1.0/barSize)*barSize;
	pattern.duration = lastBarPos
	pattern.name = os.path.basename(midiPath)

	return pattern




def fromMidi(midiPath,NoteToTagsMap,tracksToGet = [],TagsFromTrackNameEvents=False,filterOutNotMapped=True):
	""" loads a midi file as a pattern

	Args:
		midiPath: midi filePath
		NoteToTagsMap: dictionary converting pitches to tags 
			if only interssed by pitch, you can specify it to "pitchNames", and optionaly set the value to the list of string for pitches from C
			noteMapping maps classes to a list of possible Mappings, a mapping can be:
			a tuple of (note, channel) if one of those doesnt matter it canbe replaced by '*' character
			an integer if only pitch matters
			for simplicity one can pass only one integer (i.e not a list) for one to one mappings
			if midi track contain the name of one element of mapping, it'll be choosed without anyother consideration

		TagsFromTrackNameEvents: use only track names to resolve mapping, useful for midi containing named tracks
		filterOutNotMapped: if set to true, don't add event not represented by `NoteToTagsMap`
		tracksToGet: if not empty, specifies tracks wanted either by name or index
	"""
	_NoteToTagsMap=__formatNoteToTags(NoteToTagsMap)
	return __fromMidiFormatted(midiPath=midiPath,NoteToTagsMap=_NoteToTagsMap,tracksToGet = tracksToGet,TagsFromTrackNameEvents=TagsFromTrackNameEvents,filterOutNotMapped=filterOutNotMapped)



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
	_NoteToTagsMap = __formatNoteToTags(NoteToTagsMap)
	print glob.glob(midiGlobPath)
	for f in glob.glob(midiGlobPath):
		name =  os.path.splitext(os.path.basename(f))[0]
		print "getting "+name
		p = fromMidi(f,_NoteToTagsMap,TagsFromTrackNameEvents=TagsFromTrackNameEvents,filterOutNotMapped =filterOutNotMapped);
		
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

