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
	
	GSPatternEvent(const double _start,
				   const double _length,
				   const int _pitch,
				   const int _velocity,
				   const vector<string> & tags,
				   )
	:
	start(_start),
	length(_length),
	pitch(_pitch),
	velocity(_velocity),
	eventTags(_eventIds)
	{}
	
	
	double start;
	double length;
	int pitch;
	int velocity;
	vector<string> eventTags;
	
	
	 vector<string> getTagNames() const;
	
};



#endif  // GSPATTERNEVENT_H_INCLUDED
