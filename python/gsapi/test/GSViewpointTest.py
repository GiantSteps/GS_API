import unittest
import os
import sys

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))

from gsapi import *
import random,glob
from GSPatternTestUtils import *


class GSViewpointTest(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="*.mid",
                         midiFolder=self.getLocalCorpusPath('harmony'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_viewpoint_defaults(self):
        for midiPattern in self.cachedDataset:
            print "\n"+ midiPattern.name
            # checking default implementation
            midiPattern.generateViewpoint("chords")
            self.checkPatternValid(midiPattern, msg='chordviewPoint failed')
            for e in midiPattern.viewpoints["chords"].events:
                print e
            

    def test_viewpoint_custom(self):


        def _testAndPrint(descriptor,sliceType):
            print "\n"+ midiPattern.name
            # checking default implementation
            midiPattern.generateViewpoint("chords",descriptor=descriptor,sliceType=sliceType)
            self.checkPatternValid(midiPattern, msg='chordviewPoint failed')
            for e in midiPattern.viewpoints["chords"].events:
                print e


        def _testDescriptor(descriptor):
            _testAndPrint(descriptor = descriptor,sliceType="perEvent")
            _testAndPrint(descriptor = descriptor,sliceType="all")
            _testAndPrint(descriptor = descriptor,sliceType=1)
            _testAndPrint(descriptor = descriptor,sliceType=4)

        for midiPattern in self.cachedDataset:
            for descriptor in getAllDescriptors():
                _testDescriptor(GSDescriptors.GSDescriptorChord());
                _testDescriptor(GSDescriptors.GSDescriptorDensity());
            

def getAllDescriptors():
    res = []
    for elem in dir(GSDescriptors):
        if not '__' in elem and (not 'GSBase' in elem):
            res+=[ elem]
    return res
    
if __name__ == '__main__':
    print getAllDescriptors()
    runTest(profile=True, getStat=False)


