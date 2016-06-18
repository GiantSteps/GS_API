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

void PythonWrap::init(){
    if(!Py_IsInitialized())
    {

        initPath();
        Py_NoSiteFlag = 0;
//        void * h = dlopen("/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib", RTLD_NOW | RTLD_GLOBAL);
//        if(h==nullptr){
//            cout <<"preloading failed : " <<dlerror()<< endl;
//        }

        Py_InitializeEx(0);

        if(Py_NoSiteFlag>0){
            PyRun_SimpleString("import sys;print sys.executable;");
            PyRun_SimpleString("print sys.path;");

            PyRun_SimpleString("print sys.exec_prefix;");
            PyRun_SimpleString("print sys.flags;");
            PyRun_SimpleString("print sys.meta_path;");
            PyRun_SimpleString("import pdb;import ctypes; ctypes.cdll.LoadLibrary('/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/_locale.so');");
            {
                char * c =  dlerror();
                if(c){
                    cout<< "error dlopen : " << endl;
                }
            }

            PyRun_SimpleString("print sys.getdlopenflags();");
            PyRun_SimpleString("import dl;sys.setdlopenflags(dl.RTLD_NOW|dl.RTLD_GLOBAL) ");
            PyRun_SimpleString("print sys.getdlopenflags();");

            PyRun_SimpleString("import _locale");
            PyErr_Print();
            char * c =  dlerror();
            if(c){
                cout<< "error dlopen : " << endl;
            }

            PyRun_SimpleString("import os;");
            PyRun_SimpleString("print os.path.abspath(_locale.__file__)");
            PyRun_SimpleString("import site");
            PyRun_SimpleString("print os.path.abspath(site.__file__)");

        }

    }
}

void PythonWrap::initPath(){

#ifdef CUSTOM_PYTHON


    Py_SetPythonHome("/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7");

    Py_SetProgramName("/usr/local/bin/python");

    printEnv("PATH") ;
    prependEnvPath("DYLD_LIBRARY_PATH","/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload");
    printEnv("LD_LIBRARY_PATH");
    printEnv("PYTHONPATH") ;
    printEnv("PYTHONHOME") ;
    printEnv("DYLD_LIBRARY_PATH");
    printEnv("DYLD_FALLBACK_LIBRARY_PATH");
    printEnv("PYTHON_INCLUDE_DIR");


#endif

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
    if(c){
        cout<<c << endl;

    }
    else{
        cout<< "isempty" << endl;
    }

}


void PythonWrap::initSearchPath(){
    PyRun_SimpleString("import sys;site.addsitedir('/usr/local/lib/python2.7/site-packages');");
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
    else{pluginModule = PyImport_Import(moduleName);
        if(!pluginModule){
            // spitout errors if importing fails
            PyRun_SimpleString("import VSTPlugin");
        }
    }


    Py_DECREF(moduleName);
    return pluginModule!=nullptr;
}

bool PythonWrap::isFileLoaded(){return pluginModule!=nullptr;}

PyObject * PythonWrap::callFunction(const string & func){
    PyObject* pyFunc = PyObject_GetAttrString(pluginModule, func.c_str());
    if(pyFunc ==nullptr){
        cout << "function not found : " << func << endl;
        return nullptr;
    }

    return PyObject_CallObject(pyFunc,nullptr);



}

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

