/*
 ==============================================================================

 pythonWrap.cpp
 Created: 9 Jun 2016 10:52:18am
 Author:  Martin Hermant

 ==============================================================================
 */

#include "pythonWrap.h"


PythonWrap * PythonWrap::i(){
  static PythonWrap * instance = new PythonWrap();
  return instance;
}

PythonWrap::PipeIntercepter * PythonWrap::getIntercepter(){return &PythonWrap::i()->errIntercept;}

 PyObject *
PythonWrap::PyErrCB(PyObject *self, PyObject *args)
{
	const char *what;
  PipeIntercepter * errIntercept = PythonWrap::getIntercepter();
	if (!PyArg_ParseTuple(args, "s", &what))
		return NULL;
	{
		lock_guard<mutex> lk(errIntercept->mut);
		errIntercept->entries.add(PipeIntercepter::Entry(String(what),PipeIntercepter::Entry::error));
	}
	errIntercept->sendChangeMessage();
	return Py_BuildValue("");
}


 PyObject *
PythonWrap::PyOutCB(PyObject *self, PyObject *args)
{
	const char *what;
  PipeIntercepter * errIntercept = PythonWrap::getIntercepter();
	if (!PyArg_ParseTuple(args, "s", &what))
		return NULL;

	{
		lock_guard<mutex> lk(errIntercept->mut);
		errIntercept->entries.add(PipeIntercepter::Entry(String(what),PipeIntercepter::Entry::warning));
	}
	errIntercept->sendChangeMessage();
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
    Py_InitializeEx(0);

    originStdErr  = PySys_GetObject("stderr");
    originStdOut  = PySys_GetObject("stdout");

    customStdErr = Py_InitModule("PyErrCB", PyErr_methods);
    customStdOut = Py_InitModule("PyOutCB", PyOut_methods);



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
void PythonWrap::deinit(){
	Py_Finalize();
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

  PyObject* moduleName = PyFromString(name.c_str());

  PyObject * newModule = nullptr;
  if (oldModule) {
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

    //        PyRun_SimpleString(reloadS.c_str());
  }
  else{
    //    dlopen("libpython2.7.so", RTLD_LAZY | RTLD_GLOBAL);
    newModule = PyImport_Import(moduleName);

  }
  if(!newModule){
    cout << "failed to load: " << name << endl;
    // spitout errors if importing fails
    PyErr_Print();

  }
	errIntercept.flush();


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

