/*
  ==============================================================================

    GSPatternEvent.cpp
    Created: 8 Jun 2016 5:04:28pm
    Author:  martin hermant

  ==============================================================================
*/

#include "GSPatternEvent.h"


vector<string>  GSPatternEvent::getTagNames() const{
	vector<string> res;
	if(ids!=nullptr){
		res.resize(eventTags.size());
		int idx = 0;
		for(auto i:eventTags){
			res [idx]= ids->getTagForId(i);
			idx++;
		}
	}

		
	return res;
	
}




//=============================================
//


string GSPatternEventTags::getTagForId(int i){return (i<tags.size()&& i>=0)?tags[i]:"";}

int GSPatternEventTags::getIdForTag(string tag){
	int idx =0;
	for(auto & t:tags){
		if(t==tag){return idx;}
		idx++;
	}
	return -1;
}

vector<int> GSPatternEventTags::getOrAddTagIds(const vector<string> &newTags){
	vector<int> res(newTags.size());
	int idx =0;
	for(auto & nt:newTags){
		bool found = false;
		int nIdx = 0;
		for(auto & t:tags){
			if(t==nt){
				found = true;
				res[idx] =nIdx;
				break;
			}
			nIdx++;
		}
		if(!found){
			res[idx] = tags.size();
			tags.push_back(nt);
			
		}
		idx++;
	}
	return res;
}

void GSPatternEventTags::initialize(const vector<string> & c){
	tags = c;
	
}
void GSPatternEventTags::clear(){
	tags.clear();
}