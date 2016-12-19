from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import unittest
from .. import GSLogging
from .GSPatternTestUtils import *
from .AgnosticDensityTest import *
from .DescriptorTests import *
from .GSIOTest import *
from .GSPatternTest import *
from .GSViewpointTest import *
from .MarkovPatternTest import *
from .GSStylesTest import *



if __name__ == "__main__":
	# shortcut to run all tests
		
		runTest(profile=False, getStat=False)
