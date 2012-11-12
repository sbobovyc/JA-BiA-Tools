/*
@author: sbobovyc
*/

/*
Copyright (C) 2012 Stanislav Bobovych

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

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include "../h/character.h"

void dump_character(JABIA_Character * ptr, char * filepath) {
	FILE *fp;
	fp=fopen(filepath, "wb");
	fwrite(ptr, sizeof(JABIA_Character), 1, fp);
	fclose(fp);
}

void load_character(JABIA_Character * ptr, char * filepath) {
	FILE *fp;
	fp=fopen(filepath, "wb");
	fread(ptr, sizeof(JABIA_Character), 1, fp);
	fclose(fp);
}