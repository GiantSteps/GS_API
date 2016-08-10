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
    init();
  }



  ~GSPatternPyWrap(){
    Py_DECREF(NameObjName);
    Py_DECREF(DurationObjName);
    Py_DECREF(EventsObjName);
		Py_DECREF(timeSignatureName);
  }
  void init(){


  }

  GSPattern* GenerateFromObj(PyObject* o){
		if(!o)return nullptr;
    PyObject ** obj = _PyObject_GetDictPtr(o);
    if(!obj){DBG("weird class passed back"); return nullptr;}
    PyObject * dict = *obj;



    GSPattern * p = nullptr;
    if(!PyDict_Check(dict)){DBG("no dict passed back"); return p;}

    p = new GSPattern();
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
            if(e){p->events[i] = *e;}
            else{DBG("wrong event added");}
          }
        }
        else{DBG("weird events structure");}

      }

    }
    return p;
  }


private:


  PyObject * NameObjName;
  PyObject * DurationObjName;
  PyObject * EventsObjName;
	PyObject * timeSignatureName;
  
  GSPatternEventPyWrap eventWrap;
  
};


#endif  // GSPATTERNPYWRAP_H_INCLUDED
