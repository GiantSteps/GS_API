import unittest
import os
import sys

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))

from gsapi import *
import random,glob
from GSPatternTestUtils import *




class GSIOTest(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="*.mid",
                         midiFolder=self.getLocalCorpusPath('harmony'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_ImportExportMidi(self):
        for p in self.cachedDataset:

            exportedPath = GSIO.toMidi(p,folderPath="../../sandbox/midi/",name=p.name)
            exportedP = GSIO.fromMidi(midiPath=os.path.abspath(exportedPath))

            self.checkPatternEquals(p,exportedP)

    def test_ImportExportJSON(self):
        for p in self.cachedDataset:
            p.generateViewpoint("chords")

            exportedPath = GSIO.toJSONFile(p,folderPath="../../sandbox/json/")
            jsonPattern = GSIO.fromJSONFile(filePath=os.path.abspath(exportedPath))

            self.checkPatternEquals(p,jsonPattern)

  

if __name__ == '__main__':
    runTest(profile=True, getStat=False)


