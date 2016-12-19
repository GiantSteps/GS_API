/*
 ==============================================================================

 This file was auto-generated!

 It contains the basic framework code for a JUCE plugin editor.

 ==============================================================================
 */

#include "PluginEditor.h"
#include "PyPatternParameter.h"



//==============================================================================
JucepythonAudioProcessorEditor::JucepythonAudioProcessorEditor (JucepythonAudioProcessor& p)
: AudioProcessorEditor (&p), logger(nullptr),processor (p)
{
  // Make sure that before the constructor has finished, you've set the
  // editor's size to whatever you need it to be.
  setResizable(true,true);
  owner = dynamic_cast<JucepythonAudioProcessor*>(&p);
  setSize (400, 300);

  addAndMakeVisible(reloadB);
  reloadB.setButtonText("load");

  addChildComponent(pyFileChooser);
  pyFileChooser.addListener(this);

  addAndMakeVisible(autoWatchB);
  autoWatchB.setButtonText("autoWatch");
  addAndMakeVisible(showB);
  showB.setButtonText("show File");
  reloadB.setColour(TextButton::buttonColourId,owner->pyAPI.isLoaded()?Colours::green:Colours::red);

  useInternalTransportB.setButtonText("internalBPM");
  addAndMakeVisible(useInternalTransportB);

  reloadB.addListener(this);

  autoWatchB.setClickingTogglesState(true);
  autoWatchB.addListener(this);
  autoWatchB.setColour(TextButton::buttonOnColourId, Colours::orange);
  showB.addListener(this);
  useInternalTransportB.addListener(this);
  useInternalTransportB.setClickingTogglesState(true);
  useInternalTransportB.setColour(TextButton::buttonOnColourId, Colours::orange);
  useInternalTransportB.setToggleState(owner->useInternalTransport, dontSendNotification);




  owner->pyAPI.addListener(&pyCnv);
  addAndMakeVisible(pyCnv);

  pyCnv.addCanvasListener(this);
  pyCnv.newParamsLoaded(&owner->pyAPI.params);
  setSize(500,400);
  addKeyListener(this);

}

JucepythonAudioProcessorEditor::~JucepythonAudioProcessorEditor()
{

  pyCnv.paramsBeingCleared();
  pyCnv.removeCanvasListener(this);

  owner->pyAPI.removeListener(this);

  owner->pyAPI.removeListener(&pyCnv);
  removeKeyListener(this);
  if(logger)delete logger ;
  logger = nullptr;

}

//==============================================================================
void JucepythonAudioProcessorEditor::paint (Graphics& g)
{
  g.fillAll (Colours::darkgrey);
  g.setColour (Colours::white);
  g.setFont (15.0f);
  g.drawFittedText ("Python canvas", getLocalBounds(), Justification::centred, 1);
}


static int defaultLoggerWidth = 400;
void JucepythonAudioProcessorEditor::showLogger(bool show){

  if(show && !logger){
    logger = new PyLogger(owner->pyAPI.pyUID);
    addAndMakeVisible(logger);
    setSize(getLocalBounds().getWidth() + defaultLoggerWidth, getLocalBounds().getHeight());
  }
  if(!show && logger){
    int logWidth = logger->getWidth();
    removeChildComponent(logger);
    delete logger ;
    logger = nullptr;
    setSize(getLocalBounds().getWidth() - logWidth, getLocalBounds().getHeight());
  }



}
void JucepythonAudioProcessorEditor::resized()
{
  // This is generally where you'll want to lay out the positions of any
  // subcomponents in your editor..
  Rectangle<int> area = getLocalBounds();
  if(logger){
    Rectangle <int> logArea = area.removeFromLeft(defaultLoggerWidth);
    logger->setBounds(logArea);

  }
  Rectangle<int> header = area.removeFromTop(30);
  const int bSize= header.getWidth()/3;
  reloadB.setBounds(header.removeFromLeft(bSize));
  showB.setBounds(header.removeFromLeft(bSize));
  autoWatchB.setBounds(header.removeFromLeft(bSize));
  useInternalTransportB.setBounds(area.removeFromTop(30));


  //	Rectangle<int> prec = area.removeFromTop(150);
  //	patternComponent.setBounds(prec);

  pyCnv.setBounds(area);
}


void JucepythonAudioProcessorEditor::updateButtonColor(){
  if(owner->pyAPI.isLoaded()){reloadB.setColour(TextButton::buttonColourId,Colours::green);}
  else { reloadB.setColour(TextButton::buttonColourId,Colours::red);}
}


void JucepythonAudioProcessorEditor::newFileLoaded(const File & f){updateButtonColor();}


void JucepythonAudioProcessorEditor::widgetAdded(Component *c) {
  if(TimeListener * tl = dynamic_cast<TimeListener * >(c)){
    owner->addTimeListener(tl);
  }

};
void JucepythonAudioProcessorEditor::widgetRemoved(Component *c) {
  if(TimeListener * tl = dynamic_cast<TimeListener * >(c)){
    owner->removeTimeListener(tl);
  }
}

void JucepythonAudioProcessorEditor::comboBoxChanged (ComboBox* cbC) {
  if(cbC==&pyFileChooser){
    int id = pyFileChooser.getSelectedId()-1;
    if(id>=0){
      owner->pyAPI.VSTPluginName = owner->pyAPI.getVSTPluginNameByIndex(id);
      owner->pyAPI.load();
    }
  }
}

void JucepythonAudioProcessorEditor::buttonClicked (Button* b){
  if(b==&reloadB){
    Array<File> allFiles = owner->pyAPI.getAllPythonFiles();
    if (allFiles.size()){

      StringArray arr;
      for(auto & f:allFiles){
        arr.add(f.getFileName());
      }
      pyFileChooser.clear();
      pyFileChooser.addItemList(arr, 1);
      pyFileChooser.setBounds(reloadB.getBounds());
      pyFileChooser.showPopup();


    }
    else{
      owner->pyAPI.load();
    }
    updateButtonColor();
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





bool JucepythonAudioProcessorEditor::keyPressed (const KeyPress& key,
                                                 Component* originatingComponent){
#ifdef JUCE_MAC
  static KeyPress showLoggerKeyPress =KeyPress ('R', ModifierKeys::commandModifier,0);
#else
  static KeyPress showLoggerKeyPress =KeyPress ('r', ModifierKeys::ctrlModifier,0);
#endif

  if (key ==showLoggerKeyPress ) {
    showLogger(logger==nullptr);
    return true;
  }
  return false;
}
