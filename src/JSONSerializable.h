/*
  ==============================================================================

    JSONImport.h
    Created: 8 Jun 2016 9:11:11am
    Author:  martin hermant

  ==============================================================================
*/

#ifndef JSONSERIALIZABLE_H_INCLUDED
#define JSONSERIALIZABLE_H_INCLUDED

#include "json.hpp"
#include <fstream>


using namespace nlohmann;
using namespace std;

class JSONSerializable{
	
public:
	
	
	JSONSerializable(){};
	virtual ~JSONSerializable(){};
	
	
	// called from host for saving / loading JSONSerializable objects
	bool loadJSON(string path);
	bool saveJSON(string path);
	
	
	// derived class should provide implementation of these
	virtual bool fillJSONData(json &) = 0;
	virtual bool getJSONData(const json &) = 0;
	
	

	
};



#endif  // JSONSERIALIZABLE_H_INCLUDED
