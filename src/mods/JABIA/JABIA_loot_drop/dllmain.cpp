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
#include "loot_drop.h"
#include "character.h"

typedef void * (_stdcall *CalcDropLootPtr)();

DWORD WINAPI LootDropThread(LPVOID);
void myCalcDropedLoot();
void CustomCalcDroppedLoot(JABIA_Character_inventory * ptr, void * drop_ptr, int unknown);

JABIA_LOOT_DROP_parameters debugmod_params;

HMODULE game_handle; 
HMODULE g_hModule;
DWORD g_threadID;

CalcDropLootPtr CalcDropLoot;

extern float g_WeaponDropChanceConstant = 1.0f;
extern float g_ItemDropChanceConstant = 1.0f;
TCHAR debugStrBuf[DEBUG_STR_SIZE];

INT APIENTRY DllMain(HMODULE hDLL, DWORD Reason, LPVOID Reserved)
{
	UNREFERENCED_PARAMETER( Reserved );
    switch(Reason)
    {
    case DLL_PROCESS_ATTACH:
        g_hModule = hDLL;
		DisableThreadLibraryCalls(hDLL);
        CreateThread(NULL, NULL, &LootDropThread, NULL, NULL, &g_threadID);
    break;
    case DLL_THREAD_ATTACH:
    case DLL_PROCESS_DETACH:
    case DLL_THREAD_DETACH:
        break;
    }
    return TRUE;
}

DWORD WINAPI LootDropThread(LPVOID) {	
	load(PATH_TO_LOOT_DROP_XML, debugmod_params);

	// find base address of exe in memory
	if (GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle) == NULL) {
		wsprintf(debugStrBuf, _T("Failed to get module handle"));
		OutputDebugString(debugStrBuf);
		FreeLibraryAndExitThread(g_hModule, 0);
	} else {

		DWORD oldProtection;
#ifdef REDIRECT //TODO this is broken
		// find address of character update xp function
		CalcDropLoot = (CalcDropLootPtr)((uint32_t)game_handle + CALC_DROP_LOOT_OFFSET);
		wsprintf(debugStrBuf, _T("Address of CalcDropLoot 0x%x"), CalcDropLoot);
		OutputDebugString(debugStrBuf);


		// start UpdateCharacterExp redirection		
		// read + write
		VirtualProtect(CalcDropLoot, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
		DWORD JMPSize = ((DWORD)myCalcDropedLoot - (DWORD)CalcDropLoot - 5);
		//BYTE Before_JMP[6]; // save retn here
		BYTE JMP2[6] = { 0xE9, 0x90, 0x90, 0x90, 0x90, 0x90 }; // JMP NOP NOP ...
															   //memcpy((void *)Before_JMP, (void *)UpdateCharacterExp, 6); // save retn
		memcpy(&JMP2[1], &JMPSize, 4);
		// overwrite retn with JMP
		memcpy((void *)CalcDropLoot, (void *)JMP2, 6);
		// restore protection
		VirtualProtect((LPVOID)CalcDropLoot, 6, oldProtection, NULL);
		// end UpdateCharacterExp redirection
#endif

		wsprintf(debugStrBuf, _T("Address of weapon drop floating point load 0x%x"), (uint32_t)game_handle + WEAPON_DROP_FLD_OFFSET);
		OutputDebugString(debugStrBuf);
		wsprintf(debugStrBuf, _T("Address of item drop floating point load 0x%x"), (uint32_t)game_handle + ITEM_DROP_FLD_OFFSET);
		OutputDebugString(debugStrBuf);

		g_WeaponDropChanceConstant = debugmod_params.weapon_drop_chance;
		g_ItemDropChanceConstant = debugmod_params.item_drop_chance;

		// overwrite weapon drop chance from 0.25 to 1.0 (or user config)	
		// overwrite item drop chance from 0.125 to 1.0 (or user config)
		// change switch table to drop all items in inventory
		// read + write
		VirtualProtect((LPVOID)((uint32_t)game_handle + WEAPON_DROP_FLD_OFFSET), 6, PAGE_EXECUTE_READWRITE, &oldProtection);


		// create new instruction
		BYTE FLD[6] = { 0xD9, 0x05, 0x0, 0x0, 0x0, 0x0 };
		DWORD const_address = (DWORD)&g_WeaponDropChanceConstant;
		wsprintf(debugStrBuf, _T("Address of my constant 0x%x"), const_address);
		OutputDebugString(debugStrBuf);
		memcpy(&FLD[2], &const_address, sizeof(float*));

		// Assembly dump from IDA
		// fld ds:0x0072FA14 replaced with 
		memcpy((void *)((uint32_t)game_handle + WEAPON_DROP_FLD_OFFSET), FLD, 6);

		// create new instruction
		const_address = (DWORD)&g_ItemDropChanceConstant;
		memcpy(&FLD[2], &const_address, sizeof(float*));

		// Assembly dump from IDA
		// fld ds:0x00728F48 replaced with 
		memcpy((void *)((uint32_t)game_handle + ITEM_DROP_FLD_OFFSET), FLD, 6);

		// Assembly dump from IDA
		// db      0,     3,     3,     3  ; indirect table for switch statement
		// db      1,     3,     1,     1 
		// db      2
		// replaced with
		// db      0,     1,     1,     1  ; indirect table for switch statement
		// db      1,     1,     1,     1 
		// db      2

		BYTE NEW_SWITCH[9] = { 0x0, 0x3, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x2 };
		memcpy((void *)((uint32_t)game_handle + INVENTORY_DROP_SWTCH_TABLE), NEW_SWITCH, 9);

		// restore protection
		VirtualProtect((LPVOID)((uint32_t)game_handle + WEAPON_DROP_FLD_OFFSET), 6, oldProtection, NULL);
	}

	// done, leave the library in memory since g_DropChanceConstant lives in the .rdata section of this DLL
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
	OutputDebugString(_T("In Custom Drop Loot"));
	wsprintf(debugStrBuf, _T("0x%X \n0x%X \n0x%x"), ptr, drop_ptr, unknown);
	OutputDebugString(debugStrBuf);
}