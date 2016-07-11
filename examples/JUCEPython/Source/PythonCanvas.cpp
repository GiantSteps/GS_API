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
	pyWidgets.clear();
	originParams = params;
	for (auto & p:*originParams){
		Component * c = p->buildComponent();
		pyWidgets.add(c);
		addAndMakeVisible(c);
	}
	

	resized();
};

Rectangle<int> scaleRect(Rectangle<float> r,Rectangle<int> b){
	return (r.translated(b.getX(), b.getY())*Point<float>(b.getWidth()/100.0,b.getHeight()/100.0)).toNearestInt();
}

void PythonCanvas::resized(){
	if (!originParams) {return;}
	int i = 0;
	
	for(auto & p:*originParams){
		Component * c = pyWidgets.getUnchecked(i);
		c->setBounds(scaleRect(p->relativeArea,getLocalBounds()));
		i++;
	}
}