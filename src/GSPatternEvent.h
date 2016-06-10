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


// defines a bank of possible names and Ids for an event
// allow fast comparison and retrieval of ids without having to deal with strings
class GSPatternEventTags{
public:
	string getTagForId(int i);
	int getIdForTag(string tag);
	vector<int> getOrAddTagIds(const vector<string> &newTags);
	void initialize(const vector<string> &);
	void clear();
	
private:
	vector<string> tags;
};


class GSPatternEvent{
public:
	
	GSPatternEvent(const double _onTime,
				   const double _length,
				   const int _pitch,
				   const int _velocity,
				   const vector<int> & _eventIds,
				   GSPatternEventTags * _Ids
				   )
	:
	onTime(_onTime),
	length(_length),
	pitch(_pitch),
	velocity(_velocity),
	eventTags(_eventIds),
	ids(_Ids)
	{}
	
	
	double onTime;
	double length;
	int pitch;
	int velocity;
	vector<int> eventTags;
	
	
	 vector<string> getTagNames() const;
	
private:
	GSPatternEventTags * ids;
};



#endif  // GSPATTERNEVENT_H_INCLUDED
