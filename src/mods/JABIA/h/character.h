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

#ifndef _CHARACTER_H_
#define _CHARACTER_H_
#include <stdint.h>

#include "game_version.h"

#if defined(JABIA)
#define CHARACTER_CONST_OFFSET 0x132880
#define CHARACTER_CONST_RETN_OFFSET 0x2D8
#define CHARACTER_DESTRUCTOR_OFFSET 0x132B60
#define CHARACTER_DESTRUCTOR_RETN_OFFSET 0x132BB8 // pop edi 
// modding drop loot functionality
#define CALC_DROP_LOOT_OFFSET 0x0013A3F0
#define WEAPON_DROP_FLD_OFFSET 0x0053A4C5
#define ITEM_DROP_FLD_OFFSET 0x0053A519
#define ONE_FLT 0x0071E02C // 1.0 constant in .rdata segment
#define INVENTORY_DROP_SWTCH_TABLE 0x0053A540
// modding exp gain function
#define UPDATE_EXP_OFFSET 0x14C470
#elif defined(JAC)
#define CHARACTER_CONST_OFFSET 0x131CD0
#define CHARACTER_CONST_RETN_OFFSET 0x2D8
#define CHARACTER_DESTRUCTOR_OFFSET 0x131FC0
#define CHARACTER_DESTRUCTOR_RETN_OFFSET 0x132018 // pop edi 
// modding drop loot functionality
#define CALC_DROP_LOOT_OFFSET 0x001397F0
#define WEAPON_DROP_FLD_OFFSET 0x005398C5
#define ITEM_DROP_FLD_OFFSET 0x00539919
#define ONE_FLT 0x00817EB8 // 1.0 constant in .data segment
#define INVENTORY_DROP_SWTCH_TABLE 0x00539940
// modding exp gain function
#define UPDATE_EXP_OFFSET 0x14B6C0
#else
#error Need to define either JABIA or JAC.
#endif

#define Faction_HumanPlayer		0
#define Faction_HumanMilitia	1      
#define Faction_Deidranna		2
#define Faction_HillBillies		3
#define Faction_KillTarget		4
#define Faction_VillagePeople	5
#define JABIA_CHARACTER_MAX_NAME_LENGTH  16
#define JABIA_CHARACTER_INV_SLOTS  15

// medical conditions
#define JABIA_CHARACTER_MED_HEALTHY								0x0000
#define JABIA_CHARACTER_MED_WOUNDED								0x0008
#define JABIA_CHARACTER_MED_BEING_HEALED_BY_SMALL_MEDKIT		0x0080
#define JABIA_CHARACTER_MED_DEAD								0x0003


typedef struct JABIA_Character_weapon {
	// all equipment, if empty is 0xFFFF and durability 0
	uint16_t weapon; 
	uint16_t removable;	 // should be 1 for most weapons
	uint16_t weapon_durability; // divide by ten to get number reported in gui
	uint16_t ammo_count;
} JABIA_Character_weapon;

typedef struct JABIA_Character_inventory_item {
	uint16_t item_id; 
	uint16_t item_count;
	uint16_t item_durability;
	uint16_t item_charges;
} JABIA_Character_inventory_item;

typedef struct JABIA_Character_inventory {
	uint32_t maybe_ptr3;
	char cinv[4]; // just a string "cinv" = character inventory
	uint32_t maybe_ptr4;
	uint32_t maybe_ptr5;

	// all equipment, if empty is 0xFFFF and durability 0
	uint16_t weapon_in_hand; 
	uint16_t weapon_in_hand_removable; // 0 for not removable	
	uint16_t weapon_in_hand_durability; // divide by ten to get number reported in gui
	uint16_t unknown3;

	uint16_t special_equiped; // lockpick, c4, etc
	uint16_t special_equiped_status;
	uint16_t unknown5;
	uint16_t special_equiped_charges; // charges left 

	uint16_t cap_equiped;
	uint16_t cap_equiped_removable; // 0 for not removable	
	uint16_t cap_equiped_durability; // divide by ten to get number reported in gui	
	uint16_t unknown7;

	uint16_t eyewear_equiped; 
	uint16_t eyewear_equiped_status; // 0 for not removable	
	uint16_t eyewear_equiped_durability;
	uint16_t unknown10;

	uint16_t shirt_equiped;
	uint16_t shirt_equiped_status;
	uint16_t shirt_equiped_durability;
	uint16_t unknown12;

	uint16_t vest_equiped;
	uint16_t vest_equiped_status;
	uint16_t vest_equiped_durability;
	uint16_t unknown14;

	uint16_t shoes_equiped;
	uint16_t shoes_equiped_status;
	uint16_t shoes_equiped_durability;
	uint16_t unknown16;

	uint16_t pants_equiped;
	uint16_t pants_equiped_status;
	uint16_t pants_equiped_durability;
	uint16_t unknown18;

	uint16_t ammo_equiped;
	uint16_t ammo_equiped_count;
	uint32_t unknown19;

	uint16_t weapon_attachment_removable;
	uint16_t weapon_attachment_status; // 0 > means you can remove it, less than 0 means you can't
	uint32_t unknown20;

	// inventory is divided between weapons and items
	JABIA_Character_weapon weapons[3];
	JABIA_Character_inventory_item inventory_items[JABIA_CHARACTER_INV_SLOTS];
} JABIA_Character_inventory;


typedef struct JABIA_Character {			

	uint32_t unknown_ptr;
	char rahc[4]; // just a string "char"  = character 
	uint32_t unknown_const0;
	uint32_t uk0[19];

	char ctsc[4]; // just a string "ctsc"  = character statistics
	uint32_t u0;
	uint32_t u1;
	uint32_t maybe_ptr0;
	uint32_t melee_performed;
	uint32_t grenades_thrown;
	uint32_t uk1;
	uint32_t uk2;
	uint32_t uk3;
	uint32_t uk4;
	uint32_t rockets_fired;
	uint32_t bullets_fired;
	uint32_t bullets_hit;
	uint32_t bullets_hit_noncritical;
	uint32_t bullets_hit_critical;	
	uint32_t enemies_killed;
	uint32_t total_damage_dealt;
	uint32_t uk5;
	uint32_t uk6;	
	uint32_t total_damage_taken;
	uint32_t times_bleeding;
	uint32_t times_wounded;
	uint32_t times_rescued_from_dying;
	uint32_t uk7;	
	uint32_t successful_healing_checks;
	uint32_t unsuccessful_healing_checks;
	uint32_t total_amount_health_restored;
	uint32_t successful_repair_checks;
	uint32_t unsuccessful_repair_checks;
	uint32_t total_amount_durability_restored;
	uint32_t successful_mines_disarmed;
	uint32_t unsuccessful_mines_disarmed;
	uint32_t successful_mines_planted;
	uint32_t unsuccessful_mines_planted;
	uint32_t successful_explosives_planted;
	uint32_t unsuccessful_explosives_planted;
	uint32_t successful_locks_picked;
	uint32_t unsuccessful_locks_picked;
	uint32_t successful_doors_forced;
	uint32_t unsuccessful_doors_forced;
	uint32_t total_days_in_service;
	uint32_t uk8[5];
	uint32_t maybe_ptr;
	char pxec[4]; // just a string "pxec"  = character experience
	uint32_t uk9;
		

	uint32_t level;
	uint32_t experience;
	uint32_t training_points;
	uint32_t agility_inc;	// this is how many points are pending
	uint32_t dexterity_inc;
	uint32_t strength_inc;
	uint32_t intelligence_inc;
	uint32_t perception_inc;
	uint32_t medical_inc;
	uint32_t explosives_inc;
	uint32_t marksmanship_inc;
	uint32_t stealth_inc;
	uint32_t mechanical_inc;
	uint32_t unknown1[10];


	JABIA_Character_inventory inventory;

	uint32_t unknown23[4]; //3 is possibly length of something

	char merc_name[JABIA_CHARACTER_MAX_NAME_LENGTH]; // seems to be fixed length, sometimes has a null terminator
	uint32_t name_length;
	
	uint32_t unknown24;

	uint32_t faction; 

	// medical condition is managed by some state machine
	uint32_t medical_condition; // 0 or 1 = healthy, 
								// 2 or 3 = dying, 4 = dead, 17 ?= bleeding, 27 = wounded, 128 = being bandaged
								// 145 = being healed by large medkit while bleeding
	// probably a bit field
	// bit 0 = healthy? initially 1
	// bit 1 = dying
	// bit 2 = dead
	// bit 3 = wounded
	// bit 4 = unknown
	// bit 5 = unknown
	// bit 6 = 
	// bit 7 = being healed by large medkit

	float health;
	float stamina;
	
	// attributes
	uint32_t agility;
	uint32_t dexterity;
	uint32_t strength;
	uint32_t intelligence;
	uint32_t perception;

	// skills
	uint32_t medical;
	uint32_t explosives;
	uint32_t marksmanship;
	uint32_t stealth;
	uint32_t mechanical;

	uint32_t mod_health;
	uint32_t mod_stamina;

	// pentalty modifier
	uint32_t mod_agility;		// agility = base agility - penalty
	uint32_t mod_dexterity;
	uint32_t mod_strength;
	uint32_t mod_intelligence;
	uint32_t mod_perception;	// as of 1.13g this does not seem to have an affect

	uint32_t bleed_rate;		// setting this to 0 stops bleeding



} JABIA_Character;


void heal_character(JABIA_Character * ptr);
void kill_character(JABIA_Character * ptr);
void stun_character(JABIA_Character * ptr);
void give_equipment1(JABIA_Character * ptr);
void max_stats(JABIA_Character * ptr);
void dump_character(JABIA_Character * ptr, TCHAR * filepath);

#endif /* _CHARACTER_H_ */

