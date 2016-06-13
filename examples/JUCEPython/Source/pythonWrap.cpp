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
    fprintf(stderr, "vstPath : %s \n", currentVSTPath.c_str());
    return currentVSTPath;
}


void PythonWrap::initPath(){

#ifdef CUSTOM_PYTHON

    Py_SetProgramName("/usr/local/bin/python");

//    Py_SetPythonHome(getVSTPath()+"/../Frameworks/Python.framework/Versions/2.7");
#endif

    cout << Py_GetPath() << endl;
//        if(!Py_GetPythonHome()){
//
//        }
    if(Py_GetPythonHome())
        cout << Py_GetPythonHome() << endl;
    cout << Py_GetProgramFullPath() << endl;



}


void PythonWrap::initSearchPath(){
    PyRun_SimpleString("import sys");
    addSearchPath("/usr/local/lib/python2.7/site-packages");
}

void PythonWrap::addSearchPath(const string & p){
    string pathToAppend = "sys.path.append(\""+p+"\");";
    PyRun_SimpleString(pathToAppend.c_str());

}



void PythonWrap::prependEnvPath(const string &env,const string& newpath){
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
bool PythonWrap::load(){
    // Import the module "plugin" (from the file "plugin.py")
    PyRun_SimpleString("print sys.path;");

    
    PyObject* moduleName = PyString_FromString("VSTPlugin");
    Py_XDECREF(pluginModule);
    if (isFileLoaded()) {
        cout << "reload" << endl;
        PyRun_SimpleString("reload(VSTPlugin)");
    }
    else{pluginModule = PyImport_Import(moduleName);}
    // spitout errors if importing fails
        PyRun_SimpleString("import VSTPlugin");

    Py_DECREF(moduleName);
    return pluginModule!=nullptr;
}

bool PythonWrap::isFileLoaded(){return pluginModule!=nullptr;}

string PythonWrap::test(const string& s){




    if(pluginModule){
        // Retrieve the "transform()" function from the module.
        PyObject* transformFunc = PyObject_GetAttrString(pluginModule, "test");
        // Build an argument tuple containing the string.
        PyObject* argsTuple = Py_BuildValue("(s)", s.c_str());
        // Invoke the function, passing the argument tuple.
        PyObject* result = PyObject_CallObject(transformFunc, argsTuple);
        // Convert the result to a std::string.
        std::string resultStr(PyString_AsString(result));
        // Free all temporary Python objects.
        Py_DECREF(transformFunc);
        Py_DECREF(argsTuple); Py_DECREF(result);
            return resultStr;
    }
    return "";

    
}

