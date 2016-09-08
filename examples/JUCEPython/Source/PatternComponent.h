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

class VoicesContainer;
class VoiceComponent;


class BlockComponent:public Component{
public:
	BlockComponent(GSPatternEvent * ,VoiceComponent * _owner);
	void paint (Graphics& g)override;
	GSPatternEvent * evt;
	VoiceComponent * owner;
	void mouseDown (const MouseEvent& e)override;
	void mouseDrag (const MouseEvent& e)override;
	void mouseUp(const MouseEvent & e)override;
	
};

class VoiceComponent:public Component{
public:
	VoiceComponent(String _tag,VoicesContainer * container,bool _displayPitch);
	
	GSPattern * getPattern();
	vector<GSPatternEvent *> getVoiceEvents();
	void update();
	void paint(Graphics &) override;
	OwnedArray<BlockComponent> blocks;
	VoicesContainer * owner;
	String tag;
	void resized()override;
	Colour & getColour();
	bool displayPitch;
};

class VoicesContainer:public Component{
	
	public :
	VoicesContainer();
	bool displayPitchInsteadOfTags;
	void resized() override;
	void paint(Graphics &) override;
	void build();
	void setPattern(GSPattern *);
	int gridBeatSubDiv;
	GSPattern  pattern;
	set <String> allEventsTags;
	OwnedArray<VoiceComponent> voices;
	map<String,Colour> tagsColours;
	Colour & getColourForVoice(String tag);
	Colour defaultColor;
	double linePos;
	
	class BlockDragger : public ComponentBoundsConstrainer{
	public:
		BlockDragger(VoicesContainer * _owner):owner(_owner){};
		void checkBounds (Rectangle<int>& bounds,
                              const Rectangle<int>& previousBounds,
                              const Rectangle<int>& limits,
                              bool isStretchingTop,
                              bool isStretchingLeft,
                              bool isStretchingBottom,
                              bool isStretchingRight)override;
		
		void startDraggingBlock(BlockComponent * ,const MouseEvent & );
		void draggingBlock(BlockComponent * ,const MouseEvent &);
		void endDraggingBlock();
	
private:
		VoiceComponent * targetVoice ;
	VoicesContainer * owner;
		ComponentDragger dragger;
		BlockComponent * originComponent;
		


};
	BlockDragger blockDragger;
	

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
	VoicesContainer voicesContainer;

	class Listener{
	public:
		virtual ~Listener(){};
		virtual void patternChanged(PatternComponent * ) = 0;
	};
	ListenerList<Listener> patternListeners;
	void addPatternListener(Listener * l){patternListeners.add(l);}
	void	removePatternListener(Listener * l){patternListeners.remove(l);}
	void buttonClicked (Button*) override;
	GSPattern * getPattern();
	
private:
	GSPattern * nextPatternToLoad;
};


#endif  // PATTERNCOMPONENT_H_INCLUDED
