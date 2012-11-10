#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <iostream> 
#include <fstream> 

#include "../h/xpmod.h"

#include <windows.h>
void save() 
{ 	
  std::ofstream file("C:\\Users\\sbobovyc\\workspace\\JA-BiA-Tools\\src\\experimental\\vs12\\JABIA\\Debug\\archive.xml"); 
  boost::archive::xml_oarchive oa(file); 
  JABIA_XPMOD_parameters d;
  oa & BOOST_SERIALIZATION_NVP(d); 
} 

void load(JABIA_XPMOD_parameters * dr) 
{ 
  std::ifstream file("C:\\Users\\sbobovyc\\workspace\\JA-BiA-Tools\\src\\experimental\\vs12\\JABIA\\Debug\\archive.xml"); 
  boost::archive::xml_iarchive ia(file);   
  //ia >> BOOST_SERIALIZATION_NVP(dr); 
  OutputDebugString("Done loading xml");
}

unsigned int calc_marksmanship(JABIA_XPMOD_parameters * params, unsigned int kills, double accuracy) {
	char buf[100];
	sprintf(buf, "kills %i", kills);
	OutputDebugString(buf);
	sprintf(buf, "acc %f", accuracy);
	OutputDebugString(buf);

	// y = (-(marksmanship_a * (kills % 100) - marksmanship_xoffset)^2 + marksmanship_b)*accuracy_modifier
	double points = 0.0;
	double accuracy_modifier = 0.0;
	if(accuracy > 80.0) {
		accuracy_modifier = params->marksmanship_accuracy_modifier[0];
	} else {
		accuracy_modifier = params->marksmanship_accuracy_modifier[1];
	}
	points = (params->marksmanship_a * (kills % 100)) + params->marksmanship_xoffset;
	points *= points;
	points *= -1.0;
	points += params->marksmanship_b;
	points *= accuracy_modifier;
	points = floor(points);
	sprintf(buf, "points %f", points);
	OutputDebugString(buf);
	return unsigned int(points);
}