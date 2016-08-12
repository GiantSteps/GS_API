/*
  ==============================================================================

    PyJUCEPython.h
    Created: 19 Jul 2016 12:15:28pm
    Author:  Martin Hermant

  ==============================================================================
*/

#ifndef PYJUCEPYTHON_H_INCLUDED
#define PYJUCEPYTHON_H_INCLUDED

#include "PythonUtils.h"

class PyJUCEAPI;

PyMODINIT_FUNC initJUCEAPI(PyJUCEAPI * owner,PyObject ** apiModule);





#endif  // PYJUCEPYTHON_H_INCLUDED
