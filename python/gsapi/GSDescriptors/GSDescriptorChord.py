from GSBaseDescriptor import *
from GSDescriptorDensity import GSDescriptorDensity

from gsapi.GSPatternUtils import *



def intervalListToProfile(intervalList,length=12):
		profile = [0]*length
		for e in intervalList:
			profile[e]=1
		return profile

class GSDescriptorChord(GSBaseDescriptor):

	allProfiles = {k:intervalListToProfile(v) for k,v in chordTypes.iteritems()}

	def __init__(self,forceMajMin=False):
		GSBaseDescriptor.__init__(self)
		self.densityDescriptor = GSDescriptorDensity()
		self.forceMajMin = forceMajMin


	def getDescriptorForPattern(self,pattern):
		allPitches = pattern.getAllPitches()
		pitchDensities = {}
		for p in allPitches:
			voice = pattern.getPatternWithPitch(p)
			pitchDensities[p]=self.densityDescriptor.getDescriptorForPattern(voice)


		chromas = [0]*12
		for p,v in pitchDensities.iteritems():
			chroma = p%12
			chromas[chroma]+=v

		elemNum = 0
		for c in chromas : 
			if c>0 : elemNum+=1


		if elemNum==0:
			return "silence"
		ordered = [{'chroma':i,'density':chromas[i]} for i in range(len(chromas))]
		ordered.sort(cmp=lambda x,y:int(x['density']-y['density']))
		if elemNum <= 2	:
			return defaultPitchNames[ordered[0]['chroma']]
		profileToConsider = GSDescriptorChord.allProfiles
		if self.forceMajMin:
			profileToConsider = {'min':profileToConsider['min'],'maj':profileToConsider['maj']}
		bestScore = findBestScoreForProfiles(chromas,profileToConsider)
		return defaultPitchNames[bestScore[0]]+' '+bestScore[1]
		




def findBestScoreForProfiles(chromas,pitchProfileDict):
	maxScore = 0
	bestProfile = ""
	bestRoot = 0
	for k,v in pitchProfileDict.iteritems():
		conv = convolveWithPitchProfile(chromas,v)
		score =  findMaxAndIdx(conv)
		nonZero = getNumNonZero(v)
		# to be a complex chord score should be higher (not only part of it)
		# if nonZero>3:
		score[0]*=pow(nonZero,-.5)
		print  k,score[0],score[1]
		if score[0]>maxScore:
			maxScore = score[0]
			bestProfile = k
			bestRoot = score[1]
			# print bestProfile,bestRoot,maxScore
	return [bestRoot,bestProfile]

def getNumNonZero(li):
	count = 0
	for e in li:
		if e!=0 :
			count+=1
	return count

def convolveWithPitchProfile(chromas,pitchProfile):
	if len(pitchProfile) != len(chromas):
		print 'chroma and pitchProfile of different length'
		return None

	convLen = len(chromas)
	convList = [0]*convLen
	for i in range(convLen):
		conv = 0
		for c in range(convLen):
			idx = (i+c)%convLen
			conv+=chromas[c]*pitchProfile[idx]
		convList[i]=conv
	return convList

def findMaxAndIdx(convolution):
	M = 0
	Mi = -1
	i=0
	for c in convolution:
		if c>M:
			M=c
			Mi=i
		i+=1
	return [M,Mi]




	


