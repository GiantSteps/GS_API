/*
  ==============================================================================

    JSONSerializer.cpp
    Created: 8 Jun 2016 9:11:11am
    Author:  martin hermant

  ==============================================================================
*/

#include "JSONSerializer.h"

#include "GSPattern.h"
#include "GSStyle.h"




json getJSONFromFile(string path){
	bool success = true;
	std::fstream fs;
	fs.open (path, std::fstream::in );
	
	json j;
	j<<fs;
	return j;
}


//template<GSPattern>
template<> GSPattern loadJSON<GSPattern>(string path){
	json j =getJSONFromFile(path);
	GSPattern p;
	json timeInfo = j["timeInfo"];
	p.originBPM = timeInfo["BPM"].get<double>();
	p.timeSigNumerator = timeInfo["timeSignature"][0];
	p.timeSigDenominator = timeInfo["timeSignature"][1];
	p.length = timeInfo["length"];
	p.allTags.initialize(j["eventTags"]);
	
	for(auto & e:j["eventList"]){
		p.events.emplace_back(e["on"],e["length"],e["pitch"],e["velocity"],e["tagsIdx"],&p.allTags);
	}
	
	return p;
};
