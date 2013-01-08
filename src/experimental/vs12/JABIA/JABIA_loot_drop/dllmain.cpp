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

// modding drop loot functionality
#define WEAPON_DROP_FLD_OFFSET 0x0053A4C5
#define ITEM_DROP_FLD_OFFSET 0x0053A519
#define ONE_FLT 0x0071E02C // 1.0 constant in .rdata segment

DWORD WINAPI MyThread(LPVOID);

HMODULE g_hModule;
DWORD g_threadID;

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

DWORD WINAPI MyThread(LPVOID) {
	char buf [100];
	wsprintf (buf, "Address of weapon drop floating point load 0x%x", WEAPON_DROP_FLD_OFFSET);
	OutputDebugString(buf);
	wsprintf (buf, "Address of item drop floating point load 0x%x", ITEM_DROP_FLD_OFFSET);
	OutputDebugString(buf);

	// overwrite weapon drop chance from 0.25 to 1.0
	// overwrite item drop chance from 0.125 to 1.0
	DWORD oldProtection;
	// read + write
	VirtualProtect((LPVOID)WEAPON_DROP_FLD_OFFSET, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	BYTE FLD[6] = {0xD9, 0x05, 0x2C, 0xE0, 0x71, 0x00};
	// fld ds:0x0072FA14 replaced with 
	// fld ds:0x0071E02C
	memcpy((void *)WEAPON_DROP_FLD_OFFSET, FLD, 6);

	// fld ds:0x00728F48 replaced with 
	// fld ds:0x0071E02C	
	//memcpy((void *)ITEM_DROP_FLD_OFFSET, FLD, 6);

	// restore protection
    VirtualProtect((LPVOID)WEAPON_DROP_FLD_OFFSET, 6, oldProtection, NULL);

	// done
	FreeLibraryAndExitThread(g_hModule, 0);
    return 0;
}