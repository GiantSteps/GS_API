
import os,glob,random

from gsapi import * 

import logging
datasetLog = logging.getLogger("GSDataset")

class GSDataset(object):
	"""
	helper to hold a list of patterns imported from specific gpath (glob style)
	

	TODO documentation
	"""
	defaultDrumMidiMap = {"Kick":36,"Rimshot":37,"Snare":38,"Clap":39,"Clave":40,"LowTom":41,"ClosedHH":42,"MidTom":43,"Shake":44,"HiTom":45,"OpenHH":46,"LowConga":47,"HiConga":48,"Cymbal":49,"Conga":50,"CowBell":51}
	defaultMidiFolder = os.path.abspath("../../../test/midiDatasets/")
	defaultMidiGlob = "*/*.mid"

	def __init__(self,midiFolder=defaultMidiFolder,midiGlob=defaultMidiGlob,midiMap = defaultDrumMidiMap,checkForOverlapped=True):
		self.midiFolder = midiFolder;
		self.midiMap = midiMap
		self.checkForOverlapped = checkForOverlapped
		self.setMidiGlob (midiGlob);
		self.importMIDI()
		

	def setMidiGlob(self,globPattern):
		if '.mid' in globPattern[-4:]: globPattern = globPattern[:-4]
		self.midiGlob = globPattern+'.mid'
		self.globPath = os.path.abspath(os.path.join(self.midiFolder,self.midiGlob))
		self.files = glob.glob(self.globPath)
		if  len(self.files) ==0:
			datasetLog.error("no files found for path "+self.globPath)
		else:
			self.idx = random.randint(0,len(self.files)-1)


	def getAllSliceOfDuration(self,desiredDuration):
		res = []
		for p in self.patterns:
			res+=p.splitInEqualLengthPatterns(desiredLength=desiredDuration)
		return res

	def importMIDI(self,fileName=""):
		if(fileName):
			setMidiGlob(fileName)

		self.patterns=[]
		for p in self.files:
			datasetLog.info( 'using ' +p)
			p  = GSIO.fromMidi(p,self.midiMap,tracksToGet=[],checkForOverlapped=self.checkForOverlapped)
			self.patterns+=[p]
		return self.patterns
