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
	
	string name;
	double originBPM;
	int timeSigNumerator,timeSigDenominator;
	double length;
	

	vector<GSPatternEvent> events;
	
	// for dynamicly adding event
	// void addEvent(const vector<string> & tags,GSPatternEvent && );
	void addEvent(GSPatternEvent & );
	
	
    void checkLengthValid();
    double getLastNoteOff();
    GSPatternEvent & getLastEvent();
private:
	
	
	 bool fillJSONData(json &) override;
	 bool getJSONData(const json &) override;
	
	
	
	
	
};


#endif  // GSPATTERN_H_INCLUDED
