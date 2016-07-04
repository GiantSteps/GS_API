/*
  ==============================================================================

    PythonUtils.h
    Created: 19 Jun 2016 6:56:09pm
    Author:  Martin Hermant

  ==============================================================================
*/

#ifndef PYTHONUTILS_H_INCLUDED
#define PYTHONUTILS_H_INCLUDED



#define _xcat(x,y) _cat(x,y)
#define _cat(x,y) x##y
#define _toxstr(x) _tostr(x)
#define _tostr(x) #x


#include _toxstr(PYTHON_HEADER)


//#define PY3

#ifdef  PY3
#define PyToString(x) PyUnicode_AS_DATA(x)
#define PyFromString(x) PyUnicode_FromString(x)
#else
#define PyToString(x) PyString_AsString(x)
#define PyFromString(x) PyString_FromString(x)
#endif


#include <iostream>


#ifndef DBG
#define DBG(x) std::cout << x << '\n';
#endif


#endif  // PYTHONUTILS_H_INCLUDED
