# python 3 compatibility
from __future__ import absolute_import, division, print_function

import os,sys,math

if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)))


from gsapi import *
from .GSPatternTestUtils import *
from gsapi.GSPatternUtils import *
from gsapi.GSPitchSpelling import *

class DescriptorTests(GSTestBase):

    def generateCachedDataset(self):
        return GSDataset(midiGlob="funkyfresh.mid",
                         midiFolder=self.getLocalCorpusPath('drums'),
                         midiMap="pitchNames",
                         checkForOverlapped=True)

    def test_density_simple(self):

    	descriptor = GSDescriptors.GSDescriptorDensity();
    	for p in self.cachedDataset.patterns:
    		allTags = list(p.getAllTags())
    		density = descriptor.getDescriptorForPattern(p);
    		p2 = p.getPatternWithTags(allTags[0])
    		density2 = descriptor.getDescriptorForPattern(p2)
    		#print density,density2,p.duration
    		self.assertTrue(density>=0,p.name + " negative density : "+str(density))
    		self.assertTrue(density< p.duration * len(allTags),p.name +" density over maximum bound : %f %f %f"%(density,p.duration ,len(allTags)))
    		self.assertTrue(density2<=density,"part of the pattern has a bigger density than the whole")

    def test_syncopation(self):
    	descriptor = GSDescriptors.GSDescriptorSyncopation();
    	for p in self.cachedDataset.patterns:
    		# p = p.getPatternWithTags(p.getAllTags()[0])
    		sliced = p.splitInEqualLengthPatterns(descriptor.duration)
    		#print p
    		for s in sliced:
    			syncopation =  descriptor.getDescriptorForPattern(s);
    			self.assertTrue(syncopation>=0 , "syncopation value not valid : %f"%(syncopation))

    def test_chords(self):

        # TODO we only print errors for now needs fix to consider it as true errors:
        #   . wrong annotation : b9? / armature with wrong number of chromas

        descriptor = GSDescriptors.GSDescriptorChord(forceMajMin=False,
                                                     allowDuplicates=True)
        # GSIO.gsiolog.setLevel('INFO')
        harmonyDataset = GSDataset(midiGlob="*.mid",
                                   midiFolder=self.getLocalCorpusPath('harmony'),
                                   midiMap="pitchNames",
                                   checkForOverlapped=True)

        def getChromas(pattern):
            res = map(lambda x: x % 12, pattern.getAllPitches())
            res = list(set(res))
            res.sort()
            return res

        for p in harmonyDataset:
            testLog.info( "checking %s" % p.name)

            gtList = p.name.split('.')[0].split('-')
            groundTruth = list(map(stringToChord, gtList))
            # print groundTruthBase
            lengthOfChords = int(math.ceil(p.duration / len(groundTruth)))
            # print lengthOfChords
            sliced = p.splitInEqualLengthPatterns(lengthOfChords)
            chords = []
            # print sliced
            # exit()
            # print p
            gtIdx = 0
            for s in sliced:
                # print 'l',s
                # s.printASCIIGrid(1);
                gtArm = chordTypes[groundTruth[gtIdx][1]]
                curChromas = getChromas(s)
                if len(gtArm) != len(curChromas):
                    errMsg = "annotation correspond to armature of len %d" \
                             " and midi has %d chromas:" \
                             "\nannotation: %s\nmidiPattern: %s" \
                             % (len(gtArm), len(curChromas), gtArm, curChromas)
                    testLog.error( errMsg)
                    # self.assertTrue(False,errMsg)
                chords.append(descriptor.getDescriptorForPattern(s))
                gtIdx += 1
            # print chords

            def checkProposition(root, prop, truth, index):
                res = False
                if index >= len(prop):
                    return True
                for p in prop[index]:
                    if p == 'silence':
                        return False
                    if index == 0:
                        root = defaultPitchNames.index(p[0])
                    # print index,truth[index][0],defaultPitchNames.index(p[0])-root
                    if truth[index][0] == (defaultPitchNames.index(p[0]) - root + 12) % 12:
                        if index < len(truth):
                            if checkProposition(root, prop, truth, index + 1):
                                return True
                return False

            if len(chords) == len(groundTruth):
                hasValidProposition = checkProposition(0, chords, groundTruth, 0)
                if not hasValidProposition:
                    testLog.error( "\nwrong: " + p.name+"\n" \
                     "proposition not valid:" \
                          "\nproposition: %s" \
                          "\ngroundTruth: %s" \
                          "\n" % (chords, groundTruth))
                    # self.assertTrue(False,"proposition not valid :\nproposition: %s\ngroundTruth: %s"%(chords,groundTruthBase))
            else:
                # TODO fix dataset to avoid this error
                testLog.error('annotation not based on 4beat division or midiFile larger')
                # self.assertTrue(False, 'annotation not based on 4beat division or midiFile larger')


def stringToChord(s):
    isFirstPart = True
    allowedChars = 'VI'
    degree = ""
    armature = ""
    degNum = 0

    if s[0] == 'b':
        degNum -= 1
        s = s[1:]
    if s[0] == '#':
        degNum += 1
        s = s[1:]
    for e in s:

        if isFirstPart:
            if e not in allowedChars:
                isFirstPart = False

        if isFirstPart:
            degree += e
        else:
            armature += e

    degrees = {"I": 0,
               "bII": 1,
               "II": 2,
               "bIII": 3,
               "III": 4,
               "IV": 5,
               "#IV": 6,
               "V": 7,
               "bVI": 8,
               "VI": 9,
               "bVII": 10,
               "VII": 11}

    degNum += degrees[degree]

    # translate annotation to chrodType Notation
    if armature == '':
        armature = 'maj'
    elif armature == 'm':
        armature = 'min'
    elif armature == 'm9':
        armature = 'min9'
    elif armature == 'm7':
        armature = 'min7'
    elif armature == 'm6':
        armature = 'min6'
    elif armature == 'm11':
        armature = 'min11'

    return degNum, armature


if __name__ == '__main__':
    runTest(profile=False, getStat=False)
