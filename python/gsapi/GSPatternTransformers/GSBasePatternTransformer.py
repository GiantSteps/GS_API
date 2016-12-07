from gsapi.GSPattern import GSPattern


class GSBasePatternTransformer(object):
    """Base class for defining a transform algorithm.

    such class needs to provide following functions:
        - configure: configure current transformer based on implementation specific parameters passed in dict argument
        - transformPattern: return a transformed version of GSPattern
    """
    def __init__(self):
        self.type = "None"

    def configure(self, paramDict):
        """Configure current transformer based on implenmentation specific parameters passed in dict argument.

        Args:
            paramDict: a dictionary filed with configuration values.
        """
        raise NotImplementedError("Should have implemented this")

    def transformPattern(self, pattern):
        """Returns a transformed version of GSPattern

        Args:
            pattern : the pattern to be transformed
        """
        raise NotImplementedError("Should have implemented this")
