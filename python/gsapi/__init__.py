"""
The GS_API is a Python/C++ library for manipulating musical symbolic data.
all modules are documented, for more infos on the given module 
type :

 >> help(gsapi.modulename)


other useful resources :

 * online tutorials and documentation : https://giantsteps.github.io/GS_API
 * source code : https://github.com/GiantSteps/GS_API


"""

import logging
from GSLogging import gsapiLogger


import GSPatternUtils


from GSPattern import GSPatternEvent, GSPattern

from GSDataset import GSDataset
import GSBase 
import GSIO

import GSStyles 
import GSDescriptors 
import GSBassmineAnalysis 
import GSBassmineMarkov 




if __name__ == '__main__':
	p = GSPattern()
	p.addEvent(GSPatternEvent(0,2,60,100))
	p.addEvent(GSPatternEvent(1,1,60,100))
	# logger.setLevel(level=logging.ERROR)
	# logger.warning( p.duration)