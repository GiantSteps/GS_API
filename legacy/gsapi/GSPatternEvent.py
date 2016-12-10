class GSPatternEvent(object):

    def __init__(self):
        self.tags = {}
        self.startTime = -1
        self.duration = -1
        self.pitch = -1
        self.velocity = -1

    def isTimeValid(self):
        return (self.startTime != -1) and (self.duration != -1)
