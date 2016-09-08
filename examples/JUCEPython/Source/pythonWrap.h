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

    PythonWrap(){}
	~PythonWrap(){deinit();}
    string test(const string& s,PyObject * module);
  
    void printPyState();
  void init(  string  bin="");
	void setFolderPath(const string & s);
    PyObject* loadModule(const string & name,PyObject * oldModule=nullptr);
    void initSearchPath();
    void addSearchPath(const string &);
    
	PyObject * callFunction(const string & func,PyObject * module,PyObject * args=nullptr);
	PyObject * callFunction(PyObject * func,PyObject * module,PyObject * args);
		void deinit();
	class PipeIntercepter : public ChangeBroadcaster,AsyncUpdater{
	public:

		PipeIntercepter(){
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
			addChangeListener(listener);
			sendChangeMessage();
		}
		void removeLogListener (ChangeListener* listener){

			removeChangeListener(listener);
			listenerNum --;
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
	};
	static PipeIntercepter errIntercept;

	static PyObject * PyErrCB(PyObject *self, PyObject *args);
	static PyObject * PyOutCB(PyObject *self, PyObject *args);

private:
//    void prependEnvPath(const string &env,const string& newpath);
    void printEnv(const string & p);
	string curentFolderPath;




};




#endif  // PYTHONWRAP_H_INCLUDED
