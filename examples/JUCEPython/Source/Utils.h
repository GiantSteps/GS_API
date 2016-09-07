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

#include <dlfcn.h>
#include <stdio.h>



void* dummyFunc(){return nullptr;};
static String getVSTPath(){
  Dl_info dl_info;
  dladdr((void *)dummyFunc, &dl_info);
  String currentVSTPath =dl_info.dli_fname;
  return currentVSTPath;
}

static const PropertiesFile & getVSTProperties(){
	static File f(getVSTPath());
	static File propertiesFile = f.getChildFile("../../properties.xml");

	static PropertiesFile::Options o;
	static     PropertiesFile p(propertiesFile,o);
	if(!propertiesFile.exists()){
		p.setValue("dummy", "dum");
		p.save();
	}
	return p;
}
#endif  // UTILS_H_INCLUDED
