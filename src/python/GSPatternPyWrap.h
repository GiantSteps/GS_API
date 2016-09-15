/*
 ==============================================================================

 GSPatternPyWrap.h
 Created: 19 Jun 2016 6:52:28pm
 Author:  Martin Hermant

 ==============================================================================
 */

#ifndef GSPATTERNPYWRAP_H_INCLUDED
#define GSPATTERNPYWRAP_H_INCLUDED
#include "PythonUtils.h"


#include "GSPattern.h"
#include "GSPatternEventPyWrap.h"


class GSPatternPyWrap{
public:

  GSPatternPyWrap(){
    NameObjName = PyFromString("name");
    DurationObjName = PyFromString("duration");
    EventsObjName = PyFromString("events");
    timeSignatureName =PyFromString("timeSignature");

  }

  PyObject * gsapiModule ;
  PyTypeObject * gsPatternType;


  ~GSPatternPyWrap(){
    Py_DECREF(NameObjName);
    Py_DECREF(DurationObjName);
    Py_DECREF(EventsObjName);
    Py_DECREF(timeSignatureName);
  }
  void init(){
    gsapiModule = PyImport_ImportModule("gsapi");
    PyObject * gsapiDict = PyModule_GetDict(gsapiModule);
    gsPatternType = (PyTypeObject*)PyDict_GetItemString(gsapiDict, "GSPattern");
    eventWrap.gsPatternEventType = (PyTypeObject*)PyDict_GetItemString(gsapiDict, "GSPatternEvent");
    //
    //		GSPattern p;
    //		p.name = "test";
    //		GeneratePyObj(&p);



  }

  GSPattern* GenerateFromObj(PyObject* o,GSPattern * original=nullptr){
    if(!o)return nullptr;
    PyObject ** obj = _PyObject_GetDictPtr(o);
    if(!obj){DBG("weird class passed back"); return nullptr;}
    PyObject * dict = *obj;



    GSPattern * p = original;
    if(!PyDict_Check(dict)){DBG("no dict passed back"); return p;}
    if(p== nullptr){
      p = new GSPattern();
    }
    {
      PyObject * n = PyDict_GetItem(dict, NameObjName);
      if(n){p->name = PyToString(n);}
    }
    {
      PyObject * n = PyDict_GetItem(dict, DurationObjName);
      if(n){p->duration = PyFloat_AsDouble(n);}
    }
    {
      PyObject * n = PyDict_GetItem(dict, timeSignatureName);
      if(n && PyList_GET_SIZE(n)==2){
        p->timeSigNumerator=  PyInt_AsLong( PyList_GET_ITEM(n, 0));
        p->timeSigDenominator=  PyInt_AsLong( PyList_GET_ITEM(n, 1));
      }
    }

    {
      PyObject * n = PyDict_GetItem(dict, EventsObjName);
      if(n){

        if(PyList_Check(n)){
          int size = PyList_GET_SIZE(n);
          p->events.resize(size);
          for(int i = 0 ; i < size ; i++){
            GSPatternEvent * e = eventWrap.GenerateFromObj(PyList_GET_ITEM(n, i));
            if(e){p->events[i] = e;}
            else{DBG("wrong event added");}
          }
        }
        else{DBG("weird events structure");}

      }

    }
    return p;
  }

  PyObject*  GeneratePyObj(GSPattern * p,PyObject * existing=nullptr){
    if(!p)return nullptr;
    PyObject * res = existing;

    //		create one if needed
    if(res==nullptr){
      PyObject * dummyArg = PyTuple_New(0);
      res = PyObject_Call((PyObject*)gsPatternType,dummyArg,nullptr);
    }

    //		PyObject * dbg = PyObject_Dir(res);
    //		DBG(PyToString(dbg));

    if(PyObject_SetAttr(res, NameObjName, PyFromString(p->name.c_str()))==-1){DBG("can't set Name");};
    if(PyObject_SetAttr(res, DurationObjName, PyLong_FromDouble(p->duration))==-1){DBG("can't set Duration");};

    {
      PyObject * n = PyList_New(2);
      PyList_SetItem(n, 0, PyInt_FromLong(p->timeSigNumerator));
      PyList_SetItem(n, 1, PyInt_FromLong(p->timeSigDenominator));
      if(PyObject_SetAttr(res, timeSignatureName, n)==-1){DBG("can't set timesignature");};
    }


    {
      int evSize = p->events.size();
      PyObject * n = PyList_New(evSize);
      for(int i = 0 ; i < evSize ; i++){
        PyObject * e = eventWrap.generatePyObj(p->events[i]);
        if(e){PyList_SetItem(n, i, e);}
        else{DBG("can't generate pyObj for event");}
      }
      PyObject_SetAttr(res, EventsObjName, n);
    }





    return res;
  }


private:


  PyObject * NameObjName;
  PyObject * DurationObjName;
  PyObject * EventsObjName;
  PyObject * timeSignatureName;
  
  GSPatternEventPyWrap eventWrap;
  
};


#endif  // GSPATTERNPYWRAP_H_INCLUDED
