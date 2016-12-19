/*
 ==============================================================================

 This file was auto-generated!

 It contains the basic framework code for a JUCE plugin editor.

 ==============================================================================
 */

#ifndef PLUGINEDITOR_H_INCLUDED
#define PLUGINEDITOR_H_INCLUDED


#include "PluginProcessor.h"
#include "PatternComponent.h"
#include "TimeListener.h"
#include "PythonCanvas.h"
#include "PyLogger.h"

//==============================================================================
/**
 */
class JucepythonAudioProcessorEditor  : public AudioProcessorEditor,
public ButtonListener,public ComboBoxListener,
public PyJUCEAPI::Listener,
public KeyListener,
public PythonCanvas::Listener
{
public:
  JucepythonAudioProcessorEditor (JucepythonAudioProcessor&);
  ~JucepythonAudioProcessorEditor();

  //==============================================================================
  void paint (Graphics&) override;
  void resized() override;
  TextButton reloadB,showB,autoWatchB,useInternalTransportB;


  void newFileLoaded(const File & f)override;

  

  void widgetAdded(Component *c) override;
  void widgetRemoved(Component *c) override;


  PythonCanvas pyCnv;
  PyLogger *  logger;
  void showLogger(bool );

	 bool keyPressed (const KeyPress& key, Component* originatingComponent)override;

  SharedResourcePointer<TooltipWindow> tooltipWindow;

  void comboBoxChanged (ComboBox* comboBoxThatHasChanged) override;
  ComboBox pyFileChooser;
private:

  // This reference is provided as a quick way for your editor to
  // access the processor object that created it.
  JucepythonAudioProcessor& processor;


  void buttonClicked (Button*)override;
  void updateButtonColor();
  JucepythonAudioProcessor * owner;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (JucepythonAudioProcessorEditor)
};


#endif  // PLUGINEDITOR_H_INCLUDED
