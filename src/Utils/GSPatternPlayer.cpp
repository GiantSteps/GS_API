/*
  ==============================================================================

    GSPatternPlayer.cpp
    Created: 8 Jun 2016 6:48:48pm
    Author:  martin hermant

  ==============================================================================
*/

#include "GSPatternPlayer.h"
#include <cmath>

void GSPatternPlayer::updatePlayHead(double pH){
    
	lastPlayHead=playHead;
	if(isLooping && currentPattern.duration>0){
		playHead = fmod(pH,currentPattern.duration);
	}
	if(lastPlayHead==playHead){
		stop();
		
		return;
	}
	

	
	vector<MIDIMapEntry> newNotes;
	
	for(auto & n:currentPattern.events){
		if (playHead>=n.start && playHead<n.getEndTime()) {
			vector<MIDIMapEntry> nNotes=ownedMapper->getMIDINoteForEvent(n);
			for (auto & nn:nNotes){
				nn.endTime = n.getEndTime();
			}
			if(nNotes.size()>0)
				newNotes.insert(newNotes.end(), nNotes.begin(),nNotes.end());
		}
	}

	
	
//	add new notes on
	currentNoteOn.clear();
	
	for(auto &nn:newNotes){
		bool found =false;
		for(auto &n:currentNote){
			if ((nn.channel==n.channel) && (nn.pitch==n.pitch) && n.endTime>playHead) {
				found=true;
				break;
			}
		}
		if(!found){
			currentNoteOn.push_back(nn);
		}
		
		
	}
	
//	add note offs
	currentNoteOff.clear();
	for(auto &nn:currentNote){
		bool found = false;
		for(auto &n:newNotes){
			if ((nn.channel==n.channel) && (nn.pitch==n.pitch)) {
				found = true;
				break;
			}
		}
		if(!found){
		currentNoteOff.push_back(nn);
		}
	}
	currentNote = newNotes;
	
	
	
	
}
void GSPatternPlayer::setPattern(const GSPattern &p){
	currentPattern = p;
}

void GSPatternPlayer::stop(){
	if(currentNoteOn.size()==0)currentNoteOff.clear();
	else{
	for( auto & n:currentNoteOn){
		currentNoteOff.push_back(n);
	}
	currentNoteOn.clear();
	}
}

vector<MIDIMapEntry> &GSPatternPlayer::getCurrentNoteOn(){return currentNoteOn;};
vector<MIDIMapEntry> &GSPatternPlayer::getCurrentNoteOff(){return currentNoteOff;};


void GSPatternPlayer::setMidiMapper(GSPatternMidiMapper * mmap){
	if(ownedMapper!=nullptr){
		delete ownedMapper;
	}
	ownedMapper = mmap;
}