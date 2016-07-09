
import copy

"""Documentation for GSPattern module.

GSPattern
"""
class GSPatternEvent(object):
	"""Represent an event of a GSPattern

	an event is made of start and length , origin pitch , velocity and associated tags
	
	Args:
		start: startTime of event
		duration: duration of event
		pitch : pitch of event
		velocity: velocity of event
		tags: list of tags representing the event

	Attributes:
		startTime: startTime of event
		duration: duration of event
		pitch : pitch of event
		velocity: velocity of event
		tags: list of tags representing the event
	"""


	def __init__(self,start,duration,pitch,velocity=127,tags=[]):
		self.duration = duration
		if not isinstance(tags,list):tags = [tags]
		self.tags=tags
		self.startTime = start;
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


	def checkDuration(self):
		""" Verify that duration member is consistent 

		if inner events have a bigger time span than self.duration, increase duration to fit
		"""
		total = self.getLastNoteOff();
		if (total and (total > self.duration)):
			# print "resizing : "+str(total) +'old : '+ str(self.duration)
			self.duration = total

	def reorderEvents(self):
		""" ensure than our events are time sorted 
			
			can be useful for some algorithm
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
		self.checkDuration()

	def quantize(self,beatDivision,postMultiplier=1.0):
		""" Quantize events

		
		:param float beatDivision : the fraction of beat that we want to quantize to
		"""
		for e in self.events:
			e.startTime = int(e.startTime*beatDivision)*1.0*postMultiplier/beatDivision
		

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

	def getActiveEventAtTime(self,time):
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

	def discretize(self,stepSize,repeatibleTags = ['silence']):
		""" Discretize a pattern

		"""
		
		newEvents = []
		for e in self.events:
			if e.tagsAre(repeatibleTags):
				evToAdd = e.cutInSteps(stepSize)
			else:
				evToAdd = [e]
			for ea in evToAdd:
				ea.startTime = int(ea.startTime/stepSize)*stepSize
				ea.duration = stepSize
				newEvents+=[ea]
		self.events = newEvents


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
			if (allTagsMustBeEquals) : equals = event.allTagsAreEqualWith(e)
			else  : equals = event.hasOneCommonTagWith(e)

			if equals:
				res+=[e]

			

	def fillWithSilences(self,desiredLength,silenceTag = 'silence'):
		""" Fill empty (i.e no event active) spaces with silence event

		Args:
			silenceTag: tag that will be used when inserting the silence event 

		"""
		newEvents = []
		lastOff = 0;
		for e in self.events:
			if e.startTime>lastOff:
				silence = GSPatternEvent(lastOff,e.startTime-lastOff,0,0,[silenceTag])
				newEvents+= [silence]
			newEvents+=[e]
			lastOff = max(lastOff,e.startTime+e.duration)
		if lastOff<desiredLength:
			newEvents += [GSPatternEvent(lastOff,desiredLength-lastOff,0,0,[silenceTag])]
		self.events = newEvents;

	def getPatternForTimeSlice(self,startTime,length,trimEnd = True):
		""" Returns a pattern within given timeslice

		Args:
			startTime: start time for time slice
			length: length of time slice
		Returns:
			a new GSpattern within time slice
		"""
		p = self.copy()
		p.duration = length;
		p.events = []
		for e in self.events:
			if e.startTime - startTime>=0 and e.startTime-startTime<length:
				newEv = e.copy()
				newEv.startTime-=startTime
				p.events +=[newEv]
		if trimEnd:
			for e in p.events:
				toCrop = e.startTime+e.duration - startTime+length
				if toCrop>0:
					e.duration-=toCrop;
		return p



	def printEvents(self):
		""" Nicely print out an event
		"""
		for e in self.events:
			print e.tags , e.startTime , e.duration,e.pitch

	def toJSONDict(self):
		""" gives a standard dict for json output
		"""
		res = {}
		self.checkDuration()
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
		self.checkDuration()
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
			if copy:
				newEv = e.copy();
			else:
				newEv = e;
			newEv.startTime-=p*desiredLength;
			patterns[numPattern].events+=[newEv];
		
		
		
		res = []
		for p in patterns:
			patterns[p].checkDuration();
			res+=[patterns[p]]

		return res;





	