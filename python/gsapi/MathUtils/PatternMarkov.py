# python 3 compatibility
from __future__ import absolute_import, division, print_function

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
    def __init__(self, order=1, numSteps=32, loopDuration=4,):
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
        """ builds transision table for the previously given list of GSPattern
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
                curEvent = self._buildTupleForEvents(l)[0];
                combinationName = self._buildTupleForEvents(self.getLastEvents(p,step,self.order,1));

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

    def getStringTransitionTable(self,reduceTuples=True,jsonStyle=True):
        import copy
        stringTable = copy.deepcopy(self.transitionTable)

        def _tupleToString(d):
            if isinstance(d,dict):
                for k,v in d.items():
                    if isinstance(k,tuple):
                        d[str(_tupleToString(k))]=d.pop(k)
                    _tupleToString(v)
            elif isinstance(d,list):
                for v in d:
                    _tupleToString(v)
            elif isinstance(d,tuple):
                newTuple = ()
                for v in d:
                    newTuple += (_tupleToString(v),)
                if reduceTuples and len(newTuple)==1:
                    newTuple = newTuple[0]
                d = newTuple
            return d
        
        for t in stringTable:
            t = _tupleToString(stringTable)
        
        if jsonStyle:
            import json

            for i in range(len(stringTable)):
                stringTable[i] = json.dumps(stringTable[i],indent=1)
                
        return stringTable

    
       
    def __repr__(self):
        res =  "Markov Transition Table\n"
        st = self.getStringTransitionTable(reduceTuples=True,jsonStyle=True)
        i=0
        for t in st:
            res+="step %d\n%s\n"%(i,t)
            i+=1
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
            # print(d)
            # print(previousTags)
            return previousTags in d

        def _generateEventAtStep(step, previousTags):
            
            if previousTags not in self.transitionTable[step]:
                patternMarkovLog.error("wrong transition table, zero state for " + str(previousTags) )
                patternMarkovLog.error(str(self.transitionTable[step]))
                return None
            d = self.transitionTable[step][previousTags]
            chosenIdx = 0
            if len(d) > 1:
                tSum = 0
                bins = []
                for x in d.values():
                    tSum += x
                    bins += [tSum]
                r = random.random()
                for i in range(1, len(bins)):
                    if bins[i-1] <= r and bins[i] > r:
                        chosenIdx = i - 1
                        break
                
            return list(d.keys())[chosenIdx]

        cIdx = self.order
        startHypothesis = tuple()
        maxNumtries = 30
        while not _isValidState(cIdx, startHypothesis):
            startHypothesis = tuple()
            for n in range(self.order):
                startHypothesis += (random.choice(_getAvailableAtStep(n)),)
            maxNumtries-=1
            if  maxNumtries==0:
                raise Exception(" can't find start hypothesis in markov")

        events = list(startHypothesis)
        i = self.order
        maxNumtries = 10
        maxTries = maxNumtries
        while i < self.numSteps and maxTries > 0:
            newPast = tuple(events[i-self.order:i])
            newEv = _generateEventAtStep(i, newPast)
            if newEv:
                events += [newEv]
                maxTries = maxNumtries
                i += 1
            else:
                maxTries -= 1
                if maxTries == 0:
                    patternMarkovLog.error("not found combination %s at step %i \n transitions\n %s" % (','.join(newPast), i, self.transitionTable[i]))
                    raise Exception(" can't find combination in markov")
                else:
                    patternMarkovLog.warning("not found combination %s " % (','.join(newPast)))

        pattern = GSPattern()
        idx = 0

        stepSize = 1.0*self.loopDuration/self.numSteps


        for el in events:
            for tagElem in el:
                if tagElem !='silence' :
                    pattern.events+=[GSPatternEvent(idx*stepSize,stepSize,100,127,tag=tagElem)]
            
            idx+=1
        pattern.duration = self.loopDuration

        return pattern

    def checkSilences(self, p):
        for i in range(int(p.duration)):
            c = p.getStartingEventsAtTime(i)
            if len(c) > 1 and ("silence" in c):
                patternMarkovLog.error ("wrong silence")
                

    def checkSilenceInList(self, c):
        if len(c) > 1 and( 'silence' in c):
            patternMarkovLog.error ("wrong silence")
            



    def _buildTupleForEvents(self, events):
        """Build a tuple from list of lists of events:
        If list is [[a1, a2], [b1, b2, b3]] (where an and bn are tags of listed events)
        this function returns "a1/a2, b1/b2/b3"
        """
        res = tuple()
        for evAtStep in events:
            curL = list()
            for e in evAtStep:
                    curL += [e.tag]

            # set allow for having consistent ordering, and remove step-wise overlapping events
            res += (tuple(set(curL)),)
        return res

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

    def getAllPossibleStates(self):
        possibleStates = []
        for d in self.transitionTable:
            possibleStates += list(d.keys())
            for v in d.values():
                for state in v.keys():
                    possibleStates+=[state]
        possibleStates=list(set(possibleStates))
        return possibleStates

    def getAllPossibleStatesAtStep(self,step):
        return list(set(self.getPossibleInStatesAtStep(step)+self.getPossibleOutStatesAtStep(step)))

    def getPossibleOutStatesAtStep(self,step):
        d=self.transitionTable[step]
        possibleStates=[]
        for v in d.values():
                for state in v.keys():
                    possibleStates+=[state]
        possibleStates=list(set(possibleStates))
        return possibleStates

    def getPossibleInStatesAtStep(self,step):
        d=self.transitionTable[step]
        return list(d.keys())

    def getMatrixAtStep(self,step,possibleStatesIn=None, possibleStatesOut = None,matrix=None):
        possibleStatesIn = possibleStatesIn or self.getPossibleInStatesAtStep(step)
        possibleStatesOut = possibleStatesOut or self.getPossibleOutStatesAtStep(step)
        sizeIn = len(possibleStatesIn)
        sizeOut = len(possibleStatesOut)
        matrix = matrix or  [[0]*sizeOut for i in range(sizeIn)]
        d= self.transitionTable[step]
        for k,v in d.items():
            colIdx = possibleStatesIn.index(k)
            for evt,p in v.items():
                rowIdx = possibleStatesOut.index(evt)
                matrix[colIdx][rowIdx]+=p
            

        return matrix,possibleStatesIn,possibleStatesOut


    def __plotMatrix(self,m,labelsIn,labelsOut):
        import matplotlib.pyplot as plt
        from matplotlib import cm
        fig, ax = plt.subplots()#figsize=(18, 2))
        #shows zero values as black
        cmap = plt.cm.OrRd
        cmap.set_under(color='black')
        cax = ax.matshow(m,interpolation='nearest',vmin=0.000001,cmap=cmap)
        ax.set_xticks(range(len(labelsOut)))
        ax.set_xticklabels(labelsOut, rotation='vertical')
        ax.set_yticks(range(len(labelsIn)))
        ax.set_yticklabels( labelsIn)
        fig.colorbar(cax)

        plt.show()

    def plotMatrixAtStep(self,step):
        mat,labelsIn,labelsOut = self.getMatrixAtStep(step)#,possibleStates = allTags)
        self.__plotMatrix(mat,labelsIn,labelsOut)

    def plotGlobalMatrix(self):
        numSteps = len(self.transitionTable)
        possibleStatesIn = list(set([item for step in range(numSteps) for item in self.getPossibleInStatesAtStep(step)]))
        possibleStatesOut = list(set([item for step in range(numSteps) for item in self.getPossibleOutStatesAtStep(step)]))
        sizeIn = len(possibleStatesIn)
        sizeOut = len(possibleStatesOut)
        
        matrix =  [[0]*sizeOut for i in range(sizeIn)]
        for step in range(numSteps):
            self.getMatrixAtStep(step,possibleStatesIn = possibleStatesIn,possibleStatesOut=possibleStatesOut,matrix=matrix)
        self.__plotMatrix(matrix,possibleStatesIn,possibleStatesOut)


