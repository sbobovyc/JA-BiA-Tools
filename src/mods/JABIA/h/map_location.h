
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

#ifndef _MAP_LOCATION_H_
#define _MAP_LOCATION_H_

#include "game_version.h"

#if defined(JABIA)
#define MAP_LOCATION_CONSTRUCTOR_RET_OFFSET 0x194451
#elif defined(JAC)
#define MAP_LOCATION_CONSTRUCTOR_RET_OFFSET 0x194451 //TODO
#else
#error Need to define either JABIA or JAC.
#endif

#define JABIA_MAP_LOCATION_NAME_MAX_LENGTH 16
// This corresponds to comments in map_locations.txt
enum Faction {HumanPlayer, HumanMilitia, Deidranna, HillBillies, KillTarget, VillagePeople};
enum City {PlayerBase, EnemyBase};
enum Function {Airport, HideOut, Housing, Shop, Industry, Oasis, Bar, RoadBlock1, JunkYard, Prison, 
                Hospital, Farm, SAM, Mine, Barracks, Cave, Laboratory, RoadBlock2, GasStation, Harbor};

typedef struct JABIA_map_location {
    uint32_t    unknown1;
    char		name[JABIA_MAP_LOCATION_NAME_MAX_LENGTH];
	int32_t		name_length;
    uint32_t    unknown2;
    uint32_t    text_id;
    uint32_t    sector_id;
    uint32_t    unknown3;
    uint32_t    unknown4; //ptr
    uint32_t    unknown5; //ptr
    uint32_t    unknown6;
    uint32_t    unknown7;
    uint32_t    unknown8;
    Faction     Faction;
    uint32_t    unknonw9;
    Function    Function;
    uint32_t    Income;
    uint32_t    MilSlots;
    uint32_t    Defslots;
    uint32_t    DefendersLevel1;
    uint32_t    DefendersLevel2;
    uint32_t    DefendersLevel3;
    uint32_t    DefendersLevel4;
    uint32_t    DefendersLevel5;
    uint32_t    unknown10;
    uint32_t    ConquestAchievement; // subtract 1 from number given in map_locations.txt
    uint32_t    Description;
    uint32_t    unknown12;
    uint32_t    unknown13;
    uint32_t    unknown14;
    uint32_t    unknown15;
    uint32_t    unknown16;
    uint32_t    unknown17;
} JABIA_map_location;
                
#endif /* _MAP_LOCATION_H_ */