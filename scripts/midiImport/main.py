from importMidi import *
import glob
import os
import json

crawledFolder = "../../pythonWrap/test/midi/*.mid"
outFolder = "../../pythonWrap/test/slicedMidi/"

customNoteMapping = {
		"Kick":36,
		"Rimshot":37,
		"Snare":38,
		"Clap":39,
		"Clave":40,
		"LowTom":41,
		"ClosedHH":42,
		"MidTom":43,
		"Shake":44,
		"HiTom":45,
		"OpenHH":46,
		"LowConga":47,
		"HiConga":48,
		"Cymbal":49,
		"Conga":50,
		"CowBell":51
		
		
		

# combination
	# "lowFrequencies" :[33,34,35,36,63]

}


desiredPatternLength = 4;

def splitInEqualLengthPatterns(pattern,desiredLength):
	patterns = {}
	for e in pattern['eventList']:
		p = int(e["on"]/desiredLength);
		numPattern = str(p)
		if numPattern not in patterns:
			patterns[numPattern] = {}
			patterns[numPattern]['timeInfo'] = pattern['timeInfo'];
			patterns[numPattern]["timeInfo"]["length"] = desiredLength;
			patterns[numPattern]["eventTags"] = pattern['eventTags'];
			patterns[numPattern]['eventList'] = []
		e['on']-=p*desiredLength;
		patterns[numPattern]['eventList']+=[e];



	return patterns

for f in glob.glob(crawledFolder):
	name =  os.path.basename(f)[:-4]
	print "getting "+name
	res =  getPatterns(f,False,customNoteMapping);
	
	splitted = splitInEqualLengthPatterns(res,desiredPatternLength)

	indx = 0;
	needIndexing = len(splitted)>1
	for s in splitted:
		splitted[s]["metadata"] = {"name":name,"idx":indx}
		suffix = ""
		if needIndexing:
			suffix = "_"+s;

		outFilePath = os.path.join(outFolder,name)+suffix+".json"
		with open(outFilePath,'w') as outFile:
			json.dump(splitted[s],outFile)
		indx+=1
		
	


	
