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

#ifndef _ATTACHMENTS_H_
#define _ATTACHMENTS_H_

#include "game_version.h"

#if defined(JABIA)
#define ATTACHMENT_CONST_RETURN_OFFSET 0x12E56E
#elif defined(JAC)
#define ATTACHMENT_CONST_RETURN_OFFSET 0x12E56E //TODO
#else
#error Need to define either JABIA or JAC.
#endif

//TODO pad out to 128 bytes
typedef struct JABIA_Attachment {
	uint32_t	Class; // = 4 for attachments, 0 for weapons
	uint32_t	ID;
	uint32_t	ResourceID;
	bool		Deliverable;
	uint32_t	Price;
	uint32_t	Weight;
	uint32_t	unknown;
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
	uint32_t	Armament;
	uint32_t	Accuracy;
	uint32_t	Silencing;
	uint32_t	Aimtime;
} JABIA_Attachment;

#endif /* _ATTACHMENTS_H_ */