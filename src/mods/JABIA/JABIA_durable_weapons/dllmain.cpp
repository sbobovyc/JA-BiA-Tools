#include <windows.h>

#include "durable_weapons.h"
#include "game_version.h"
#include "weapons.h"

HMODULE game_handle; 
HMODULE g_hModule;
DWORD g_threadID;

DWORD WINAPI DurableWeaponsThread(LPVOID);

float new_max_durability_multiplier = 0.5;
JABIA_DURABLE_WEAPONS_parameters durable_weapons_params;

INT APIENTRY DllMain(HMODULE hDLL, DWORD Reason, LPVOID Reserved)
{
	UNREFERENCED_PARAMETER( Reserved );
    switch(Reason)
    {
    case DLL_PROCESS_ATTACH:
        g_hModule = hDLL;
		DisableThreadLibraryCalls(hDLL);
        CreateThread(NULL, NULL, &DurableWeaponsThread, NULL, NULL, &g_threadID);
    break;
    case DLL_THREAD_ATTACH:
    case DLL_PROCESS_DETACH:
    case DLL_THREAD_DETACH:
        break;
    }
    return TRUE;
}


DWORD WINAPI DurableWeaponsThread(LPVOID) {
	load(PATH_TO_DURABLE_WEAPONS_XML, durable_weapons_params);


	char buf [100];
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle);
	// find address of minimum durability calculation
	uint32_t opcode_address = (uint32_t)game_handle+WEAPON_MINUMUM_FUNCTIONAL_DURABILITY_CALCULATION_OFFSET;
	wsprintf (buf, "Address WEAPON_MINUMUM_FUNCTIONAL_DURABILITY_CALCULATION_OFFSET 0x%x", opcode_address);
	OutputDebugString(buf);

	// overwrite weapon durability multiplier from 0.9 to something else
	DWORD oldProtection;
	// read + write
	VirtualProtect((LPVOID)opcode_address, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	BYTE instruction[8];
	// copy old instruction 
	memcpy((void *)instruction, (void *)opcode_address, 8);
	// create new instruction
	uint32_t * new_max_durability_multiplier_address = (uint32_t *)&durable_weapons_params.new_max_durability_multiplier;
	memcpy((void *)(instruction+4), (void *)&new_max_durability_multiplier_address, sizeof(uint32_t *));

	wsprintf (buf, "Address of new multiplier 0x%x", (uint32_t)&new_max_durability_multiplier);
	OutputDebugString(buf);
	for(int i = 0; i < 8; i++) 
	{
		wsprintf (buf, "0x%x", instruction[i]);
		OutputDebugString(buf);
	}
	// patch old instruction with new instruction
	memcpy((void *)opcode_address, (void *)instruction, 8);

	// restore protection
	OutputDebugString("Will try to restore protection");
    //boolean result = VirtualProtect((LPVOID)opcode_address, 6, oldProtection, NULL);
	//wsprintf(buf, "Protection restoration succeeded? %s", result? "true" : "false");
	//OutputDebugString(buf);

    return 0;
}