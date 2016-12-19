# python 3 compatibility
from __future__ import absolute_import, division, print_function

from .GSBasePatternTransformer import *
from ..GSDescriptors import GSDescriptorDensity
import random


class AgnosticDensity(GSBasePatternTransformer):
    """ Agnostic transformation algorithm.

    Args:
        numSteps : number of steps to consider
        mode:['random','syncopation'] :  algorithm used

    Attributes:
        globalDensity: float (0..2) the desired global density,
        (0 = empty pattern, 1 = origin pattern, 2 = pattern with all events)
        individualDensities: dict[tag]=density :  a per Tag density, densities should be in the same range as globalDensity
        mode:['random','syncopation'] :  algorithm used
        originPattern: the origin pattern, e.g : the one given if all densities are equals to 1
    """
    def __init__(self, mode='random', numSteps=32):
        self.globalDensity = 1
        self.normalizedDensities = {}
        self.targetDensities = {}
        self.mode = 'random'
        self.originPattern = None
        self.currentPattern = None
        self.originDuration = 0
        self.numSteps = numSteps
        self.originDensities = {}
        self.densityDescriptor = GSDescriptorDensity()
        self.currentDistribution = {}
        self.originDistribution = {}

    def configure(self, paramDict):
        if 'inputPattern' in paramDict:
            buildDensityMap(paramDict['inputPattern'])

    def transformPattern(self, pattern, paramDict):
        if pattern!=None and pattern != self.originPattern:
            self.buildDensityMap(pattern)
        
        if self.originPattern==None:
            # print ("no pattern given for agnosticDensity transformation")
            return
        if 'normalizedDensities' in paramDict:
            self.updateNormalizedDensities(paramDict['normalizedDensities'])

        res = self.currentPattern.copy()
        res.timeStretch(self.originDuration*1.0/self.numSteps)

        return res

    def updateNormalizedDensities(self, normalizedDict):
        for k,v in normalizedDict.items():
            if k in self.normalizedDensities:
                originDensity = self.normalizedDensities[k]
    # if we cross density one, reset to one then do the subsequent calculations
                if (v<1 and originDensity>1) or (v>1 and originDensity<1):
                    # print "reset densities"
                    self.resetDensities()

                diffNormalized =  v-self.normalizedDensities[k]
                if diffNormalized==0:
                    # were already here
                    continue

                # here we are sure to not need to crossdensity one (and have to do both increment styles)
                if originDensity>=1 and v >=1:
                    step = 1.0/(self.numSteps - self.originDensities[k])
                    n  = originDensity
                    v = max(1,min(v,2))-step
                    if diffNormalized>step:

                        while( n<v ):
                            self.addEventForTag(k,n)
                            n+=step
                    if diffNormalized<-step:
                        while( n>v ) :
                            self.removeEventForTag(k,n)
                            n-=step
                    self.normalizedDensities[k] = 1.0+int((v-1.0)/step)*1.0*step

                if originDensity<=1 and v <1:
                    step = 1.0/(self.originDensities[k])
                    n  = originDensity
                    v = max(0,min(v,1))+step
                    if diffNormalized>step:
                        while( n<v ) :
                            self.addEventForTag(k,n)
                            n+=step
                    if diffNormalized<-step:
                        while(n>v ):
                            self.removeEventForTag(k,n)
                            n-=step
                    self.normalizedDensities[k] = int(v/step)*1.0*step
        self.currentPattern.reorderEvents()

    def addEventForTag(self,tag,targetDensity):

        availableIdx = self.currentState[tag]['silences']
        # we need to go toward origin pattern if adding while having lower density
        if targetDensity<1:
            availableIdx = self.currentState[tag]['removedNotes']

        idx = 0
        if self.mode == 'hysteresis':
            idx = random.randint(0,len (availableIdx)-1)

        idxToAdd = availableIdx[idx]

        orIdx = self.currentState[tag]['silences'].index(idxToAdd)
        del self.currentState[tag]['silences'][orIdx]
        if targetDensity<1:
            del self.currentState[tag]['removedNotes'][idx]

        self.currentState[tag]['addedNotes']+=[idxToAdd]
        tPattern =self.currentPattern.getPatternWithTags(tag, makeCopy=False);
        newEv = tPattern.events[0].copy()
        newEv.startTime = idxToAdd
        newEv.duration = 1
        self.currentPattern.events+=[newEv]

    def removeEventForTag(self, tag, targetDensity):

        availableIdx = self.currentState[tag]['notes']

        # we need to go toward origin pattern if removing while having higher density
        if targetDensity > 1:
            availableIdx = self.currentState[tag]['addedNotes']

        idx = 0
        if self.mode == 'hysteresis':
            idx = random.randint(0,len (availableIdx)-1)

        idxToRemove = availableIdx[idx]

        orIdx = self.currentState[tag]['notes'].index(idxToRemove)
        del self.currentState[tag]['notes'][orIdx]
        if targetDensity > 1:
            del self.currentState[tag]['addedNotes'][idx]

        self.currentState[tag]['removedNotes'] += [idxToRemove]
        tPattern =self.currentPattern.getPatternWithTags(tag, makeCopy=False)

        eventToRemove = tPattern.getStartingEventsAtTime(idxToRemove)[0]
        self.currentPattern.removeEvent(eventToRemove)

    def createCurrentState(self):
        self.currentState = {}
        for tag in self.originPattern.getAllTags():
            dist = self.__initStateFromVoice(self.originPattern.getPatternWithTags(tag))
            self.currentState[tag] = dist

    def __shuffleList(self, l):
        for iteration in range(len(l)):
            idx1 = iteration
            idx2 = random.randint(0, len(l)-1)
            t = l[idx1]
            l[idx1] = l[idx2]
            l[idx2] = t

    def __initStateFromVoice(self, voice):
        state = {'notes': [], 'silences': [], 'addedNotes':[], 'removedNotes': []}
        curEvent = voice.events[0]
        curEvtIdx = 0
        for t in range(self.numSteps):
            if curEvent.containsTime(t):
                curEvtIdx += 1
                curEvtIdx = min(len(voice.events) - 1, curEvtIdx)
                curEvent = voice.events[curEvtIdx]
                state['notes'] += [t]
            else:
                state['silences'] += [t]
        self.__shuffleList(state['notes'])
        self.__shuffleList(state['silences'])
        return state

    def resetDensities(self):
        self.originDensities = {}
        self.targetDensities = {}
        self.normalizedDensities = {}
        for t in self.originPattern.getAllTags():

            self.densityDescriptor.includedTags = t
            density = self.densityDescriptor.getDescriptorForPattern(self.originPattern)
            self.originDensities[t] = density * self.numSteps * 1.0 / self.originPattern.duration
            self.targetDensities[t] = density * self.numSteps * 1.0 / self.originPattern.duration
            self.normalizedDensities[t] = 1
        

    def buildDensityMap(self, pattern):
        self.originPattern = pattern.copy()
        self.originDuration = pattern.duration
        self.originPattern.timeStretch(self.numSteps * 1.0 / self.originPattern.duration)
        self.originPattern.alignOnGrid(1)
        self.currentPattern = self.originPattern.copy()
        self.resetDensities()
        self.createCurrentState()
