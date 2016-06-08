/*
 ==============================================================================
 
 GSPatternPlayer.h
 Created: 8 Jun 2016 6:48:48pm
 Author:  martin hermant
 
 ==============================================================================
 */

#ifndef GSPATTERNPLAYER_H_INCLUDED
#define GSPATTERNPLAYER_H_INCLUDED



#include "GSPattern.h"


typedef struct MIDIMapEntry{
	MIDIMapEntry(int ch,int pi,int vel):channel(ch),pitch(pi),velocity(vel){}
	int channel;
	int pitch;
	int velocity;
}MIDIMapEntry;



class GSPatternMidiMapper{
public:
	virtual ~GSPatternMidiMapper(){};
	
	virtual vector<MIDIMapEntry> getMIDINoteForEvent(const GSPatternEvent & e) =0;
	
};


class GSDummyMapper:public GSPatternMidiMapper{
public:
	int baseNote = 60;
	vector<MIDIMapEntry> getMIDINoteForEvent(const GSPatternEvent & e) override{
		vector<MIDIMapEntry> res;
		for(auto & ev:e.eventIds){
			res.push_back(MIDIMapEntry(1,ev+baseNote,e.velocity));
		}
		return res;
	}
	
};

class GSLiveMapper:public GSPatternMidiMapper{
public:
	
	std::map<string,int> tagToLiveMidi = {
		{"Kick",36},
		{"Snare",40},
		{"ClosedHH",42},
		{"OpenHH",46},
		{"Clap",39},
		{"Rimshot",37},
		{"LowConga",43},
		{"HiConga",47}};
	vector<MIDIMapEntry> getMIDINoteForEvent(const GSPatternEvent & e) override{
		vector<MIDIMapEntry> res;
		vector<string> tags = e.getTagNames();
		for(auto & t:tags){
			auto it = tagToLiveMidi.find(t);
			if(it!=tagToLiveMidi.end())
				res.push_back(MIDIMapEntry(1,it->second,e.velocity));
		}
		return res;
	}
	
};

class GSPatternPlayer{
public:
	
	typedef struct{
		vector<MIDIMapEntry> entries;
		double duration;
		double startTime;
	}MIDINoteEntries;
	
	GSPatternPlayer(GSPatternMidiMapper * mmap):isLooping(true),ownedMapper(mmap){}
	
	
	void updatePlayHead(double pH);
	vector<MIDIMapEntry> &getCurrentNoteOn();
	vector<MIDIMapEntry> &getCurrentNoteOff();
	
	
	GSPattern currentPattern;
	
	void setMidiMapper(GSPatternMidiMapper * mmap);
	void setPattern(GSPattern &);
	void stop();
	bool isLooping;
private:
	
	double playHead;
	GSPatternMidiMapper * ownedMapper;
	
	vector<MIDIMapEntry> currentNote;
	vector<MIDIMapEntry> currentNoteOn;
	vector<MIDIMapEntry> currentNoteOff;
	
	
	
	
};



#endif  // GSPATTERNPLAYER_H_INCLUDED
