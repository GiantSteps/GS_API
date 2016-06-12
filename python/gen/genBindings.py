import pybindgen
import sys


mod = pybindgen.Module('gsapi')

sourcePath = '../src/'
mod.add_include('"'+sourcePath+'GSPattern.h"')
cl = mod.add_class('GSPattern')
cl.add_constructor([])
cl.add_instance_attribute('originBPM', 'double')


# // write to file
mod.generate(sys.stdout)