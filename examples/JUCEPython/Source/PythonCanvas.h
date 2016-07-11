/*
  ==============================================================================

    PythonCanvas.h
    Created: 6 Jul 2016 1:33:03pm
    Author:  martin hermant

  ==============================================================================
*/

#ifndef PYTHONCANVAS_H_INCLUDED
#define PYTHONCANVAS_H_INCLUDED

#include "JuceHeader.h"
#include "PyJUCEAPI.h"
class PythonCanvas: public Component,public PyJUCEAPI::Listener{
public:
	PythonCanvas():originParams(nullptr){}
	void newParamsLoaded( OwnedArray<PyJUCEParameter> *) override;

	void resized() override;
	OwnedArray<PyJUCEParameter> * originParams;
	
	OwnedArray<Component> pyWidgets;
	
};



#endif  // PYTHONCANVAS_H_INCLUDED
