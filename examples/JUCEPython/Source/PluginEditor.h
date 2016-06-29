/*
  ==============================================================================

    This file was auto-generated!

    It contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#ifndef PLUGINEDITOR_H_INCLUDED
#define PLUGINEDITOR_H_INCLUDED


#include "PluginProcessor.h"


//==============================================================================
/**
*/
class JucepythonAudioProcessorEditor  : public AudioProcessorEditor,public ButtonListener
{
public:
    JucepythonAudioProcessorEditor (JucepythonAudioProcessor&);
    ~JucepythonAudioProcessorEditor();

    //==============================================================================
    void paint (Graphics&) override;
    void resized() override;
    TextButton reloadB,generateB,showB,autoWatchB,useInternalTransportB;





private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    JucepythonAudioProcessor& processor;

    void buttonClicked (Button*)override;

    JucepythonAudioProcessor * owner;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (JucepythonAudioProcessorEditor)
};


#endif  // PLUGINEDITOR_H_INCLUDED
