/*
 ==============================================================================

 PatternComponent.cpp
 Created: 4 Jul 2016 7:20:08pm
 Author:  martin hermant

 ==============================================================================
 */

#include "PatternComponent.h"


PatternComponent::PatternComponent():TimeListener(1),voicesContainer(this){
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
  voicesContainer.blockDragger.interruptDrag();
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
    int displayedTime = pattern.duration;
    float timeScale = area.getWidth()*1.0/displayedTime;
    g.setColour(Colours::chartreuse);
    double moduloPos = fmod(linePos,displayedTime);
    int xpos =timeScale*moduloPos+area.getX();
    g.drawLine(xpos,area.getY(),xpos,area.getBottom());
  }
}


void VoicesContainer::BlockDragger::checkBounds (Rectangle<int>& bounds,const Rectangle<int>& previousBounds,const Rectangle<int>& limits,
                                                 bool isStretchingTop,bool isStretchingLeft,bool isStretchingBottom,bool isStretchingRight){

  int overLap = 0;

  if(isDragging){
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

      if(e !=originComponent){
        if (e->getRight()> bounds.getX() && e->getX()<bounds.getRight()){
          bounds.setX(e->getRight());
        }
      }
    }
  }

  // resizing
  else {
    targetVoice = originComponent->owner;

    if(isResizingLeft){
      if (BlockComponent * last = targetVoice->getLastBlock(originComponent)){
        if (bounds.getX()<last->getRight()+1){
          bounds.setX(last->getRight()+1);
          bounds.setWidth(previousBounds.getWidth());
        }
        else if ((bounds.getX()<0)){bounds = previousBounds;}

      }
    }
    else{

      if(BlockComponent * next = targetVoice->getNextBlock(originComponent)){
        if (bounds.getRight()>next->getX()-1 ){bounds.setWidth(next->getX()-1 - bounds.getX());}
      }
      else if (bounds.getRight()>targetVoice->getWidth()){bounds = previousBounds;}
    }
    if (bounds.getWidth() < 6){bounds = previousBounds;}

  }


  bounds.setX(jmax(0,bounds.getX()));
  bounds.setX(jmin(targetVoice->getWidth()-bounds.getWidth(),bounds.getX()));


}

void VoicesContainer::BlockDragger::interruptDrag(){
  if(originComponent){
    originComponent->removeMouseListener(targetVoice);
    endDraggingBlock();
  }


  originComponent = nullptr;
}

void VoicesContainer::BlockDragger::startDraggingBlock(BlockComponent * bk,const MouseEvent & e){
  isDragging = true;
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
  updatePattern();

}
void VoicesContainer::BlockDragger::updatePattern(){

  if(!originComponent){
    jassertfalse;
    return;
  }
  if(lastVoice == nullptr){lastVoice = originVoice ;}

  if(targetVoice ){
    double scale = owner->pattern.duration*1.0/targetVoice->getWidth();
    originComponent->evt->start = scale*originComponent->getX();
    originComponent->evt->duration = scale*originComponent->getWidth();
    if( Time::currentTimeMillis() -lastPatternUpdateTime >300){
      owner->owner->patternListeners.call(&PatternComponent::Listener::patternChanged,owner->owner);
      lastPatternUpdateTime = Time::currentTimeMillis();
    }
    if(lastVoice!=targetVoice){
      if(!lastVoice)lastVoice = targetVoice;
      if(targetVoice->displayPitch){originComponent->evt->pitch = targetVoice->tag.getIntValue();}
      else{
        auto  res = std::find(originComponent->evt->eventTags.begin(),originComponent->evt->eventTags.end(),lastVoice->tag);
        if( res != originComponent->evt->eventTags.end()){res->assign(targetVoice->tag.toStdString());}
        else{
          jassertfalse;
          originComponent->evt->eventTags.push_back(targetVoice->tag.toStdString());
        }
      }
    }
  }
  lastVoice = targetVoice;
}


void VoicesContainer::BlockDragger::endDraggingBlock(){
  isDragging = false;
  owner->owner->patternListeners.call(&PatternComponent::Listener::patternChanged,owner->owner);
  if(targetVoice){
    originComponent->setTopLeftPosition(originComponent->getX(), 0);
    targetVoice->addAndMakeVisible(originComponent);
    targetVoice->blocks.add(originComponent);
    originComponent->owner = targetVoice;
    targetVoice = nullptr;
    lastVoice = nullptr;
    originVoice = nullptr;

  }
}
void VoicesContainer::BlockDragger::setOriginComponent(BlockComponent * b){
  originComponent = b;
}


void VoicesContainer::build(){

  if(!displayPitchInsteadOfTags){
    allEventsTags.clear();
    for(auto & p:pattern.events){
      for(auto & t:p->eventTags){
        allEventsTags.insert(t);
      }
      if(p->eventTags.size()==0){allEventsTags.insert("None");}
    }
  }
  else{
    allEventsTags.clear();
    for(auto & p:pattern.events){
      allEventsTags.insert(String(p->pitch));
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

VoiceComponent::VoiceComponent(String _tag,VoicesContainer * container,bool _displayPitch):
owner(container),tag(_tag),displayPitch(_displayPitch){
  quantization = 1/4.;
  setInterceptsMouseClicks(true,false);
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
BlockComponent * VoiceComponent::getNextBlock(BlockComponent * bk){
  jassert(blocks.contains(bk));
  int minDist = getWidth()-bk->getRight() ;
  BlockComponent * res = nullptr;

  for(auto & b:blocks){
    if(b!=bk){
      int newDist = b->getX() - bk->getRight();
      if(newDist>0 && newDist < minDist){
        minDist = newDist;
        res = b;
      }
    }
  }
  return res;
}
BlockComponent * VoiceComponent::getLastBlock(BlockComponent * bk){
  jassert(blocks.contains(bk));
  int minDist = bk->getX() ;
  BlockComponent * res = nullptr;
  for(auto & b:blocks){
    if(b!=bk){
      int newDist = bk->getX() - b->getRight() ;
      if(newDist>0 && newDist<minDist){
        minDist = newDist;
        res = b;
      }
    }
  }
  return res;
}

double VoiceComponent::getQuantizedTimeForX(int x){
  double absTime = x*owner->pattern.duration/getWidth();
  double quant = getQuantizedForTime(absTime);
  return quant;
}

double VoiceComponent::getQuantizedForTime(double t){
  double q = getQuantization();
  return floor(t/q)*q;
}
double VoiceComponent::getQuantization(){
  return quantization;
}


void VoiceComponent::mouseDoubleClick (const MouseEvent& event) {
  if(event.originalComponent==this){
    GSPatternEvent *  ev = new GSPatternEvent();
    ev->start =  getQuantizedTimeForX(event.getMouseDownX());
    ev->duration = getQuantization();
    if(displayPitch){
      ev->pitch = tag.getIntValue();
    }
    else{
      ev->eventTags.push_back(tag.toStdString());
      ev->pitch = 0;
      vector<GSPatternEvent*>similarEvents = owner->pattern.getEventsWithTag(tag.toStdString());
      if(similarEvents.size()>0){
        ev->pitch = similarEvents[0]->pitch;
      }
    }
    owner->pattern.addEvent(ev);


    update();
  }
  // click on blick
  else if (BlockComponent * bk = dynamic_cast<BlockComponent*>(event.originalComponent)){
    owner->pattern.removeEvent(bk->evt);
    bk->evt = nullptr;
    update();
  }
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
    bk->addMouseListener(this, false);
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


  int numBeatPerBar = owner->pattern.timeSigNumerator;
  int numBars = ceil(owner->pattern.duration/numBeatPerBar);
  int displayedTime = owner->pattern.duration;//(numBars*numBeatPerBar);
  float timeScale = a.getWidth()*1.0/displayedTime;
  g.setColour(Colours::darkgrey.brighter());
  for(int i = 0;i < numBars*numBeatPerBar*owner->gridBeatSubDiv ; i++){
    int xpos = a.getX()+i*timeScale/owner->gridBeatSubDiv;
    g.drawLine(xpos,a.getY(), xpos, a.getBottom(),0.5);
  }

}
void VoiceComponent::paintOverChildren(Graphics & g){
  Rectangle<int> a = getLocalBounds();
  g.setColour(Colours::lightgrey);
  g.drawText(tag, a, Justification::left);
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

BlockComponent::BlockComponent(GSPatternEvent* _evt,VoiceComponent * o):evt(_evt),owner(o){
  leftResize = new ResizableEdgeComponent(this,&owner->owner->blockDragger,ResizableEdgeComponent::leftEdge);
  rightResize = new ResizableEdgeComponent(this,&owner->owner->blockDragger,ResizableEdgeComponent::rightEdge);
  addAndMakeVisible(leftResize);
  addAndMakeVisible(rightResize);
  leftResize->addMouseListener(this, true);
  rightResize->addMouseListener(this, true);

}

void BlockComponent::resized(){
  Rectangle<int> area = getLocalBounds();
  leftResize->setBounds(area.removeFromLeft(2));
  rightResize->setBounds(area.removeFromRight(2));
}
void BlockComponent::paint (Graphics& g){

  g.setColour(Colours::red);//owner->getColour());
  Rectangle<int> a = getLocalBounds();
  a.reduce(1, 1);
  g.fillRect(a);
}

void BlockComponent::mouseEnter(const MouseEvent&) {
  owner->owner->blockDragger.setOriginComponent( this);
}
void BlockComponent::mouseExit(const MouseEvent&) {
  owner->owner->blockDragger.setOriginComponent( nullptr);
}


void BlockComponent::mouseDown (const MouseEvent& e)
{
  Component * c =e.originalComponent;
  isDragging = (c==this);
  if(isDragging){
    owner->owner->blockDragger.startDraggingBlock (this, e);
  }
  else{

    owner->owner->blockDragger.isResizingLeft = (c == leftResize);
  }

}

void BlockComponent::mouseDrag (const MouseEvent& e)
{
  if(isDragging){
    owner->owner->blockDragger.draggingBlock (this, e);
  }
  else{
    owner->owner->blockDragger.updatePattern();
  }
}

void BlockComponent::mouseUp(const MouseEvent & e){
  if(isDragging){
    owner->owner->blockDragger.endDraggingBlock();
  }
  isDragging = false;
  
}
