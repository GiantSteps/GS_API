# python 3 compatibility
from __future__ import absolute_import, division, print_function

import unittest
import os
import sys

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))

from gsapi import *
import random,glob
from .GSPatternTestUtils import *


class GSViewpointTest(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="*.mid",
                         midiFolder=self.getLocalCorpusPath('harmony'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_viewpoint_defaults(self):
        for midiPattern in self.cachedDataset:
            print( "\n"+ midiPattern.name)
            # checking default implementation
            midiPattern.generateViewpoint("chords")
            self.checkPatternValid(midiPattern, msg='chordviewPoint failed')
            for e in midiPattern.viewpoints["chords"].events:
                print (e)
            

    def test_viewpoint_allDescriptors_allSliceTypes(self):


        def _testAndPrint(sliceType):
            
            # checking default implementation
            patternBeforeVP = midiPattern.copy()
            midiPattern.generateViewpoint(descriptorName,descriptor=descriptor,sliceType=sliceType)
            self.assertTrue(patternBeforeVP==midiPattern, msg='viewpoint generation modified original pattern failed')
            self.checkPatternValid(midiPattern.viewpoints[descriptorName],checkOverlap=False, msg='generated viewpoint is not a valid pattern %s'%midiPattern.viewpoints[descriptorName])
            # for e in midiPattern.viewpoints["chords"].events:
            #     print e


        def _testDescriptor(name):

            _testAndPrint(sliceType="perEvent")
            _testAndPrint(sliceType="all")
            _testAndPrint(sliceType=1)
            _testAndPrint(sliceType=4)
            _testAndPrint(sliceType=3)

        for midiPattern in self.cachedDataset:

            for descriptorName,descriptorClass in getAllDescriptorsClasses():
                descriptor = descriptorClass()
                _testDescriptor(name=descriptorName);
                
            testLog.info( midiPattern.name+" ok")


    
if __name__ == '__main__':
    print( getAllDescriptors())
    runTest(profile=False, getStat=False)


