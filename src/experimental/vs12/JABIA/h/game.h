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

#ifndef GAME
#define GAME

#if defined(JABIA)
#define PARSE_GAME_INFO_RETURN 0x598A5
#elif defined(JAC)
#define PARSE_GAME_INFO_RETURN 0x58C95
#else
#error Need to define either JABIA or JAC.
#endif

typedef void * (_stdcall *ParseGameInfoReturnPtr)();

typedef struct SaveGame {
	int unknown[8];
	int money;
} GameInfo;


#endif /* GAME */
