"""
The GS_API is a Python/C++ library for manipulating musical symbolic data.
all modules are documented, for more infos on the given module 
type:

>> help(gsapi.modulename)

online tutorials and documentation:
    https://giantsteps.github.io/GS_API

source code:
    https://github.com/GiantSteps/GS_API
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import logging
from .GSAPIVersion import *
from .GSLogging import gsapiLogger
from . import GSPitchSpelling
from . import GSPatternUtils
from .GSPattern import GSPatternEvent, GSPattern
from .GSDataset import GSDataset
from . import GSIO
from . import GSStyles 
from . import GSDescriptors
from . import GSPatternTransformers
# from . import GSBassmineAnalysis 
# from . import GSBassmineMarkov 




if __name__ == '__main__':
    p = GSPattern()
    p.addEvent(GSPatternEvent(0,2,60,100))
    p.addEvent(GSPatternEvent(1,1,60,100))
    # logger.setLevel(level=logging.ERROR)
    # logger.warning( p.duration)
