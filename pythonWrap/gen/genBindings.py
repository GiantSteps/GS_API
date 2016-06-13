import pybindgen
from pybindgen import ReturnValue, Module,Parameter, Function, FileCodeSink

import sys
import os

def generate(buildPath):
	
	
	mod = pybindgen.Module('gsapi')

	sourcePath = '../src/'
	mod.add_include('"'+sourcePath+'GSPattern.h"')
	cl = mod.add_class('GSPattern')
	cl.add_constructor([])

	ev = mod.add_class('GSPatternEvent')

	vecTags = mod.add_container('std::vector<std::string>', 'std::string', 'vector',custom_name="VecTags")

	cl.add_instance_attribute('name','std::string')
	ev.add_constructor([]);
	ev.add_constructor([Parameter.new('double','start'),
		Parameter.new('double','length'),
		Parameter.new('int','pitch'),
		Parameter.new('int','velocity'),
		Parameter.new('std::vector<std::string>','tags')]);

	ev.add_instance_attribute('length','double');
	ev.add_instance_attribute('start','double');
	ev.add_instance_attribute('pitch','int');
	ev.add_instance_attribute('velocity','int');
	ev.add_instance_attribute('eventTags','std::vector<std::string>');

	cl.add_instance_attribute('originBPM', 'double')
	cl.add_instance_attribute('length', 'double')
	cl.add_instance_attribute('timeSigNumerator', 'int')
	cl.add_instance_attribute('timeSigDenominator', 'int')
	vecEv = mod.add_container('std::vector<GSPatternEvent>', 'GSPatternEvent', 'vector',custom_name="VecEv")
	cl.add_method('events.size();cout<< PyLong_Check(retval) << endl;int','unsigned long',[],custom_name='__len__');
	# cl.add_method('events.at','GSPatternEvent',[Parameter.new('int','num')],custom_name='__getitem__')

	cl.add_instance_attribute('events','std::vector<GSPatternEvent>')
	cl.add_method('addEvent', None, [Parameter.new('GSPatternEvent&','event')])
	# // write to file

	outFilePath = os.path.join(buildPath,"PyGSPattern.cpp")

	with open(outFilePath,'w') as f:
		mod.generate(f)

if __name__ == '__main__':
	import logging
	logging.basicConfig(filename ='log.log', level=logging.DEBUG)
	generate("../generated")