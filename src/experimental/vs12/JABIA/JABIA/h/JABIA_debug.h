#ifndef JABIA_DEBUG
#define JABIA_DEBUG

#include "character.h"

#ifdef JABIA_EXPORTS
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __declspec(dllimport)
#endif

#define FULL
#define WITH_XP_MOD
//#define DEMO


#define CHARACTER_CONST_OFFSET 0x132880
#define CHARACTER_CONST_RETN_OFFSET 0x2D8
#define CHARACTER_DESTRUCTOR_OFFSET 0x132B60
#define CHARACTER_DESTRUCTOR_RETN_OFFSET 0x132BB8 // pop edi 
static char ProcessName[] = "GameJABiA.exe";


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