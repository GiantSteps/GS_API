from GSLogging import gsapiLogger
from GSPattern import GSPatternEvent, GSPattern
from GSBassmineAnalysis import *
from GSBassmineMarkov import *
from GSDataset import GSDataset
from gsapi.GSBase import *
from GSDescriptors import *
from GSIO import *
from GSInternalStyles import *
from MidiMap import *



if __name__ == '__main__':
	p = GSPattern()
	p.addEvent(GSPatternEvent(0,2,60,100))
	p.addEvent(GSPatternEvent(1,1,60,100))
	# logger.setLevel(level=logging.ERROR)
	# logger.warning( p.duration)