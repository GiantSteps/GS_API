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
        return GSDataset(midiGlob="funkyfresh.mid",
                         midiFolder=self.getLocalCorpusPath('midiTests'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_viewpoint(self):
        patternList = self.cachedDataset[0].splitInEqualLengthPatterns(4, makeCopy=False)
        for p in patternList:
            p.generateViewpoint("chord")
            self.checkPatternValid(p, msg='chordviewPoint failed')


if __name__ == '__main__':
    runTest(profile=True, getStat=False)


