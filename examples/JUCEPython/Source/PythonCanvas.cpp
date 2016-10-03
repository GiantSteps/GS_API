/*
  ==============================================================================

    PythonCanvas.cpp
    Created: 6 Jul 2016 1:33:03pm
    Author:  martin hermant

  ==============================================================================
*/

#include "PythonCanvas.h"

#include "PyJUCEParameter.h"
void PythonCanvas::newParamsLoaded( OwnedArray<PyJUCEParameter> *params){
  originParams = params;
  DBG("post rebuild");
  postCommandMessage(REBUILD_PARAMS);

};

PythonCanvas::~PythonCanvas(){
  paramsBeingCleared();
}
void PythonCanvas::handleCommandMessage(int cID){
  switch (cID) {
    case REBUILD_PARAMS:
      paramsBeingCleared();
      for (auto & p:*originParams){
        Component * c = p->buildComponent();
        pyWidgets.add(c);
        addAndMakeVisible(c);
        listeners.call(&Listener::widgetAdded,c);
      }
      resized();
      break;

    default:
      break;
  }
}


void PythonCanvas::paramsBeingCleared(){
	for(auto & p:pyWidgets){
		listeners.call(&Listener::widgetRemoved,p);
	}
	pyWidgets.clear();
}

inline Rectangle<int> scaleRect(Rectangle<float> r,Rectangle<int> b){
	return (r.translated(b.getX(), b.getY())*Point<float>(b.getWidth()/100.0,b.getHeight()/100.0)).toNearestInt();
}

void PythonCanvas::resized(){
	if (!originParams || pyWidgets.size()==0) {return;}

	int i = 0;
	
	for(auto & p:*originParams){
		Component * c = pyWidgets.getUnchecked(i);
		if(p->relativeArea.getWidth()>0 && p->relativeArea.getHeight()>0)
		c->setBounds(scaleRect(p->relativeArea,getLocalBounds()));
		i++;
	}
}
