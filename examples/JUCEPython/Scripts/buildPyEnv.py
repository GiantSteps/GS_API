import os,sys
import subprocess
from subprocess import Popen

import inspect, os
scriptPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 


def getCmd(cmd,useShell=False):
	proc = Popen(cmd,shell = useShell,stdout=subprocess.PIPE);
	proc.wait()
	res = ""
	with proc.stdout as p:
		res+=p.readline()
	if( res and res[-1]=='\n') : res = res[:-1]
	return res

JUCEPyFolder = os.path.abspath(os.path.join(scriptPath,os.pardir));
GSAPIPythonFolder = os.path.abspath(os.path.join(JUCEPyFolder,os.pardir,os.pardir,"python"));
print GSAPIPythonFolder
os.chdir(JUCEPyFolder)
pyEnvFolder = str(os.path.abspath('pythonEnv'))

print pyEnvFolder

print getCmd(['virtualenv','--version'])
print Popen(['virtualenv','--always-copy',pyEnvFolder],shell = False).wait()
Popen(['virtualenv', '--relocatable',pyEnvFolder],shell = False).wait()
try:
	oldEnv = os.environ.copy()
	activateScript = os.path.abspath(os.path.join(pyEnvFolder,'bin','activate_this.py'));
	execfile(activateScript, dict(__file__=activateScript))
	# print "switching pyenv ", activateScript, getCmd(['source '+activateScript],useShell=True)

	Popen([pyEnvFolder+'/bin/python2.7',os.path.join(GSAPIPythonFolder,'setup.py'),'build'],shell = False).wait()
	

	print 'installing to dist'
	
	Popen([pyEnvFolder+'/bin/pip2.7','install','--upgrade','--force-reinstall',GSAPIPythonFolder],shell = False).wait()

finally:
	print "end configuring python"
	os.environ = oldEnv
	#print getCmd(['deactivate'],useShell=True)


Popen(['touch', pyEnvFolder],shell = False).wait()

print('getting compile flags')


cFlags = getCmd([pyEnvFolder+'/bin/python-config','--cflags']);
linkerFlags = getCmd([pyEnvFolder+'/bin/python-config','--ldflags'])

#  remove flags that can be overriden in Jucer (isysroot messes xcode indexing, other are useless...)
argToKeep = ['I']

# if '-isysroot' in cFlags:
print 'removing useless cflags from : '+cFlags
argList =  cFlags[1:].split(' -')
newList = []
for a in argList:
	found = False
	for aa in argToKeep:
		if aa == a[0:len(aa)]:
			newList+=[a]
			break

newCFlags = '-'+' -'.join(newList)
print 'keeped cflags :'+newCFlags

print 'removing useless linkerflags from : '+linkerFlags
argList =  linkerFlags.split(' ')
argList.remove('-ldl')
newLFlags =' '.join(argList)

print 'linker flags : '+newLFlags



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
	flags['PYCFLAGS'] = '"'+newCFlags+'"'
	flags['PYLDFLAGS'] = '"'+newLFlags+'"'
	flags['PYENVPATH'] = pyEnvFolder

	x.attrib['customXcodeFlags'] = ''
	for k,v in flags.iteritems():
		x.attrib['customXcodeFlags']+= str(k)+"="+str(v)+','
	x.attrib['customXcodeFlags'] = x.attrib['customXcodeFlags'][:-1]
	


tree.write(JucerFile)
