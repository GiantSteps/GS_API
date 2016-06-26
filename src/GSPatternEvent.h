/*
  ==============================================================================

    GSPatternEvent.h
    Created: 8 Jun 2016 4:46:34pm
    Author:  martin hermant

  ==============================================================================
*/

#ifndef GSPATTERNEVENT_H_INCLUDED
#define GSPATTERNEVENT_H_INCLUDED

#include <vector>
#include <string>
using namespace std;

class GSPatternEvent{
public:
    GSPatternEvent():duration(0){}
	GSPatternEvent(const double _start,
				   const double _duration,
				   const int _pitch,
				   const int _velocity,
				   const vector<string> & tags
				   )
	:
	start(_start),
	duration(_duration),
	pitch(_pitch),
	velocity(_velocity),
	eventTags(tags)
	{}
	
	
	double start;
	double duration;
	int pitch;
	int velocity;
	vector<string> eventTags;

    bool isValid();

    static GSPatternEvent empty;
	
	 vector<string> getTagNames() const;
	
};



#endif  // GSPATTERNEVENT_H_INCLUDED
