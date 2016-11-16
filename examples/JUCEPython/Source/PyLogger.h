/*
 ==============================================================================

 PyLogger.h
 Created: 8 Sep 2016 12:16:06pm
 Author:  martin hermant

 ==============================================================================
 */

#ifndef PYLOGGER_H_INCLUDED
#define PYLOGGER_H_INCLUDED

#include "pythonWrap.h"


class PyLogger :public ListBox,ListBoxModel,ChangeListener{
public:
  PyLogger(int64 pyUID):ListBox("Logger"),pyUID(pyUID){
    PythonWrap::i(pyUID)->getIntercepter()->addLogListener(this);
    
    setModel(this);
    setRowHeight(12);
  }
  ~PyLogger(){
		
    PythonWrap::i(pyUID)->getIntercepter()->removeLogListener(this);

  }

  int maxEntrySize = 1000;
  typedef PythonWrap::PipeIntercepter::Entry Entry;
  Array<Entry> entries;


  void changeListenerCallback (ChangeBroadcaster* source)override{
    {
      PythonWrap::PipeIntercepter * intercept =PythonWrap::i(pyUID)->getIntercepter();
      lock_guard<mutex> lk(intercept->mut);
      int size = intercept->entries.size();
      for(int i = 0 ; i < size ; i++){
        if(intercept->entries[i].msg!="\n"){
          entries.add(intercept->entries[i]);
        }
      }
      if(entries.size()>maxEntrySize){
        entries.removeRange(0, entries.size()-maxEntrySize);
      }
    }
    updateContent();
    setVerticalPosition(1.0);
  }



  // listbox model

	 int getNumRows() override {return entries.size();};

  /** This method must be implemented to draw a row of the list.
   Note that the rowNumber value may be greater than the number of rows in your
   list, so be careful that you don't assume it's less than getNumRows().
   */
	 void paintListBoxItem (int rowNumber,
                          Graphics& g,
                          int width, int height,
                          bool rowIsSelected) override{

     g.setColour(getColourForEntry(entries[rowNumber]));
     g.fillRect(0, 0, width, height);
     g.setColour(Colours::white);
     g.drawLine(0, height, width, height,1);
     g.drawText(entries[rowNumber].msg, Rectangle<int>(0, 1, width, height-2), Justification::left,true);
   };
  String getTooltipForRow (int row)override{
    return entries[row].msg;
  }

  Colour  getColourForEntry(Entry e){
    if(e.type == Entry::Type::error){
      return Colours::red;
    }
    
    if(e.type == Entry::Type::warning){
      return Colours::orange;
    }
    
    return Colours::darkgrey;
    
  }

  int64 pyUID;
  
};



#endif  // PYLOGGER_H_INCLUDED
