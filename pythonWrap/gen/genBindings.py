import pybindgen
from pybindgen import ReturnValue, Parameter, Module, Function, FileCodeSink
import sys
import os

def generate(buildPath):

	mod = pybindgen.Module('gsapi')

	sourcePath = '../src/'
	mod.add_include('"'+sourcePath+'GSPattern.h"')
	cl = mod.add_class('GSPattern')
	ev = mod.add_class('GSPatternEvent')
	ev.add_constructor([]);
	cl.add_constructor([])
	cl.add_instance_attribute('originBPM', 'double')
	cl.add_instance_attribute('length', 'double')
	cl.add_instance_attribute('timeSigNumerator', 'int')
	cl.add_instance_attribute('timeSigDenominator', 'int')
	vec = mod.add_container('std::vector<GSPatternEvent>', 'GSPatternEvent', 'vector',custom_name="VecEv")
	cl.add_instance_attribute('events','std::vector<GSPatternEvent>')
	# // write to file

	outFilePath = os.path.join(buildPath,"PyGSPattern.cpp")
	with open(outFilePath,'w') as f:
		mod.generate(f)