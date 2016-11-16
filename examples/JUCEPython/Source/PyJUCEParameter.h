/*
 ==============================================================================
 
 PyJUCEParameter.h
 Created: 6 Jul 2016 10:36:47am
 Author:  martin hermant
 
 ==============================================================================
 */

#ifndef PYJUCEPARAMETER_H_INCLUDED
#define PYJUCEPARAMETER_H_INCLUDED
#include "PythonUtils.h"
#include "JuceHeader.h"


class PyJUCEAPI;

class PyJUCEParameter:ComponentListener{
public:
	
  PyJUCEParameter(PyObject * o,const String & _name);
  virtual ~PyJUCEParameter();

  bool  updateUidFromObject(PyObject * o);
  static int64 getUidFromObject(PyObject *o);
  int64 pyUID;
  static PyObject * uidKey;
  String name;
  var value;
  Rectangle<float> relativeArea;
  NamedValueSet  properties;

  virtual void setValue(var v);
  virtual var getValue();

  class ParameterListener{
  public:
    virtual ~ParameterListener(){};
    virtual void parameterChanged(PyJUCEParameter * )=0;
  };

  ListenerList<ParameterListener> paramListeners;
  void addParameterListener(ParameterListener * l){paramListeners.add(l);}
  void removeParameterListener(ParameterListener * l){paramListeners.remove(l);}

  Component * buildComponent();

	
protected:
	// need to be overriden
	virtual Component * createComponent(var v,const NamedValueSet & properties)=0;
	virtual PyObject* getPythonObject()=0;
  virtual void updateComponentState(Component * ){};
  virtual   void registerListener(Component *){};
  virtual void removeListener(Component *){};

  void updateFromPython();

	
  friend class PyJUCEAPI;
  friend class PyJUCEParameterBuilder;
	PyObject* cbFunc;
  PyObject* pyRef;
  PyObject * pyVal;


  PyObject* listenerName;
	PyJUCEAPI * pyJuceApi;


  void deleteOldComponents();
  Array<WeakReference<Component> > linkedComponents;

private:
  void linkToJuceApi(PyJUCEAPI * );
  void setPythonCallback(PyObject *);
	
	void componentBeingDeleted(Component & c)override;

	
};

class PyJUCEParameterBuilder{
public:
	PyJUCEParameterBuilder(PyJUCEAPI* _py):pyAPI(_py){}
  PyJUCEParameter * buildParamFromObject( PyObject* );
	PyJUCEAPI * pyAPI;
};

class PyFloatParameter;

#endif  // PYJUCEPARAMETER_H_INCLUDED
