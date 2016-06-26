/*
 ==============================================================================

 PyJUCEAPI.cpp
 Created: 13 Jun 2016 5:00:10pm
 Author:  Martin Hermant

 ==============================================================================
 */

#include "PyJUCEAPI.h"
//#include "PyGSPattern.h"



GSPattern *  PyJUCEAPI::getNewPattern(){
  PyObject * o = py.callFunction("onGenerateNew");
  GSPattern*  p =nullptr;
  if(o){

    p = nullptr;
    p = GSPatternWrap.GenerateFromObj(o);

    if(p){
      p->checkDurationValid();
      DBG( p->duration );
    }

  }
  return p;
}
//


void PyJUCEAPI::init(){
  py.init();
  pythonFile = File (py.getVSTPath()+"/../../Resources/python/VSTPlugin.py");
  py.initSearchPath();
  py.addSearchPath(pythonFile.getParentDirectory().getFullPathName().toStdString());
}


void PyJUCEAPI::load(){
  py.load(pythonFile.getFileNameWithoutExtension().toStdString());
  lastPythonFileMod = pythonFile.getLastModificationTime();
  listeners.call(&Listener::newFileLoaded,pythonFile);

}




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