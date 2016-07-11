/*
 ==============================================================================
 
 PyJUCEParameter.cpp
 Created: 6 Jul 2016 10:36:47am
 Author:  martin hermant
 
 ==============================================================================
 */

#include "PyJUCEParameter.h"
#include "pythonWrap.h"

void PyJUCEParameter::setValue(var v){
	value=v;
	py->callFunction(cbFunc,getPythonObject());;
}

var PyJUCEParameter::getValue(){return value;}

Component * PyJUCEParameter::buildComponent(){
	Component *res = createComponent( value,properties);
	if (res) {
		var * x,*y,*w,*h;
    if((x=properties.getVarPointer("x")) &&
				(y=properties.getVarPointer("y")) &&
				(w=properties.getVarPointer("width")) &&
				(h=properties.getVarPointer("height")))
		{
			relativeArea.setBounds(*x, *y, *w, *h);
		}
		else{DBG("no size given");}
	}
	return res;
	
}

void PyJUCEParameter::linkToPyWrap(PythonWrap * p){py=p;};

void PyJUCEParameter::setPythonCallback(PyObject * cb){
	cbFunc = cb;
}

class PyFloatParameter:public PyJUCEParameter,public SliderListener{
	
	void sliderValueChanged (Slider* slider) override{setValue(slider->getValue());}
	
	Component *  createComponent(var v,const NamedValueSet & properties) override{
		Slider * s = new Slider(juce::Slider::SliderStyle::LinearVertical, juce::Slider::TextEntryBoxPosition::TextBoxBelow);
		var *p = nullptr;
		{
			var *p2 = nullptr;
			if((p =properties.getVarPointer("min")) && (p2=properties.getVarPointer("max"))){s->setMinAndMaxValues(*p, *p2);}
		}
		// TODO style handling
		//		if((p=properties.getVarPointer("style"))){s->setStyle(*p);}
		s->addListener(this);
		return s;
	}
	
	PyObject * getPythonObject() override{return PyFloat_FromDouble(value);}
};




var pyToVar(PyObject * o){
	var  res;
	if(PyInt_Check(o)){	res = (int)PyInt_AsLong(o);}
	else if(PyFloat_Check(o)){res = (double)PyFloat_AsDouble(o);}
	else if(PyString_Check(o)){res = (char *)PyString_AsString(o);}
	
	return res;
}


PyJUCEParameter * PyJUCEParameterBuilder::buildParamFromObject( PyObject* o){
	NamedValueSet properties;
	PyObject* props = PyObject_GetAttrString(o, "UIparams");
	if(props && 		PyDict_Check(props)){
		PyObject *key, *value;
		Py_ssize_t pos = 0;
		
		while (PyDict_Next(props, &pos, &key, &value)) {
			var v = pyToVar(value);
			if(!v.isUndefined())properties.set(PyString_AsString(key), v);
			else{DBG("cant find type for param property :" << PyString_AsString(key));}
		}
	}
	
	
	
	
	PyJUCEParameter* res = nullptr;
	PyObject * value = PyObject_GetAttrString(o, "_UIParameter__value");
	if(!value){DBG("ui element not valid");jassertfalse;return nullptr;}
	
	if(PyInt_Check(value)){
		res = new PyFloatParameter();
	}
	else if(PyFloat_Check(value)){
		res = new PyFloatParameter();
	}
	else {
		DBG("ui element not supported : " <<value->ob_type->tp_name);
	}
	if(res){
		res->setPythonCallback(PyObject_GetAttrString(o, "setValue"));
		res->properties = properties;
	}
	return res;
}