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

#ifndef JABIA_DEBUG
#define JABIA_DEBUG

#include "character.h"

#ifdef JABIA_EXPORTS
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __declspec(dllimport)
#endif

#define FULL

typedef void * (_stdcall *CharacterConstReturnPtr)();
typedef void * (_stdcall *UpdateCharacterExpPtr)();
typedef void * (_stdcall *CharacterDestReturnPtr)();
typedef int (_stdcall *CharacterDestructorPtr)(JABIA_Character *);

#ifdef __cplusplus
extern "C" {
#endif 

EXPORT BOOL CALLBACK DialogProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
#ifdef __cplusplus
}
#endif


DWORD WINAPI MyThread(LPVOID);
// my hooks
void* myCharacterConstReturn();
void* myCharacterDestReturn();
void __fastcall recordCharacters(void* instance);
void __fastcall removeCharacter(JABIA_Character * ptr);
int myCharacterDestructor(JABIA_Character * ptr);

// gui functions
void dump_current_character(HWND hwnd, JABIA_Character * ptr);
BOOL dump_all_characters(HWND hwnd);
void fillDialog(HWND hwnd, JABIA_Character * ptr);
void setCharacter(HWND hwnd, JABIA_Character * ptr);


#endif /* JABIA_DEBUG */