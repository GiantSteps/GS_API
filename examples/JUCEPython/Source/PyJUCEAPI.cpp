/*
  ==============================================================================

    PyJUCEAPI.cpp
    Created: 13 Jun 2016 5:00:10pm
    Author:  Martin Hermant

  ==============================================================================
*/

#include "PyJUCEAPI.h"
//#include "PyGSPattern.h"


extern int _wrap_convert_py2c__GSPattern(PyObject *value, GSPattern *address);


GSPattern  PyJUCEAPI::getNewPattern(){
    PyObject * o = py.callFunction("onGenerateNew");
    GSPattern p ;
    if(o){

        _wrap_convert_py2c__GSPattern(o,&p);
        p.checkLengthValid();
        cout << p.length << endl;

    }
    return p;
}

void PyJUCEAPI::init(){
    py.init();
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