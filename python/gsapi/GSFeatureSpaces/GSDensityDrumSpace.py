# python 3 compatibility
from __future__ import absolute_import, division, print_function

import os,sys
if __name__=='__main__':
	sys.path.insert(1,os.path.abspath(os.path.join(__file__,os.pardir,os.pardir,os.pardir)))

from gsapi.GSDescriptors import GSDescriptorDensity,GSDescriptorNumberOfTags


class GSDensityDrumSpace():
		# #Descriptor1: number of instruments

		# listofinstruments=[]
		# for steps in pattern:
		# 	for events in steps:
		# 		listofinstruments.append(events)
		# setofinstruments=list(set(listofinstruments))
		# setofinstruments.remove(0)
		# noi=len(setofinstruments)
		# descriptorvector.append(noi)

		# #Descriptor2: loD density of low pitched instrumenst (kick and low conga)
		# #Descriptor3: midD density of the upbeat instruments(snare, rimshot, hiconga)
		# #Descriptor4: hiD density of high pitched sounds (closed hihat, shaker, clave)
		# #Descriptor5: stepD density: percentage of the steps that have onsets (loD+midD+hiD)
		# #Descriptors 6 7 8: lowness, midness, hiness
	drumMidiMap = {}
	def __init__(self):
		self.descriptors = {
		"numberOfInstruments" : GSDescriptorNumberOfTags(),
		"loD": GSDescriptors.GSDescriptorDensity(includedTags=["Kick","low Congas"]),
		"midD": GSDescriptors.GSDescriptorDensity(includedTags=["snare", "rimshot", "hiconga"]),
		"hiD": GSDescriptors.GSDescriptorDensity(includedTags=["closed hihat", "shaker", "clave"])
		}
	def getFeatureSpace(self,pattern):
		res = {}
		for d in self.descriptors:
			res[d] = self.descriptors[d].getDescriptorForPattern(pattern)
		return res 



if __name__=='__main__':
	from gsapi import *
	dataset = GSDataset(midiGlob="*.mid")
	drumSpace = GSDensityDrumSpace()
	for p in dataset.patterns:
		
		print (drumSpace.getFeatureSpace(p))

