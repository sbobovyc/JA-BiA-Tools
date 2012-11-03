#ifndef _CHARACTER_H_
#define _CHARACTER_H_
#include <stdint.h>

typedef struct JABIA_Character {
	uint32_t uk0[24];
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
	uint32_t uk9[3];
	

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
	uint32_t unknown1[14];
	
	// all equipment, if empty is 0xFFFF and durability 0
	uint16_t weapon_in_hand;
	uint16_t unknown2;
	
	uint16_t weapon_in_hand_durability; // divide by ten to get number reported in gui
	uint16_t unknown3;

	uint16_t special_equiped; // lockpick, c4, etc
	uint16_t unknown4;
	uint16_t unknown5;
	uint16_t special_equiped_charges; // charges left 

	uint16_t helmet_equiped;
	uint16_t unknown6;
	uint16_t helmet_equiped_durability; // divide by ten to get number reported in gui	
	uint16_t unknown7;

	uint16_t eyewear_equiped; 
	uint16_t unknown8;
	uint16_t eyewear_equiped_durability;
	uint16_t unknown10;

	uint16_t shirt_equiped;
	uint16_t unknown11;
	uint16_t shirt_equiped_durability;
	uint16_t unknown12;

	uint16_t vest_equiped;
	uint16_t unknown13;
	uint16_t vest_equiped_durability;
	uint16_t unknown14;

	uint16_t shoes_equiped;
	uint16_t unknown15;
	uint16_t shoes_equiped_durability;
	uint16_t unknown16;

	uint16_t pants_equiped;
	uint16_t unknown17;
	uint16_t pants_equiped_durability;
	uint16_t unknown18;

	uint16_t ammo_equiped;
	uint16_t ammo_equiped_count;
	uint32_t unknown19;

	uint16_t weapon_attachment_equiped;
	uint16_t weapon_attachment_status; // 0 > means you can remove it, less than 0 means you can't
	uint32_t unknown20;

	// then the weapon slots come
	uint32_t inventory[36];

	uint32_t unknown21[4]; //3 is possibly length of something

	char merc_name[6]; //don't know if this is fixed length or determined by null terminator

	uint16_t unknown22;
	uint32_t possible_pointer1;
	uint32_t possible_pointer2;
	uint32_t name_length;
	
	uint32_t unknown23;

	uint32_t faction; //Faction_HumanPlayer   = 0
						//kFaction_HumanMilitia = 1      
						//Faction_Deidranna     = 2
						//Faction_HillBillies	= 3
						//Faction_KillTarget   	= 4
						//Faction_VillagePeople = 5

	uint32_t medical_condition; // 0 or 1 = healthy, 2 or 3 = dying, 4 = dead, 17 ?= bleeding, 27 = wounded, 128 = being bandaged

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

	uint32_t unknown24;
	uint32_t unknown25;

	// modifier
	uint32_t mod_agility;
	uint32_t mod_dexterity;
	uint32_t mod_strength;
	uint32_t mod_intelligence;
	uint32_t mod_perception;


} JABIA_Character;

#endif /* _CHARACTER_H_ */
