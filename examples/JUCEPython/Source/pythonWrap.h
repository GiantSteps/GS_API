/*
  ==============================================================================

    pythonWrap.h
    Created: 9 Jun 2016 10:52:18am
    Author:  Martin Hermant

  ==============================================================================
*/

#ifndef PYTHONWRAP_H_INCLUDED
#define PYTHONWRAP_H_INCLUDED

#include "PythonUtils.h"


#include <string>
#include <iostream>
using namespace std;


class PythonWrap{
    public :

    PythonWrap():pluginModule(nullptr){}
    string test(const string& s);
    string getVSTPath();
    void printPyState();
  void init();
	void setFolderPath(const string & s);
    bool load(const string & name);
    void initSearchPath();
    void addSearchPath(const string &);
    bool isFileLoaded();
	PyObject * callFunction(const string & func,PyObject * args=nullptr);
	

    
private:
    void prependEnvPath(const string &env,const string& newpath);
    void printEnv(const string & p);
	string curentFolderPath;
    PyObject* pluginModule;

};




#endif  // PYTHONWRAP_H_INCLUDED
