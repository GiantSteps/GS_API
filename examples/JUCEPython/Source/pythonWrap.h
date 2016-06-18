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
#include <Python/Python.h>
#else
#include "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/include/python2.7/Python.h"
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
    void init();
    bool load();
    void initSearchPath();
    void addSearchPath(const string &);
    bool isFileLoaded();
    PyObject* callFunction(const string&);
    
private:
    void prependEnvPath(const string &env,const string& newpath);
    void printEnv(const string & p);

    PyObject* pluginModule;

};




#endif  // PYTHONWRAP_H_INCLUDED
