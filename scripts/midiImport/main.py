from importMidi import *
import glob
import os
import json

crawledFolder = "../../pythonWrap/test/midi/*.mid"
outFolder = "../../pythonWrap/test/slicedMidi/"

customNoteMapping = {
	"Kick":[36]
	,"Snare":[(38,'*')]
	,"ClosedHH":[42,43]
	,"OpenHH":46
	,"Clap":48
	,"Rimshot":49 # also reffered as sidestick
	,"LowConga":51
	,"HiConga":45

# combination
	# "lowFrequencies" :[33,34,35,36,63]

}


desiredPatternLength = 4;

def splitInequalLengthPatterns(pattern,desiredLength):
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
	
	splitted = splitInequalLengthPatterns(res,desiredPatternLength)

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
		
	


	
