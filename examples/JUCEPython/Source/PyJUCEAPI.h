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




class PyJUCEAPI : public Timer{
public:
  PyJUCEAPI(){}

  void load();
  void init();
  bool isLoaded();
  void setWatching(bool);
  GSPattern *  getNewPattern();
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

protected:

  void timerCallback()override;
  Time lastPythonFileMod;

  GSPatternPyWrap GSPatternWrap;


};


#endif  // PYJUCEAPI_H_INCLUDED
