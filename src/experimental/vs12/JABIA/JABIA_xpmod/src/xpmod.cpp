#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <iostream> 
#include <fstream> 

#include "../../h/character.h"
#include "../h/xpmod.h"

#include <windows.h>
void save() 
{ 	
  std::ofstream file("C:\\Users\\sbobovyc\\workspace\\JA-BiA-Tools\\src\\experimental\\vs12\\JABIA\\Debug\\JABIA_xpmod.xml"); 
  boost::archive::xml_oarchive oa(file); 
  JABIA_XPMOD_parameters d;
  oa & BOOST_SERIALIZATION_NVP(d); 
} 

void load(JABIA_XPMOD_parameters * dr) 
{ 
  std::ifstream file("C:\\Users\\sbobovyc\\workspace\\JA-BiA-Tools\\src\\experimental\\vs12\\JABIA\\Debug\\JABIA_xpmod.xml"); 
  boost::archive::xml_iarchive ia(file);   
  //ia >> BOOST_SERIALIZATION_NVP(dr); 
  OutputDebugString("Done loading xml");
}

unsigned int calc_medical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	// y = (-(medical_a * (heal points % modulo) - medical_xoffset)^2 + medical_b)*medical_modifier
	double points = 0.0;
	double medical_modifier = 0.0;

	if(ptr->intelligence > 80.0) {
		medical_modifier = params->medical_modifier[0];
	} else {
		medical_modifier = params->medical_modifier[1];
	}
	points = (params->medical_a * (ptr->total_amount_health_restored % params->medical_modulo)) + params->medical_xoffset;
	points *= points;
	points *= -1.0;
	points += params->medical_b;
	points *= medical_modifier;
	points = floor(points);
	return unsigned int(points);
}

unsigned int calc_explosives(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	// y = (-(explosives_a * (explosive actions % modulo) - explosives_xoffset)^2 + explosives_b)*explosives_modifier
	double points = 0.0;
	double explosives_modifier = 0.0;
	unsigned int total_explosives_actions = 0;

	if(ptr->intelligence > 80.0) {
		explosives_modifier = params->explosives_modifier[0];
	} else if(ptr->intelligence > 70.0){
		explosives_modifier = params->explosives_modifier[1];
	} else {
		explosives_modifier = params->explosives_modifier[2];
	}
	total_explosives_actions += ptr->grenades_thrown + ptr->successful_mines_planted + ptr->successful_mines_disarmed + ptr->successful_explosives_planted + ptr->rockets_fired;
	points = (params->explosives_a * (total_explosives_actions % params->explosives_modulo)) + params->explosives_xoffset;
	points *= points;
	points *= -1.0;
	points += params->explosives_b;
	points *= explosives_modifier;
	points = floor(points);
	return unsigned int(points);
}

unsigned int calc_marksmanship(JABIA_XPMOD_parameters * params, unsigned int kills, double accuracy) {
	char buf[100];
	sprintf(buf, "kills %i", kills);
	OutputDebugString(buf);
	sprintf(buf, "acc %f", accuracy);
	OutputDebugString(buf);

	// y = (-(marksmanship_a * (kills % modulo) - marksmanship_xoffset)^2 + marksmanship_b)*accuracy_modifier
	double points = 0.0;
	double accuracy_modifier = 0.0;
	if(accuracy > 80.0) {
		accuracy_modifier = params->marksmanship_accuracy_modifier[0];
	} else {
		accuracy_modifier = params->marksmanship_accuracy_modifier[1];
	}
	points = (params->marksmanship_a * (kills % params->marksmanship_modulo)) + params->marksmanship_xoffset;
	points *= points;
	points *= -1.0;
	points += params->marksmanship_b;
	points *= accuracy_modifier;
	points = floor(points);
	sprintf(buf, "points %f", points);
	OutputDebugString(buf);
	return unsigned int(points);
}

unsigned int calc_stealth(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {

	double points = 0.0;
	double counter_stealth_actions;
	double damage_taken = 0.0;
	
	counter_stealth_actions = ptr->times_bleeding + ptr->times_wounded + ptr->times_rescued_from_dying;
	// Watch out for divide by zero, since counter_stealth_actions and/or enemies killed could be 0.
	// In either case, assume 1:2 ration in favor of stealth and kills. This is probably fine since this
	// case would arise most likely only in the early game.
	if(counter_stealth_actions == 0.0) {
		counter_stealth_actions = ptr->enemies_killed * 0.5;
	}
	if(ptr->total_damage_taken == 0.0) {
		damage_taken = ptr->total_damage_taken * 0.5;
	} else {
		damage_taken = ptr->total_damage_taken;
	}

	// y = modifier_1 * (enemies killed / counter stealth) + modifier_2 * (damage dealt / damage taken)
	points = params->stealth_kills_to_counterstealth_ratio_modifier * (ptr->enemies_killed / counter_stealth_actions) + params->stealth_damage_ratio_modifier * (ptr->total_damage_dealt / damage_taken);


	return unsigned int(points);
}