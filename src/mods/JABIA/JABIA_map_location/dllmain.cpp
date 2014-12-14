#include <windows.h>
#include "map_location.h"
#include "assembly_opcodes.h"

DWORD WINAPI MapLocationThread(LPVOID);
void myLoadLocation();
HMODULE game_handle; // address of GameJABiA.exe
DWORD g_threadID;
HMODULE g_hModule;

typedef void * (_stdcall *LoadLocationReturnPtr)();
LoadLocationReturnPtr LoadLocation;
void* myLoadLocationReturn();
void __fastcall recordMapLocation(void* instance);

INT APIENTRY DllMain(HMODULE hDLL, DWORD Reason, LPVOID Reserved)
{
	UNREFERENCED_PARAMETER( Reserved );
    switch(Reason)
    {
	case DLL_PROCESS_ATTACH:
        g_hModule = hDLL;
		DisableThreadLibraryCalls(hDLL);
        CreateThread(NULL, NULL, &MapLocationThread, NULL, NULL, &g_threadID);
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}

DWORD WINAPI MapLocationThread(LPVOID)
{		
	BYTE LoadLocationSavedReturn[6]; // save retn here

	TCHAR debugStrBuf [100];
	wsprintf(debugStrBuf, _T("Size of map_location %i"), sizeof(JABIA_map_location));
	OutputDebugString(debugStrBuf);

	// find base address of exe in memory
	if(GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle) == NULL) {
		wsprintf(debugStrBuf, _T("Failed to get module handle"));
		OutputDebugString(debugStrBuf);
	} else {
		wsprintf(debugStrBuf, _T("%s at 0x%x"), ProcessName, game_handle);
		OutputDebugString(debugStrBuf);

		LoadLocation = (LoadLocationReturnPtr)((uint32_t)game_handle+SOMEOFFSET);
		wsprintf(debugStrBuf, _T("Return at 0x%x"), LoadLocation);
		OutputDebugString(debugStrBuf);
	}

	returnHook(LoadLocation, myLoadLocationReturn, LoadLocationSavedReturn);
	while(true);

	FreeLibraryAndExitThread(g_hModule, 0);
    return 0;
}


__declspec(naked) void* myLoadLocationReturn(){	
	__asm{
		// save registers
		push eax;
		push edx;
		push ecx;
		push esi;
		mov ecx, esi;
		call recordMapLocation;
		// restore registers
		pop esi;
		pop ecx;
		pop edx;
		pop eax;
		retn 0x28;
	}
}

void __fastcall recordMapLocation(void* instance){
	char buf [100];
	JABIA_map_location * map_location;

	map_location = (JABIA_map_location *)instance;

	sprintf(buf, "Location %s, sector id %i, at 0x%X", map_location->name, map_location->sector_id, map_location);
	OutputDebugStringA(buf);
	//jabia_ammo_map[ammo_ptr->ID] = ammo_ptr;
}