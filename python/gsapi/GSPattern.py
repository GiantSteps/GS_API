
import copy

"""Documentation for GSPattern module.

GSPattern
"""
class GSPatternEvent(object):
	"""Represent an event of a GSPattern

	an event is made of start and length , origin pitch , velocity and associated tags


	Attributes:
		startTime: startTime of event
		duration: duration of event
		pitch : pitch of event
		velocity: velocity of event
		tags: list of tags representing the event
	"""


	def __init__(self,startTime,duration,pitch,velocity=127,tags=[]):
		self.duration = duration
		if not isinstance(tags,list):tags = [tags]
		self.tags=tags
		self.startTime = startTime;
		self.pitch = pitch;
		self.velocity = velocity;
		self.tags = tags;
		

	def hasOneCommonTagWith(self,event):
		""" compare tags between events

		Args:
			event: event to compare with
		Returns:
			true if at least one tag is equal
		"""
		return self.hasOneOfTags(events.tags);

	def hasOneOfTags(self,tags):
		""" Compare this event's tags with a list of strings

		Args:
			tags: list of strings to compare with
		Returns:
			true if at least one tag is equal
		"""

		for t in tags:
			if t in self.tags:
				return True;
		return False;

	def tagsAre(self,tags):
		""" Compare this event's tags with a list of strings

		Args:
			tags: list of strings to compare with
		Returns:
			true if all tags are equal
		"""
		return all([x in self.tags for x in tags])


	def allTagsAreEqualWith(self,event):
		""" Compare this event's tags with an other event

		Args:
			event: event to compare with
		Returns:
			true if all tags are equal
		"""
		self.tagsAre(event.tags)

	def getEndTime(self):
		""" returns the time when this events ends

		Returns:
			the time when this event ends
		"""
		return self.startTime + self.duration


	def copy(self):
		""" Copy an event
		
		Returns:
			 A deep copy of this event to be manipulated without changing original
		"""
		# return copy.deepcopy(self)
		return copy.deepcopy(self)

	def cutInSteps(self,stepSize):
		""" Cut an event in steps of stepsize length

		Args:
			stepSize: the desired size of each produced events
		Returns:
			a list of events of length `stepSize`
		"""
		res = []
		# if smaller still take it
		num = max(1,int(self.duration/stepSize))
		for i in range(num):
			newE = self.copy()
			newE.startTime = self.startTime+i*stepSize
			newE.duration = stepSize
			res+=[newE]
		return res


# ///////////////
#  GSPattern
class GSPattern(object):
	""" Class representing a pattern made of GSPatternEvent

	holds a list of GSEvents and provide basic manipulation function

	Args:
		duration: length of pattern usually in beat, but time scale is up to the user (can be useful if working on 32th note steps)
		events: list of GSPatternEvent for this pattern
		bpm:origin BPM for this pattern (default: 120)
		timeSignature: list of integer representing time signature ; i.e [numerator,denominator]
	"""
	defaultTimeSignature =[4,4];
	defaultBPM = 120

	def __init__(self):
		self.duration = 0;
		self.events = [];
		self.bpm = GSPattern.defaultBPM;
		self.timeSignature = GSPattern.defaultTimeSignature;
		self.originFilePath=""
		self.name=""


	def setDurationFromLastEvent(self,onlyIfBigger=True):
		""" sets duration to last event NoteOff

		Args:
			onlyIfBigger: update duration only if last Note off is bigger

		if inner events have a bigger time span than self.duration, increase duration to fit
		"""
		total = self.getLastNoteOff();
		if (total and (total > self.duration or not onlyIfBigger)):
			# print "resizing : "+str(total) +'old : '+ str(self.duration)
			self.duration = total

	def reorderEvents(self):
		""" ensure than our internal event list `events` is time sorted 
			
			can be useful for time sensitive events iteration
		"""
		self.events.sort(key=lambda x: x.startTime, reverse=False)

	def getLastNoteOff(self):
		""" Gets last event end time

		Returns:
			lastNoteOff, i.e the time corresponding to the end of the last event
		"""
		
		if(len(self.events)):
			self.reorderEvents()
			return self.events[-1].duration + self.events[-1].startTime
		else :
			return None

	def addEvent(self,GSPatternEvent ):
		"""Add an event increasing duration if needed

		Args:
			GSPatternEvent : the event to be added
		"""
		self.events+=[GSPatternEvent]
		self.setDurationFromLastEvent()

	def quantize(self,beatDivision):
		""" Quantize events

		
		Args:
			beatDivision : the fraction of beat that we want to quantize to
		"""
		for e in self.events:
			e.startTime = int(e.startTime*beatDivision)*1.0/beatDivision
		
	def timeStretch(self,ratio):
		"""time  stretch a pattern

		Args:
			ratio : the ratio used for time stretching
		"""
		for e in self.events:
			e.startTime*=ratio
			e.duration*=ratio
		self.duration *=ratio 



	def getStartingEventsAtTime(self,time,tolerance = 0):
		""" Get all events activating at a givent time

		Args:
			time: time asked for 
			tolerance: admited deviation of start time 
		Returns:
			list of events
		"""
		res = []
		for e in self.events:
			if(time - e.startTime>=0 and time - e.startTime<=tolerance ):
				res+=[e]
		return res

	def getActiveEventsAtTime(self,time):
		""" Get all events currently active at a givent time

		Args:
			time: time asked for 
			tolerance: admited deviation of start time 
		Returns:
			list of events
		"""
		res = []
		for e in self.events:
			if(time-e.startTime>=0 and time-e.startTime<=e.duration ):
				res+=[e]
		return res


	def copy(self):
		""" Deepcopy a pattern
		"""
		return copy.deepcopy(self)

	def getACopyWithoutEvents(self):
		""" copy all fields but events

			useful for creating patterns from patterns
		"""
		p = GSPattern();
		p.duration =self.duration;
		p.bpm =self.bpm ;
		p.timeSignature =self.timeSignature ;
		p.originFilePath=self.originFilePath;
		p.name=self.name;
		return p

	def getAllTags(self):
		""" Returns all used tags in this pattern

		Returns:
			list of string composed of all possible tags
		"""
		tags = []
		for e in self.events:
			for  t in e.tags:
				if not t in tags:
					tags+=[t];
		return tags

	def getPatternWithTags(self,tags,exactSearch=True,copy=True):
		"""Returns a sub-pattern with the given tags

		Args:
			tags: string list : tags to be checked for
			exactSearch: bool : if True the tags have to be exactly the same, else they can be included in events Tags
			copy: do we return a copy of original events (avoid modifying originating events when modifying the returned subpattern)
		Returns:
			a GSPattern with only events that tags corresponds to given tags
		"""
		res = self.getACopyWithoutEvents();
		for e in self.events:
			if exactSearch: found = e.tags==tags;
			else: found = tags in e.tags
			if found:
				newEv = e if not copy else e.copy()
				res.events+=[newEv]
		return res


	def alignOnGrid(self,stepSize,repeatibleTags = ['silence']):
		""" align this pattern on a temporal grid
		
		very useful to deal with step-sequenced pattern : 
			- all events durations are shortened to stepsize
			- all events startTimes are quantified to stepsize

		repeatibleTags allow to deal with `silences type` of events :
			- if a silence spread over more than one stepsize, we generate an event for each stepSize

		thus each step is ensured to be filled with one distinct event at least
		Args:
			stepSize: temporal definition of the grid
		"""
		
		newEvents = []
		for e in self.events:
			if e.tagsAre(repeatibleTags):
				evToAdd = e.cutInSteps(stepSize)
			else:
				evToAdd = [e]
			for ea in evToAdd:
				ea.startTime = int(ea.startTime/stepSize+0.5)*stepSize
				ea.duration = stepSize
				newEvents+=[ea]
		self.events = newEvents

	def removeOverlapped(self):
		"""remove overlapped elements

		"""
		self.reorderEvents();
		newList = []; idx = 0;
		for e in self.events:
			found = False
			for i in range(idx+1,len(self.events)):
				ee = self.events[i]
				if ee.tags==e.tags:
					found |= (ee.startTime>=e.startTime) and (ee.startTime < e.startTime+e.duration)
				if ee.startTime>(e.startTime+e.duration):
					break
			if not found :
				newList+=[e]
			idx+=1
		self.events = newList


	def getAllIdenticalEvents(self,event,allTagsMustBeEquals = True):
		""" Get a list of event with same tags

		Args:
			event:event to compare with
			allTagsMustBeEquals : shall we get exact tags equality or be fine with one common tag
		Returns:
			list of events that have all or one tags in common
		"""
		res = []
		for e in self.events:
			equals = False;
			equals = event.allTagsAreEqualWith(e) if allTagsMustBeEquals else event.hasOneCommonTagWith(e)

			if equals:
				res+=[e]

			

	def fillWithSilences(self,maxSilenceTime = 0,perTag=False,silenceTag = 'silence'):
		""" Fill empty (i.e no event ) spaces with silence event

		Args:
			maxSilenceTime : if positive value is given, will add multiple silence of maxSilenceTime for empty time larger than maxSilenceTime
			perTag: fill silence for each Tag
			silenceTag: tag that will be used when inserting the silence event 

		"""
		
		
		self.reorderEvents();
		

		def _fillListWithSilence(list,silenceTag):
			lastOff = 0
			newEvents = []
			for e in self.events:
				if e.startTime>lastOff:
					if maxSilenceTime>0:
						while e.startTime-lastOff>maxSilenceTime:
							newEvents+=[GSPatternEvent(lastOff,maxSilenceTime,0,0,[silenceTag])]
							lastOff+=maxSilenceTime 
					newEvents+= [GSPatternEvent(lastOff,e.startTime-lastOff,0,0,[silenceTag])]
				newEvents+=[e]
				lastOff = max(lastOff,e.startTime+e.duration)

			if lastOff<self.duration:
				if maxSilenceTime>0:
					while lastOff<self.duration-maxSilenceTime:
						newEvents+=[GSPatternEvent(lastOff,maxSilenceTime,0,0,[silenceTag])]
						lastOff+=maxSilenceTime 
				newEvents+= [GSPatternEvent(lastOff,self.duration-lastOff,0,0,[silenceTag])]

			return newEvents


		if not perTag:
			self.events = _fillListWithSilence(self.events,silenceTag);
		else:
			allEvents = []
			for t in self.getAllTags():
				allEvents+=_fillListWithSilence(self.getPatternWithTags(tags=[t],exactSearch=False,copy = False),silenceTag)
			self.events = allEvents



	def getPatternForTimeSlice(self,startTime,length,trimEnd = True):
		""" Returns a pattern within given timeslice

		Args:
			startTime: start time for time slice
			length: length of time slice
			trimEnd: cut any events that ends after startTime + length
		Returns:
			a new GSpattern within time slice
		"""
		p = self.getACopyWithoutEvents()
		p.duration = length;
		for e in self.events:
			if e.startTime - startTime>=0 and e.startTime-startTime<length:
				newEv = e.copy()
				newEv.startTime-=startTime
				p.events +=[newEv]
		if trimEnd:
			for e in p.events:
				toCrop = e.startTime+e.duration - length
				if toCrop>0:
					e.duration-=toCrop;
		return p



	def printEvents(self):
		""" Nicely print out the list of events

		each line represents an event formatted as  : tags pitch startTime duration
		"""
		for e in self.events:
			print e.tags,'\t', e.pitch,'\t', e.startTime,'\t', e.duration

	def toJSONDict(self):
		""" gives a standard dict for json output
		"""
		res = {}
		self.setDurationFromLastEvent()
		allTags =self.getAllTags()
		res['eventTags'] = allTags
		res['timeInfo'] = {'duration':self.duration,'BPM':self.bpm}
		res['eventList'] = []
		def findIdxforTags(tags,allTags):
			return [allTags.index(x) for x in tags]
		for e in self.events:
			res['eventList']+=[{'on':e.startTime,'duration':e.duration,'pitch':e.pitch,'velocity':e.velocity,'tagsIdx':findIdxforTags(e.tags,allTags)}]
		return res
		

	def fromJSONDict(self,json):
		""" Loads a json API dict object to this pattern

		Args:
			json: a dict created from reading json file with GS API JSON format
		"""
		tags = json['eventTags']
		self.duration = json['timeInfo']['duration']
		self.bpm = json['timeInfo']['BPM']
		for e in json['eventList']:
			self.events+=[GSPatternEvent(e['on'],e['duration'],e['pitch'],e['velocity'],[tags[f] for f in e['tagsIdx']])]
		self.setDurationFromLastEvent()
		return self

	def splitInEqualLengthPatterns(self,desiredLength,copy=True):
		""" splits a pattern in consecutive equal length cuts

		Args:
			desiredLength: length desired for each pattern
			copy: retruns a distinc copy of original pattern events, if you don't need original pattern anymore setting it to False will increase speed

		Returns:
			a list of patterns of length desiredLength
		"""
		patterns = {}
		
		for e in self.events:
			p = int(e.startTime/desiredLength);
			numPattern = str(p)
			if numPattern not in patterns:
				patterns[numPattern] = self.getACopyWithoutEvents()
				patterns[numPattern].duration = desiredLength;
				patterns[numPattern].name = self.name + "_"+numPattern;
			newEv = e if not copy else e.copy();
			newEv.startTime-=p*desiredLength;
			patterns[numPattern].events+=[newEv];
		
		
		
		res = []
		for p in patterns:
			patterns[p].setDurationFromLastEvent();
			res+=[patterns[p]]

		return res;





	