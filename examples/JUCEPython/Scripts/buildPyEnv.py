import os,sys
import subprocess
from subprocess import Popen

def getCmd(cmd):
	proc = Popen(cmd,shell = False,stdout=subprocess.PIPE);
	proc.wait()
	res = ""
	with proc.stdout as p:
		res+=p.readline()
	if( res[-1]=='\n') : res = res[:-1]
	return res

os.chdir('..')
pyEnvFolder = str(os.path.abspath('pythonEnv'))

print pyEnvFolder

print getCmd(['virtualenv','--version'])
print Popen(['virtualenv',pyEnvFolder],shell = False).wait()

print ('enable relocatable')
Popen(['virtualenv', '--relocatable',pyEnvFolder],shell = False).wait()

print('getting compile flags')


cFlags = getCmd([pyEnvFolder+'/bin/python-config','--cflags']);
linkerFlags = getCmd([pyEnvFolder+'/bin/python-config','--ldflags'])


print ('updating Jucer file')
import xml.etree.ElementTree as ET

JucerFile = os.path.abspath('JUCEPython.jucer')
tree = ET.parse(JucerFile)
root = tree.getroot()
for x in root.findall('EXPORTFORMATS')[0].findall('XCODE_MAC')[0].findall('CONFIGURATIONS')[0].findall('CONFIGURATION'):
	if not 'customXcodeFlags' in x.attrib:
		x.attrib['customXcodeFlags'] = ''
	old = x.attrib['customXcodeFlags']
	flags ={}
	for f in old.split(','):
		elem = f.split('=')
		if len(elem) and elem[0] != '':
			flags[elem[0]] = elem[1]
	flags['PYCFLAGS'] = '"'+cFlags+'"'
	flags['PYLDFLAGS'] = '"'+linkerFlags+'"'
	flags['PYENVPATH'] = pyEnvFolder

	x.attrib['customXcodeFlags'] = ''
	for k,v in flags.iteritems():
		x.attrib['customXcodeFlags']+= str(k)+"="+str(v)+','
	x.attrib['customXcodeFlags'] = x.attrib['customXcodeFlags'][:-1]
	print flags


tree.write(JucerFile)
# with open(pyEnvFolder+"/flags",'w') as f:
# 	f.write('# auto generated file from buildPyEnv.py : do not modify !!!!!\n\n')
# 	f.write('export PYLINKFLAGS=\"'+str(linkerFlags)+'\"\n')
# 	f.write('export PYCFLAGS=\"'+str(cFlags)+'\"\n')
# print linkerFlags