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

// weapon 
std::map<int, JABIA_Weapon *> jabia_weapons_map;

// attachment 
std::map<int, JABIA_Attachment *> jabia_attachments_map;

// clothing
std::map<int, JABIA_Cloth *> jabia_cloth_map;

// headgear 
std::map<int, JABIA_Cloth *> jabia_headgear_map;

// vest 
std::map<int, JABIA_Cloth *> jabia_vest_map;

// torso
std::map<int, JABIA_Cloth *> jabia_torso_map;

// pants
std::map<int, JABIA_Cloth *> jabia_pants_map;

// shoes
std::map<int, JABIA_Cloth *> jabia_shoes_map;

// eyewear
std::map<int, JABIA_Cloth *> jabia_eyewear_map;

// items
std::map<int, JABIA_Item *> jabia_item_map;

// ammo
std::map<int, JABIA_Ammo *> jabia_ammo_map;


void heal_character(JABIA_Character * ptr) {
	// set medical status to healthy
	ptr->medical_condition = JABIA_CHARACTER_MED_HEALTHY;
	ptr->health = 100; // may overflow max health
	ptr->stamina = 100;
	ptr->mod_health = 0;
	ptr->mod_stamina = 0;
	ptr->mod_strength = 0;
	ptr->bleed_rate = 0;
}

void kill_character(JABIA_Character * ptr) {
	// set medical status to dead
	ptr->medical_condition |= JABIA_CHARACTER_MED_DEAD;
	ptr->health = -1;
}

void stun_character(JABIA_Character * ptr) {
	// set medical status to dead, but don't set health to negative 
	ptr->medical_condition |= JABIA_CHARACTER_MED_DEAD;
}

void give_equipment1(JABIA_Character * ptr) {
	ptr->inventory.cap_equiped = 1125; // urban camo
	ptr->inventory.cap_equiped_removable = 1;
	ptr->inventory.cap_equiped_durability = 100;

	ptr->inventory.shirt_equiped = 2105; // urban uniform
	ptr->inventory.shirt_equiped_durability = 100;

	ptr->inventory.pants_equiped = 3065; // urban spectra pants
	ptr->inventory.pants_equiped_durability = 100;

	ptr->inventory.vest_equiped = 4006; // special guardian vest
	ptr->inventory.vest_equiped_durability = 100;

	ptr->inventory.shoes_equiped = 5040; // black military boots
	ptr->inventory.shoes_equiped_durability = 100;

	ptr->inventory.eyewear_equiped = 6040; // gas mask
	ptr->inventory.eyewear_equiped_durability = 100;
	ptr->inventory.eyewear_equiped_status = 1;

	ptr->inventory.weapon_in_hand = 1; // ak
	ptr->inventory.weapon_in_hand_removable = 1;
	ptr->inventory.weapon_in_hand_durability = 1200;
	

	ptr->inventory.ammo_equiped = 907; // 5_45mm
	ptr->inventory.ammo_equiped_count = 1000;

	ptr->inventory.weapon_attachment_removable = 97; // eotech
	ptr->inventory.weapon_attachment_status = 1; 
}

void max_stats(JABIA_Character * ptr) {
	// set medical status to healthy
	ptr->agility = 100;
	ptr->dexterity = 100;
	ptr->strength = 100;
	ptr->intelligence = 100;
	ptr->perception = 100;
	ptr->medical = 100;
	ptr->explosives = 100;
	ptr->marksmanship = 100;
	ptr->stealth = 100;
	ptr->mechanical = 100;
}

void fix_gear(JABIA_Character * ptr) {
	if(ptr->inventory.weapon_in_hand != EMPTY_SLOT) {
		ptr->inventory.weapon_in_hand_durability = jabia_weapons_map[ptr->inventory.weapon_in_hand]->Quality;
	}
	if(ptr->inventory.special_equiped != EMPTY_SLOT) {
		ptr->inventory.special_equiped_charges = jabia_item_map[ptr->inventory.special_equiped]->Charges;
	}
	if(ptr->inventory.cap_equiped != EMPTY_SLOT) {
		ptr->inventory.cap_equiped_durability = 100;
	}
	if(ptr->inventory.eyewear_equiped != EMPTY_SLOT) {
		ptr->inventory.eyewear_equiped_durability = 100;
	}
	if(ptr->inventory.shirt_equiped != EMPTY_SLOT) {
		ptr->inventory.shirt_equiped_durability = 100;
	}
	if(ptr->inventory.vest_equiped != EMPTY_SLOT) {
		ptr->inventory.vest_equiped_durability = 100;
	}
	if(ptr->inventory.shoes_equiped != EMPTY_SLOT) {
		ptr->inventory.shoes_equiped_durability = 100;
	}
	if(ptr->inventory.pants_equiped != EMPTY_SLOT) {
		ptr->inventory.pants_equiped_durability = 100;
	}
	if(ptr->inventory.ammo_equiped != EMPTY_SLOT) {
		ptr->inventory.ammo_equiped_count = jabia_ammo_map[ptr->inventory.ammo_equiped]->BoxSize;
	}
}

void dump_character(JABIA_Character * ptr, TCHAR * filepath) {
	FILE *fp;
	fp=_wfopen(filepath, _T("wb"));
	fwrite(ptr, sizeof(JABIA_Character), 1, fp);
	fclose(fp);
}

void load_character(JABIA_Character * ptr, TCHAR * filepath) {
	FILE *fp;
	fp=_wfopen(filepath, _T("wb"));
	fread(ptr, sizeof(JABIA_Character), 1, fp);
	fclose(fp);
}