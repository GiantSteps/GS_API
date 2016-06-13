/*
  ==============================================================================

    PyJUCEAPI.cpp
    Created: 13 Jun 2016 5:00:10pm
    Author:  Martin Hermant

  ==============================================================================
*/

#include "PyJUCEAPI.h"


GSPattern * PyJUCEAPI::getNewPattern(){
    PyObject * o = py.callFunction("onGenerateNew");
    GSPattern * p;
    _wrap_convert_py2c__GSPattern(o,p);
    return p;
}

void PyJUCEAPI::init(){
    if(!Py_IsInitialized())
    {
        py.initPath();
        Py_Initialize();
    }

    File f (py.getVSTPath()+"/../../Resources/python");
    py.initSearchPath();
    py.addSearchPath(f.getFullPathName().toStdString());
}
void PyJUCEAPI::load(){
    py.load();
    DBG(py.test("lala"));
}

bool PyJUCEAPI::isLoaded(){
    return py.isFileLoaded();
}