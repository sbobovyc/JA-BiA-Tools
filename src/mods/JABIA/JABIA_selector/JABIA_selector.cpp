// JABIA_selector.cpp : Defines the exported functions for the DLL application.
//

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers
// Windows Header Files:
#include <windows.h>
#include <SDKDDKVer.h>
#include <tchar.h>
#include "game_version.h"
#include "selector.h"
#include "detours.h"

#pragma comment(lib,"detours.lib")

HMODULE game_handle;
DWORD g_threadID;
HMODULE g_hModule;

DWORD WINAPI SelectorThread(LPVOID);


HANDLE(WINAPI *oldCreateFile) (LPCTSTR, DWORD,
	DWORD,
	LPSECURITY_ATTRIBUTES,
	DWORD,
	DWORD,
	HANDLE) = CreateFile;


HANDLE WINAPI CreateFileHook(LPCTSTR lpFileName, DWORD                 dwDesiredAccess,
	DWORD                 dwShareMode,
	LPSECURITY_ATTRIBUTES lpSecurityAttributes,
	DWORD                 dwCreationDisposition,
	DWORD                 dwFlagsAndAttributes,
	HANDLE                hTemplateFile);

char * custom_config_path = "bin_win32_mods\\";
TCHAR buf[100];

BOOL APIENTRY DllMain(HMODULE hDLL, DWORD  Reason, LPVOID Reserved)
{
	UNREFERENCED_PARAMETER(Reserved);
	switch (Reason)
	{
	case DLL_PROCESS_ATTACH:
		OutputDebugString(_T("In selector attach"));
		g_hModule = hDLL;
		//DisableThreadLibraryCalls(hDLL);
		//CreateThread(NULL, NULL, &SelectorThread, NULL, NULL, &g_threadID);
		SelectorThread(NULL);
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}


DWORD WINAPI SelectorThread(LPVOID)
{
	OutputDebugString(_T("In selector thread"));
	// start detour  function
	DetourRestoreAfterWith();
	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)oldCreateFile, CreateFileHook);
	DetourTransactionCommit();
	// end detour function

	/*
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle);
	uint32_t opcode_address = (uint32_t)game_handle + CONFIGS_PUSH_INSTRUCTION_1_OFFSET;

	wsprintf(buf, _T("Patching %p"), opcode_address);
	OutputDebugString(buf);

	DWORD oldProtection;
	// read + write
	VirtualProtect((LPVOID)opcode_address, 6, PAGE_EXECUTE_READWRITE, &oldProtection);

	BYTE instruction[5];
	// copy old instruction 
	memcpy((void *)instruction, (void *)opcode_address, 5);

	memcpy((void *)(instruction + 1), (void *)&custom_config_path, sizeof(char *));

	// patch old instruction with new instruction
	memcpy((void *)opcode_address, (void *)instruction, 5);

	// restore protection
	VirtualProtect((LPVOID)opcode_address, 6, oldProtection, NULL);


	// read + write
	opcode_address = (uint32_t)game_handle + CONFIGS_PUSH_INSTRUCTION_2_OFFSET;

	wsprintf(buf, _T("Patching %p"), opcode_address);
	OutputDebugString(buf);

	VirtualProtect((LPVOID)opcode_address, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	
	// copy old instruction 
	memcpy((void *)instruction, (void *)opcode_address, 5);

	memcpy((void *)(instruction + 1), (void *)&custom_config_path, sizeof(char *));

	// patch old instruction with new instruction
	memcpy((void *)opcode_address, (void *)instruction, 5);

	// restore protection
	VirtualProtect((LPVOID)opcode_address, 6, oldProtection, NULL);

	*/
	return 0;
}


HANDLE WINAPI CreateFileHook(LPCTSTR lpFileName, DWORD                 dwDesiredAccess,
	DWORD                 dwShareMode,
	LPSECURITY_ATTRIBUTES lpSecurityAttributes,
	DWORD                 dwCreationDisposition,
	DWORD                 dwFlagsAndAttributes,
	HANDLE                hTemplateFile)
{	
	wsprintf(buf, _T("CreateFile %s"), lpFileName);
	OutputDebugString(buf);
	HANDLE h = oldCreateFile(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
	return h;
}