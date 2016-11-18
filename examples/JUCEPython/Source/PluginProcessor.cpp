/*
  ==============================================================================

    This file was auto-generated!

    It contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"
#include "PyPatternParameter.h"
PropertiesFile & getVSTProperties();

int JucepythonAudioProcessor::instanceCount = 0;
//==============================================================================
JucepythonAudioProcessor::JucepythonAudioProcessor():player(&mapper),pyAPI(this),playHead(0),useInternalTransport(false)
{
	instanceCount++;
  pyAPI.addListener(this);
	addTimeListener(&pyAPI);
  mainPattern = nullptr;
//  disableNonMainBuses();
//  setPlayConfigDetails(0,0,getSampleRate(),getBlockSize());
}

JucepythonAudioProcessor::~JucepythonAudioProcessor()
{
	instanceCount--;
  pyAPI.removeListener(this);
	removeTimeListener(&pyAPI);
//	if(instanceCount==0)
//		PythonWrap::deleteInstance();
//  if( PythonWrap * i = PythonWrap::i(pyUID)){
//    delete i;
//		i=nullptr;
//  }
}



void JucepythonAudioProcessor::newPatternLoaded( GSPattern * p){
if(p)
  player.setPattern(*p);
}


//==============================================================================
const String JucepythonAudioProcessor::getName() const
{
    return getVSTProperties().getValue("VSTName")+String("u");
}

bool JucepythonAudioProcessor::acceptsMidi() const
{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}

bool JucepythonAudioProcessor::producesMidi() const
{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}

double JucepythonAudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int JucepythonAudioProcessor::getNumPrograms()
{
    return 1;   // NB: some hosts don't cope very well if you tell them there are 0 programs,
                // so this should be at least 1, even if you're not really implementing programs.
}

int JucepythonAudioProcessor::getCurrentProgram()
{
    return 0;
}

void JucepythonAudioProcessor::setCurrentProgram (int index)
{
}

const String JucepythonAudioProcessor::getProgramName (int index)
{
    return String();
}

void JucepythonAudioProcessor::changeProgramName (int index, const String& newName)
{
}

//==============================================================================
void JucepythonAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    // Use this method as the place to do any pre-playback
    // initialisation that you need..

    pyAPI.init();
    pyAPI.load();

//    player.setMidiMapper(&mapper);
}

void JucepythonAudioProcessor::releaseResources()
{
    // When playback stops, you can use this as an opportunity to free up any
    // spare memory, etc.
}



void JucepythonAudioProcessor::processBlock (AudioSampleBuffer& buffer, MidiBuffer& midiMessages)
{
    const int totalNumInputChannels  = getTotalNumInputChannels();
    const int totalNumOutputChannels = getTotalNumOutputChannels();
if(!useInternalTransport){
    juce::AudioPlayHead::CurrentPositionInfo ct;
    getPlayHead()->getCurrentPosition(ct);
    playHead = ct.timeInSeconds/60.0*ct.bpm;
}
else{
  // 120bpm
    playHead+=  buffer.getNumSamples()*1.0/getSampleRate();
}
	timeListeners.call(&TimeListener::setTime,playHead);
    player.updatePlayHead(playHead);
    for(auto & n:player.getCurrentNoteOn()){
        if(n.pitch>=0)midiMessages.addEvent(MidiMessage::noteOn(1,n.pitch,(uint8)n.velocity),0);
    }
    for(auto & n:player.getCurrentNoteOff()){
        if(n.pitch>=0)midiMessages.addEvent(MidiMessage::noteOff(1,n.pitch,(uint8)n.velocity),0);
    }
    // In case we have more outputs than inputs, this code clears any output
    // channels that didn't contain input data, (because these aren't
    // guaranteed to be empty - they may contain garbage).
    // This is here to avoid people getting screaming feedback
    // when they first compile a plugin, but obviously you don't need to keep
    // this code if your algorithm always overwrites all the output channels.
    for (int i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear (i, 0, buffer.getNumSamples());

    // This is the place where you'd normally do the guts of your plugin's
//    // audio processing...
//    for (int channel = 0; channel < totalNumInputChannels; ++channel)
//    {
//        float* channelData = buffer.getWritePointer (channel);
//
//        // ..do something to the data...
//    }
}

void JucepythonAudioProcessor::newParamsLoaded(OwnedArray<PyJUCEParameter> * ps){
  for (int i = 0 ; i  < ps->size() ; i++){
    if(PyPatternParameter * patt = dynamic_cast<PyPatternParameter*>(ps->getUnchecked(i))){
      if(patt->isMainPattern()){

        if(mainPattern !=nullptr){
          mainPattern->removeParameterListener(this);
        }
        newPatternLoaded(patt->pattern);
        mainPattern = patt;
        mainPattern->addParameterListener(this);
        
        break;
      }
    }
  }
};

void JucepythonAudioProcessor::parameterChanged(PyJUCEParameter * p){
  newPatternLoaded(mainPattern->pattern);
}

//==============================================================================
bool JucepythonAudioProcessor::hasEditor() const
{
    return true; // (change this to false if you choose to not supply an editor)
}

AudioProcessorEditor* JucepythonAudioProcessor::createEditor()
{
    return new JucepythonAudioProcessorEditor (*this);
}

//==============================================================================
void JucepythonAudioProcessor::getStateInformation (MemoryBlock& destData)
{
    // You should use this method to store your parameters in the memory block.
    // You could do that either as raw data, or use the XML or ValueTree classes
    // as intermediaries to make it easy to save and load complex data.
}

void JucepythonAudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    // You should use this method to restore your parameters from this memory block,
    // whose contents will have been created by the getStateInformation() call.
}

//==============================================================================
// This creates new instances of the plugin..
AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new JucepythonAudioProcessor();
}
