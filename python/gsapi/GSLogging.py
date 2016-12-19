from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import logging


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30
# These are the sequences need to get colored output
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ  = "\033[1m"
COLORS = {'WARNING': YELLOW,
          'INFO': WHITE,
          'DEBUG': BLUE,
          'CRITICAL': YELLOW,
          'ERROR': RED
          }


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):

        levelname = record.levelname
        if ColoredLogger.USE_COLOR_OUTPUT and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
            record.boldSeq = BOLD_SEQ
            record.resetSeq = RESET_SEQ
        else:
            record.boldSeq = ""
            record.resetSeq = ""

        return logging.Formatter.format(self, record)


class ColoredLogger(logging.Logger):
    """Custom logger class with multiple destinations."""
    USE_COLOR_OUTPUT = False
    FORMAT = "[%(boldSeq)s%(name)-15s%(resetSeq)s][%(levelname)-8s]  %(message)s (%(boldSeq)s%(filename)s%(resetSeq)s:%(lineno)d)"
    color_formatter = ColoredFormatter(FORMAT)
    consoleHandler = logging.StreamHandler()

    consoleHandler.setFormatter(color_formatter)
    
    def __init__(self, name):
        logging.Logger.__init__(self, name)
        return


logging.setLoggerClass(ColoredLogger)
gsapiLogger = logging.getLogger("gsapi")

# handler is only on the root to avoid logs duplications while propagating to the root
if not len(gsapiLogger.handlers):
    gsapiLogger.addHandler(ColoredLogger.consoleHandler)
else:
    # for debugging purpose this line can be commented out but
    # when using local and global version of gsapi at the same time, this line is triggered some times
    raise ImportError("double import of GSLogging, should never happen")
    pass


def setDefaultLoggingLevel(lvl):
    """ sets the default log level if not defined inner each module
    Args:
        lvl: one of default python's logging levels : logging.[CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET]
    """
    gsapiLogger.setLevel(lvl)

setDefaultLoggingLevel(logging.WARNING)
def setUseColoredOutput(useColor):
    """ Enable or not colored console output powerful in the console, but annoying otherwise
    Args:
        useColor: do we use colored output
    """
    ColoredLogger.USE_COLOR_OUTPUT = useColor