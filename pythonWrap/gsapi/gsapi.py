
class GSPatternEvent(object):
	def __init__(self,start,duration,pitch,velocity=127,tags=[]):
		self.duration = duration
		self.tags=[]
		self.startTime = start;
		self.pitch = pitch;
		self.velocity = velocity
		self.tags = tags


class GSPattern(object):

	def __init__(self):
		self.duration = 0;
		self.events = [];
		self.bpm = 0;

	def checkDuration(self):
		total = self.getLastNoteOff();
		if (total and total > self.duration):
			self.duration = total

	def getLastNoteOff(self):
		if(len(self.events)):
			return self.events[-1].duration + self.events[-1].startTime
		else :
			return None

	def addEvent(self,GSPatternEvent ):
		self.events+=[GSPatternEvent]
		self.checkDuration()





if __name__ == '__main__':
	p = GSPattern()
	p.addEvent(GSPatternEvent(0,2,60,100))
	p.addEvent(GSPatternEvent(1,1,60,100))

	print p.duration