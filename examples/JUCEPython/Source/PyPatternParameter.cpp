/*
  ==============================================================================

    PyPatternParameter.cpp
    Created: 15 Sep 2016 9:06:24am
    Author:  Martin Hermant

  ==============================================================================
*/

#include "PyPatternParameter.h"
int PyPatternParameter::count = 0;

PyPatternParameter::PyPatternParameter(PyObject * o,const String & n):PyJUCEParameter(o,n){
  pattern =  PyJUCEAPI::GSPatternWrap.GenerateFromObj(pyVal);
  count++;

}
PyPatternParameter::~PyPatternParameter(){
  count--;
  //    delete pattern;
}
void PyPatternParameter::registerListener(Component *c) {((PatternComponent*)c)->addPatternListener(this);}
void PyPatternParameter::removeListener(Component *c){((PatternComponent*)c)->removePatternListener(this);}
void PyPatternParameter::patternChanged(PatternComponent * ){
  setValue(var());
}
void PyPatternParameter::updateComponentState(Component *c) {
  pattern = PyJUCEAPI::GSPatternWrap.GenerateFromObj(pyVal,pattern);
  ((PatternComponent*)c)->newPatternLoaded(pattern);

}


Component *  PyPatternParameter::createComponent(var v,const NamedValueSet & properties) {
  PatternComponent * pc =  new PatternComponent();
  pc->newPatternLoaded(pattern);
  return pc;

}
bool PyPatternParameter::isMainPattern(){
  return count==1 || name=="Main";
}

PyObject * PyPatternParameter::getPythonObject() {return PyJUCEAPI::GSPatternWrap.GeneratePyObj(pattern,pyVal);}