/*
@author: sbobovyc
*/

/*
Copyright (C) 2012 Stanislav Bobovych

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

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include "character.h"

void heal_character(JABIA_Character * ptr) {
	// set medical status to healthy
	ptr->medical_condition = JABIA_CHARACTER_MED_HEALTHY;
	ptr->health = 100; // may overflow max health
	ptr->stamina = 100;
	ptr->mod_strength = 0;
	ptr->bleed_rate = 0;
}

void kill_character(JABIA_Character * ptr) {
	// set medical status to healthy
	ptr->medical_condition |= JABIA_CHARACTER_MED_DEAD;
	ptr->health = -1;
}

void stun_character(JABIA_Character * ptr) {
	// set medical status to dead, but don't set health to negative 
	ptr->medical_condition |= JABIA_CHARACTER_MED_DEAD;
}

void dump_character(JABIA_Character * ptr, char * filepath) {
	FILE *fp;
	fp=fopen(filepath, "wb");
	fwrite(ptr, sizeof(JABIA_Character), 1, fp);
	fclose(fp);
}

void load_character(JABIA_Character * ptr, char * filepath) {
	FILE *fp;
	fp=fopen(filepath, "wb");
	fread(ptr, sizeof(JABIA_Character), 1, fp);
	fclose(fp);
}