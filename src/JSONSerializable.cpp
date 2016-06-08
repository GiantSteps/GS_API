/*
  ==============================================================================

    JSONSerializable.cpp
    Created: 8 Jun 2016 9:11:11am
    Author:  martin hermant

  ==============================================================================
*/

#include "JSONSerializable.h"


bool JSONSerializable::loadJSON(string path){
	bool success = true;
	std::fstream fs;
	fs.open (path, std::fstream::in );
	
	json j;
	j<<fs;
	success &=!j.is_null();
	success&=getJSONData(j);
	return success;
}