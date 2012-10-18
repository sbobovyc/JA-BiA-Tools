#ifndef _CHARACTER_H_
#define _CHARACTER_H_
#include <stdint.h>

typedef struct JABIA_Character {
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

	uint16_t unknown_equiped;
	uint16_t unknown8;
	uint16_t unknown9;
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




} JABIA_Character;

#endif /* _CHARACTER_H_ */