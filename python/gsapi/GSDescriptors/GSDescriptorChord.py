# python 3 compatibility
from __future__ import absolute_import, division, print_function

from .GSBaseDescriptor import  *

from .GSDescriptorDensity import GSDescriptorDensity
from gsapi.GSPatternUtils import *
from gsapi.GSPitchSpelling import *


def intervalListToProfile(intervalList, length=12):
    profile = [-1] * length
    profile[0] = 1
    for e in intervalList:
        profile[e % length] = 0.8
    return profile

class ChordTag(tuple):
    """ helper for nicely print chords tags
    chord tags are tuples (root, type), ex : ('C','maj')
    """
    def __repr__(self):
        return "".join(self)

class GSDescriptorChord(GSBaseDescriptor):

    allProfiles = {k: intervalListToProfile(v) for k, v in chordTypes.items()}

    def __init__(self, forceMajMin=False, allowDuplicates=False):
        GSBaseDescriptor.__init__(self)
        self.densityDescriptor = GSDescriptorDensity()
        self.forceMajMin = forceMajMin
        self.allowDuplicates = allowDuplicates

    def configure(self, paramDict):
        """Configure current descriptor mapping dict to parameters."""
        raise NotImplementedError("Should have implemented this")

    def getDescriptorForPattern(self, pattern):
        allPitches = pattern.getAllPitches()
        pitchDensities = {}

        for p in allPitches:
            voice = pattern.getPatternWithPitch(p)
            pitchDensities[p] = self.densityDescriptor.getDescriptorForPattern(voice)

        chromas = [0] * 12
        for p, v in pitchDensities.items():
            chroma = p % 12
            chromas[chroma] += v

        elemNum = 0
        for c in chromas:
            if c > 0:
                elemNum += 1

        if elemNum == 0:
            return "silence"
        ordered = [{'chroma': i, 'density': chromas[i]} for i in range(len(chromas))]
        ordered.sort(key=lambda x: (x['density']))
        # if elemNum <= 2:
        # 	return defaultPitchNames[ordered[0]['chroma']]
        profileToConsider = GSDescriptorChord.allProfiles
        if self.forceMajMin:
            profileToConsider = {'min': profileToConsider['min'], 'maj': profileToConsider['maj']}
        bestScore = findBestScoreForProfiles(chromas,
                                             profileToConsider,
                                             penalityWeight=pattern.duration / 2.0,
                                             allowDuplicates=self.allowDuplicates)
        if self.allowDuplicates:
            return [ChordTag((defaultPitchNames[x[0]], x[1])) for x in bestScore]
        else:
            return ChordTag((defaultPitchNames[bestScore[0]], bestScore[1]))


def findBestScoreForProfiles(chromas, pitchProfileDict, penalityWeight,allowDuplicates=False):
    maxScore = 0
    if allowDuplicates:
        bestProfile = []
        bestRoot = []
    else:
        bestProfile = ""
        bestRoot = 0
    for k, v in pitchProfileDict.items():
        conv = convolveWithPitchProfile(chromas, v, penalityWeight)
        score = findMaxAndIdx(conv)
        nonZero = getNumNonZero(v)
        # print v
        # print chromas
        # print conv
        # print  k,score[0]
        if score[0] >= maxScore:
            if allowDuplicates:
                if score[0] > maxScore:
                    bestProfile = [k]
                    bestRoot = [score[1]]
                else:
                    bestProfile += [k]
                    bestRoot += [score[1]]
            else:
                bestProfile = k
                bestRoot = score[1]
            maxScore = score[0]
            # print bestProfile, bestRoot, maxScore
    if allowDuplicates:
        return [(bestRoot[i], bestProfile[i]) for i in range(len(bestRoot))]
    else:
        return bestRoot, bestProfile


def getNumNonZero(li):
    count = 0
    for e in li:
        if e != 0:
            count += 1
    return count


def convolveWithPitchProfile(chromas, pitchProfile, penalityWeight):
    if len(pitchProfile) != len(chromas):
        print ('chroma and pitchProfile of different length')
        return None

    convLen = len(chromas)
    convList = [0] * convLen
    for i in range(convLen):
        conv = 0
        for c in range(convLen):
            idx = (c - i + convLen) % convLen
            conv += chromas[c] * pitchProfile[idx]
            # penalize if notes from pitch profile are missing
            if pitchProfile[idx] > 0 >= chromas[c]:
                conv -= penalityWeight
        convList[i] = conv
    return convList


def findMaxAndIdx(convolution):
    M = 0
    Mi = -1
    i = 0
    for c in convolution:
        if c > M:
            M = c
            Mi = i
        i += 1
    return [M, Mi]
