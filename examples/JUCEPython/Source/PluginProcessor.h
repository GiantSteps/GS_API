/*
 ==============================================================================
 
 This file was auto-generated!
 
 It contains the basic framework code for a JUCE plugin processor.
 
 ==============================================================================
 */

#ifndef PLUGINPROCESSOR_H_INCLUDED
#define PLUGINPROCESSOR_H_INCLUDED

#include "PyJUCEAPI.h"
#include "JuceHeader.h"
#include "GS_API.h"
#include "GSPatternPlayer.h"




//==============================================================================
/**
 */
class JucepythonAudioProcessor  : public AudioProcessor,PyJUCEAPI::Listener
{
public:
	//==============================================================================
	JucepythonAudioProcessor();
	~JucepythonAudioProcessor();
	
	GSPatternPlayer player;
	GSDummyMapper mapper;
	PyJUCEAPI pyAPI;
	double playHead;
	bool useInternalTransport;
	
  
  void newPatternLoaded( GSPattern * p)override;
  
	
	//==============================================================================
	void prepareToPlay (double sampleRate, int samplesPerBlock) override;
	void releaseResources() override;
	
#ifndef JucePlugin_PreferredChannelConfigurations
	bool setPreferredBusArrangement (bool isInput, int bus, const AudioChannelSet& preferredSet) override;
#endif
	
	void processBlock (AudioSampleBuffer&, MidiBuffer&) override;
	
	//==============================================================================
	AudioProcessorEditor* createEditor() override;
	bool hasEditor() const override;
	
	//==============================================================================
	const String getName() const override;
	
	bool acceptsMidi() const override;
	bool producesMidi() const override;
	double getTailLengthSeconds() const override;
	
	//==============================================================================
	int getNumPrograms() override;
	int getCurrentProgram() override;
	void setCurrentProgram (int index) override;
	const String getProgramName (int index) override;
	void changeProgramName (int index, const String& newName) override;
	
	//==============================================================================
	void getStateInformation (MemoryBlock& destData) override;
	void setStateInformation (const void* data, int sizeInBytes) override;
	
	ListenerList<TimeListener> timeListeners;
	void addTimeListener(TimeListener * l){timeListeners.add(l);}
	void removeTimeListener(TimeListener * l){timeListeners.remove(l);}
  

private:
	//==============================================================================
	JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (JucepythonAudioProcessor)

};




#endif  // PLUGINPROCESSOR_H_INCLUDED
