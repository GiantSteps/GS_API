/*
  ==============================================================================

    PyPatternParameter.h
    Created: 15 Sep 2016 9:06:24am
    Author:  Martin Hermant

  ==============================================================================
*/

#ifndef PYPATTERNPARAMETER_H_INCLUDED
#define PYPATTERNPARAMETER_H_INCLUDED
#include "PatternComponent.h"
#include "PyJUCEParameter.h"


class PyPatternParameter :public PyJUCEParameter, PatternComponent::Listener{
public:

  PyPatternParameter(PyObject * o,const String & n);
  ~PyPatternParameter();
  void registerListener(Component *c) override;
  void removeListener(Component *c)override;
  void patternChanged(PatternComponent * )override;
  void updateComponentState(Component *c) override;
  
  bool isMainPattern();


  Component *  createComponent(var v,const NamedValueSet & properties) override;

  GSPattern * pattern;
  PyObject * getPythonObject() override;
  static HashMap<int64, int> counts;
};



#endif  // PYPATTERNPARAMETER_H_INCLUDED
