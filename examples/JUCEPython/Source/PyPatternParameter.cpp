/*
  ==============================================================================

    PyPatternParameter.cpp
    Created: 15 Sep 2016 9:06:24am
    Author:  Martin Hermant

  ==============================================================================
*/

#include "PyPatternParameter.h"

HashMap<int64, int>  PyPatternParameter::counts ;

PyPatternParameter::PyPatternParameter(PyObject * o,const String & n):PyJUCEParameter(o,n){
  pattern =  PyJUCEAPI::GSPatternWrap->GenerateFromObj(pyVal);
  int originCount = 0;
  if(counts.contains(pyUID)){originCount = counts[pyUID];}
  counts.set(pyUID, originCount+1);
}
PyPatternParameter::~PyPatternParameter(){

  if(counts.contains(pyUID)){

    int originCount = counts[pyUID];

    if(originCount>1) {counts.set(pyUID,originCount-1);}
    else              {counts.remove(pyUID);}
  }

  
  //    delete pattern;
}
void PyPatternParameter::registerListener(Component *c) {((PatternComponent*)c)->addPatternListener(this);}
void PyPatternParameter::removeListener(Component *c){((PatternComponent*)c)->removePatternListener(this);}
void PyPatternParameter::patternChanged(PatternComponent * p){
  pattern = p->getPattern();
  setValue(var());
}
void PyPatternParameter::updateComponentState(Component *c) {
  pattern = PyJUCEAPI::GSPatternWrap->GenerateFromObj(pyVal,pattern);
  ((PatternComponent*)c)->newPatternLoaded(pattern);

}


Component *  PyPatternParameter::createComponent(var v,const NamedValueSet & properties) {
  PatternComponent * pc =  new PatternComponent();
  pc->newPatternLoaded(pattern);
  return pc;

}
bool PyPatternParameter::isMainPattern(){
  jassert(counts.contains(pyUID));
  bool isFirstAdded = counts[pyUID]==1;
  return isFirstAdded|| name=="Main";
}

PyObject * PyPatternParameter::getPythonObject() {return PyJUCEAPI::GSPatternWrap->GeneratePyObj(pattern,pyVal);}
