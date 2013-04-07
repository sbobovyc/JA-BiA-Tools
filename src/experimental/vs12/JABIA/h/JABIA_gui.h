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

#ifndef JABIA_GUI
#define JABIA_GUI

#define PRINT_XP_FUN_OFFSET 0x2AF52E

typedef void * (_cdecl *PrintCharacterXpGainPtr)(wchar_t * xp_increase, int unknown, wchar_t * xp_string);

#endif /* JABIA_GUI */