/*
 ==============================================================================
 
 PatternComponent.cpp
 Created: 4 Jul 2016 7:20:08pm
 Author:  martin hermant
 
 ==============================================================================
 */

#include "PatternComponent.h"


PatternComponent::PatternComponent():voicesContainer(this),TimeListener(1){
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

VoicesContainer::VoicesContainer(PatternComponent * _o):blockDragger(this),owner(_o){
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
}
void VoicesContainer::paintOverChildren(Graphics & g){
	if(linePos>=0){
		int numBeatPerBar = pattern.timeSigNumerator;
		int numBars = ceil(pattern.duration/numBeatPerBar);
		Rectangle<int> area = getLocalBounds();
		int displayedTime = (numBars*numBeatPerBar);
		float timeScale = area.getWidth()*1.0/displayedTime;
		g.setColour(Colours::chartreuse);
		double moduloPos = fmod(linePos,displayedTime);
		int xpos =timeScale*moduloPos+area.getX();
		g.drawLine(xpos,area.getY(),xpos,area.getBottom());
	}
}
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

//	}


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
	
	if(targetVoice==nullptr){
		bounds = previousBounds;
		return;}
	
	bounds.setY(targetVoice->getY());
	
	for(auto & e:targetVoice->blocks){
		
		if(e !=originComponent && e->getRight()> bounds.getX() && e->getX()<bounds.getRight()){
			bounds.setX(e->getRight());
		}
	}
	
	bounds.setX(jmax(0,bounds.getX()));
	bounds.setX(jmin(targetVoice->getWidth()-bounds.getWidth(),bounds.getX()));
	
}

void VoicesContainer::BlockDragger::startDraggingBlock(BlockComponent * bk,const MouseEvent & e){
	originVoice = (VoiceComponent*)bk->getParentComponent();
	originVoice->removeChildComponent(bk);
	int idx = originVoice->blocks.indexOf(bk);
	originComponent = originVoice->blocks.removeAndReturn(idx);
	owner->addAndMakeVisible(originComponent);
	
	dragger.startDraggingComponent(bk, e);
	lastVoice = nullptr;
	lastPatternUpdateTime = -1;
	
}
void VoicesContainer::BlockDragger::draggingBlock(BlockComponent * bk,const MouseEvent & e){
	dragger.dragComponent(bk, e, this);
	if(lastVoice == nullptr){lastVoice = originVoice ;}
	if(targetVoice ){
		double scale = owner->pattern.duration*1.0/targetVoice->getWidth();
		bk->evt->start = scale*bk->getX();
		if( Time::currentTimeMillis() -lastPatternUpdateTime >300){
			owner->owner->patternListeners.call(&PatternComponent::Listener::patternChanged,owner->owner);
			lastPatternUpdateTime = Time::currentTimeMillis();
		}
		if(lastVoice!=targetVoice){
			
			if(targetVoice->displayPitch){bk->evt->pitch = targetVoice->tag.getIntValue();}
			else{
				auto  res = std::find(bk->evt->eventTags.begin(),bk->evt->eventTags.end(),lastVoice->tag);
				if( res != bk->evt->eventTags.end()){res->assign(targetVoice->tag.toStdString());}
				else{
					jassertfalse;
					bk->evt->eventTags.push_back(targetVoice->tag.toStdString());
				}
			}
		}
	}
	lastVoice = targetVoice;
}


void VoicesContainer::BlockDragger::endDraggingBlock(){
	owner->owner->patternListeners.call(&PatternComponent::Listener::patternChanged,owner->owner);
	if(targetVoice){
		originComponent->setTopLeftPosition(originComponent->getX(), 0);
		targetVoice->addAndMakeVisible(originComponent);
		targetVoice->blocks.add(originComponent);
		targetVoice = nullptr;
		lastVoice = nullptr;
		originVoice = nullptr;
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
	
	if( tagsColours.count(tag)){
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
	
	int numBeatPerBar = owner->pattern.timeSigNumerator;
	int numBars = ceil(owner->pattern.duration/numBeatPerBar);
	int displayedTime = (numBars*numBeatPerBar);
	float timeScale = a.getWidth()*1.0/displayedTime;
	g.setColour(Colours::darkgrey.brighter());
	for(int i = 0;i < numBars*numBeatPerBar*owner->gridBeatSubDiv ; i++){
		int xpos = a.getX()+i*timeScale/owner->gridBeatSubDiv;
		g.drawLine(xpos,a.getY(), xpos, a.getBottom(),0.5);
	}
	
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
	
	g.setColour(Colours::red);//owner->getColour());
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
