/*
  ==============================================================================

    GSPattern.cpp
    Created: 8 Jun 2016 9:11:22am
    Author:  martin hermant

  ==============================================================================
*/

#include "GSPattern.h"

GSPattern::GSPattern(){};
GSPattern::~GSPattern(){};
// void GSPattern::addEvent(const vector<string> & tags,GSPatternEvent && event){
// 	event.eventTags = allTags.getOrAddTagIds(tags);
// 	events.emplace_back(event);
// }



void GSPattern::addEvent(GSPatternEvent & event){
	events.emplace_back(event);
}

bool GSPattern::fillJSONData(json & j) {
//	json  timeInfo = j["timeInfo"];
//	originBPM = timeInfo["BPM"].get<double>();
//	timeSigNumerator = timeInfo["timeSignature"][0];
//	timeSigDenominator = timeInfo["timeSignature"][1];
//	length = timeInfo["length"];
//	allTags.initialize(j["eventTags"]);
//	
//	for(auto & e:j["eventList"]){
//		events.emplace_back(e["on"],e["length"],e["pitch"],e["velocity"],e["tagsIdx"],&allTags);
//	}
		return false;
};


bool GSPattern::getJSONData(const json & j) {
	json  timeInfo = j["timeInfo"];
	originBPM = timeInfo["BPM"].get<double>();
	timeSigNumerator = timeInfo["timeSignature"][0];
	timeSigDenominator = timeInfo["timeSignature"][1];
	length = timeInfo["length"];
	// allTags.initialize(j["eventTags"]);
	
	for(auto & e:j["eventList"]){
		events.emplace_back(e["on"],e["length"],e["pitch"],e["velocity"],e["tagsIdx"]);
	}
	
	return true;
};