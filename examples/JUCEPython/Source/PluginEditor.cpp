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
    reloadB.setColour(TextButton::buttonColourId,owner->py.isFileLoaded()?Colours::green:Colours::red);
    reloadB.addListener(this);
}

JucepythonAudioProcessorEditor::~JucepythonAudioProcessorEditor()
{
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
    Rectangle<int> header = area.removeFromTop(20);
    reloadB.setBounds(header.removeFromLeft(20));
}

void JucepythonAudioProcessorEditor::buttonClicked (Button* b){
    if(b==&reloadB){
        bool loadOK = owner->py.load();
        if(loadOK){
            reloadB.setColour(TextButton::buttonColourId,Colours::green);
//            reloadB.setColour(Button::colo)
        }
        else
            reloadB.setColour(TextButton::buttonColourId,Colours::red);
    }

}
