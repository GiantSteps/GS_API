/*
  ==============================================================================

    TimeListener.h
    Created: 5 Jul 2016 4:34:23pm
    Author:  martin hermant

  ==============================================================================
*/

#ifndef TIMELISTENER_H_INCLUDED
#define TIMELISTENER_H_INCLUDED


class TimeListener:public AsyncUpdater{
	public:
	TimeListener(double _beatInterval):lastSendTime(0),beatInterval(_beatInterval){ }
  virtual ~TimeListener(){
//		handleUpdateNowIfNeeded();
	}
	void handleAsyncUpdate() override{timeChanged(getQuantized(lastSendTime));};
	void setTime(double t){
		time =t;
		if(t==0 && lastSendTime>=0){reset();}
		if((time - lastSendTime)> beatInterval){
			lastSendTime = getQuantized(time);
			triggerAsyncUpdate();
			
		}
	}
	
	double getQuantized(double t){
		return floor(t/beatInterval)*beatInterval;
	}
	
	void reset(){
		lastSendTime=-beatInterval;
	}
	double time;
	double lastSendTime;
	double beatInterval;
	virtual void timeChanged(double time) =0;
	

};


#endif  // TIMELISTENER_H_INCLUDED
