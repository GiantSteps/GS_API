/*
 ==============================================================================
 
 PyJUCEAPI.cpp
 Created: 13 Jun 2016 5:00:10pm
 Author:  Martin Hermant
 
 ==============================================================================
 */

#include "PyJUCEAPI.h"
//#include "PyGSPattern.h"

#include "PluginProcessor.h"
#include "PyJUCEPython.h"
#include "Utils.h"


GSPatternPyWrap * PyJUCEAPI::GSPatternWrap(nullptr);
int PyJUCEAPI::instanceCount =0;

PyJUCEAPI::PyJUCEAPI(JucepythonAudioProcessor * o):

TimeListener(1),
owner(o),
pluginModule(nullptr),
apiModuleObject(nullptr),
isInitialized(false),
interfaceModule(nullptr),
paramBuilder(this)
{
  timePyObj = PyDict_New();
  timeKey=PyFromString("time");
  instanceCount++;
  pyUID = instanceCount;
  
}
PyJUCEAPI::~PyJUCEAPI(){
  cancelPendingUpdate();
  isInitialized = false;
  Py_DECREF(timePyObj);
  Py_DECREF(timeKey);
  Py_CLEAR(interfaceModule);
  Py_CLEAR(pluginModule);
  if(PythonWrap *pyW = PythonWrap::i(pyUID)){
    PythonWrap::interpreters.remove(pyUID);
    delete pyW;
  }
  if(PythonWrap::interpreters.size()==0){
    delete GSPatternWrap;
    GSPatternWrap = nullptr;
    PythonWrap::finalize();
  }
}


void PyJUCEAPI::callTimeChanged(double time){
	// TODO bug multiple load
  PyDict_SetItem(timePyObj, timeKey, PyFloat_FromDouble(time));
  PythonWrap::i(pyUID)->callFunction("onTimeChanged",pluginModule,timePyObj);
	
  Py_DECREF(timePyObj);
	
}



bool PyJUCEAPI::setNewPattern(PyObject * o){
	
  GSPattern * p=nullptr;
  bool found = false;
  // Legacy
	
  
	//		if(o!=Py_None){
	//      p = GSPatternWrap.GenerateFromObj(o);
	//      if(p){p->checkDurationValid();found = true;}
	//      else{DBG("pattern not valid");}
	//
	//    }
	////		Py_DECREF(o);
	//
	//  if(p)listeners.call(&Listener::newPatternLoaded,p);
  return found;
}


void PyJUCEAPI::callSetupFunction(){
  PyObject * o=nullptr;
	
  if((o = PythonWrap::i(pyUID)->callFunction("setup",pluginModule))){
		
    if(PyString_Check(o)){
      DBG("setup returned " << PyToString(o));
			
			
    }
    else if (o!=Py_None){
			
      DBG("unhandeled return type : "<< o->ob_type->tp_name);
    }
    Py_DECREF(o);
		
		
  }
  else {
    DBG("no setup function found or file not loaded");
  }
}
//


String PyJUCEAPI::getVSTPluginNameByIndex(int idx){
  Array<File> res = getAllPythonFiles();
	if (idx<res.size()) {return res[idx].getFileNameWithoutExtension();}
	return "";
}
Array<File> PyJUCEAPI::getAllPythonFiles(){

  jassert(VSTPluginFolder.isDirectory());
  
  Array<File> tmp ,res;
  VSTPluginFolder.findChildFiles(tmp, File::TypesOfFileToFind::findFiles, false,"*.py");
  for (auto & f : tmp){
    String name=f.getFileNameWithoutExtension();
    if(!name.endsWith("_interface") && name.startsWith("VST")){
      res.add(f);
    }
  }

  return res;
}
void PyJUCEAPI::init(){
  if(!isInitialized){
		String bin = getVSTProperties().getValue("pythonBin");
    String pyHome = getVSTProperties().getValue("pythonHome");
    if(pyHome==""){pyHome = getVSTPath()+"/../../Resources/pythonEnv";}
    else if(pyHome=="system"){pyHome = "";}
    if (bin=="") {bin = pyHome+"/bin/python2.7";}
    else if(bin=="system"){bin = "";}
		else{		DBG("using custom python : " << bin);}
    PythonWrap::i(pyUID)->printPyState();
    if (pyHome!="") bin=File(pyHome).getFullPathName();
    if (bin!="") bin=File(bin).getFullPathName();
    PythonWrap::i(pyUID)->init(bin.toStdString(),pyHome.toStdString());
    PyThreadState_Swap(PythonWrap::i(pyUID)->threadState);
    initJUCEAPI(this,&apiModuleObject);
    if(GSPatternWrap==nullptr){GSPatternWrap = new GSPatternPyWrap();}
    GSPatternWrap->init();
		String pythonFolder = getVSTProperties().getValue("VSTPythonFolderPath");
		bool loadCustom = pythonFolder=="custom";
		bool loadDefault = pythonFolder=="default";
		if (!loadCustom) {
			if (loadDefault  ) {
				VSTPluginFolder = File (getVSTPath()+"/../../Resources/python/");
				VSTPluginName = getVSTPluginNameByIndex(0);
        
			}
			else{
				VSTPluginFolder = pythonFolder;
				VSTPluginName = getVSTPluginNameByIndex(0);
			}
		}
		
		pythonFile = File (VSTPluginFolder).getChildFile(VSTPluginName+".py");
		
		if(loadCustom  || !pythonFile.exists()){
			juce::FileChooser fc("select Folder containing VSTPlugin.py");
			if(fc.browseForDirectory()){
				VSTPluginFolder = fc.getResult();
				VSTPluginName = getVSTPluginNameByIndex(0);
				getVSTProperties().setValue("VSTPythonFolderPath",fc.getResult().getFullPathName());
			}
			
		}

		if(pythonFile.exists()){
			PythonWrap::i(pyUID)->initSearchPath();
			PythonWrap::i(pyUID)->setFolderPath(VSTPluginFolder.getFullPathName().toStdString());
		}
		else{
			jassertfalse;
		}
  }
  isInitialized = pythonFile.exists();
	
}

bool PyJUCEAPI::setParam(PyObject* o){
  for(auto & p:params){
    if(p->pyRef==o){
      p->updateFromPython();
      DBG("found param to update");
      return true;
    }
  }
  return false;
}


void PyJUCEAPI::load(){
	// hack to load only the first time VST is called and for subsequent UI actions
	if(MessageManager::getInstance()->isThisTheMessageThread()  || !pluginModule){
  pluginModule =  PythonWrap::i(pyUID)->loadModule(VSTPluginName.toStdString(),pluginModule);
  lastPythonFileMod = pythonFile.getLastModificationTime();
	
  if (pluginModule){
    buildParamsFromScript();
		callSetupFunction();
  }
  listeners.call(&Listener::newFileLoaded,pythonFile);
	}
	else{
		DBG("can't load python from other threads");
	}
	
}

void PyJUCEAPI::buildParamsFromScript(){
	listeners.call(&Listener::paramsBeingCleared);
  params.clear();
  
  if((interfaceModule = PythonWrap::i(pyUID)->loadModule(VSTPluginName.toStdString()+"_interface",interfaceModule))){
		
    PyObject * o = PythonWrap::i(pyUID)->callFunction("getAllParameters",interfaceModule);
    if (o){

      if(PyList_Check(o)) {
        int s = PyList_GET_SIZE(o);
        for (int i = 0 ; i < s; i++){
          PyObject * it = PyList_GET_ITEM(o, i);
           PyObject * uidVal = PyLong_FromLong(pyUID);
          jassert(PyObject_SetAttr(it, PyJUCEParameter::uidKey, uidVal)!=-1);
          PyJUCEParameter * p = paramBuilder.buildParamFromObject(it);
          if(p){
            params.add(p);
          }
        }
      }
      Py_DECREF(o);
    }
    listeners.call(&Listener::newParamsLoaded,&params);
  }
  else{
    DBG("cant load interface or none provided");
  }
	
}



void PyJUCEAPI::timeChanged(double time) {callTimeChanged(time);};

void PyJUCEAPI::setWatching(bool w){
  if(w){startTimer(200);}
  else{stopTimer();}
}

void PyJUCEAPI::timerCallback(){
  if(pythonFile.getLastModificationTime()!=lastPythonFileMod){
    load();
  };
}
bool PyJUCEAPI::isLoaded(){
  return pluginModule!=nullptr;
}
