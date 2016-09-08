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
class JucepythonAudioProcessorEditor  : public AudioProcessorEditor,public ButtonListener,public PyJUCEAPI::Listener,public KeyListener,PatternComponent::Listener
{
public:
    JucepythonAudioProcessorEditor (JucepythonAudioProcessor&);
    ~JucepythonAudioProcessorEditor();

    //==============================================================================
    void paint (Graphics&) override;
    void resized() override;
    TextButton reloadB,showB,autoWatchB,useInternalTransportB;


	void newFileLoaded(const File & f)override;
	void newPatternLoaded( GSPattern * p)override;
	
	PatternComponent patternComponent;
	void patternChanged(PatternComponent * )override;
	PythonCanvas pyCnv;
	PyLogger *  logger;
	void showLogger(bool );
	
	 bool keyPressed (const KeyPress& key,
										Component* originatingComponent)override;

	SharedResourcePointer<TooltipWindow> tooltipWindow;
private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    JucepythonAudioProcessor& processor;
	ListenerList<TimeListener> timeListeners;
	void addTimeListener(TimeListener *l){timeListeners.add(l);}
	void removeTimeListener(TimeListener *l){timeListeners.remove(l);}

    void buttonClicked (Button*)override;
	void updateButtonColor();
    JucepythonAudioProcessor * owner;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (JucepythonAudioProcessorEditor)
};


#endif  // PLUGINEDITOR_H_INCLUDED
