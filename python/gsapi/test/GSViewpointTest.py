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

    def test_viewpoint(self):
        for midiPattern in self.cachedDataset:
            print "\n"+ midiPattern.name
            patternList = midiPattern.splitInEqualLengthPatterns(4, makeCopy=False)
            for p in patternList:
                print p.startTime
                p.generateViewpoint("chords")
                self.checkPatternValid(p, msg='chordviewPoint failed')
                for e in p.viewpoints["chords"].events:
                    print e


if __name__ == '__main__':
    runTest(profile=True, getStat=False)


