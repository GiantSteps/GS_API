/*
 ==============================================================================
 
 PatternComponent.cpp
 Created: 4 Jul 2016 7:20:08pm
 Author:  martin hermant
 
 ==============================================================================
 */

#include "PatternComponent.h"


PatternComponent::PatternComponent():TimeListener(1){
	addAndMakeVisible(blockContainer);
	addAndMakeVisible(displayTagToggle);
	displayTagToggle.setClickingTogglesState(true);
	displayTagToggle.setButtonText("display tags");
	displayTagToggle.setColour(TextButton::buttonOnColourId, Colours::orange);
	displayTagToggle.setToggleState(!blockContainer.displayPitchInsteadOfTags, dontSendNotification);
	displayTagToggle.addListener(this);
}

void PatternComponent::newPatternLoaded(GSPattern * p) {
	blockContainer.currentPattern = p;
	blockContainer.build();
	blockContainer.repaint();
}

void PatternComponent::paint(Graphics & g){
	g.setColour(Colours::darkgrey.darker());
	g.fillRect(getLocalBounds());
}

void PatternComponent::resized() {
	Rectangle<int> area = getLocalBounds();
	displayTagToggle.setBounds(area.removeFromBottom(20));
	blockContainer.setBounds(area);
}


void PatternComponent::timeChanged(double time){
	blockContainer.linePos = time;
	blockContainer.repaint();
	beatInterval = 1.0/(2*blockContainer.gridBeatSubDiv);
}

void PatternComponent::buttonClicked (Button* b) {
	if(b==&displayTagToggle){
		blockContainer.displayPitchInsteadOfTags = !b->getToggleState();
		blockContainer.build();
		blockContainer.repaint();
	}
};

//////////////////////////////////////

BlockContainer::BlockContainer(){
	currentPattern = nullptr;
	gridBeatSubDiv = 8;
	displayPitchInsteadOfTags = true;
}

void BlockContainer::resized(){
	
}


void BlockContainer::paint(Graphics & g){
	if (currentPattern && allEventsTags.size()>0 ) {
		Rectangle<int> area = getLocalBounds();
		Rectangle<int> leftTags = area.removeFromLeft(70);
		int step = leftTags.getHeight()/allEventsTags.size();
		for(auto & t:allEventsTags){
			g.drawFittedText(t, leftTags.removeFromTop(step),Justification::left,1);
		}
		
		
		int numBeatPerBar = currentPattern->timeSigNumerator;
		int numBars = ceil(currentPattern->duration/numBeatPerBar);
		
		int displayedTime = (numBars*numBeatPerBar);
		float timeScale = area.getWidth()*1.0/displayedTime;
		g.setColour(Colours::darkgrey);
		for(int i = 0;i < numBars*numBeatPerBar*gridBeatSubDiv ; i++){
			int xpos = area.getX()+i*timeScale/gridBeatSubDiv;
			g.drawLine(xpos,area.getY(), xpos, area.getBottom());
		}
		for(auto & e:currentPattern->events){
			if(displayPitchInsteadOfTags){
				Rectangle<int> currect(e.start*timeScale+area.getX(), area.getY()+std::distance(  allEventsTags.begin(),allEventsTags.find(String(e.pitch)))*step, jmax(2.0,e.duration*timeScale), jmax(2,step));
				
				g.setColour(Colours::wheat);
				g.fillRect(currect);
				g.setColour(Colours::black);
				g.drawRect(currect);
			}
			else{
				
				if(e.eventTags.size()==0){
					Rectangle<int> currect(e.start*timeScale+area.getX(), area.getY()+std::distance(  allEventsTags.begin(),allEventsTags.find("None"))*step, jmax(2.0,e.duration*timeScale), jmax(2,step));
					g.setColour(Colours::wheat);
					g.fillRect(currect);
					g.setColour(Colours::black);
					g.drawRect(currect);
				}
				else{
					for(auto & t:e.eventTags){
						Rectangle<int> currect(e.start*timeScale+area.getX(), area.getY()+std::distance(  allEventsTags.begin(),allEventsTags.find(t))*step, jmax(2.0,e.duration*timeScale), jmax(2,step));
						g.setColour(Colours::wheat);
						g.fillRect(currect);
						g.setColour(Colours::black);
						g.drawRect(currect);
					}
				}
			}
		}
		if(linePos>=0){
			g.setColour(Colours::chartreuse);
			double moduloPos = fmod(linePos,displayedTime);
			int xpos =timeScale*moduloPos+area.getX();
			g.drawLine(xpos,area.getY(),xpos,area.getBottom());
		}
	}
}

void BlockContainer::build(){
	if (currentPattern) {
		if(!displayPitchInsteadOfTags){
			allEventsTags.clear();
			for(auto & p:currentPattern->events){
				for(auto & t:p.eventTags){
					allEventsTags.insert(t);
				}
				if(p.eventTags.size()==0){allEventsTags.insert("None");}
			}
		}
		else{
			allEventsTags.clear();
			for(auto & p:currentPattern->events){
				allEventsTags.insert(String(p.pitch));
			}
		}
	}
}