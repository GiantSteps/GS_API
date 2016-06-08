/*
  ==============================================================================

    GSPattern.h
    Created: 8 Jun 2016 9:11:22am
    Author:  martin hermant

  ==============================================================================
*/

#ifndef GSPATTERN_H_INCLUDED
#define GSPATTERN_H_INCLUDED

#include "JSONSerializable.h"

#include "GSPatternEvent.h"

class GSPattern: public JSONSerializable{

public:
	GSPattern();
	virtual ~GSPattern();
	
	double originBPM;
	int timeSigNumerator,timeSigDenominator;
	double length;
	
	
	GSPatternEventTags allTags;
	vector<GSPatternEvent> events;
	
	// for dynamicly adding event
	void addEvent(const vector<string> & tags,GSPatternEvent && );
	void addEvent(GSPatternEvent && );
	
	
	
	

private:
	
	
	 bool fillJSONData(json &) override;
	 bool getJSONData(const json &) override;
	
	
	
	
	
};


#endif  // GSPATTERN_H_INCLUDED
