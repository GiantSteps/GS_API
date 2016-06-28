from GSPattern import *
from GSStyle import *
from GSInternalStyles import *

if __name__ == '__main__':
	p = GSPattern()
	p.addEvent(GSPatternEvent(0,2,60,100))
	p.addEvent(GSPatternEvent(1,1,60,100))

	print p.duration