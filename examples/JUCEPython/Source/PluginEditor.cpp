/*
 ==============================================================================

 This file was auto-generated!

 It contains the basic framework code for a JUCE plugin editor.

 ==============================================================================
 */

#include "PluginEditor.h"



//==============================================================================
JucepythonAudioProcessorEditor::JucepythonAudioProcessorEditor (JucepythonAudioProcessor& p)
: AudioProcessorEditor (&p), processor (p)
{
  // Make sure that before the constructor has finished, you've set the
  // editor's size to whatever you need it to be.
  owner = dynamic_cast<JucepythonAudioProcessor*>(&p);
  setSize (400, 300);

  addAndMakeVisible(reloadB);
  reloadB.setButtonText("load");
  addAndMakeVisible(generateB);
  generateB.setButtonText("generate New");
  addAndMakeVisible(autoWatchB);
  autoWatchB.setButtonText("autoWatch");
  addAndMakeVisible(showB);
  showB.setButtonText("show File");
  reloadB.setColour(TextButton::buttonColourId,owner->pyAPI.isLoaded()?Colours::green:Colours::red);

	useInternalTransportB.setButtonText("internalBPM");
	addAndMakeVisible(useInternalTransportB);

  reloadB.addListener(this);
  generateB.addListener(this);
  autoWatchB.setClickingTogglesState(true);
  autoWatchB.addListener(this);
  autoWatchB.setColour(TextButton::buttonOnColourId, Colours::orange);
  showB.addListener(this);
  useInternalTransportB.addListener(this);
  useInternalTransportB.setClickingTogglesState(true);
  useInternalTransportB.setColour(TextButton::buttonOnColourId, Colours::orange);
  useInternalTransportB.setToggleState(owner->useInternalTransport, dontSendNotification);
	
	addAndMakeVisible(patternComponent);
	owner->pyAPI.addListener(&patternComponent);
	owner->pyAPI.addListener(this);
	owner->addTimeListener(&patternComponent);
}

JucepythonAudioProcessorEditor::~JucepythonAudioProcessorEditor()
{
	owner->pyAPI.removeListener(&patternComponent);
	owner->pyAPI.removeListener(this);
	owner->removeTimeListener(&patternComponent);
}

//==============================================================================
void JucepythonAudioProcessorEditor::paint (Graphics& g)
{
  g.fillAll (Colours::darkgrey);

  g.setColour (Colours::white);
  g.setFont (15.0f);
  g.drawFittedText ("Python canvas", getLocalBounds(), Justification::centred, 1);
}

void JucepythonAudioProcessorEditor::resized()
{
  // This is generally where you'll want to lay out the positions of any
  // subcomponents in your editor..
  Rectangle<int> area = getLocalBounds();
  Rectangle<int> header = area.removeFromTop(30);
  const int bSize= header.getWidth()/4;
  reloadB.setBounds(header.removeFromLeft(bSize));
  generateB.setBounds(header.removeFromLeft(bSize));
  showB.setBounds(header.removeFromLeft(bSize));
  autoWatchB.setBounds(header.removeFromLeft(bSize));
  useInternalTransportB.setBounds(area.removeFromTop(30));
	
	
	Rectangle<int> prec = area.removeFromTop(60);
	patternComponent.setBounds(prec);
}


void JucepythonAudioProcessorEditor::updateButtonColor(){
	if(owner->pyAPI.isLoaded()){reloadB.setColour(TextButton::buttonColourId,Colours::green);}
	else { reloadB.setColour(TextButton::buttonColourId,Colours::red);}
}


void JucepythonAudioProcessorEditor::newFileLoaded(const File & f){updateButtonColor();}
void JucepythonAudioProcessorEditor::newPatternLoaded( GSPattern * p){}

void JucepythonAudioProcessorEditor::buttonClicked (Button* b){
  if(b==&reloadB){
    owner->pyAPI.load();
		updateButtonColor();
	}
  else if(b==&generateB){
    owner->updatePattern();
  }
  else if(b==&autoWatchB){
    owner->pyAPI.setWatching(autoWatchB.getToggleState());
  }
  else if (b==& showB){
    owner->pyAPI.pythonFile.startAsProcess();
  }
  else if(b==&useInternalTransportB){
    owner->useInternalTransport = useInternalTransportB.getToggleState();
  }

}
