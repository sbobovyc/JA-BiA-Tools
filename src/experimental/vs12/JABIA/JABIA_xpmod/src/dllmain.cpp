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

#include <windows.h>
#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <vector>

#include "detours.h"
#include "../../h/character.h"
#include "../../h/JABIA_gui.h"
#include "../h/xpmod.h"

#pragma comment(lib,"detours.lib")

#define WITH_XP_MOD
static char ProcessName[] = "GameJABiA.exe";

// modding exp function
#define UPDATE_EXP_OFFSET 0x14C470
typedef void * (_stdcall *UpdateCharacterExpPtr)();

BOOL CALLBACK DialogProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
DWORD WINAPI MyThread(LPVOID);
void* myUpdateCharacterExp();
void changeCharacterStats(void* instance);
void myPrintCharacterXpGain(wchar_t * xp_increase, int unknown, wchar_t * xp_string);


UpdateCharacterExpPtr UpdateCharacterExp;
PrintCharacterXpGainPtr PrintCharacterXpGain;


JABIA_XPMOD_parameters xpmod_params;

HMODULE game_handle; // address of GameDemo.exe
DWORD g_threadID;
HMODULE g_hModule;


INT APIENTRY DllMain(HMODULE hDLL, DWORD Reason, LPVOID Reserved)
{
	UNREFERENCED_PARAMETER( Reserved );
    switch(Reason)
    {
    case DLL_PROCESS_ATTACH:
        g_hModule = hDLL;
		DisableThreadLibraryCalls(hDLL);
        CreateThread(NULL, NULL, &MyThread, NULL, NULL, &g_threadID);
    break;
    case DLL_THREAD_ATTACH:
    case DLL_PROCESS_DETACH:
    case DLL_THREAD_DETACH:
        break;
    }
    return TRUE;
}

DWORD WINAPI MyThread(LPVOID)
{
	
	//DWORD cwdsz = GetCurrentDirectory(0,0); // determine size needed
	//char *cwd = (char*)malloc(cwdsz);
	//if ( GetCurrentDirectory(cwdsz, cwd) == 0 ) { /*OS error.. */ }
	//else { /* success.. */ 
	//	OutputDebugString(cwd);
	//}
	//free((void*)cwd);
	

	load(&xpmod_params);
	char buf [100];
	// find base address of GameDemo.exe in memory
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle);
	// find address of character update xp function
	UpdateCharacterExp = (UpdateCharacterExpPtr)((uint32_t)game_handle+UPDATE_EXP_OFFSET);
	wsprintf (buf, "Address of UpdateCharacterExp 0x%x", UpdateCharacterExp);
	OutputDebugString(buf);


	// find address of print character xp function
		// find address of character update xp function
	PrintCharacterXpGain = (PrintCharacterXpGainPtr)((uint32_t)game_handle+PRINT_XP_FUN_OFFSET);
	wsprintf (buf, "Address of PrintCharacterXpGain 0x%x", PrintCharacterXpGain);
	OutputDebugString(buf);

	// start UpdateCharacterExp redirection
	DWORD oldProtection;
	// read + write
	VirtualProtect(UpdateCharacterExp, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	DWORD JMPSize2 = ((DWORD)myUpdateCharacterExp - (DWORD)UpdateCharacterExp - 5);
	BYTE Before_JMP[6]; // save retn here
	BYTE JMP2[6] = {0xE9, 0x90, 0x90, 0x90, 0x90, 0x90}; // JMP NOP NOP ...
	memcpy((void *)Before_JMP, (void *)UpdateCharacterExp, 6); // save retn
	memcpy(&JMP2[1], &JMPSize2, 4);
	// overwrite retn with JMP
	memcpy((void *)UpdateCharacterExp, (void *)JMP2, 6);
	// restore protection
    VirtualProtect((LPVOID)UpdateCharacterExp, 6, oldProtection, NULL);
	// end UpdateCharacterExp redirection

	// start detour print xp function
	DetourRestoreAfterWith();
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)PrintCharacterXpGain, myPrintCharacterXpGain);
	DetourTransactionCommit();
	// end detour print xp function

    while(true)
    {
		if(GetAsyncKeyState(VK_F8) &1) {
			OutputDebugString("Unloading JABIA_xpmod DLL");
            break;
		}
    Sleep(100);
	/*
		wchar_t wbuf[512];
		swprintf(wbuf, 512, L"THIS is a tEst!");
		PrintCharacterXpGain(L"+++", 0x200, wbuf);
	*/
    }
	// restore exp update hook
	// read + write
	VirtualProtect(UpdateCharacterExp, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	memcpy((void *)UpdateCharacterExp, (void *)Before_JMP, 6);
	// restore protection
    VirtualProtect((LPVOID)UpdateCharacterExp, 6, oldProtection, NULL);

	// restore print xp function
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
    DetourDetach(&(PVOID&)PrintCharacterXpGain, myPrintCharacterXpGain);
    DetourTransactionCommit();


	FreeLibraryAndExitThread(g_hModule, 0);
    return 0;
}

__declspec(naked) void* myUpdateCharacterExp(){	
	// this function uses thiscall convention
	// ECX has this pointer
	// ESI has by how much to increase xp
	// 0054C470    56              PUSH ESI

	_asm{
		push esi	           // push exp increase on stack
		mov esi,eax
		xor al,al            // zero out eax
		test esi,esi         // is esi 0?
		jle jmp1     // if esi != 0 continue else jmp to return
		mov edx,DWORD PTR DS:[ecx+0x10]         // ecx is the character (this pointer - 0x110), get current exp from character datastructure and put it in edx
		cmp edx,0x000059D8         // exp >= 23000?
		jae jmp1     // if yes, return
		add esi,edx          // else
		cmp DWORD PTR DS: [ecx+0x0C],0x0A    // level >= 10?
		mov DWORD PTR DS:[ecx+0x10],esi         // copy new exp into character datastructure
		jae jmp1     // if yes, return
		nop 
	jmp3:
		mov edx,DWORD PTR DS:[ecx+0x0C]		
		CMP ESI,DWORD PTR DS:[EDX*4+0x71DF84] // find xp required for next level and compare to current level
		jb jmp1									// and current xp > xp for next level? if yes then don't jump
		cmp edx,0x0A							// current level >= 10?
		jae jmp2								// if yes then jump 
		lea eax,DWORD PTR DS:[edx+0x01]			// increment level
		mov DWORD PTR DS:[ecx+0x0C],eax			// store level in character data structure
		MOV EAX,DWORD PTR DS:[EAX*4+0x71DFAC]   // look up how many training points we get for this level
#ifdef WITH_XP_MOD
		nop										// don't add training points
		nop
		nop
#else
		add DWORD PTR DS:[ecx+0x14],eax         // add training points into character data structure
#endif
	jmp2:
		cmp DWORD PTR DS: [ecx+0x0C],0x0A		// current level < 10?
		mov al,0x01
		jb jmp3									// if yes, then jump
	jmp1:
#ifdef WITH_XP_MOD
		push ecx
		call changeCharacterStats
		pop ecx
#endif
		pop esi
		ret 
	}
}

void changeCharacterStats(void* instance) {
	char buf [100];
	JABIA_Character * character_ptr = (JABIA_Character *)((uint32_t)instance - 0x110);
	OutputDebugString("Updating character stats!");

	wsprintf(buf, "Character at 0x%X", character_ptr);
	OutputDebugString(buf);

	// do whatever i want with the character	
	if(! (character_ptr->total_amount_health_restored % xpmod_params.medical_modulo) ) {
		character_ptr->medical += calc_medical(&xpmod_params, character_ptr);
	}
	unsigned int total_explosives_actions = 0;
	unsigned int total_stealth_actions = 0;

	total_explosives_actions += character_ptr->grenades_thrown + 
										character_ptr->successful_mines_planted + 
										character_ptr->successful_mines_disarmed + character_ptr->successful_explosives_planted;
	if(! (total_explosives_actions % xpmod_params.explosives_modulo) ) {
		character_ptr->explosives += calc_explosives(&xpmod_params, character_ptr);
	}

	if(! (character_ptr->enemies_killed % xpmod_params.marksmanship_modulo) ) {		
		character_ptr->marksmanship += calc_marksmanship(&xpmod_params, character_ptr);
	}	

	total_stealth_actions += character_ptr->times_bleeding + character_ptr->times_wounded + character_ptr->times_rescued_from_dying + character_ptr->enemies_killed;
	if(! (total_stealth_actions % xpmod_params.stealth_modulo) ) {
		character_ptr->stealth += calc_stealth(&xpmod_params, character_ptr);
	}
}

void myPrintCharacterXpGain(wchar_t * xp_increase, int unknown, wchar_t * xp_string) {
	// this function possibly uses thiscall
	//006AF52E  /$  8BFF          MOV EDI,EDI
	wchar_t wbuf[100];
	char buf[100];
	wsprintf(buf, "%ls %i %ls", xp_increase, unknown, xp_string);
	//OutputDebugString(buf);
	swprintf(wbuf, 100, L"%ls\nXPmod", xp_string);
	PrintCharacterXpGain(xp_increase, unknown, wbuf);
}