/*
 ==============================================================================
 
 PatternComponent.cpp
 Created: 4 Jul 2016 7:20:08pm
 Author:  martin hermant
 
 ==============================================================================
 */

#include "PatternComponent.h"


PatternComponent::PatternComponent():TimeListener(1){
	addAndMakeVisible(voicesContainer);
	addAndMakeVisible(displayTagToggle);
	displayTagToggle.setClickingTogglesState(true);
	displayTagToggle.setButtonText("display tags");
	displayTagToggle.setColour(TextButton::buttonOnColourId, Colours::orange);
	displayTagToggle.setToggleState(!voicesContainer.displayPitchInsteadOfTags, dontSendNotification);
	displayTagToggle.addListener(this);
}

void PatternComponent::newPatternLoaded(GSPattern * p) {
	nextPatternToLoad = p;
  postCommandMessage(0);
}
GSPattern * PatternComponent::getPattern(){
	return &voicesContainer.pattern;
}
void PatternComponent::handleCommandMessage(int cid){
	
  voicesContainer.setPattern(nextPatternToLoad);
  voicesContainer.repaint();
}

void PatternComponent::paint(Graphics & g){
	g.setColour(Colours::darkgrey.darker());
	g.fillRect(getLocalBounds());
}

void PatternComponent::resized() {
	Rectangle<int> area = getLocalBounds();
	displayTagToggle.setBounds(area.removeFromBottom(20));
	voicesContainer.setBounds(area);
}


void PatternComponent::timeChanged(double time){
	voicesContainer.linePos = time;
	voicesContainer.repaint();
	beatInterval = 1.0/(2*voicesContainer.gridBeatSubDiv);
}

void PatternComponent::buttonClicked (Button* b) {
	if(b==&displayTagToggle){
		voicesContainer.displayPitchInsteadOfTags = !b->getToggleState();
		voicesContainer.build();
		voicesContainer.repaint();
	}
};

//////////////////////////////////////

VoicesContainer::VoicesContainer():blockDragger(this){
	gridBeatSubDiv = 8;
	displayPitchInsteadOfTags = true;
	defaultColor = Colours::blueviolet;
}

void VoicesContainer::resized(){
	if(voices.size() == 0)return;
	Rectangle<int> area = getLocalBounds();
	int step = area.getHeight()/voices.size();
	for(auto & v:voices){
		v->setBounds(area.removeFromTop(step));
	}
	
}

void VoicesContainer::setPattern(GSPattern *p){
	pattern = *p;
	build();
}
void VoicesContainer::paint(Graphics & g){
	g.setColour(Colours::black);
	g.fillAll();
//	if (pattern.events.size()>0 && allEventsTags.size()>0 ) {
//		Rectangle<int> area = getLocalBounds();
//		Rectangle<int> leftTags = area.removeFromLeft(70);
//		int step = leftTags.getHeight()/allEventsTags.size();
//		for(auto & t:allEventsTags){
//			g.drawFittedText(t, leftTags.removeFromTop(step),Justification::left,1);
//		}
//		
//		
//		int numBeatPerBar = pattern.timeSigNumerator;
//		int numBars = ceil(pattern.duration/numBeatPerBar);
//		
//		int displayedTime = (numBars*numBeatPerBar);
//		float timeScale = area.getWidth()*1.0/displayedTime;
//		g.setColour(Colours::darkgrey);
//		for(int i = 0;i < numBars*numBeatPerBar*gridBeatSubDiv ; i++){
//			int xpos = area.getX()+i*timeScale/gridBeatSubDiv;
//			g.drawLine(xpos,area.getY(), xpos, area.getBottom());
//		}
//    for(int i = 0;i <= pattern.events.size() ; i++){
//      int ypos = area.getY()+i*step;
//      g.drawLine(area.getX(),ypos, area.getRight(),ypos);
//    }
//		for(auto & e:pattern.events){
//			if(displayPitchInsteadOfTags){
//				Rectangle<int> currect(e.start*timeScale+area.getX(), area.getY()+std::distance(  allEventsTags.begin(),allEventsTags.find(String(e.pitch)))*step, jmax(2.0,e.duration*timeScale), jmax(2,step));
//				
//				g.setColour(Colours::wheat);
//				g.fillRect(currect);
//				g.setColour(Colours::black);
//				g.drawRect(currect);
//			}
//			else{
//				
//				if(e.eventTags.size()==0){
//					Rectangle<int> currect(e.start*timeScale+area.getX(), area.getY()+std::distance(  allEventsTags.begin(),allEventsTags.find("None"))*step, jmax(2.0,e.duration*timeScale), jmax(2,step));
//					g.setColour(Colours::wheat);
//					g.fillRect(currect);
//					g.setColour(Colours::black);
//					g.drawRect(currect);
//				}
//				else{
//					for(auto & t:e.eventTags){
//						Rectangle<int> currect(e.start*timeScale+area.getX(), area.getY()+std::distance(  allEventsTags.begin(),allEventsTags.find(t))*step, jmax(2.0,e.duration*timeScale), jmax(2,step));
//						g.setColour(Colours::wheat);
//						g.fillRect(currect);
//						g.setColour(Colours::black);
//						g.drawRect(currect);
//					}
//				}
//			}
//		}
//		if(linePos>=0){
//			g.setColour(Colours::chartreuse);
//			double moduloPos = fmod(linePos,displayedTime);
//			int xpos =timeScale*moduloPos+area.getX();
//			g.drawLine(xpos,area.getY(),xpos,area.getBottom());
//		}
//	}
}

void VoicesContainer::BlockDragger::checkBounds (Rectangle<int>& bounds,const Rectangle<int>& previousBounds,const Rectangle<int>& limits,
																										 bool isStretchingTop,bool isStretchingLeft,bool isStretchingBottom,bool isStretchingRight){
	
	int overLap = 0;

	for(auto & vv:owner->voices){
		Rectangle<int> v = vv->getBounds();
		int top = jmax(v.getY(),bounds.getY());
		int bottom = jmin(v.getBottom(),bounds.getBottom());
		int cOverLap = bottom-top;
		if(cOverLap>overLap){
			overLap = cOverLap;
			targetVoice =vv;
		}
	}
	
	if(targetVoice==nullptr){return;}
	
	bounds.setY(targetVoice->getY());
	
	for(auto & e:targetVoice->blocks){

		if(e !=originComponent && e->getRight()> bounds.getX() && e->getX()<bounds.getRight()){
			bounds.setX(e->getRight());
		}
	}
	
	
}

void VoicesContainer::BlockDragger::startDraggingBlock(BlockComponent * bk,const MouseEvent & e){
	owner->addAndMakeVisible(bk);
	originComponent = bk;
	dragger.startDraggingComponent(bk, e);
}
void VoicesContainer::BlockDragger::draggingBlock(BlockComponent * bk,const MouseEvent & e){
	dragger.dragComponent(bk, e, this);
}
void VoicesContainer::BlockDragger::endDraggingBlock(){
	if(targetVoice){
		targetVoice->addAndMakeVisible(originComponent);
		targetVoice = nullptr;
	}
}


void VoicesContainer::build(){
	
		if(!displayPitchInsteadOfTags){
			allEventsTags.clear();
			for(auto & p:pattern.events){
				for(auto & t:p.eventTags){
					allEventsTags.insert(t);
				}
				if(p.eventTags.size()==0){allEventsTags.insert("None");}
			}
		}
		else{
			allEventsTags.clear();
			for(auto & p:pattern.events){
				allEventsTags.insert(String(p.pitch));
			}
		}
	for(auto & v:voices){
		removeChildComponent(v);
	}
	voices.clear();
	for(auto & t:allEventsTags){
		VoiceComponent * v = new VoiceComponent(t,this,displayPitchInsteadOfTags);
		voices.add(v);
		addAndMakeVisible(v);
	}
	resized();
	
}

Colour & VoicesContainer::getColourForVoice(String tag){
	
	if(tagsColours.size() && tagsColours.count(tag)){
		return tagsColours[tag];
	}
	else{
		return defaultColor;
	}
}



//////////////////////////
// Voice Component

VoiceComponent::VoiceComponent(String _tag,VoicesContainer * container,bool _displayPitch):tag(_tag),owner(container),displayPitch(_displayPitch){
	update();
};
GSPattern * VoiceComponent::getPattern(){return owner?&owner->pattern:nullptr;}
vector<GSPatternEvent*> VoiceComponent::getVoiceEvents(){
	if(GSPattern *p = getPattern()){
		if(displayPitch){
			return p->getEventsWithPitch(tag.getIntValue());
	}
		else{

		return p->getEventsWithTag(tag.toStdString());
		}
	}

	return  vector<GSPatternEvent*>();
}

void VoiceComponent::update(){
	vector<GSPatternEvent*> evts = getVoiceEvents();
	for(auto & bk:blocks){
		removeChildComponent(bk);
	}
	blocks.clear();
	int i=0;
	for(auto e:evts){
		BlockComponent * bk = new BlockComponent(e,this);
		blocks.add(bk);
		addAndMakeVisible(bk);
		i++;
	}
	resized();
}
Colour & VoiceComponent::getColour(){
	return owner->getColourForVoice(tag);
}

void VoiceComponent::paint(Graphics & g) {
	Rectangle<int> a = getLocalBounds();
	a.reduce(1, 1);
	g.setColour(Colours::darkgrey);
	g.fillRect(a);
	g.setColour(Colours::lightgrey);
	g.drawText(tag, 0, 0, 30, a.getHeight(), Justification::left);
	
}

void VoiceComponent::resized(){
	Rectangle<int> area = getLocalBounds();
	double scale = area.getWidth()*1.0/owner->pattern.duration;
	for (auto & bk:blocks){
		bk->setBounds(bk->evt->start*scale, area.getY(), bk->evt->duration*scale, area.getHeight());
		
	}
}


////////////////////////////
// block Component

BlockComponent::BlockComponent(GSPatternEvent* _evt,VoiceComponent * o):owner(o),evt(_evt){
	
}


void BlockComponent::paint (Graphics& g){
	
	g.setColour(owner->getColour());
	Rectangle<int> a = getLocalBounds();
	a.reduce(1, 1);
	g.fillRect(a);
}

void BlockComponent::mouseDown (const MouseEvent& e)
{
	owner->owner->blockDragger.startDraggingBlock (this, e);
}

void BlockComponent::mouseDrag (const MouseEvent& e)
{
	owner->owner->blockDragger.draggingBlock (this, e);
}

void BlockComponent::mouseUp(const MouseEvent & e){
	owner->owner->blockDragger.endDraggingBlock();
	
}
