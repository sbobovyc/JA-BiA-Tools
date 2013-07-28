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


#include <windows.h>
#include "detours.h"

#include "game_version.h"
#include "character.h"

#pragma comment(lib,"detours.lib")

typedef void * (_stdcall *CalcDropLootPtr)();

DWORD WINAPI MyThread(LPVOID);
void myCalcDropedLoot();
void CustomCalcDroppedLoot(JABIA_Character_inventory * ptr, void * drop_ptr, int unknown);

HMODULE game_handle; 
HMODULE g_hModule;
DWORD g_threadID;

CalcDropLootPtr CalcDropLoot;

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

//DWORD WINAPI MyThread(LPVOID) {
//	char buf [100];
//	// find base address of GameDemo.exe in memory
//	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle);
//	// find address of character update xp function
//	CalcDropLoot = (CalcDropLootPtr)((uint32_t)game_handle+CALC_DROP_LOOT_OFFSET);
//	wsprintf (buf, "Address of CalcDropLoot 0x%x", CalcDropLoot);
//	OutputDebugString(buf);
//
//
//	// start UpdateCharacterExp redirection
//	DWORD oldProtection;
//	// read + write
//	VirtualProtect(CalcDropLoot, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
//	DWORD JMPSize = ((DWORD)myCalcDropedLoot - (DWORD)CalcDropLoot - 5);
//	//BYTE Before_JMP[6]; // save retn here
//	BYTE JMP2[6] = {0xE9, 0x90, 0x90, 0x90, 0x90, 0x90}; // JMP NOP NOP ...
//	//memcpy((void *)Before_JMP, (void *)UpdateCharacterExp, 6); // save retn
//	memcpy(&JMP2[1], &JMPSize, 4);
//	// overwrite retn with JMP
//	memcpy((void *)CalcDropLoot, (void *)JMP2, 6);
//	// restore protection
//    VirtualProtect((LPVOID)CalcDropLoot, 6, oldProtection, NULL);
//	// end UpdateCharacterExp redirection
//
//	return 0;
//}

DWORD WINAPI MyThread(LPVOID) {
	char buf [100];
	wsprintf (buf, "Address of weapon drop floating point load 0x%x", WEAPON_DROP_FLD_OFFSET);
	OutputDebugString(buf);
	wsprintf (buf, "Address of item drop floating point load 0x%x", ITEM_DROP_FLD_OFFSET);
	OutputDebugString(buf);

	// overwrite weapon drop chance from 0.25 to 1.0	
	// overwrite item drop chance from 0.125 to 1.0
	// change switch table to drop all items in inventory
	DWORD oldProtection;
	// read + write
	VirtualProtect((LPVOID)WEAPON_DROP_FLD_OFFSET, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	BYTE FLD[6] = {0xD9, 0x05, 0x2C, 0xE0, 0x71, 0x00};

	// Assembly dump from IDA
	// fld ds:0x0072FA14 replaced with 
	// fld ds:0x0071E02C
	memcpy((void *)WEAPON_DROP_FLD_OFFSET, FLD, 6);

	// Assembly dump from IDA
	// fld ds:0x00728F48 replaced with 
	// fld ds:0x0071E02C	
	memcpy((void *)ITEM_DROP_FLD_OFFSET, FLD, 6);

	// Assembly dump from IDA
	// db      0,     3,     3,     3  ; indirect table for switch statement
    // db      1,     3,     1,     1 
    // db      2
	// replaced with
	// db      0,     1,     1,     1  ; indirect table for switch statement
    // db      1,     1,     1,     1 
    // db      2

	BYTE NEW_SWTCH[9] = {0x0, 0x3, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x2};
	memcpy((void *)INVENTORY_DROP_SWTCH_TABLE, NEW_SWTCH, 9);

	// restore protection
    VirtualProtect((LPVOID)WEAPON_DROP_FLD_OFFSET, 6, oldProtection, NULL);

	// done
	FreeLibraryAndExitThread(g_hModule, 0);
    return 0;
}

__declspec(naked) void myCalcDropedLoot() {	
	_asm {		
		push [esp+8]
		push [esp+8]		
		push esi
		call CustomCalcDroppedLoot
		pop ebx
		pop ebx
		pop ebx
		ret 
	}
}

void CustomCalcDroppedLoot(JABIA_Character_inventory * ptr, void * drop_ptr, int unknown) {
	char buf[100];
	OutputDebugString("In Custom Drop Loot");
	wsprintf(buf, "0x%X \n0x%X \n0x%x", ptr, drop_ptr, unknown);
	OutputDebugString(buf);
}