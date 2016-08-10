/*
 ==============================================================================
 
 PyJUCEAPI.h
 Created: 13 Jun 2016 5:00:10pm
 Author:  Martin Hermant
 
 ==============================================================================
 */

#ifndef PYJUCEAPI_H_INCLUDED
#define PYJUCEAPI_H_INCLUDED

#include "JuceHeader.h"

#include "GS_API.h"
#include "GSPatternPyWrap.h"

#include "pythonWrap.h"
#include "TimeListener.h"

#include "PyJUCEParameter.h"

class JucepythonAudioProcessor;

class PyJUCEAPI : public Timer,public TimeListener{
public:
  PyJUCEAPI(JucepythonAudioProcessor * o);
	~PyJUCEAPI(){Py_DECREF(timePyObj);Py_DECREF(timeKey);}
	
  void load();
  void init();
  bool isLoaded();
  void setWatching(bool);
	
	// function callers
 void  getNewPattern();
  void callSetupFunction();
	void callTimeChanged(double time);
	void buildParamsFromScript();

  bool setNewPattern(PyObject * o);
	
	// python wrapper object
  PythonWrap  py ;
  File pythonFile;

  JucepythonAudioProcessor * owner;
  bool isInitialized;


  class Listener{
  public:
    virtual ~Listener(){};
    virtual void newFileLoaded(const File & f){};
		virtual void newPatternLoaded( GSPattern * p){};
		virtual void newParamsLoaded( OwnedArray<PyJUCEParameter> *){};
  };
  ListenerList<Listener> listeners;
  void addListener(Listener * l){listeners.add(l);}
  void removeListener(Listener * l){listeners.remove(l);}
	void timeChanged(double time) override;
	
	OwnedArray<PyJUCEParameter> params;


  PyObject * pluginModule;
  PyObject* interfaceModule;
protected:
	
  void timerCallback()override;
  Time lastPythonFileMod;
	
	PyObject * timePyObj ;
	PyObject *timeKey;

GSPatternPyWrap GSPatternWrap;
	
  
	
	
	
};


#endif  // PYJUCEAPI_H_INCLUDED
