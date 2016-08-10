/*
 ==============================================================================
 
 PyJUCEParameter.h
 Created: 6 Jul 2016 10:36:47am
 Author:  martin hermant
 
 ==============================================================================
 */

#ifndef PYJUCEPARAMETER_H_INCLUDED
#define PYJUCEPARAMETER_H_INCLUDED
#include "JuceHeader.h"
#include "PythonUtils.h"
class PyJUCEAPI;

class PyJUCEParameter{
public:
	
  PyJUCEParameter(const String & _name):name(_name){}

	virtual ~PyJUCEParameter(){}
	
	void linkToJuceApi(PyJUCEAPI * );
	String name;
	var value;
	
	Rectangle<float> relativeArea;

	NamedValueSet  properties;
	
	virtual void setValue(var v);
	virtual var getValue();
	Component * buildComponent(bool unique=false);
	
	void setPythonCallback(PyObject *);

	
protected:
	// need to be overriden
	virtual Component * createComponent(var v,const NamedValueSet & properties)=0;
	virtual PyObject* getPythonObject()=0;
	
	
	PyObject* cbFunc;
	PyJUCEAPI * pyJuceApi;
  ScopedPointer<Component> component;

	
};

class PyJUCEParameterBuilder{
public:
	PyJUCEParameterBuilder(PyJUCEAPI* _py):pyAPI(_py){}
	static PyJUCEParameter * buildParamFromObject( PyObject* );

	PyJUCEAPI * pyAPI;
};

class PyFloatParameter;

#endif  // PYJUCEPARAMETER_H_INCLUDED
