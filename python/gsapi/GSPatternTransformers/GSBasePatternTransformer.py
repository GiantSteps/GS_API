# python 3 compatibility
from __future__ import absolute_import, division, print_function

from ..GSPattern import GSPattern


class GSBasePatternTransformer(object):
    """Base class for defining a transform algorithm.

    such class needs to provide the following functions:
        - configure: configure current transformer based on implementation
        specific parameters passed in the dict argument
        - transformPattern: return a transformed version of GSPattern
    """
    def __init__(self):
        self.type = "None"

    def configure(self, paramDict):
        """Configure current transformer based on implementation
        specific parameters passed in paramDict argument.

        Args:
            paramDict: a dictionary with configuration values.
        """
        raise NotImplementedError("Should have implemented this")

    def transformPattern(self, pattern):
        """Return a transformed GSPattern

        Args:
            pattern: the GSPattern to be transformed.
        """
        raise NotImplementedError("Should have implemented this")
