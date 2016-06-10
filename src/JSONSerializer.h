/*
  ==============================================================================

    JSONImport.h
    Created: 8 Jun 2016 9:11:11am
    Author:  martin hermant

  ==============================================================================
*/

#ifndef JSONSerializer_H_INCLUDED
#define JSONSerializer_H_INCLUDED

#include "json.hpp"
#include <fstream>


using namespace nlohmann;
using namespace std;



	inline template <class T>
	T loadJSON(string path);
	inline template <class T>
	bool saveJSON(string path,T);
	

	





#endif  // JSONSerializer_H_INCLUDED
