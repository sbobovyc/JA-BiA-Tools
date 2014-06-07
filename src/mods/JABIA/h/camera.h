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

#ifndef CAMERA
#define CAMERA

typedef struct Camera {
	float unknown1[77];
	float current_angle;
	float unknown2[3];
	float camera_min;
	float camera_max;
	float min_angle;  // 2.0 is 90 degree, ie directly overhead
	float max_angle_delta; // min + delta = max angle
	float current_height;
} Camera;

#if defined(JABIA)
// modding camera callback
#define CAMERA_CALLBACK_OFFSET 0x001A7020 
#elif defined(JAC)
// modding camera callback
#define CAMERA_CALLBACK_OFFSET 0x001A6050
#else
#error Need to define either JABIA or JAC.
#endif


#endif /* CAMERA */
