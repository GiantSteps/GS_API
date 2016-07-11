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
class PythonWrap;

class PyJUCEParameter{
public:
	
	PyJUCEParameter(){}

	virtual ~PyJUCEParameter(){}
	
	void linkToPyWrap(PythonWrap * );
	String name;
	var value;
	
	Rectangle<float> relativeArea;

	NamedValueSet  properties;
	
	virtual void setValue(var v);
	virtual var getValue();
	Component * buildComponent();
	
	void setPythonCallback(PyObject *);

	
protected:
	// need to be overriden
	virtual Component * createComponent(var v,const NamedValueSet & properties)=0;
	virtual PyObject* getPythonObject()=0;
	
	
	PyObject* cbFunc;
	PythonWrap * py;
	
};

class PyJUCEParameterBuilder{
public:
	PyJUCEParameterBuilder(PythonWrap* _py):py(_py){}
	static PyJUCEParameter * buildParamFromObject( PyObject* );

	PythonWrap * py;
};

class PyFloatParameter;

#endif  // PYJUCEPARAMETER_H_INCLUDED
