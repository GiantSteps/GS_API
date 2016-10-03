import unittest,os,sys
if __name__=='__main__': sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi import *
from gsapi.MathUtils import *
import random,glob

from GSPatternTestUtils import *



class MarkovPatternTest(GSPatternTestUtils):

	dataSet = GSDataSet(midiGlob="corpus-harmony/*.mid",midiMap="pitchNames")

	# def __init__(self,*args):
	# 	GSPatternTestUtils.__init__(self,*args)

	def buildMarkov(self,order,numSteps,loopDuration):
		for p in self.dataSet.patterns:
			self.patternList = p.splitInEqualLengthPatterns(loopDuration,False);
		self.markovChain = PatternMarkov(order=order,numSteps=numSteps,loopDuration=loopDuration);
		self.markovChain.generateTransitionTableFromPatternList(self.patternList)
		self.assertTrue(self.markovChain.isBuilt(),"markov has not been built")
		self.__testMarkov(100)

	def __testMarkov(self,numPatternToTest):
		for i in range(numPatternToTest):
			pattern = self.markovChain.generatePattern();
			self.checkPatternValid(pattern,msg="markov generated a wrong patternat iteration : "+str(i))
			self.assertTrue(pattern.duration==self.markovChain.loopDuration)



	def test_Markov_1_32_4(self):
		self.buildMarkov(1,32,4);
	def test_Markov_2_32_4(self):
		self.buildMarkov(2,32,4);
	def test_Markov_3_32_4(self):
		self.buildMarkov(3,32,4);
	def test_Markov_4_32_4(self):
		self.buildMarkov(4,32,4);

	def test_Markov_1_16_4(self):
		self.buildMarkov(1,32,4);
	def test_Markov_2_16_4(self):
		self.buildMarkov(2,32,4);
	def test_Markov_3_16_4(self):
		self.buildMarkov(3,32,4);
	def test_Markov_4_32_4(self):
		self.buildMarkov(4,32,4);

	def test_Markov_1_16_2(self):
		self.buildMarkov(1,32,4);
	def test_Markov_2_16_2(self):
		self.buildMarkov(2,32,4);
	def test_Markov_3_16_2(self):
		self.buildMarkov(3,32,4);
	def test_Markov_4_32_2(self):
		self.buildMarkov(4,32,4);

	def test_random_markov(self):
		numSteps = random.randint(4,128)
		loopDuration = random.randint(1,16);
		order = random.randint(0,numSteps-1);
		self.buildMarkov(order = order,numSteps=numSteps,loopDuration=loopDuration)



if __name__ == "__main__":
	runTest(profile=False,getStat=False)

