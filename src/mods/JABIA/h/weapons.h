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

#ifndef _WEAPONS_H_
#define _WEAPONS_H_

#include "game_version.h"

#if defined(JABIA)
#define WEAPON_MINUMUM_FUNCTIONAL_DURABILITY_CALCULATION_OFFSET 0x1420CD
#define WEAPON_CONST_RETURN_OFFSET 0x12E328
#elif defined(JAC)
#define WEAPON_MINUMUM_FUNCTIONAL_DURABILITY_CALCULATION_OFFSET 0x1412FD
#define WEAPON_CONST_RETURN_OFFSET 0x12E328 //TODO
#else
#error Need to define either JABIA or JAC.
#endif

// This corresponds to the Armament comment in weapons.txt
enum ArmamentType {Launcher=0, Rifle=1, HandGun=2, Knife=3, None=4};
enum GunType {Shotgun=0, Handgun=1, AssaultRifle=2, SniperRifle=3, MachineGun=4, SubmachineGun=5};

#define AMMO_START_ID 900

typedef struct JABIA_Weapon {
	uint32_t	Class; // = 4 for attachments, 0 for weapons
	uint32_t	ID;
	uint32_t	ResourceId;
	bool		Deliverable;
	uint32_t	Price;
	uint32_t	Weight;
	uint32_t	unknown1;
	uint32_t	ui_equipment_icons_number;
	uint16_t	icon_x_offset;
	uint16_t	icon_y_offset;
	uint16_t	icon_width;
	uint16_t	icon_height;
	uint32_t	ui_equipment_pictures_number;
	uint16_t	picture_x_offset;
	uint16_t	picture_y_offset;
	uint16_t	picture_width;
	uint16_t	picture_height;
	ArmamentType	ArmamentType;
	GunType		GunType;
	uint32_t	AmmunitionType;
	uint32_t	Quality; //Durability
	uint32_t	Damage;
	uint32_t	Burst;
	uint32_t	Auto; // unused by game
	uint32_t	RPM; //Rate of fire
	uint32_t	ClipSize; 
	float		BestRange; 
	uint32_t	unknown3; 
	float		unknown4;
	float		unknown5;
	float		unknown6;
	float		unknown7;
	uint32_t	unknown8;
	bool		DisableAttachments;
	uint32_t	unknown9; 
	uint32_t	unknown10;
} JABIA_Weapon;

#endif /* _WEAPONS_H_ */