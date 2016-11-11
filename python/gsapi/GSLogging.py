import logging


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30
# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ  = "\033[1m"

USE_COLOR_OUTPUT = False
COLORS = {'WARNING': YELLOW,
          'INFO': WHITE,
          'DEBUG': BLUE,
          'CRITICAL': YELLOW,
          'ERROR': RED
          }


def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class ColoredLogger(logging.Logger):
    """Custom logger class with multiple destinations."""
    FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    # enable / disable colored output for console that suports
    
    useColor = USE_COLOR_OUTPUT
    COLOR_FORMAT = formatter_message(FORMAT, USE_COLOR_OUTPUT)

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)                
        color_formatter = ColoredFormatter(self.COLOR_FORMAT,self.useColor)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)
        return


gsapiLogger = logging.getLogger("gsapi")
logging.basicConfig(format="%(levelname)s: %(name)s: %(message)s")
logging.setLoggerClass(ColoredLogger)