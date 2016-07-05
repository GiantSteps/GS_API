/*
 ==============================================================================
 
 PyJUCEAPI.h
 Created: 13 Jun 2016 5:00:10pm
 Author:  Martin Hermant
 
 ==============================================================================
 */

#ifndef PYJUCEAPI_H_INCLUDED
#define PYJUCEAPI_H_INCLUDED


#include "GS_API.h"

#include "pythonWrap.h"
#include "JuceHeader.h"

//#define GETDICTOBJ(

#include "GSPatternPyWrap.h"


#include "TimeListener.h"

class PyJUCEAPI : public Timer,public TimeListener{
public:
  PyJUCEAPI():TimeListener(1){timePyObj = PyDict_New();timeKey=PyFromString("time");}
	~PyJUCEAPI(){Py_DECREF(timePyObj);Py_DECREF(timeKey);}
	
  void load();
  void init();
  bool isLoaded();
  void setWatching(bool);
	
	// function callers
  GSPattern *  getNewPattern();
  void callSetupFunction();
	GSPattern * callTimeChanged(double time);
	
	// python wrapper object
  PythonWrap  py ;
	
	
  File pythonFile;
  class Listener{
  public:
    virtual ~Listener(){};
    virtual void newFileLoaded(const File & f){};
		virtual void newPatternLoaded( GSPattern * p){};
  };
  ListenerList<Listener> listeners;
  void addListener(Listener * l){listeners.add(l);}
  void removeListener(Listener * l){listeners.remove(l);}
	void timeChanged(double time) override;
	
protected:
	
  void timerCallback()override;
  Time lastPythonFileMod;
	
	PyObject * timePyObj ;
	PyObject *timeKey;
	
  GSPatternPyWrap GSPatternWrap;
	
	
};


#endif  // PYJUCEAPI_H_INCLUDED
