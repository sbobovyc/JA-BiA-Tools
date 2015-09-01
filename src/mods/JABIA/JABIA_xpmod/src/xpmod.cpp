/*
@author: sbobovyc
*/

/*
Copyright (C) 2013 Stanislav Bobovych

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

#include <windows.h>
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/filesystem.hpp>
#include <iostream> 
#include <fstream> 

#include "character.h"
#include "xpmod.h"

unsigned int calc_medical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	char buf[100];
	double points = 0.0;
	const double scaler = params->medical_scaler;
	const double intel_scaler = params->medical_intel_scaler;
	const double learning_time = params->medical_learning_time; 

	// init, solve for x
	double x = double(ptr->medical) / ((100 / sqrt(scaler)) * (1. + ptr->intelligence / intel_scaler));
	x *= x;
	sprintf_s(buf, "Medical X = %f, intelligence = %i", x, ptr->intelligence);
	OutputDebugString(buf);

#define DEBUG_MEDICAL
#ifdef DEBUG_MEDICAL
	double pred_x = double(ptr->medical + 1) / ((100 / sqrt(scaler)) * (1. + ptr->intelligence / intel_scaler));
	pred_x *= pred_x;
	sprintf_s(buf, "Predicted health restored till update %i", int(floor(pred_x)));
	OutputDebugString(buf);
#endif

	if (ptr->total_amount_health_restored < unsigned int(floor(x))) {
		OutputDebugString("Predicted medical is lower than real medical");
		if (ptr->total_amount_health_restored > x*learning_time) {
			ptr->total_amount_health_restored = int(floor(x));
			OutputDebugString("Medical learning over");
		}
		return ptr->medical;
	}
	// end init

	points = floor(sqrt(ptr->total_amount_health_restored) * (100 / sqrt(scaler)) * (1. + ptr->intelligence / intel_scaler));
	sprintf_s(buf, "Calculated medical points %f", points);
	OutputDebugString(buf);

	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->medical) {
		points = ptr->medical;
	}

	wsprintf(buf, "calc_medical = %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}

unsigned int calc_explosives(JABIA_XPMOD_parameters * params, JABIA_Character * ptr, unsigned int total_explosives_actions) {
	char buf[100];
	double points = 0.0;
	double scaler = params->explosives_scaler;
	double intel_scaler = params->explosives_intel_scaler;

	// init, solve for x
	double x = ptr->explosives / ((100 / sqrt(scaler)) * (1. + ptr->intelligence / intel_scaler));
	x *= x;
	sprintf_s(buf, "Explosive X = %f", x);
	OutputDebugString(buf);

#define DEBUG_EXPLOSIVE
#ifdef DEBUG_EXPLOSIVE
	double pred_x = ptr->explosives / ((100 / sqrt(scaler)) * (1. + ptr->intelligence / intel_scaler));
	pred_x *= pred_x;
	sprintf_s(buf, "Predicted explosives actions till update %f", pred_x);
	OutputDebugString(buf);
#endif

	points = floor(sqrt(total_explosives_actions) * (100 / sqrt(scaler)) * (1. + ptr->intelligence / intel_scaler));
	
	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->explosives) {
		points = ptr->explosives;
	}
	
	wsprintf(buf, "calc_explosvies = %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}

unsigned int calc_marksmanship(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	char buf[100];
	const double scaler = params->marksmanship_scaler;
	const double intel_scaler = params->marksmanship_intel_scaler;	
	const double learning_time = params->marksmanship_learning_time;

	if (ptr->bullets_fired == 0) { // prevent divide by zero
		return ptr->marksmanship;
	}

	double accuracy = double(ptr->bullets_hit) / double(ptr->bullets_fired);
	sprintf_s(buf, "Marksmanship accuracy %f, bullets_hit addr = %p, bullets_fired = %p", accuracy, &ptr->bullets_hit, &ptr->bullets_fired);
	OutputDebugString(buf);

	// init, solve for x
	double x =  double(ptr->marksmanship) / ((1. + (ptr->intelligence / intel_scaler)) * (1. + accuracy) * scaler);
	x *= x;
	sprintf_s(buf, "Marksmanship X = %i", int(floor(x)));
	OutputDebugString(buf);
	if (ptr->bullets_fired < unsigned int(floor(x))) {
		sprintf_s(buf, "calc_marksmanship, learning stage, %s, estimated learning time %i", ptr->merc_name, int(floor(x*learning_time)));
		OutputDebugString(buf);
		if (ptr->bullets_fired > x*learning_time) {
			ptr->bullets_fired = int(floor(x));
			ptr->bullets_hit = int(floor(x * accuracy));
			OutputDebugString("Learning over");
			
		}
		return ptr->marksmanship;		
	}
	// end init

#define DEBUG_MARKSMANSHIP
#ifdef DEBUG_MARKSMANSHIP
	x = double(ptr->marksmanship+1) / ((1. + (ptr->intelligence / intel_scaler)) * (1. + accuracy) * scaler);
	x *= x;
	sprintf_s(buf, "calc_marksmanship, %s, estimated bullets fired till increase %i", ptr->merc_name, int(floor(x - ptr->bullets_fired)));
	OutputDebugString(buf);
#endif

	double points = 0.0;
	points = floor(sqrt(ptr->bullets_fired) * (1. + (ptr->intelligence / intel_scaler)) * (1. + accuracy) * scaler);

	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < ptr->marksmanship) {
		points = ptr->marksmanship;
	}
	else if (points < 0.0) {
		points = 0;
	}

	sprintf_s(buf, "Marksmanship points %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}

unsigned int calc_stealth(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	char buf[100];
	double points = 0.0;
	double stealth_actions = 0.0;
	double anti_stealth_actions = 0.0;
	double damage_ratio = 0.0;
	double scaler = 800.0;

	stealth_actions = ptr->hand_to_hand_kills + ptr->melee_performed;
	anti_stealth_actions = double(ptr->times_bleeding) + double(ptr->times_wounded) + double(ptr->times_rescued_from_dying);
	damage_ratio = double(ptr->total_damage_dealt) / double(ptr->total_damage_taken);

	// learning period
	if (stealth_actions < 20) {
		return ptr->stealth;
	}

	sprintf_s(buf, "Damage ratio %f", damage_ratio);
	OutputDebugString(buf);

	if ((stealth_actions - anti_stealth_actions) <= 0.) {
		return ptr->stealth;
	}

	if (ptr->total_damage_taken == 0) {
		return ptr->stealth;
	}

	double recalculated_damage_ratio = 1.0;
	if (damage_ratio < (1 / 3.)) {
		recalculated_damage_ratio = damage_ratio;
	}
	else if(damage_ratio > 2.) {
		recalculated_damage_ratio = 2.;
	}

	sprintf_s(buf, "Recalculated damage ratio %f", recalculated_damage_ratio);
	OutputDebugString(buf);
	sprintf_s(buf, "Stealth actions %i", int(stealth_actions));
	OutputDebugString(buf);
	sprintf_s(buf, "Times bleeding %p, times wounded %p, times rescued %p", &ptr->times_bleeding, &ptr->times_wounded, &ptr->times_rescued_from_dying);
	OutputDebugString(buf);
	sprintf_s(buf, "Times bleeding %i, times wounded %i, times rescued %i", ptr->times_bleeding, ptr->times_wounded, ptr->times_rescued_from_dying);
	OutputDebugString(buf);
	sprintf_s(buf, "ptr->total_damage_dealt %p, ptr->total_damage_taken %p", &ptr->total_damage_dealt, &ptr->total_damage_taken);
	OutputDebugString(buf);
	sprintf_s(buf, "ptr->total_damage_dealt %i, ptr->total_damage_taken %i", ptr->total_damage_dealt, ptr->total_damage_taken);
	OutputDebugString(buf);
	sprintf_s(buf, "anti st actions = %i", int(floor( anti_stealth_actions)));
	OutputDebugString(buf);
	// init, solve for x
	double x = double(ptr->stealth) / ((100. / sqrt(scaler)) * recalculated_damage_ratio);
	x *= x;
	sprintf_s(buf, "Stealth X = %i", int(floor(x)));
	OutputDebugString(buf);
	// end init

	if ((stealth_actions - anti_stealth_actions) < x) {
		OutputDebugString("Calculated stealth < real stealth");
		return ptr->stealth;
	}

#define DEBUG_STEALTH
#ifdef DEBUG_STEALTH
	x = double(ptr->stealth+1) / ((100. / sqrt(scaler)) * recalculated_damage_ratio);
	x *= x;
	sprintf_s(buf, "calc_stealth, %s, estimated positive stealth actions till increase %i", ptr->merc_name, int(floor(stealth_actions )));
	OutputDebugString(buf);
#endif

	points = floor(sqrt(stealth_actions - anti_stealth_actions) * (100. / sqrt(scaler)) * recalculated_damage_ratio);

	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->stealth) {
		points = ptr->stealth;
	}
	sprintf_s(buf, "Stealth points %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}


unsigned int calc_mechanical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	char buf[255];
	double points = 0.0;
	const double scaler = params->mechanical_scaler;
	const double intel_scaler = params->mechanical_intel_scaler;
	const double multiplier = params->mechanical_multiplier;	
	double total_mechanical_actions = 0;	
	total_mechanical_actions = ptr->total_amount_durability_restored + ptr->successful_locks_picked*multiplier + ptr->successful_doors_forced*multiplier + ptr->successful_repair_checks*multiplier;

	points = floor(sqrt(total_mechanical_actions) * (100 / sqrt(scaler)) * (1. + (ptr->intelligence / intel_scaler)));
	
	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->mechanical) {
		points = ptr->mechanical;
	}
	sprintf_s(buf, "Mechanical points %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}
