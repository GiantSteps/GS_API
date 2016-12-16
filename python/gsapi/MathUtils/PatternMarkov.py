from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import GSPattern, GSPatternEvent
import copy
import random
import logging
patternMarkovLog = logging.getLogger('gsapi.MathUtils.PatternMarkov')


class PatternMarkov(object):
    """Computes a Markov chains from pattern.

    Args:
        order: order used for markov computation
        numSteps: number of steps to consider (binarization of pattern)

    Attributes:
        order: order used for markov computation
        numSteps: number of steps to consider (binarization of pattern)
    """
    def __init__(self, order, numSteps, loopDuration):
        self.order = order
        self.numSteps = numSteps
        self.loopDuration = loopDuration
        self.transitionTable = {}

    def generateTransitionTableFromPatternList(self, patternClasses):
        """Generate style based on list of GSPattern
        Args:
            patternClasses:  list of GSPatterns
        """
        if not isinstance(patternClasses, list):
            patternMarkovLog.error("PatternMarkov need a list")
            return False
        else:
            self.originPatterns = patternClasses
            self.buildTransitionTable()

    def getMarkovConfig(self):
        return "order(%i), loopLength(%f), numSteps(%i)" % (self.order, self.loopDuration, self.numSteps)

    def buildTransitionTable(self):
        """ builds transisiont table for the previously given list of GSPattern
        """
        self.transitionTable = [{} for f in range(int(self.numSteps))]

        self.binarizedPatterns = copy.deepcopy(self.originPatterns)
        for p in self.binarizedPatterns:
            self.formatPattern(p)
            self.checkSilences(p)
            if(self.numSteps != int(p.duration)):
                    patternMarkovLog.warning( "PatternMarkov : quantization to numSteps failed, numSteps="+str(self.numSteps)+" duration="+str(p.duration) + " cfg : "+self.getMarkovConfig())
            for step in range(self.numSteps):
                l = [p.getStartingEventsAtTime(step)];
                self.checkSilenceInList(l)
                curEvent = self._buildNameForEvents(l);
                combinationName = self._buildNameForEvents(self.getLastEvents(p,step,self.order,1));

                curDic = self.transitionTable[int(step)]

                if combinationName not in curDic:
                    curDic[combinationName] = {}

                if curEvent not in curDic[combinationName]:
                    curDic[combinationName][curEvent] = 1
                else:
                    curDic[combinationName][curEvent] += 1



        def _normalize():
            for t in self.transitionTable:
                for d in t:
                    sum= 0
                    for pe in t[d]:
                        sum+= t[d][pe]
                    for pe in t[d]:
                        t[d][pe]/=1.0*sum
        _normalize()

    def __repr__(self):
        res = "Markov Transition Table\n"
        for s in self.transitionTable:
            res += str(s) + "\n"
        return res

    def generatePattern(self, seed=None):
        """Generate a new pattern from current transitionTable.

        Args:
            seed: seed used for random initialisation of pattern (value of None generates a new one)
        """
        random.seed(seed)
        potentialStartEvent = []

        def _getAvailableAtStep(step):
            res = []
            if step < 0:
                step += len(self.transitionTable)
            for n in self.transitionTable[step]:
                for t in self.transitionTable[step][n]:
                    res += [t]
            return res

        def _isValidState(step, previousTags):
            d = self.transitionTable[step]
            # print d, previousTags
            return previousTags in d

        def _generateEventAtStep(step, previousTags):
            if previousTags not in self.transitionTable[step]:
                patternMarkovLog.error("wrong transition table, zero state for " + str(previousTags))
                return None
            d = self.transitionTable[step][previousTags]
            chosenIdx = 0
            if len(d) > 1:
                tSum = 0
                bins = []
                for x in d.itervalues():
                    tSum += x
                    bins += [tSum]
                r = random.random()
                for i in range(1, len(bins)):
                    if bins[i-1] <= r and bins[i] > r:
                        chosenIdx = i - 1
                        break
                # print chosenIdx
            return list(d.keys())[chosenIdx]

        cIdx = self.order
        startHypothesis = []
        for n in range(self.order):
            startHypothesis += [random.choice(_getAvailableAtStep(n))]

        while not _isValidState(cIdx, ','.join(startHypothesis)):
            startHypothesis = []
            for n in range(self.order):
                startHypothesis += [random.choice(_getAvailableAtStep(n))]

        # print startHypothesis
        events = startHypothesis
        i = self.order
        maxNumtries = 10
        maxTries = maxNumtries
        while i < self.numSteps and maxTries > 0:
            newPast = events[i-self.order:i]
            newEv = _generateEventAtStep(i, ','.join(newPast))
            if newEv:
                # print i,newEv
                events += [newEv]
                maxTries = maxNumtries
                i += 1
            else:
                maxTries -= 1
                if maxTries == 0:
                    patternMarkovLog.error("not found combination %s at step %i \n transitions\n %s" % (','.join(newPast), i, self.transitionTable[i]))
                else:
                    patternMarkovLog.warning("not found combination %s " % (','.join(newPast)))

        pattern = GSPattern()
        idx = 0

        stepSize = 1.0*self.loopDuration/self.numSteps

        for el in events:
            l = el.split("/")
            for e in l:
                if(e!='silence') :
                    pattern.events+=[GSPatternEvent(idx*stepSize,stepSize,100,127,e)]
            idx+=1
        pattern.duration = self.loopDuration

        return pattern

    def checkSilences(self, p):
        for i in range(int(p.duration)):
            c = p.getStartingEventsAtTime(i)
            if len(c) > 1 and ("silence" in c):
                print ("wrong silence")
                exit()

    def checkSilenceInList(self, c):
        if len(c) > 1 and( 'silence' in c):
            print ("wrong silence")
            exit()

    def _buildNameForEvents(self, events):
        """Build a string from list of lists of events:
        If list is [[a1, a2], [b1, b2, b3]] (where an and bn are tags of listed events)
        this function returns "a1/a2, b1/b2/b3"
        """
        res = []
        for evAtStep in events:
            curL = []
            for e in evAtStep:
                for t in e.tags:
                    if t not in curL:
                        curL += [t]
            # we sort it for having consistent ordering
            curL.sort()
            res += [curL]
        out = ""
        for l in res:
            out += '/'.join(l)
            out += ","
        out = out[:-1]

        return out

    def formatPattern(self, p):
        """Format pattern to have a grid aligned on markov steps size."""
        # p.quantize(self.loopDuration*1.0/self.numSteps);
        p.timeStretch(self.numSteps * 1.0 / self.loopDuration)

        p.alignOnGrid(1)
        p.removeOverlapped()
        p.fillWithSilences(maxSilenceTime=1)

    def getLastEvents(self, pattern, step, num, stepSize):
        events = []
        for i in reversed(range(1, num + 1)):
            idx = step - i * stepSize
            if idx < 0:
                idx += pattern.duration
            events += [pattern.getStartingEventsAtTime(idx)]
        return events

    def getInternalState(self):
        res = {"transitionTable": self.transitionTable,
               "order": self.order,
               "numSteps": self.numSteps,
               "loopDuration": self.loopDuration}
        return res

    def setInternalState(self, state):
        self.transitionTable = state["transitionTable"]
        self.order = state["order"]
        self.numSteps = state["numSteps"]
        self.loopDuration = state["loopDuration"]

    def isBuilt(self):
        return self.transitionTable != {}
