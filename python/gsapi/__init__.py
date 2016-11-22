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

import GSIO

import GSStyles 
import GSDescriptors 
import GSPatternTransformers
import GSBassmineAnalysis 
import GSBassmineMarkov 


# this is the full version name
# changing it will change version when uploading to pip and in the documentation
GSAPIFullVersion = u'1.0.1'


def getGSAPIFullVersion():
	"""helper to get full version name
	"""
	return GSAPIFullVersion


def getGSAPIShortVersion():
	"""helper to get only first two elements of full version name
	"""
	return u'.'.join(GSAPIFullVersion.split('.')[:2])



if __name__ == '__main__':
	p = GSPattern()
	p.addEvent(GSPatternEvent(0,2,60,100))
	p.addEvent(GSPatternEvent(1,1,60,100))
	# logger.setLevel(level=logging.ERROR)
	# logger.warning( p.duration)