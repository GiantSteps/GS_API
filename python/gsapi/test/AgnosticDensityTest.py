# python 3 compatibility
from __future__ import absolute_import, division, print_function
import os
import sys

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os. pardir, os.pardir, os.pardir)))
    from GSPatternTestUtils import *
else:
    from .GSPatternTestUtils import *
from gsapi import *




class AgnosticDensityTest(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="funkyfresh.mid",
                         midiFolder=self.getLocalCorpusPath('drums'),
                         midiMap=GSPatternUtils.simpleDrumMap,
                         checkForOverlapped=True)

    def test_AgnosticDensity_simple(self):
        numSteps = 32
        agnosticDensity = GSPatternTransformers.AgnosticDensity(numSteps=numSteps)
        for p in self.cachedDataset:
            shortPatterns = p.splitInEqualLengthPatterns(4, makeCopy=False)
            for shortPattern in shortPatterns:
                testLog.info( 'checking pattern' + shortPattern.name)
                randomDensity = {}
                for t in shortPattern.getAllTags():
                    randomDensity[t] = random.random()*2.0
                # shortPattern.printASCIIGrid(blockSize =shortPattern.duration*1.0/numSteps)
                # print 'old',shortPattern.duration
                # print shortPattern.printASCIIGrid(blockSize =shortPattern.duration*1.0/numSteps);
                newP = agnosticDensity.transformPattern(shortPattern, {'normalizedDensities': randomDensity})
                # print 'new'
                # newP.printASCIIGrid(blockSize = shortPattern.duration*1.0/numSteps)
                self.checkPatternValid(newP)


if __name__ == '__main__':
    runTest(profile=True, getStat=False)
