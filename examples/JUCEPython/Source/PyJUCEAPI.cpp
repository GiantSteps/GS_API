/*
 ==============================================================================

 PyJUCEAPI.cpp
 Created: 13 Jun 2016 5:00:10pm
 Author:  Martin Hermant

 ==============================================================================
 */

#include "PyJUCEAPI.h"
//#include "PyGSPattern.h"

#include "PluginProcessor.h"
#include "PyJUCEPython.h"
#include "Utils.h"



PyJUCEAPI::PyJUCEAPI(JucepythonAudioProcessor * o):
owner(o),
TimeListener(1),
isInitialized(false),
pluginModule(nullptr),
interfaceModule(nullptr),
apiModuleObject(nullptr){
  timePyObj = PyDict_New();
  timeKey=PyFromString("time");
}


void PyJUCEAPI::callTimeChanged(double time){
	// TODO bug multiple load
  PyDict_SetItem(timePyObj, timeKey, PyFloat_FromDouble(time));
  py.callFunction("onTimeChanged",pluginModule,timePyObj);

  Py_DECREF(timePyObj);

}



bool PyJUCEAPI::setNewPattern(PyObject * o){

  GSPattern * p=nullptr;
  bool found = false;
		if(o!=Py_None){
      p = GSPatternWrap.GenerateFromObj(o);
      if(p){p->checkDurationValid();found = true;}
      else{DBG("pattern not valid");}

    }
//		Py_DECREF(o);

  if(p)listeners.call(&Listener::newPatternLoaded,p);
  return found;
}


void PyJUCEAPI::callSetupFunction(){
  PyObject * o=nullptr;

  if((o = py.callFunction("setup",pluginModule))){

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
  if(!isInitialized){
		String bin = getVSTProperties().getValue("pythonBin");

    if (bin=="") {bin = getVSTPath()+"/../../Resources/pythonEnv/bin/python2.7";}
		else{		DBG("using custom python : " << bin);}
    py.init(File(bin).getFullPathName().toStdString());
    initJUCEAPI(this,&apiModuleObject);
    pythonFile = File (getVSTPath()+"/../../Resources/python/VSTPlugin.py");
    py.initSearchPath();
    py.setFolderPath(pythonFile.getParentDirectory().getFullPathName().toStdString());
  }
  isInitialized = true;

}

bool PyJUCEAPI::setParam(PyObject* o){
  for(auto & p:params){
    if(p->pyRef==o){
      p->updateFromPython();
      DBG("found param to update");
      return true;
    }
  }
  return false;
}


void PyJUCEAPI::load(){
  pluginModule =  py.loadModule(pythonFile.getFileNameWithoutExtension().toStdString(),pluginModule);
  lastPythonFileMod = pythonFile.getLastModificationTime();

  if (pluginModule){
    callSetupFunction();
    buildParamsFromScript();
  }
  listeners.call(&Listener::newFileLoaded,pythonFile);

}

void PyJUCEAPI::buildParamsFromScript(){
  params.clear();
  
  if((interfaceModule = py.loadModule("interface",interfaceModule))){

    PyObject * o = py.callFunction("getAllParameters",interfaceModule);
    if (o){

      if(PyList_Check(o)) {
        int s = PyList_GET_SIZE(o);
        for (int i = 0 ; i < s; i++){
          PyObject * it = PyList_GET_ITEM(o, i);
          PyJUCEParameter * p = PyJUCEParameterBuilder::buildParamFromObject(it);
          if(p){
            p->linkToJuceApi(this);
            params.add(p);
          }
        }
      }
      Py_DECREF(o);
    }
    listeners.call(&Listener::newParamsLoaded,&params);
  }
  else{
    DBG("cant load interface or none provided");
  }

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
  return pluginModule!=nullptr;
}