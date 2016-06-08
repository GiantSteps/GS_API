/*
  ==============================================================================

    GSStyle.h
    Created: 8 Jun 2016 9:11:32am
    Author:  martin hermant

  ==============================================================================
*/

#ifndef GSSTYLE_H_INCLUDED
#define GSSTYLE_H_INCLUDED

#include "JSONSerializable.h"

class GSStyle:public JSONSerializable{
public:
	GSStyle();
	virtual ~GSStyle();
	
	
	virtual bool fillJSONData(json &) override;
	virtual bool getJSONData(const json &) override;
};


#endif  // GSSTYLE_H_INCLUDED
