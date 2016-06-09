/*
  ==============================================================================

    pythonWrap.cpp
    Created: 9 Jun 2016 10:52:18am
    Author:  Martin Hermant

  ==============================================================================
*/

#include "pythonWrap.h"

#include <dlfcn.h>
#include <stdio.h>

void* dummyFunc(){return nullptr;};

string PythonWrap::getVSTPath(){
    Dl_info dl_info;
    dladdr((void *)dummyFunc, &dl_info);
    string currentVSTPath =dl_info.dli_fname;
    fprintf(stderr, "module %s loaded\n", currentVSTPath.c_str());
    return currentVSTPath;
}


void PythonWrap::initPath(){

//    prependPath("PATH", "/usr/local/bin");
//    prependPath("PYTHONPATH","/usr/local/lib/python2.7/site-packages");
#ifdef CUSTOM_PYTHON
    Py_SetProgramName("python2.7");

    Py_SetPythonHome(currentVSTPath+"/../Frameworks/Python.framework/Versions/2.7");
#endif

    cout << Py_GetPath() << endl;
//    if(!Py_GetPythonHome()){

//    }
    if(Py_GetPythonHome())
        cout << Py_GetPythonHome() << endl;
    cout << Py_GetProgramFullPath() << endl;
    
}

void PythonWrap::prependPath(const string &env,const string& newpath){
    const char* env_p = getenv(env.c_str());
    std::string mergedPath ;
    if(env_p){
        mergedPath+=newpath+":"+env_p;
    }
    else{
        mergedPath = newpath;
    }
    setenv(env.c_str(),mergedPath.c_str(),1);
    std::cout << "Your"<<env << " is: " << getenv(env.c_str()) << '\n';
}

string PythonWrap::test(const string& s){


        // Import the module "plugin" (from the file "plugin.py")
        PyObject* moduleName = PyString_FromString("plugin");
        PyObject* pluginModule = PyImport_Import(moduleName);
        // Retrieve the "transform()" function from the module.
        PyObject* transformFunc = PyObject_GetAttrString(pluginModule, "transform");
        // Build an argument tuple containing the string.
        PyObject* argsTuple = Py_BuildValue("(s)", s.c_str());
        // Invoke the function, passing the argument tuple.
        PyObject* result = PyObject_CallObject(transformFunc, argsTuple);
        // Convert the result to a std::string.
        std::string resultStr(PyString_AsString(result));
        // Free all temporary Python objects.
        Py_DECREF(moduleName); Py_DECREF(pluginModule); Py_DECREF(transformFunc);
        Py_DECREF(argsTuple); Py_DECREF(result);
        
        return resultStr;
    
}

