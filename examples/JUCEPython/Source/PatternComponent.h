/*
  ==============================================================================

    PatternComponent.h
    Created: 4 Jul 2016 7:20:08pm
    Author:  martin hermant

  ==============================================================================
*/

#ifndef PATTERNCOMPONENT_H_INCLUDED
#define PATTERNCOMPONENT_H_INCLUDED


#include "PyJUCEAPI.h"
#include "JuceHeader.h"
#include <set>



class BlockContainer:public Component{
	
	public :
	BlockContainer();
	bool displayPitchInsteadOfTags;
	void resized() override;
	void paint(Graphics &) override;
	void build();
	int gridBeatSubDiv;
	GSPattern * currentPattern;
	set <String> allEventsTags;
	
	double linePos;
};


class PatternComponent : public Component,public PyJUCEAPI::Listener,public TimeListener,Button::Listener{
public:
	PatternComponent();
	
	
	void newPatternLoaded( GSPattern * p) override;
	
	void timeChanged(double time)override;
	void paint(Graphics & g) override;
	void resized() override;
  void handleCommandMessage(int cid)override;
	TextButton displayTagToggle;
	BlockContainer blockContainer;

	
	
	void buttonClicked (Button*) override;
};


#endif  // PATTERNCOMPONENT_H_INCLUDED
