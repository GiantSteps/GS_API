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





void PythonWrap::init(){
  if(!Py_IsInitialized())
  {
    Py_InitializeEx(0);
  }
}


void PythonWrap::initSearchPath(){
  //  default brew python on OSX
  PyRun_SimpleString("import sys;import site;site.addsitedir('/usr/local/lib/python2.7/site-packages');");
  //    addSearchPath("/usr/local/lib/python2.7/site-packages");
  PyRun_SimpleString("print sys.path;");

}

void PythonWrap::addSearchPath(const string & p){
  string pathToAppend = "sys.path.append(\""+p+"\");";
  PyRun_SimpleString(pathToAppend.c_str());

}


bool PythonWrap::load(const string & name){
  // Import the module "plugin" (from the file "plugin.py")
  PyObject* moduleName = PyString_FromString(name.c_str());
  //    Py_XDECREF(pluginModule);

  if (isFileLoaded()) {
    //        cout << "reloading : " << name << endl;
    //        const string reloadS = "reload("+name+")";
    pluginModule = PyImport_ReloadModule(pluginModule);
    //        PyRun_SimpleString(reloadS.c_str());
  }
  else{
    pluginModule = PyImport_Import(moduleName);
  }
  if(!pluginModule){
      // spitout errors if importing fails
      const string importS = "import "+name;
      cout << "failed : " << name << endl;
      PyRun_SimpleString(importS.c_str());
    
  }


  Py_DECREF(moduleName);
  return pluginModule!=nullptr;
}



bool PythonWrap::isFileLoaded(){return pluginModule!=nullptr;}

PyObject * PythonWrap::callFunction(const string & func){
  if(isFileLoaded()){
    PyObject* pyFunc = PyObject_GetAttrString(pluginModule, func.c_str());
    if(pyFunc ==nullptr){
      cout << "function not found : " << func << endl;
      return nullptr;
    }

    return PyObject_CallObject(pyFunc,nullptr);
  }
  else{
    return nullptr;
  }


}

void* dummyFunc(){return nullptr;};
string PythonWrap::getVSTPath(){
  Dl_info dl_info;
  dladdr((void *)dummyFunc, &dl_info);
  string currentVSTPath =dl_info.dli_fname;
  fprintf(stderr, "vstPath : %s \n", currentVSTPath.c_str());
  return currentVSTPath;
}



//////////////////////////////
// debug utils

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

void PythonWrap::printPyState(){


  cout << "pre : " << Py_GetPrefix() <<endl;
  cout <<"execpre : "<<Py_GetExecPrefix() << endl;
  cout << "pypath : " << Py_GetPath() << endl;
  cout << "version : " << Py_GetVersion() << endl;
  cout << "compiler : " << Py_GetCompiler() << endl;
  cout << "buildI : " << Py_GetBuildInfo() << endl;
  //        if(!Py_GetPythonHome()){
  //
  //        }
  if(Py_GetPythonHome())
    cout <<"home : "<< Py_GetPythonHome() << endl;
  cout <<"full : " <<  Py_GetProgramFullPath() << endl;



}


void PythonWrap::printEnv(const string & p){
  char * c = getenv(p.c_str());
  cout<<p<<" : " ;
  if(c){cout<<c << endl;}
  else{cout<< "isempty" << endl;}

}



void PythonWrap::prependEnvPath(const string &env,const string& newpath){
  const char* env_p = getenv(env.c_str());
  std::string mergedPath ;
  if(env_p){mergedPath+=newpath+":"+env_p;}
  else{mergedPath = newpath;}
  setenv(env.c_str(),mergedPath.c_str(),1);
  std::cout << "Your"<<env << " is: " << getenv(env.c_str()) << '\n';
}

