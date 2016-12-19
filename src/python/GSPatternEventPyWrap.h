/*
 ==============================================================================

 GSPatternEventPyWrap.h
 Created: 19 Jun 2016 6:52:46pm
 Author:  Martin Hermant

 ==============================================================================
 */

#ifndef GSPATTERNEVENTPYWRAP_H_INCLUDED
#define GSPATTERNEVENTPYWRAP_H_INCLUDED

#include "PythonUtils.h"
#include "GSPatternEvent.h"


class GSPatternEventPyWrap{
public:

  GSPatternEventPyWrap(){

    StartObjName = PyFromString("startTime");
    DurationObjName = PyFromString("duration");
    PitchObjName = PyFromString("pitch");
    VelocityObjName = PyFromString("velocity");
    TagsObjName = PyFromString("tag");

    init();
  }
  ~GSPatternEventPyWrap(){
    Py_CLEAR(TagsObjName);
    Py_CLEAR(DurationObjName);
    Py_CLEAR(StartObjName);
    Py_CLEAR(PitchObjName);
    Py_CLEAR(VelocityObjName);
  }

  void init(){


  }

  PyTypeObject * gsPatternEventType;

  GSPatternEvent* GenerateFromObj(PyObject* o){
    GSPatternEvent * e = nullptr;
    PyObject ** obj = _PyObject_GetDictPtr(o);
    if(!obj){DBG("weird class passed back"); return nullptr;}
    PyObject * dict = *obj;
    if(!PyDict_Check(dict)){DBG("no dict passed back");}
    else{
      e = new GSPatternEvent();
      {
        PyObject * n = PyDict_GetItem(dict, StartObjName);
        if(n){e->start = PyFloat_AsDouble(n);}
      }
      {
        PyObject * n = PyDict_GetItem(dict, DurationObjName);
        if(n){e->duration = PyFloat_AsDouble(n);}
      }

      {
        PyObject * n = PyDict_GetItem(dict, PitchObjName);
        if(n){e->pitch = PyLong_AsLong(n);}
      }

      {
        PyObject * n = PyDict_GetItem(dict, VelocityObjName);
        if(n){e->velocity = PyLong_AsLong(n);}
      }
      {
        PyObject * n = PyDict_GetItem(dict, TagsObjName);
        if(n){
          e->eventTags.clear();
          if(PyTuple_Check(n)){

            int s = PyTuple_Size(n);
            for(int i = 0 ; i < s; i++){
              if(PyObject * to = PyTuple_GetItem(n,i)){
                if(PyObject * stringOb = PyObject_Str(to)){
                  e->eventTags.push_back(PyToString(stringOb));
                }
                else{DBG("wrong type of tags in tuple : " << to->ob_type->tp_name);}
              }

            }

          }
          else if(PyObject * stringOb = PyObject_Str(n)) {
            e->eventTags.push_back(PyToString(stringOb));
          }
          else{DBG("wrong type of tags : " << n->ob_type->tp_name);}

        }
      }

    }



    return e;
  }

  PyObject * generatePyObj(GSPatternEvent * e,PyObject * original=nullptr){
    PyObject * res = original;

    PyObject* start = PyFloat_FromDouble(e->start);

    PyObject *duration= PyFloat_FromDouble(e->duration);
    PyObject *pitch=PyInt_FromLong(e->pitch);
    PyObject *velocity =PyInt_FromLong(e->velocity);

    int size = e->eventTags.size();
    PyObject * tags =nullptr;
    if(size==1){
      cout << e->eventTags[0] << endl;
      tags = PyFromString(e->eventTags[0].c_str());
    }
    else{
    tags = PyTuple_New(size);
    for(int i = 0 ; i < size; i++){
      PyObject * pe = PyFromString(e->eventTags[i].c_str());
      if(pe)PyTuple_SetItem(tags,i,pe);
      else{DBG("can't create event");}
    }
    }

    if(res==nullptr){

      PyObject * creationArg = Py_BuildValue("(f,f,i,i,O)",start,duration,pitch,velocity,tags);
      res = PyObject_Call((PyObject*)gsPatternEventType,creationArg,nullptr);
    }
    else{
      if(PyObject_SetAttr(res, StartObjName,start)==-1){DBG("can't set start");};
      if(PyObject_SetAttr(res, DurationObjName, duration)==-1){DBG("can't set duration");};
      if(PyObject_SetAttr(res, PitchObjName, pitch)==-1){DBG("can't set pitch");};
      if(PyObject_SetAttr(res, VelocityObjName, velocity)==-1){DBG("can't set velocity");};
      if(PyObject_SetAttr(res, TagsObjName, tags) == -1){DBG("can't set tag");}
    }

    //Py_DecRef(tags);

    return res;

  }

  PyObject*  TagsObjName ;
  PyObject*  DurationObjName ;
  PyObject*  StartObjName ;
  PyObject*  PitchObjName ;
  PyObject*  VelocityObjName ;
  
  
};



#endif  // GSPATTERNEVENTPYWRAP_H_INCLUDED
