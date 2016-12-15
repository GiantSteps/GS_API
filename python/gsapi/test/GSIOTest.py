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

    # def test_ImportExportJSON(self):
    #     for p in self.cachedDataset:
    #         exportedPath = GSIO.toJSONFile(p,folderPath="../../sandbox/json/",useTagIndexing=False,conserveTuple=False)
    #         jsonPattern = GSIO.fromJSONFile(filePath=os.path.abspath(exportedPath),conserveTuple=False)
    #         self.checkPatternEquals(p,jsonPattern,checkViewpoints=False)

    def test_ImportExportJSONTuplesAndViewpoints(self):
        # chords descriptor return tuple so save it in json
        for p in self.cachedDataset:
            for name,descriptorClass in getAllDescriptorsClasses():
                p.generateViewpoint(name,descriptorClass(),sliceType=4)
            
            exportedPath = GSIO.toJSONFile(p,folderPath="../../sandbox/json/",useTagIndexing=False,conserveTuple=True)
            jsonPattern = GSIO.fromJSONFile(filePath=os.path.abspath(exportedPath),conserveTuple=True)
            self.checkPatternEquals(p,jsonPattern,checkViewpoints=True)


    def test_ImportExportPickle(self):
        for p in self.cachedDataset:
            for name,descriptorClass in getAllDescriptorsClasses():
                p.generateViewpoint(name,descriptorClass(),sliceType=4)
            

            exportedPath = GSIO.toPickleFile(p,folderPath="../../sandbox/pickle/")
            picklePattern = GSIO.fromPickleFile(filePath=os.path.abspath(exportedPath))

            self.checkPatternEquals(p,picklePattern,checkViewpoints = True)

if __name__ == '__main__':
    runTest(profile=True, getStat=False)


