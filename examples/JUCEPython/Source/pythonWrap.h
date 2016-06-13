/*
  ==============================================================================

    pythonWrap.h
    Created: 9 Jun 2016 10:52:18am
    Author:  Martin Hermant

  ==============================================================================
*/

#ifndef PYTHONWRAP_H_INCLUDED
#define PYTHONWRAP_H_INCLUDED

//#define CUSTOM_PYTHON

#ifndef CUSTOM_PYTHON
#include <Python.h>
#else
#include "Python.h"
#endif

#include <string>
#include <iostream>
using namespace std;

class PythonWrap{
    public :

    PythonWrap():pluginModule(nullptr){}
    void initPath();
    string test(const string& s);
    string getVSTPath();
    bool load();
    void initSearchPath();
    void addSearchPath(const string &);
    bool isFileLoaded();

private:
    void prependEnvPath(const string &env,const string& newpath);


    PyObject* pluginModule;

};




#endif  // PYTHONWRAP_H_INCLUDED
