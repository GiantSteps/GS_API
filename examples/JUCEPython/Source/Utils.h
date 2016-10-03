/*
  ==============================================================================

    Utils.h
    Created: 7 Sep 2016 6:45:13pm
    Author:  martin hermant

  ==============================================================================
*/

#ifndef UTILS_H_INCLUDED
#define UTILS_H_INCLUDED
#include "JuceHeader.h"


#include <stdio.h>



void* dummyFunc(){return nullptr;};
#ifdef JUCE_WINDOWS
#include <Shlwapi.h>
static String getVSTPath() {
	HMODULE hModule = GetModuleHandleW(NULL);
	WCHAR path[MAX_PATH];
	GetModuleFileNameW(hModule, path, MAX_PATH);
	return String(path);
}
#else
#include <dlfcn.h>
static String getVSTPath(){
  Dl_info dl_info;
  dladdr((void *)dummyFunc, &dl_info);
  String currentVSTPath =dl_info.dli_fname;
  return currentVSTPath;
}
#endif

PropertiesFile & getVSTProperties(){
	static File f(getVSTPath());
	static File propertiesFile = f.getChildFile("../../Resources/properties.xml");

	static PropertiesFile::Options o;
	static     PropertiesFile p(propertiesFile,o);
	if(!propertiesFile.exists()){
		p.setValue("pythonBin", "");
    p.setValue("pythonHome", "");
		p.setValue("VSTPythonFolderPath", "default");
		p.setValue("VSTName", "JPython");
		p.save();
	}
	return p;
}
#endif  // UTILS_H_INCLUDED
