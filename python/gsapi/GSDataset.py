import os
import random
import GSIO,GSPatternUtils

import logging
datasetLog = logging.getLogger("gsapi.GSDataset")



class GSDataset(object):
    """
    Helper to hold a list of patterns imported from specific gpath (glob style)
    TODO documentation
    """

    defaultMidiFolder = os.path.abspath(__file__ + "../../../../corpus/drums/")
    defaultMidiGlob = "*.mid"

    def __init__(self,
                 midiFolder=defaultMidiFolder,
                 midiGlob=defaultMidiGlob,
                 midiMap=GSPatternUtils.simpleDrumMap,
                 checkForOverlapped=True):

        self.midiFolder = midiFolder
        self.midiMap = midiMap
        self.checkForOverlapped = checkForOverlapped
        self.setMidiGlob(midiGlob)
        self.importMIDI()


    def setMidiGlob(self, globPattern):

        import glob
        if '.mid' in globPattern[-4:]:
            globPattern = globPattern[:-4]
        self.midiGlob = globPattern + '.mid'
        self.globPath = os.path.abspath(os.path.join(self.midiFolder,
                                                     self.midiGlob))
        self.files = glob.glob(self.globPath)
        if  len(self.files) == 0:
            datasetLog.error("no files found for path: " + self.globPath)
        else:
            self.idx = random.randint(0, len(self.files) - 1)


    def getAllSliceOfDuration(self, desiredDuration):
        res = []
        for p in self.patterns:
            res += p.splitInEqualLengthPatterns(desiredLength=desiredDuration)
        return res


    def importMIDI(self, fileName=""):

        if fileName:
            self.setMidiGlob(fileName)

        self.patterns = []

        for p in self.files:
            datasetLog.info('using ' + p)
            p = GSIO.fromMidi(p,
                              self.midiMap,
                              tracksToGet=[],
                              checkForOverlapped=self.checkForOverlapped)
            self.patterns += [p]

        return self.patterns
    def __getitem__(self, index):
    	"""Utility to access paterns as list member : GSDataset[idx] = GSDataset.patterns[idx]
    	"""
    	return self.patterns[index]


