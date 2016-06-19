/*
 ==============================================================================

 GSPattern.cpp
 Created: 8 Jun 2016 9:11:22am
 Author:  martin hermant

 ==============================================================================
 */

#include "GSPattern.h"

GSPattern::GSPattern():duration(-1){};
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
    //	duration = timeInfo["duration"];
    //	allTags.initialize(j["eventTags"]);
    //
    //	for(auto & e:j["eventList"]){
    //		events.emplace_back(e["on"],e["duration"],e["pitch"],e["velocity"],e["tagsIdx"],&allTags);
    //	}
    return false;
};

void GSPattern::checkDurationValid(){

    bool isValid = (duration>0) ;
    if(!isValid){
        double lastNoteOff = getLastNoteOff();
        isValid = duration> lastNoteOff && (duration - lastNoteOff < 20.0);

        if(!isValid){
            duration = lastNoteOff;
        }
    }



}

double GSPattern::getLastNoteOff(){
    GSPatternEvent lastEv = getLastEvent();
    return (lastEv.isValid())?lastEv.start+ lastEv.duration : 0;
}

GSPatternEvent & GSPattern::getLastEvent(){
    return (events.size()>0) ? events[events.size()-1] : GSPatternEvent::empty;
}


bool GSPattern::getJSONData(const json & j) {
    json  timeInfo = j["timeInfo"];
    originBPM = timeInfo["BPM"].get<double>();
    timeSigNumerator = timeInfo["timeSignature"][0];
    timeSigDenominator = timeInfo["timeSignature"][1];
    duration = timeInfo["duration"];
    // allTags.initialize(j["eventTags"]);

    for(auto & e:j["eventList"]){
        events.emplace_back(e["on"],e["duration"],e["pitch"],e["velocity"],e["tagsIdx"]);
    }
    
    return true;
};