/*
  ==============================================================================

    PythonCanvas.h
    Created: 6 Jul 2016 1:33:03pm
    Author:  martin hermant

  ==============================================================================
*/

#ifndef PYTHONCANVAS_H_INCLUDED
#define PYTHONCANVAS_H_INCLUDED

#include "PyJUCEAPI.h"
#include "JuceHeader.h"

class PythonCanvas: public Component,public PyJUCEAPI::Listener{
public:
	PythonCanvas():originParams(nullptr){}
	void newParamsLoaded( OwnedArray<PyJUCEParameter> *) override;

	void resized() override;
  void handleCommandMessage(int cID)override ;
	OwnedArray<PyJUCEParameter> * originParams;
	
	OwnedArray<Component> pyWidgets;


  typedef enum{
    REBUILD_PARAMS
  }AsyncCommandID;
};



#endif  // PYTHONCANVAS_H_INCLUDED
