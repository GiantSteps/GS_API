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
Popen(['virtualenv', '--relocatable',pyEnvFolder],shell = False).wait()


Popen([pyEnvFolder+'/bin/python2.7','/Users/Tintamar/Dev/GS_API/python/setup.py','build'],shell = False).wait()
print 'installing to dist'
Popen([pyEnvFolder+'/bin/pip2.7','install','--upgrade','/Users/Tintamar/Dev/GS_API/python'],shell = False).wait()




Popen(['touch', pyEnvFolder],shell = False).wait()

print('getting compile flags')


cFlags = getCmd([pyEnvFolder+'/bin/python-config','--cflags']);
linkerFlags = getCmd([pyEnvFolder+'/bin/python-config','--ldflags'])

#  remove flags that can be overriden in Jucer (isysroot messes xcode indexing...)
argToKeep = ['I']
print 'original cflags : '+cFlags
if '-isysroot' in cFlags:
	print 'removing sysroot'
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
	flags['PYLDFLAGS'] = '"'+linkerFlags+'"'
	flags['PYENVPATH'] = pyEnvFolder

	x.attrib['customXcodeFlags'] = ''
	for k,v in flags.iteritems():
		x.attrib['customXcodeFlags']+= str(k)+"="+str(v)+','
	x.attrib['customXcodeFlags'] = x.attrib['customXcodeFlags'][:-1]
	


tree.write(JucerFile)
