/*
  ==============================================================================

    PythonUtils.h
    Created: 19 Jun 2016 6:56:09pm
    Author:  Martin Hermant

  ==============================================================================
*/

#ifndef PYTHONUTILS_H_INCLUDED
#define PYTHONUTILS_H_INCLUDED



#define PYTHON_HEADER <Python/Python.h>


#include PYTHON_HEADER



#include <iostream>


#ifndef DBG
#define DBG(x) std::cout << x << '\n';
#endif


#endif  // PYTHONUTILS_H_INCLUDED
