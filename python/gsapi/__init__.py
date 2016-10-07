from GSPattern import *
from GSStyle import *
from GSInternalStyles import *
from GSIO import *
from GSDataset import *
from GSDescriptor import *
from GSDescriptors import *


import logging

gsapiLogger = logging.getLogger("gsapi")
logging.basicConfig(format="%(levelname)s:%(name)s : %(message)s")

if __name__ == '__main__':
	p = GSPattern()
	p.addEvent(GSPatternEvent(0,2,60,100))
	p.addEvent(GSPatternEvent(1,1,60,100))
	# logger.setLevel(level=logging.ERROR)
	# logger.warning( p.duration)