from importMidi import *
import glob
import os
import json

crawledFolder = "/Users/mhermant/Documents/Work/MTGDrive/MaschineScript/renamed/*mid"
outFolder = "/Users/mhermant/Documents/Work/Dev/GS_API/sandBox/testMartin/jsonOut/"

customNoteMapping = {
	"Kick":[33,34,35,36]
	,"Snare":[(38,'*'),  40]
	,"ClosedHH":[42,43]
	,"OpenHH":44
	,"Clap":(39,10)
	,"Rimshot":37 # also reffered as sidestick
	,"LowConga":64
	,"HiConga":63,

# combination
	"lowFrequencies" :[33,34,35,36,63]

}


desiredPatternLength = 4;

for f in glob.glob(crawledFolder):
	name =  os.path.basename(f)[:-4]
	print "getting "+name
	res =  getPatterns(f,True);
	print res

	res["metadata"] = {"name":name}


	outFilePath = os.path.join(outFolder,name)+".json"
	with open(outFilePath,'w') as outFile:
		json.dump(res,outFile)
	
	


	
