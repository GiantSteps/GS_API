# python 3 compatibility
from __future__ import absolute_import, division, print_function

import unittest
import os
import sys

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))
    from GSPatternTestUtils import *
else:
    from .GSPatternTestUtils import *

from gsapi import *
import random,glob


class GSPatternTest(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="funkyfresh.mid",
                         midiFolder=self.getLocalCorpusPath('drums'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_Import(self):
        for p in self.cachedDataset.patterns:
            self.assertTrue(p != None, 'cant import midi file %s' % p.name)
            self.assertTrue(p.duration > 0, 'cant import midi file %s: no duration' % p.name)
            self.assertTrue(p.events != [], 'cant import midi file %s: no events' % p.name)
            self.checkPatternValid(p, msg='import Pattern %s failed' % p.name)
            sliced = p.getPatternForTimeSlice(0, 4)
            self.checkPatternValid(sliced, msg='slicing pattern failed')
            ps = p.splitInEqualLengthPatterns(4, makeCopy=True)
            for p in ps:
                self.checkPatternValid(p, msg='spit in equalLength failed')

    def test_Silences(self):
        for p in self.cachedDataset.patterns:
            pattern1 = p.getFilledWithSilences(perTag=True)
            pattern2 = p.getFilledWithSilences(perTag=False)
            self.checkPatternValid(pattern1,
                                   checkForDoublons=False,
                                   checkOverlap=False,
                                   msg='fill with silence per tag failed')
            self.checkPatternValid(pattern2,
                                   checkForDoublons=False,
                                   checkOverlap=False,
                                   msg='fill with silence failed')

    def test_stretch(self):
        for bp in self.cachedDataset.patterns:
            originPattern = bp.copy()
            p = bp.getPatternForTimeSlice(0, 4)
            p.timeStretch(32/4.0)
            p.alignOnGrid(1)
            # p.removeOverlapped()
            p.fillWithSilences(maxSilenceTime=1)
            p.setDurationFromLastEvent(onlyIfBigger=False)
            self.assertTrue(p.events[-1].startTime == 31)
            self.checkPatternValid(p, msg='stretch failed \n\n%s \n\n%s' % (originPattern, p))

    def test_legato(self):
        patternList = self.cachedDataset[0].splitInEqualLengthPatterns(4, makeCopy=False)
        for p in patternList:
            p.applyLegato()
            self.checkPatternValid(p, msg='legato failed')


if __name__ == '__main__':
    runTest(profile=True, getStat=False)


