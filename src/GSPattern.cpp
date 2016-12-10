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



void GSPattern::addEvent(GSPatternEvent * event){
    events.push_back(event);
}

bool GSPattern::fillJSONData(json & j) {
    //	json  timeInfo = j["timeInfo"];
    //	originBPM = timeInfo["bpm"].get<double>();
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
    GSPatternEvent  *lastEv = getLastEvent();
    return (lastEv && lastEv->isValid())?lastEv->start+ lastEv->duration : 0;
}
vector<GSPatternEvent*> GSPattern::getEventsWithTag(string tag){
	vector<GSPatternEvent*> res;
	for(auto & e:events){
		for(auto & t:e->eventTags){
			if(t==tag){
				res.push_back(e);
				break;
			}
		}
	}
	return res;
}

vector<GSPatternEvent*> GSPattern::getEventsWithPitch(int pitch){
	vector<GSPatternEvent*> res;
	for(auto & e:events){
			if(e->pitch==pitch){
				res.push_back(e);

		}
	}
	return res;
}
GSPattern GSPattern::getCopyWithoutEvents(){
	GSPattern p;
	p.name = name;
	p.duration = duration;
	p.timeSigDenominator = timeSigDenominator;
	p.timeSigNumerator = timeSigNumerator;
	p.originBPM = originBPM;
	return p;

}
GSPatternEvent * GSPattern::getLastEvent(){
    return (events.size()>0) ? events[events.size()-1] : nullptr;
}
bool GSPattern::removeEvent(GSPatternEvent * ev){
  auto it = find(events.begin(),events.end(),ev);
  bool found = it!=events.end();
  if(found){events.erase(it);}
  delete ev;
  return found;
}



bool GSPattern::getJSONData(const json & j) {
    json  timeInfo = j["timeInfo"];
    originBPM = timeInfo["bpm"].get<double>();
    timeSigNumerator = timeInfo["timeSignature"][0];
    timeSigDenominator = timeInfo["timeSignature"][1];
    duration = timeInfo["duration"];
    // allTags.initialize(j["eventTags"]);

    for(auto & e:j["eventList"]){
        events.push_back(new GSPatternEvent(e["on"],e["duration"],e["pitch"],e["velocity"],e["tagsIdx"]));
    }

    return true;
};
