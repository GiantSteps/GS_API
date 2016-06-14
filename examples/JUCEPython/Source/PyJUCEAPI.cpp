/*
  ==============================================================================

    PyJUCEAPI.cpp
    Created: 13 Jun 2016 5:00:10pm
    Author:  Martin Hermant

  ==============================================================================
*/

#include "PyJUCEAPI.h"
//#include "PyGSPattern.h"

GSPattern  PyJUCEAPI::getNewPattern(){
    PyObject * o = py.callFunction("onGenerateNew");
    GSPattern p ;
    if(o){
//        PyGSPattern *tmp_GSPattern;
//
//        py_retval = Py_BuildValue((char *) "(O)", value);
//        if (!PyArg_ParseTuple(py_retval, (char *) "O!", &PyGSPattern_Type, &tmp_GSPattern)) {
//            Py_DECREF(py_retval);
//            return 0;
//        }
//        *address = *tmp_GSPattern->obj;
//        PyGSPattern *  tmp =reinterpret_cast<PyGSPattern *> (o);
//        p = *tmp->obj;
//        p = *o->obj;
    _wrap_convert_py2c__GSPattern(o,&p);
    }
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