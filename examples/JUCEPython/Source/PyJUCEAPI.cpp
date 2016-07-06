/*
 ==============================================================================
 
 PyJUCEAPI.cpp
 Created: 13 Jun 2016 5:00:10pm
 Author:  Martin Hermant
 
 ==============================================================================
 */

#include "PyJUCEAPI.h"
//#include "PyGSPattern.h"


GSPattern * PyJUCEAPI::callTimeChanged(double time){
	PyDict_SetItem(timePyObj, timeKey, PyFloat_FromDouble(time));
	PyObject * o = py.callFunction("onTimeChanged",timePyObj);
	GSPattern * p=nullptr;
	if(o){
		if(o!=Py_None){
			p = GSPatternWrap.GenerateFromObj(o);
			if(p){p->checkDurationValid();}
			else{DBG("no valid pattern returned when calling get TimeChanged");}
		}
		Py_DECREF(o);
  }
	
	if(p)listeners.call(&Listener::newPatternLoaded,p);
	Py_DECREF(timePyObj);
	return p;
	
}
GSPattern *  PyJUCEAPI::getNewPattern(){
  PyObject * o = nullptr;
	GSPattern*  p =nullptr;
  if((o=py.callFunction("onGenerateNew",nullptr))){
    p = nullptr;
    p = GSPatternWrap.GenerateFromObj(o);
		
    if(p){
      p->checkDurationValid();
      DBG( p->duration );
    }
		Py_DECREF(o);
  }
	
	if(p==nullptr){DBG("no pattern found when calling get NewPattern");}
	listeners.call(&Listener::newPatternLoaded,p);
  return p;
}

void PyJUCEAPI::callSetupFunction(){
	PyObject * o=nullptr;
	
	if((o = py.callFunction("setup"))){
		
		if(PyString_Check(o)){
			DBG("setup returned " << PyToString(o));
			
			
		}
		else if (o!=Py_None){
			
			DBG("unhandeled return type : "<< o->ob_type->tp_name);
		}
		Py_DECREF(o);
		
		
	}
	else {
		DBG("no setup function found or file not loaded");
	}
}
//


void PyJUCEAPI::init(){
  py.init();
  pythonFile = File (py.getVSTPath()+"/../../Resources/python/VSTPlugin.py");
  py.initSearchPath();
  py.setFolderPath(pythonFile.getParentDirectory().getFullPathName().toStdString());
}


void PyJUCEAPI::load(){
  bool hasLoaded = py.load(pythonFile.getFileNameWithoutExtension().toStdString());
  lastPythonFileMod = pythonFile.getLastModificationTime();
	
	if (hasLoaded){
		callSetupFunction();
		buildParamsFromScript();
	}
  listeners.call(&Listener::newFileLoaded,pythonFile);
	
}

void PyJUCEAPI::buildParamsFromScript(){
	params.clear();
	listeners.call(&Listener::newParamsLoaded,&params);
	
	PyObject * o = py.callFunction("getAllParameters");
	if (o){
		
		if(PyList_Check(o)) {
			int s = PyList_GET_SIZE(o);
			for (int i = 0 ; i < s; i++){
				PyObject * it = PyList_GET_ITEM(o, i);
				PyJUCEParameter * p = PyJUCEParameterBuilder::buildParamFromObject(it);
				if(p){
					p->linkToPyWrap(&py);
				}
				params.add(p);
			}
		}
    Py_DECREF(o);
	}
	
	listeners.call(&Listener::newParamsLoaded,&params);
}

void PyJUCEAPI::timeChanged(double time) {callTimeChanged(time);};




void PyJUCEAPI::setWatching(bool w){
  if(w){startTimer(200);}
  else{stopTimer();}
}

void PyJUCEAPI::timerCallback(){
  if(pythonFile.getLastModificationTime()!=lastPythonFileMod){
    load();
  };
}
bool PyJUCEAPI::isLoaded(){
  return py.isFileLoaded();
}