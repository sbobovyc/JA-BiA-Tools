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

#ifndef DOORHACKS
#define DOORHACKS

#if defined(JABIA)
// various offsets for master key hack
#define DOOR_GUI_JMP_OFFSET 0x00133611 
#define DOOR_ANIMATION_JMP_OFFSET 0x0018427C
#define DOOR_KEYCHECK1_JMP_OFFSET 0x00184360
#define DOOR_KEYCHECK2_JMP_OFFSET 0x00184368
#elif defined(JAC)
// various offsets for master key hack
#error This is not supported yet.
#else
#error Need to define either JABIA or JAC.
#endif

#endif /* DOORHACKS */