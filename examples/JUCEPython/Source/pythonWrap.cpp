/*
 ==============================================================================

 pythonWrap.cpp
 Created: 9 Jun 2016 10:52:18am
 Author:  Martin Hermant

 ==============================================================================
 */

#include "pythonWrap.h"

//juce_ImplementSingleton(PythonWrap);

HashMap<int64, PythonWrap* > PythonWrap::interpreters;

PyThreadState * PythonWrap::globalTs;


PythonWrap * PythonWrap::i(int64 pyUID){
  if(!interpreters.contains(pyUID)){
    interpreters.set(pyUID,(PythonWrap*) new PythonWrap(pyUID));
  }
  return interpreters[pyUID];
}

PythonWrap::PythonWrap(int64 p):pyUID(p),errIntercept(p),threadState(nullptr){}
PythonWrap::~PythonWrap(){
  if(Py_IsInitialized()){
//    Py_DecRef(originStdErr);
//    Py_DecRef(originStdOut);
//    Py_DecRef(customStdErr);
//    Py_DecRef(customStdOut);
    PyThreadState_Swap(threadState);
    Py_EndInterpreter(threadState);

  }
}
PythonWrap::PipeIntercepter * PythonWrap::getIntercepter(){return &errIntercept;}

PythonWrap * PythonWrap::getCurrentPythonWrap(){

  HashMap<int64, PythonWrap* >::Iterator it(interpreters);
  while(it.next()){
    if(PythonWrap * pyW=it.getValue()){
      if(_PyThreadState_Current == pyW->threadState){
        return pyW;
      }
    }
  }
  return nullptr;
}
PyObject *
PythonWrap::PyErrCB(PyObject *self, PyObject *args)
{
  if(PythonWrap * pyW = PythonWrap::getCurrentPythonWrap()){
    const char *what;

    PipeIntercepter * errIntercept = pyW->getIntercepter();
    if (!PyArg_ParseTuple(args, "s", &what))
      return NULL;
    {
      lock_guard<mutex> lk(errIntercept->mut);
      errIntercept->entries.add(PipeIntercepter::Entry(String(what),PipeIntercepter::Entry::error));
    }
    errIntercept->sendChangeMessage();

  }
  return Py_BuildValue("");
}


PyObject *
PythonWrap::PyOutCB(PyObject *self, PyObject *args)
{
  if(PythonWrap * pyW = PythonWrap::getCurrentPythonWrap()){
    const char *what;
    PipeIntercepter * errIntercept = pyW->getIntercepter();
    if (!PyArg_ParseTuple(args, "s", &what))
      return NULL;

    {
      lock_guard<mutex> lk(errIntercept->mut);
      errIntercept->entries.add(PipeIntercepter::Entry(String(what),PipeIntercepter::Entry::warning));
    }
    errIntercept->sendChangeMessage();
  }
  return Py_BuildValue("");
}
static PyMethodDef PyErr_methods[] = {
  {"write", PythonWrap::PyErrCB, METH_VARARGS, "PyErr Callback"},
  {NULL, NULL, 0, NULL}
};

static PyMethodDef PyOut_methods[] = {
  {"write", PythonWrap::PyOutCB, METH_VARARGS, "PyOut Callback"},
  {NULL, NULL, 0, NULL}
};





void PythonWrap::init(  string home, string  bin){

  if(!Py_IsInitialized())
  {

    Py_SetPythonHome(&home[0]);
    if(bin!=""){Py_SetProgramName(&bin[0]);}
    char* c =  Py_GetPythonHome();
    if(c){ DBG("home : "<<c);}
    char* cc =  Py_GetProgramName();
    if(cc){ DBG("prog : " <<cc);}
    printPyState();
    Py_NoSiteFlag =0;
    Py_VerboseFlag = 0;
    Py_DebugFlag = 0;
//    PyEval_InitThreads();

    Py_InitializeEx(0);
    globalTs = PyThreadState_GET();
    int dbg;
    dbg++;




  }
  if(Py_IsInitialized()){
    jassert(threadState==nullptr);
    if(threadState==nullptr){
      threadState = Py_NewInterpreter();
      originStdErr  = PySys_GetObject("stderr");
      originStdOut  = PySys_GetObject("stdout");

      customStdErr = Py_InitModule("PyErrCB", PyErr_methods);
      customStdOut = Py_InitModule("PyOutCB", PyOut_methods);
//      PyThreadState_Swap(threadState);
    }
  }
}


void PythonWrap::redirectStd(bool t){


  if(t){

    PySys_SetObject("stderr", customStdErr);
    PySys_SetObject("stdout", customStdOut);
    
  }
  else{
    PySys_SetObject("stderr", originStdErr);
    PySys_SetObject("stdout", originStdOut);
  }

}
void PythonWrap::finalize(){


  bool pyInitialized = Py_IsInitialized();
  if(pyInitialized){
    PyThreadState_Swap(globalTs);
    PyThreadState * ts= PyThreadState_GET();
    if(ts){
// crashes for unknown reason when recreating, creates a memory leak but better that than crash
//      Py_Finalize();
    }
  }
}


void PythonWrap::setFolderPath(const string & s){
  curentFolderPath = s;
  DBG("currentFolderPath : " << s);
  addSearchPath(s);

}

void PythonWrap::initSearchPath(){
  //  site will add site-package depending on pythonhome
  // this function is useful if python is started without
  PyRun_SimpleString("import sys;import site;");
  PyRun_SimpleString("print sys.path;");

}



void PythonWrap::addSearchPath(const string & p){
  string pathToAppend = "sys.path.append(\""+p+"\");";
  PyRun_SimpleString(pathToAppend.c_str());

}




PyObject * PythonWrap::loadModule(const string & name,PyObject * oldModule){
  // Import the module "plugin" (from the file "plugin.py")

  if(threadState){
    jassert(PyThreadState_Swap(threadState));
  }
  else{
    jassertfalse;
  }
  PyObject* moduleName = PyFromString(name.c_str());
  bool hasChangedModule = false;
  if(oldModule){
    if(PyModule_GetName(oldModule) != name){
      Py_DECREF(oldModule);
      hasChangedModule = true;
      
    }

  }
  PyObject * newModule = nullptr;
  if (oldModule && !hasChangedModule ) {
    //        cout << "reloading : " << name << endl;
    //        const string reloadS = "reload("+name+")";
      setFolderPath(curentFolderPath);
    
    newModule= PyImport_ReloadModule(oldModule);
    if(newModule){
      Py_DECREF(oldModule);
    }
    else{
      cout << "failed reload: " << name << endl;
      printPyState();
      PyErr_Print();

    }


    //    newModule = PyImport_Import(moduleName);


  }
  else{
    //    dlopen("libpython2.7.so", RTLD_LAZY | RTLD_GLOBAL);
    //		PyImport_ExecCodeModuleEx
    newModule = PyImport_Import(moduleName);

  }
  if(!newModule){
    cout << "failed to load: " << name << endl;
    // spitout errors if importing fails
    PyErr_Print();

  }
  getIntercepter()->flush();


  Py_DECREF(moduleName);
  return newModule;
}





PyObject *  PythonWrap::callFunction(const string & func,PyObject * module,PyObject * args){
  if(module){
    PyObject* pyFunc = PyObject_GetAttrString(module, func.c_str());
    if(pyFunc ==nullptr){cout << "function not found " << func<< endl;return nullptr;}
    return callFunction(pyFunc,module,args);

  }

  return nullptr;



}
PyObject *  PythonWrap::callFunction(PyObject * pyFunc,PyObject * module,PyObject * args){
  if(pyFunc ==nullptr){return nullptr;}

  if(threadState){
    jassert(PyThreadState_Swap(threadState));
  }
  else{
    jassertfalse;
  }

  PyObject * targs = nullptr;
  if(args){
    if(!PyTuple_CheckExact(args)) targs =PyTuple_Pack(1,args);
    else targs = args;
    Py_IncRef(targs);
  }

  PyObject *res= PyObject_CallObject(pyFunc,targs);
  if(targs)Py_DecRef(targs);
  PyErr_Print();
  errIntercept.flush();

  return res;
}





//////////////////////////////
// debug utils

string PythonWrap::test(const string& s,PyObject * module){

  if(module){
    // Retrieve the "transform()" function from the module.
    PyObject* transformFunc = PyObject_GetAttrString(module, "test");
    // Build an argument tuple containing the string.
    PyObject* argsTuple = Py_BuildValue("(s)", s.c_str());
    // Invoke the function, passing the argument tuple.
    PyObject* result = PyObject_CallObject(transformFunc, argsTuple);
    // Convert the result to a std::string.
    std::string resultStr(PyToString(result));
    // Free all temporary Python objects.
    Py_DECREF(transformFunc);
    Py_DECREF(argsTuple); Py_DECREF(result);
    return resultStr;
  }
  return "";


}

void PythonWrap::printPyState(){


  cout << "prefix : " << Py_GetPrefix() <<endl;
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
  cout <<"fullPath : " <<  Py_GetProgramFullPath() << endl;

  printEnv("LD_LIBRARY_PATH");



}


void PythonWrap::printEnv(const string & p){
  char * c = getenv(p.c_str());
  cout<<p<<" : " ;
  if(c){cout<<c << endl;}
  else{cout<< "isempty" << endl;}

}




//void PythonWrap::prependEnvPath(const string &env,const string& newpath){
//  const char* env_p = getenv(env.c_str());
//  std::string mergedPath ;
//  if(env_p){mergedPath+=newpath+":"+env_p;}
//  else{mergedPath = newpath;}
//  setenv(env.c_str(),mergedPath.c_str(),1);
//  std::cout << "Your"<<env << " is: " << getenv(env.c_str()) << '\n';
//}

