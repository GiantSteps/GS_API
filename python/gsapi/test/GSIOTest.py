# python 3 compatibility
from __future__ import absolute_import, division, print_function

import unittest
import os,sys

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))
    from GSPatternTestUtils import *
else:
    from .GSPatternTestUtils import *
from gsapi import *
import random,glob





class GSIOTest(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="*.mid",
                         midiFolder=self.getLocalCorpusPath('drums'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_ImportExportMidi(self):
        for p in self.cachedDataset:
            print(p.name)
            self.assertTrue(len(p.events)>0)
            exportedPath = GSIO.toMidi(p,folderPath="../../sandbox/midi/",name=p.name)
            exportedPath =os.path.abspath(exportedPath)
            self.assertTrue(os.path.exists(exportedPath))
            exportedP = GSIO.fromMidi(midiPath=exportedPath)

            self.checkPatternEquals(p,exportedP,tolerance = 0.02) # we have roundings error when converting to beats back and forth...

    def test_ImportExportJSON(self):
        for p in self.cachedDataset:
            exportedPath = GSIO.toJSONFile(p,folderPath="../../sandbox/json/",useTagIndexing=False,conserveTuple=False)
            jsonPattern = GSIO.fromJSONFile(filePath=os.path.abspath(exportedPath),conserveTuple=False)
            self.checkPatternEquals(p,jsonPattern,checkViewpoints=False)

    def test_ImportExportJSONTuplesAndViewpoints(self):
        # chords descriptor return tuple so save it in json
        for p in self.cachedDataset:
            for name,descriptorClass in getAllDescriptorsClasses():
                p.generateViewpoint(name,descriptorClass(),sliceType=4)
            
            exportedPath = GSIO.toJSONFile(p,folderPath="../../sandbox/json/",useTagIndexing=False,conserveTuple=True)
            self.assertTrue(os.path.exists(exportedPath))
            jsonPattern = GSIO.fromJSONFile(filePath=os.path.abspath(exportedPath),conserveTuple=True)
            self.checkPatternEquals(p,jsonPattern,checkViewpoints=True)


    def test_ImportExportPickle(self):
        for p in self.cachedDataset:
            for name,descriptorClass in getAllDescriptorsClasses():
                p.generateViewpoint(name,descriptorClass(),sliceType=4)
            

            exportedPath = GSIO.toPickleFile(p,folderPath="../../sandbox/pickle/")
            self.assertTrue(os.path.exists(exportedPath))
            picklePattern = GSIO.fromPickleFile(filePath=os.path.abspath(exportedPath))

            self.checkPatternEquals(p,picklePattern,checkViewpoints = True)

if __name__ == '__main__':
    runTest(profile=False, getStat=False)


