import midi
import math
import copy


'''
the function getPattern take a noteMapping to resolve midi to class entities
noteMapping maps classes to a list of possible Mappings, a mapping can be:
	a tuple of (note, channel) if one of those doesnt matter it canbe replaced by '*' character
	an integer if only pitch matters

for simplicity one can pass only one integer (i.e not a list) for one to one mappings
if midi track contain the name of one element of mapping, it'll be choosed without anyother consideration



'''

# this default mapping is a subset of GM drums mapping
defaultNoteMapping = {
	"Kick":[(33,10),(34,10),(35,10),(36,10)]
	,"Snare":[(38,'*'),40]
	,"ClosedHH":[42,43]
	,"OpenHH":46
	,"Clap":39
	,"Rimshot":37 # also reffered as sidestick
	,"LowConga":64
	,"HiConga":63

}


defaultTimeInfo = {
	"BPM":60,
	"timeSignature":[4,4],
	"loopLength":0, # has to be provided
}

'''
arguments :
f : filePath
searchOnlyTrackNameEvent : if multiple MIDI tracks are provided with names that we want to retrieve
			it forbids pitch/channel based retrievals as they are not representative
'''

def getPatterns(f,searchOnlyTrackNameEvent=False,noteMapping = defaultNoteMapping,timeInfo = defaultTimeInfo):
	globalMidi = midi.read_midifile(f)
	globalMidi.make_ticks_abs();
	res = {}

# first get signature
	res["timeInfo"] = findTimeInfoFromMidi(globalMidi,timeInfo);
	res["eventTags"] = [k for k in noteMapping]

	
		
	tick2quarterNote = 1.0/(globalMidi.resolution) ;

	res["eventList"]=[]
	lastNoteOff = 0;
	for tracks in globalMidi:
		patternLength = 0	
		
		
		for e in tracks:
			noteType = []
			
			if midi.MetaEvent.is_event(e.statusmsg):
				if e.metacommand==midi.TrackNameEvent.metacommand:
					noteType = findTypesFromName(e.text,noteMapping)

			if(midi.NoteOnEvent.is_event(e.statusmsg) or midi.NoteOffEvent.is_event(e.statusmsg) ):
				if noteType == []:
					if searchOnlyTrackNameEvent:
						continue
					noteType = findTypesFromPithchAndChannel(e.pitch,e.channel,noteMapping)
				if noteType ==[]:
					print "not processed "+str(e.channel) +" "+str(e.pitch)
					continue;

				
				if midi.NoteOnEvent.is_event(e.statusmsg):
					
					res["eventList"]+=[{
					"tagsIdx":noteType
					,"on": e.tick*tick2quarterNote
					,"velocity":e.velocity
					,"pitch":e.pitch,"duration":-1}]
					
				# we forbid overlapping of two consecutive note of the same pitch
				if midi.NoteOnEvent.is_event(e.statusmsg) or midi.NoteOffEvent.is_event(e.statusmsg):
					foundNoteOn = False
					
					for i in reversed(res["eventList"]):
						
						if (i["pitch"] == e.pitch) and (i["tagsIdx"]==noteType) and e.tick*tick2quarterNote > i["on"] and i["duration"]<0:
							foundNoteOn = True
							duration = e.tick*tick2quarterNote - i["on"]
							i["duration"]= duration
							lastNoteOff = max(e.tick*tick2quarterNote,lastNoteOff);
							break;
					if not foundNoteOn and midi.NoteOffEvent.is_event(e.statusmsg):
						print "not found note on "+str(e)+str(res["eventList"][-1])
						# exit()
					


	for e in res['eventList']:
		if e['on']<=0:
			print 'midi file not valid'
			exit();
	elementSize = 4.0/res["timeInfo"]["timeSignature"][1]
	barSize = res["timeInfo"]["timeSignature"][0]*elementSize;
	lastBarPos = math.ceil(lastNoteOff*1.0/barSize)*barSize;
	res["timeInfo"]["length"] = lastBarPos

	

	return res



def findTimeInfoFromMidi(gl,defaultTimeInfo):
	res = defaultTimeInfo;
	foundTimeSignatureEvent = False
	foundTempo = False
	for ee in gl:
		for e in ee:
			if midi.MetaEvent.is_event(e.statusmsg):
				if e.metacommand == midi.TimeSignatureEvent.metacommand :
					if foundTimeSignatureEvent:
						print "multiple time signature found, not supported"
						exit(-1)

					foundTimeSignatureEvent = True;
					res["timeSignature"] = [e.numerator, e.denominator]
					#  e.metronome = e.thirtyseconds ::  do we need that ???
				elif e.metacommand == midi.SetTempoEvent.metacommand :
					if foundTempo:
						print "multiple bpm found, not supported"
						exit(-1)

					foundTempo = True;
					res["BPM"] = e.bpm



		if foundTimeSignatureEvent:
			break;

	if not foundTimeSignatureEvent:
		print "no time event found"
	return res


def findTypesFromName(name,noteMapping):
	res =[]
	idx =0;
	for l in noteMapping:
		if l in name:
			res+=[idx] 	
		idx+=1;
	return res

def findTypesFromPithchAndChannel(pitch,channel,noteMapping):
	res = []
	idx =0;
	
	for l in noteMapping:

		cMap = noteMapping[l]
		listToCheck  = []
		if isinstance(cMap,int) or isinstance(cMap,tuple):
			listToCheck = [cMap]
		elif isinstance(cMap,list):
			listToCheck = cMap;
		else:

			print "wrongMapping : "+str(cMap)
		
		for le in listToCheck:
			if isinstance(le, int):
				if le == pitch:
					res+=[idx]
					continue
			elif isinstance(le, tuple):
				if le[0] in {'*',pitch} and le[1] in {'*',channel}:
					res+=[idx]
					continue
		idx+=1;
	
	return res










	
