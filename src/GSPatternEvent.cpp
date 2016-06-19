/*
  ==============================================================================

    GSPatternEvent.cpp
    Created: 8 Jun 2016 5:04:28pm
    Author:  martin hermant

  ==============================================================================
*/

#include "GSPatternEvent.h"


GSPatternEvent GSPatternEvent::empty;

vector<string>  GSPatternEvent::getTagNames() const{
	return eventTags;	
}

bool GSPatternEvent::isValid(){
    return duration>0 ;
}


