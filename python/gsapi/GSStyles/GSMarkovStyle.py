# python 3 compatibility
from __future__ import absolute_import, division, print_function
from .GSBaseStyle import *
from ..MathUtils import PatternMarkov
import logging
markovLog = logging.getLogger('gsapi.GSStyle.GSMarkovStyle')


class GSMarkovStyle(GSBaseStyle):  # TODO: check added PatternMarkov here, needed?
    """Computes a style based on markov chains.

    Args:
        order: order used for markov computation
        numSteps: number of steps to consider (binarization of pattern)

    Attributes:
        order: order used for markov computation
        numSteps: number of steps to consider (binarization of pattern)
    """
    def __init__(self, order, numSteps, loopDuration):
        GSBaseStyle.__init__(self)
        self.type = "None"
        self.markovChain = PatternMarkov(order=order, numSteps=numSteps, loopDuration=loopDuration)

    def generateStyle(self, PatternList):
        """Generates a style based on list of GSPatterns.

        Args:
            PatternList:  list of GSPatterns
        """
        self.markovChain.generateTransitionTableFromPatternList(PatternList)

    def buildStyle(self):
        """Builds transition table for a previously given list of GSPatterns."""
        self.markovChain.buildTransitionTable()

    def generatePattern(self, seed=None):
        """Generates a new pattern.

        Args:
            seed: seed used for random initialisation of pattern (value of None generates a new one)
        """
        return self.markovChain.generatePattern(seed=seed)

    def formatPattern(self, p):
        # p.quantize(self.loopDuration * 1.0 / self.numSteps, self.numSteps * 1.0/ self.loopDuration)
        p.timeStretch(self.numSteps * 1.0 / self.loopDuration)
        p.alignOnGrid(1)
        p.removeOverlapped()
        p.fillWithSilences(maxSilenceTime=1)

    def getLastEvents(self, pattern, step, num, stepSize):
        events = []
        for i in reversed(range(1, num+1)):
            idx = step - i * stepSize
            if idx < 0:
                idx += pattern.duration
            events += [pattern.getStartingEventsAtTime(idx)]
        return events

    def getDistanceFromStyle(self, Pattern):
        raise NotImplementedError("Should have implemented this")

    def getClosestPattern(self, Pattern, seed=0):
        raise NotImplementedError("Should have implemented this")

    def getInterpolated(self, PatternA, PatternB, distanceFromA, seed=0):
        raise NotImplementedError("Should have implemented this")

    def getInternalState(self):
        res = {"markovChain": self.markovChain.getInternalState()}
        return res

    def setInternalState(self, state):
        self.markovChain.setInternalState(state["markovChain"])

    def isBuilt(self):
        return self.markovChain.isBuilt()
