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
	double points = 0.0;
	points = floor(sqrt(ptr->total_amount_health_restored) * (100 / sqrt(7000)) * (1. + ptr->intelligence / 150.));
	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->medical) {
		points = ptr->medical;
	}

	char buf[100];
	wsprintf(buf, "calc_medical = %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}

unsigned int calc_explosives(JABIA_XPMOD_parameters * params, JABIA_Character * ptr, unsigned int total_explosives_actions) {
	double points = 0.0;
	points = floor(sqrt(total_explosives_actions) * (100 / sqrt(500)) * (1. + ptr->intelligence / 150.));
	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->explosives) {
		points = ptr->explosives;
	}

	char buf[100];
	wsprintf(buf, "calc_explosvies = %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}

unsigned int calc_marksmanship(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	char buf[100];
	const double intelligence_denominator = 150.0;
	const double scaler = 0.5;
	const double learning_time = 0.1; // 10%


	double accuracy = double(ptr->bullets_hit) / double(ptr->bullets_fired);
	sprintf(buf, "Marksmanship accuracy %f, bullets_hit addr = 0x%x, bullets_fired = 0x%x", accuracy, &ptr->bullets_hit, &ptr->bullets_fired);
	OutputDebugString(buf);

	// init, solve for x
	double x =  double(ptr->marksmanship) / ((1. + (ptr->intelligence / intelligence_denominator)) * (1. + accuracy) * scaler);
	x *= x;
	sprintf(buf, "X = %i", int(floor(x)));
	OutputDebugString(buf);
	if (ptr->bullets_fired < int(floor(x))) {
		sprintf(buf, "calc_marksmanship, learning stage, %s, estimated learning time %i", ptr->merc_name, int(floor(x*learning_time)));
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
	x = double(ptr->marksmanship+1) / ((1. + (ptr->intelligence / intelligence_denominator)) * (1. + accuracy) * scaler);
	x *= x;
	sprintf(buf, "calc_marksmanship, %s, estimated bullets fired till increase %i", ptr->merc_name, int(floor(x - ptr->bullets_fired)));
	OutputDebugString(buf);
#endif

	double points = 0.0;
	points = floor(sqrt(ptr->bullets_fired) * (1. + (ptr->intelligence / intelligence_denominator)) * (1. + accuracy) * scaler);

	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < ptr->marksmanship) {
		points = ptr->marksmanship;
	}
	else if (points < 0.0) {
		points = 0;
	}

	sprintf(buf, "Marksmanship points %i", int(points));
	OutputDebugString(buf);
	return unsigned int(points);
}

unsigned int calc_stealth(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	char buf[100];
	double points = 0.0;
	double stealth_actions = 0.0;
	double anti_stealth_actions = 0.0;
	double damage_ratio = 0.0;
	
	stealth_actions = ptr->hand_to_hand_kills + ptr->melee_performed;
	anti_stealth_actions = ptr->times_bleeding + ptr->times_wounded + ptr->times_rescued_from_dying;
	damage_ratio = double(ptr->total_damage_dealt) / double(ptr->total_damage_taken);

	if ((stealth_actions - anti_stealth_actions) < 0.) {
		return ptr->stealth;
	}

	double recalculated_damage_ratio = 1.0;
	if (damage_ratio < 1 / 3.) {
		recalculated_damage_ratio = damage_ratio;
	}
	else {
		recalculated_damage_ratio = damage_ratio / 3.;
	}

	points = floor(sqrt(stealth_actions - anti_stealth_actions) * (100. / sqrt(200.0)) * recalculated_damage_ratio);

	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->stealth) {
		points = ptr->stealth;
	}
	sprintf(buf, "Stealth points %i", points);
	OutputDebugString(buf);
	return unsigned int(points);
}


unsigned int calc_mechanical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr) {
	char buf[255];
	
	double points = 0.0;
	unsigned int total_mechanical_actions = 0;	
	total_mechanical_actions = ptr->total_amount_durability_restored + ptr->successful_repair_checks*100 + ptr->successful_doors_forced*100 + ptr->successful_locks_picked*100;

	points = floor(sqrt(total_mechanical_actions) * (100 / sqrt(70000.)) * (1. + (ptr->intelligence / 130.0)));
	
	if (points > 100.0) {
		points = 100.0;
	}
	else if (points < 0.0) {
		points = 0;
	}
	else if (points < ptr->marksmanship) {
		points = ptr->marksmanship;
	}
	sprintf(buf, "Mechanical points %i", points);
	OutputDebugString(buf);
	return unsigned int(points);
}
