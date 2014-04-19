/*
@author: sbobovyc
*/

/*
Copyright (C) 2014 Stanislav Bobovych

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

#ifndef _ITEMS_H_
#define _ITEMS_H_

#include "game_version.h"

#if defined(JABIA)
#define ITEM_CONST_RETURN_OFFSET 0x12E458
#elif defined(JAC)
#define ITEM_CONST_RETURN_OFFSET 0x12E458 //TODO
#else
#error Need to define either JABIA or JAC.
#endif

enum ItemType {Medikit=0, Grenade=1, Mine=2, Defuse=3, Explosive=4, Opener=5, Tool=6};
typedef struct JABIA_Item {
	uint32_t	Class; // = 4 for attachments, 0 for weapons
	uint32_t	ID;
	uint32_t	ResourceID;
	bool		Deliverable;
	uint32_t	Price;
	uint32_t	Weight;
	uint32_t	unknown1;
	uint32_t	ui_equipment_icons_number;
	uint16_t	icon_x_upper_left;
	uint16_t	icon_y_upper_left;
	uint16_t	icon_x_lower_right;
	uint16_t	icon_y_lower_right;
	uint32_t	ui_equipment_pictures_number;
	uint16_t	picture_x_upper_left;
	uint16_t	picture_y_upper_left;
	uint16_t	picture_x_lower_right;
	uint16_t	picture_y_lower_right;
    ItemType	ItemType;
    uint32_t     SubType;
	uint32_t    Charges;
	uint32_t    Requirement;
	uint32_t	Efficiency;
	float		unknown2;
	uint32_t	unknown3[13];
} JABIA_Item;

#endif /* _ITEMS_H_ */