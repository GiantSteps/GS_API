import unittest
import os
import sys
# todo check we need import glob and random
import glob
import random

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))

from gsapi import *

testLog = logging.getLogger("gsapi.GSTest")

def runTest(profile=False, getStat=False):
    if profile:
        import cProfile
        # todo check we need import re
        import re
        cProfile.run('unittest.main()', filename='profiled')
    if getStat:
        import pstats
        p = pstats.Stats('profiled')
        p.strip_dirs().sort_stats(1).print_stats()
    if not getStat and not profile:
        unittest.main()


class singleTonDataset(GSDataset):
    """class to parse only once a dataset and share it between tests
    """
    def __init__(self, **kwargs):
        self.creationArgs = kwargs
        self.dataset = None

    def get(self):  # Todo: check added self to args is correct
        if not self.dataset:
            self.dataset = GSDataset(**self.creationArgs)
        return self.dataset  # Todo: check prepent self to variable

def getAllDescriptorsClasses():
    """return list of tuples (descriptorName, descriptorClass)
    """
    res = []
    for elem in dir(GSDescriptors):
        if not '__' in elem and (not 'GSBase' in elem):
            res+=[ (elem, getattr(GSDescriptors,elem,None))]
    return res

class GSTestBase(unittest.TestCase):
    """
    helper function for test classes.
    """
    __cachedDataset = None

    @property
    def cachedDataset(self):
        if not self.__cachedDataset:
            self.__cachedDataset = self.generateCachedDataset()
        return self.__cachedDataset

    # sub class can override that to load a cached dataset only once per session (not per test)
    #  default will crawl all drums Folder
    def generateCachedDataset(self):
        raise GSDataset(midiGlob="*.mid",
                        midiFolder=self.getLocalCorpusPath('drums'),
                        midiMap="pitchNames",
                        checkForOverlapped=True)

    # helper to get local corpus path
    def getLocalCorpusPath(self, toAppend=""):
        import os
        return os.path.abspath(__file__ + "../../../../../corpus/" + toAppend)

    def checkNoTagsOverlaps(self, pattern, msg=None):
        tags = pattern.getAllTags()
        pattern.reorderEvents();
        for t in tags:
            lastTimeOff = 0
            for e in pattern.events:
                if t in e.tags:
                    self.assertTrue(e.startTime >= lastTimeOff,
                                    "%s: (%f < %f) tag: %s" % (msg, e.startTime, lastTimeOff, t))
                    lastTimeOff = e.getEndTime()

    def checkPatternValid(self, pattern, checkForDoublons=True, checkOverlap=True, msg=""):
        self.assertTrue(len(pattern.events) > 0, msg)
        self.assertTrue(pattern.duration > 0, msg)
        i = 0
        for e in pattern.events:
            errMsg = "%s %s" % (msg, e)
            self.assertTrue(e.duration > 0, errMsg)
            self.assertTrue(e.startTime >= 0, errMsg)
            i += 1

        if checkForDoublons:
            i = 0
            for e in pattern.events:
                for ii in range(i + 1, len(pattern.events)):
                    ee = pattern.events[ii]
                    if e.startTime == ee.startTime and e.duration == ee.duration and e.pitch == ee.pitch and e.tags == ee.tags:
                        self.assertTrue(False, "%s: %s doublons %s // %s" % (pattern.name, msg, e, ee))
                i += 1

        if checkOverlap:
            self.checkNoTagsOverlaps(pattern, msg)

    def checkPatternEquals(self,patternA,patternB,checkViewpoints = False):
        if patternA!=patternB:
            self.assertEquals(patternA.duration,patternB.duration)
            self.assertEquals(patternA.bpm,patternB.bpm)
            self.assertEquals(patternA.startTime,patternB.startTime)
            self.assertEquals(patternA.timeSignature,patternB.timeSignature)
            self.checkEventsEquals(patternA,patternB)

            # if we hit next line, no exception were raised so we may have forgotten to check something
            self.assertTrue(False,'pattern not equals for unknown reasons')
        if checkViewpoints and patternA.viewpoints!=patternB.viewpoints:
            self.assertEquals(len(patternA.viewpoints),len(patternB.viewpoints))
            for k in patternA.viewpoints:
                self.checkPatternEquals(patternA.viewpoints[k],patternB.viewpoints[k],checkViewpoints=checkViewpoints)



    def checkEventsEquals(self,patternA,patternB):
        self.assertEquals(len(patternA.events),len(patternB.events))
        patternA.reorderEvents();
        patternB.reorderEvents();
        for i in range(len(patternA.events)):
            self.assertEquals(patternA.events[i],patternB.events[i])

    def setUp(self):
        testLog.info(
        '-------------------------------------\n' \
        'Starting test: '+ self._testMethodName +\
        '-------------------------------------')
