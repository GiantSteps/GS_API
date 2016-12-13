import unittest
import os
import sys

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))

from gsapi import *
import random,glob
from GSPatternTestUtils import *


class GSPatternTest(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="*.mid",
                         midiFolder=self.getLocalCorpusPath('midiTests'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_ImportExport(self):
        for p in self.cachedDataset:

            exportedPath = GSIO.toMidi(p,path="../../sandbox/midi/",name=p.name)
            exportedP = GSIO.fromMidi(midiPath=os.path.abspath(exportedPath))

            print p.events[62].duration,exportedP.events[62].duration
            self.assertEqual(p.events,exportedP.events)
            self.assertEqual(p,exportedP)

  

if __name__ == '__main__':
    runTest(profile=True, getStat=False)


