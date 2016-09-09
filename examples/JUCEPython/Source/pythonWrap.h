/*
  ==============================================================================

    pythonWrap.h
    Created: 9 Jun 2016 10:52:18am
    Author:  Martin Hermant

  ==============================================================================
*/

#ifndef PYTHONWRAP_H_INCLUDED
#define PYTHONWRAP_H_INCLUDED

#include "JuceHeader.h"
#include "PythonUtils.h"

#include <string>
#include <iostream>
using namespace std;


class PythonWrap{
    public :


  PythonWrap():errIntercept(this){}
	~PythonWrap(){deinit();}
    string test(const string& s,PyObject * module);
  
    void printPyState();
  void init( string home, string  bin="");
	void setFolderPath(const string & s);
    PyObject* loadModule(const string & name,PyObject * oldModule=nullptr);
    void initSearchPath();
    void addSearchPath(const string &);
    
	PyObject * callFunction(const string & func,PyObject * module,PyObject * args=nullptr);
	PyObject * callFunction(PyObject * func,PyObject * module,PyObject * args);
		void deinit();
	class PipeIntercepter : public ChangeBroadcaster,AsyncUpdater{
	public:

    PipeIntercepter(PythonWrap * o):owner(o){
			listenerNum = 0;
		}
		~PipeIntercepter(){

			handleUpdateNowIfNeeded();
		}
		class Entry{
		public:
			enum Type{
				warning,
				error
			};
			Entry(){}
			Entry(String str,Type t):type(t),msg(str){
				time = Time::getCurrentTime();
			}
			Type type;
			String msg;
			Time time;
			
		};
		Array<Entry> entries;
		mutex mut;
		int listenerNum;
		
		void addLogListener (ChangeListener* listener){

			listenerNum ++;
      if(listenerNum==1){owner->redirectStd(true);}
			addChangeListener(listener);
			sendChangeMessage();
		}
		void removeLogListener (ChangeListener* listener){

			removeChangeListener(listener);
			listenerNum --;
      if(listenerNum==0){owner->redirectStd(false);}
			jassert(listenerNum>=0);
		}
		
		void handleAsyncUpdate() override{
			flush();
		}
		void flush(){
			if(listenerNum==0)return;
			if(MessageManager::getInstance()->isThisTheMessageThread()){
			dispatchPendingMessages();
				{
					lock_guard<mutex> lk(mut);
					entries.clearQuick();
				}
			}
			else{
				triggerAsyncUpdate();
			}

		}
    PythonWrap *owner;
	};

  
  static PipeIntercepter * getIntercepter();
	static PyObject * PyErrCB(PyObject *self, PyObject *args);
	static PyObject * PyOutCB(PyObject *self, PyObject *args);
  PyObject * originStdErr,* originStdOut;
  PyObject * customStdErr,* customStdOut;
   void redirectStd(bool t);
  static PythonWrap *  i();



private:
  
   PipeIntercepter   errIntercept;
//    void prependEnvPath(const string &env,const string& newpath);
    void printEnv(const string & p);
	string curentFolderPath;




};




#endif  // PYTHONWRAP_H_INCLUDED
