# python 3 compatibility
from __future__ import absolute_import, division, print_function

import logging



class GSBaseDescriptor(object):

    def __init__(self):
        pass

    def getDescriptorForPattern(self, pattern):
        """Compute a unique value for a given pattern,
        which can be a sliced part of a bigger one.
        """
        raise NotImplementedError("Should have implemented this")

    def configure(self, paramDict):
        """Configure current descriptor mapping dict to parameters"""
        raise NotImplementedError("Should have implemented this")
