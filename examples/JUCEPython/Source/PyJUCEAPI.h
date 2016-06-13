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

extern int _wrap_convert_py2c__GSPattern(PyObject *value, GSPattern *address);

class PyJUCEAPI{
public:
    PyJUCEAPI(){}

    void load();
    void init();
    bool isLoaded();
    GSPattern * getNewPattern();
    PythonWrap  py ;
};


#endif  // PYJUCEAPI_H_INCLUDED
