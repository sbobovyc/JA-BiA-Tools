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
#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include <shlobj.h>
#include <objbase.h>
#include <detours.h>
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/filesystem.hpp>

#include "game_version.h"
#include "game.h"
#include "debug.h"
#include "resource.h"
#include "character.h"
#include "weapons.h"
#include "attachments.h"
#include "clothing.h"
#include "items.h"
#include "ammo.h"
#include "doorhacks.h"
#include "assembly_opcodes.h"
#include "ctx_file.h"

#pragma comment(lib, "detours.lib")

#define DEBUG_STR_SIZE 1024

CharacterConstReturnPtr ParseCharacter;
CharacterDestReturnPtr RemoveCharacter;
CharacterDestructorPtr CharacterDestructor;
ParseGameInfoReturnPtr ParseGameInfoReturn;
SaveGame * CurrentSaveGamePtr = NULL;
WeaponReturnPtr WeaponReturn;
AttachmentReturnPtr AttachmentReturn;
ClothReturnPtr ClothReturn;
ItemReturnPtr ItemReturn;
AmmoReturnPtr AmmoReturn;
int * money_ptr;

JABIA_DEBUGMOD_parameters debugmod_params;

HMODULE game_handle; 
DWORD g_threadID;
HMODULE g_hModule;
HINSTANCE TheInstance = 0;


// character vector
std::vector<JABIA_Character *> jabia_characters;
int last_character_selected_index = 0;
int last_weaponslot_selected_index = 0;
int last_weapon_inhand_selected_index = 0;
int last_inventory_selected_index = 0;



CTX_file ctx;
COMBO_BOX_STATUS inventory_combo_status;

INT APIENTRY DllMain(HMODULE hDLL, DWORD Reason, LPVOID Reserved)
{	
	DWORD dwCreateionFlags = NULL;
    switch(Reason)
    {
    case DLL_PROCESS_ATTACH:		
        g_hModule = hDLL;
		DisableThreadLibraryCalls(hDLL);		
		//dwCreateionFlags |= CREATE_SUSPENDED; // this is only for testing with JABIA_launch_hook
        CreateThread(NULL, NULL, &MyThread, NULL, dwCreateionFlags, &g_threadID);
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
	OutputDebugString(_T("In debugger MyThread"));
	load(PATH_TO_DEBUGMOD_XML, debugmod_params);
	TCHAR debugStrBuf [DEBUG_STR_SIZE];
	DWORD oldProtection;
	BYTE ParseCharacterSavedReturn[6]; // save retn here
	BYTE RemoveCharacterSavedReturn[6]; // save retn here
	BYTE ParseGameInfoSavedReturn[6]; // save retn here
	BYTE WeaponSavedReturn[6]; // save retn here
	BYTE AttachmentSavedReturn[6]; // save retn here
	BYTE ClothSavedReturn[6]; // save retn here
	BYTE ItemSavedReturn[6]; // save retn here
	BYTE AmmoSavedReturn[6]; // save retn here

	// find base address of exe in memory
	if(GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle) == NULL) {
		wsprintf(debugStrBuf, _T("Failed to get module handle"));
		OutputDebugString(debugStrBuf);
	} else {
		// find address of character constructor
		ParseCharacter = (CharacterConstReturnPtr)((uint32_t)game_handle+CHARACTER_CONST_OFFSET);
		wsprintf (debugStrBuf, _T("Address of CharacterConstructor 0x%x"), ParseCharacter);
		OutputDebugString(debugStrBuf);
		// find address of character constructor return
		ParseCharacter = (CharacterConstReturnPtr)((uint32_t)game_handle+CHARACTER_CONST_OFFSET+CHARACTER_CONST_RETN_OFFSET);
		wsprintf (debugStrBuf, _T("Address of retn in CharacterConstructor 0x%x"), ParseCharacter);
		OutputDebugString(debugStrBuf);
		// find addres of character destructor return
		RemoveCharacter = (CharacterDestReturnPtr)((uint32_t)game_handle+CHARACTER_DESTRUCTOR_RETN_OFFSET);
		wsprintf (debugStrBuf, _T("Address of retn in CharacterDestReturnPtr 0x%x"), RemoveCharacter);
		OutputDebugString(debugStrBuf);
		// find address of character destructor
		CharacterDestructor = (CharacterDestructorPtr)((uint32_t)game_handle+CHARACTER_DESTRUCTOR_OFFSET);
		wsprintf (debugStrBuf, _T("Address of CharacterDestructor 0x%x"), CharacterDestructor);
		OutputDebugString(debugStrBuf);
		// find address of game info access function
		ParseGameInfoReturn = (ParseGameInfoReturnPtr)((uint32_t)game_handle+PARSE_GAME_INFO_RETURN);
		wsprintf (debugStrBuf, _T("Address of ParseGameInfoReturn 0x%x"), ParseGameInfoReturn);
		OutputDebugString(debugStrBuf); 
		// find address of weapon constructor return
		WeaponReturn = (WeaponReturnPtr)((uint32_t)game_handle+WEAPON_CONST_RETURN_OFFSET);
		wsprintf (debugStrBuf, _T("Address of WeaponReturn 0x%x"), WeaponReturn);
		OutputDebugString(debugStrBuf); 
		// find address of attachment constructor return
		AttachmentReturn = (AttachmentReturnPtr)((uint32_t)game_handle+ATTACHMENT_CONST_RETURN_OFFSET);
		wsprintf (debugStrBuf, _T("Address of AttachmentReturn 0x%x"), AttachmentReturn);
		OutputDebugString(debugStrBuf); 
		// find address of cloth constructor return
		ClothReturn = (ClothReturnPtr)((uint32_t)game_handle+CLOTHING_CONST_RETURN_OFFSET);
		wsprintf (debugStrBuf, _T("Address of ClothReturn 0x%x"), ClothReturn);
		OutputDebugString(debugStrBuf); 
		// find address of item constructor return
		ItemReturn = (ItemReturnPtr)((uint32_t)game_handle+ITEM_CONST_RETURN_OFFSET);
		wsprintf (debugStrBuf, _T("Address of ItemReturn 0x%x"), ItemReturn);
		OutputDebugString(debugStrBuf); 
		// find address of ammo constructor return
		AmmoReturn = (AmmoReturnPtr)((uint32_t)game_handle+AMMO_CONST_RETURN_OFFSET);
		wsprintf (debugStrBuf, _T("Address of AmmoReturn 0x%x"), AmmoReturn);
		OutputDebugString(debugStrBuf); 
		// If jabia_characters is not empty, clear it. Every time the game loads a level, character pointers change.
		//TODO this function crashes on exit game
		
		/*
		// start detour characer destructor function		
		DetourRestoreAfterWith();
		DetourTransactionBegin();
		DetourUpdateThread(GetCurrentThread());
		DetourAttach(&(PVOID&)CharacterDestructor, myCharacterDestructor);
		DetourTransactionCommit();		
		// end detour characer destructor function
		*/

		jabia_characters.clear();
		
		// hook character constructor return
		returnHook(ParseCharacter, myCharacterConstReturn, ParseCharacterSavedReturn);

		// hook character destructor return
		returnHook(RemoveCharacter, myCharacterDestReturn, RemoveCharacterSavedReturn);
		
		// hook parse game info return
		returnHook(ParseGameInfoReturn, mySaveGameParseReturn, ParseGameInfoSavedReturn);

		// hook weapon constructor return
		returnHook(WeaponReturn, myWeaponConstReturn, WeaponSavedReturn);

		// hook attachment constructor return
		returnHook(AttachmentReturn, myAttachmentConstReturn, AttachmentSavedReturn);

		// hook cloth constructor return
		returnHook(ClothReturn, myClothConstReturn, ClothSavedReturn);

		// hook item constructor return
		returnHook(ItemReturn, myItemConstReturn, ItemSavedReturn);

		// hook ammo constructor return
		returnHook(AmmoReturn, myAmmoConstReturn, AmmoSavedReturn);

		wsprintf(debugStrBuf, _T("Size of JABIA_Character struct %i"), sizeof(JABIA_Character));
		OutputDebugString(debugStrBuf);
		wsprintf(debugStrBuf, _T("Size of JABIA_Weapon struct %i"), sizeof(JABIA_Weapon));
		OutputDebugString(debugStrBuf);
		wsprintf(debugStrBuf, _T("Size of JABIA_Attachment struct %i"), sizeof(JABIA_Attachment));
		OutputDebugString(debugStrBuf);
		wsprintf(debugStrBuf, _T("Size of JABIA_Cloth struct %i"), sizeof(JABIA_Cloth));
		OutputDebugString(debugStrBuf);
		wsprintf(debugStrBuf, _T("Size of JABIA_Item struct %i"), sizeof(JABIA_Item));
		OutputDebugString(debugStrBuf);
		wsprintf(debugStrBuf, _T("Size of JABIA_Ammo struct %i"), sizeof(JABIA_Ammo));
		OutputDebugString(debugStrBuf);
		wsprintf(debugStrBuf, _T("First run? %i"), debugmod_params.first_run);
		OutputDebugString(debugStrBuf);

		if(debugmod_params.first_run) {
			wsprintf(debugStrBuf, _T("DLL successfully loaded. Load a save game and press F7 to bring up editor. Due to some bugs, you need to quit to main menu before you load another savegame. This message will not be shown on next launch."));
			MessageBox (0, debugStrBuf, _T("JABIA character debugger"), MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
			debugmod_params.first_run = false;
			boost::filesystem::path working_dir = boost::filesystem::current_path();
			boost::filesystem::path modpath(PATH_TO_DEBUGMOD_XML);
			boost::filesystem::path fullpath = working_dir / modpath;
			save(fullpath.string(), debugmod_params);
		}

		Sleep(100); //TODO instead of sleeping to wait for ctx to get loaded into memory, hook the function that loads it
		MEM_SCAN:
		uint32_t address = NULL;
		// TODO put memory scanner in its own function
		// TODO if search for patter happens before ctx file is loaded in memory, crash will occur
		// begin mem scan function
		int MIN_MEM = 0x00BF0000;
		int MAX_MEM = 0x7FFFFFFF;
		unsigned char BYTE_PATTER[] = {0xDC, 0x00, 0x10, 0x00, 0x00, 0x00, 0x63, 0x6F, 
							0x75, 0x72, 0x69, 0x65, 0x72, 0x5F, 0x64, 0x63,
							0x5F, 0x64, 0x6D, 0x5F, 0x30, 0x30};
		MEMORY_BASIC_INFORMATION mbi = {0};
		SYSTEM_INFO sInfo;
		GetSystemInfo(&sInfo);	
		unsigned char * pAddress   = NULL,*pEndRegion = NULL;
		DWORD dwProtectionMask=  PAGE_READONLY | PAGE_EXECUTE_WRITECOPY 
                        | PAGE_READWRITE | PAGE_WRITECOMBINE;
		pEndRegion = (unsigned char *)(sInfo.lpMinimumApplicationAddress);
		while( sizeof(mbi) == VirtualQuery(pEndRegion, &mbi, sizeof(mbi)) ){
			pAddress = pEndRegion;
			pEndRegion += mbi.RegionSize;
			(PAGE_GUARD | PAGE_NOCACHE | PAGE_NOACCESS);
			if ((mbi.AllocationProtect & dwProtectionMask) && (mbi.State & MEM_COMMIT) && !(mbi.Protect & (PAGE_GUARD | PAGE_NOCACHE | PAGE_NOACCESS))) {
				wsprintf (debugStrBuf, _T("Scanning page 0x%x"), pAddress);
				OutputDebugString(debugStrBuf); 							
					for (pAddress; pAddress < pEndRegion ; pAddress++){
					// make sure to skip the page that has BYTE_PATTER so not to have a false positive
						if(pAddress == BYTE_PATTER)
							continue;
					int diff = 0;
					for(int j = 0; j < 22; j++) {
						diff = BYTE_PATTER[j] - *((unsigned char *)pAddress+j);
						if(diff != 0) break;
					}
					if(diff == 0) {
						wsprintf (debugStrBuf, _T("Found pattern at 0x%x"), pAddress);
						OutputDebugString(debugStrBuf); 
						address = (uint32_t)pAddress;
						goto DONE_MEM_SCAN;
					}
					}
			}
		}
		// end mem scan function
		DONE_MEM_SCAN:
		if(address == NULL) {
			OutputDebugString(_T("CTX not found")); 		
			goto MEM_SCAN;
		}
		_stprintf_s (debugStrBuf, DEBUG_STR_SIZE, _T("CTX at 0x%x"), address+22);
		OutputDebugString(debugStrBuf); 		
		ctx = CTX_file((void *)(address+22));

		while(true)
		{
			//TODO add size checking to all data structures and give a warning and exit thread if something is size 0
			if(GetAsyncKeyState(VK_F7) & 1)
			{								
				if(jabia_characters.size() == 0) {
					wsprintf(debugStrBuf, _T("You need to load a save or start a new game."));
					MessageBox (0, debugStrBuf, _T("JABIA character debugger"), MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
					continue;
				}

				wsprintf (debugStrBuf, _T("CurrentSaveGamePtr 0x%x"), CurrentSaveGamePtr);
				OutputDebugString(debugStrBuf); 
				wsprintf (debugStrBuf, _T("Current money %i"), CurrentSaveGamePtr->money);
				OutputDebugString(debugStrBuf); 

				if(jabia_characters.at(last_character_selected_index) == NULL) {
					MessageBox (0, debugStrBuf, _T("Memory error"), MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
				} else {
					HWND hDialog = 0;
				
					hDialog = CreateDialog (g_hModule,
								MAKEINTRESOURCE (IDD_DIALOG1),
								0,
								DialogProc);

					fillDialog(hDialog, jabia_characters.at(last_character_selected_index));
				
					if (!hDialog)
					{
						wsprintf (debugStrBuf, _T("Error x%x"), GetLastError ());
						MessageBox (0, debugStrBuf, _T("CreateDialog"), MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
						return 1;
					 }
				
					MSG  msg;
					int status;
					while ((status = GetMessage (& msg, 0, 0, 0)) != 0)
					{
						if (status == -1)
							return -1;
						if (!IsDialogMessage (hDialog, & msg))
						{
							TranslateMessage ( & msg );
							DispatchMessage ( & msg );
						}
					}
				}
			} /* else if(GetAsyncKeyState(VK_F8) &1) {
				//TODO this is unsafe since I have not restored all the hooks
				TCHAR unloadString[] = _T("You've unloaded the JABIA_debug DLL. To fix this, relaunch the game.");
				OutputDebugString(unloadString);
				MessageBox (0, debugStrBuf, _T("CreateDialog"), MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
				break;
			} */
		Sleep(100);
		}
		// restore retn hook
		// read + write
		VirtualProtect(ParseCharacter, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
		memcpy((void *)ParseCharacter, (void *)ParseCharacterSavedReturn, 6);
		// restore protection
		VirtualProtect((LPVOID)ParseCharacter, 6, oldProtection, NULL);

		FreeLibraryAndExitThread(g_hModule, 0);
	}
    return 0;
}

BOOL CALLBACK DialogProc (HWND hwnd, 
                          UINT message, 
                          WPARAM wParam, 
                          LPARAM lParam)
{
	HMENU hMenu;
	HWND comboControl1;
	HWND comboControl2;
	HWND comboControl3;
	HWND comboControl4;
	HWND comboControl5;
	HWND comboControl6;
	HWND comboControl7;
	HWND comboControl8;
	HWND comboControl9;
	HWND comboControl10;
	HWND comboControl11;
	HWND comboControl12;
	HWND comboControl13;
	HWND comboControl14;
	comboControl1=GetDlgItem(hwnd,IDC_COMBO_CHARACTER);	
	comboControl2=GetDlgItem(hwnd,IDC_COMBO_WEAPON_SLOT);	
	comboControl3=GetDlgItem(hwnd,IDC_COMBO_INVENTORY_SLOT);	
	comboControl4=GetDlgItem(hwnd,IDC_COMBO_INVENTORY_WEAPON);	
	comboControl5=GetDlgItem(hwnd,IDC_COMBO_EQUIPED_WEAPON);	
	comboControl6=GetDlgItem(hwnd,IDC_COMBO_WEAPON_MOD);	
	comboControl7=GetDlgItem(hwnd,IDC_COMBO_HELMET);
	comboControl8=GetDlgItem(hwnd,IDC_COMBO_VEST);
	comboControl9=GetDlgItem(hwnd,IDC_COMBO_SHIRT);
	comboControl10=GetDlgItem(hwnd,IDC_COMBO_PANTS);
	comboControl11=GetDlgItem(hwnd,IDC_COMBO_SHOES);
	comboControl12=GetDlgItem(hwnd,IDC_COMBO_EYEWEAR);
	comboControl13=GetDlgItem(hwnd,IDC_COMBO_AMMO);
	comboControl14=GetDlgItem(hwnd,IDC_COMBO_SPECIAL);
	BOOL status = FALSE;
	JABIA_Character * ptr = 0; // character address
	TCHAR debugStrBuf[255];

    switch (message)
    {
		case WM_INITDIALOG:
			BringWindowToTop(hwnd);

			// add menu
			hMenu = LoadMenu(g_hModule, MAKEINTRESOURCE(IDR_MENU1));
			SetMenu(hwnd,hMenu);
			
			// add icon
			HICON hIcon;

			hIcon = (HICON)LoadImage(   g_hModule,
                           MAKEINTRESOURCE(IDI_ICON1),
                           IMAGE_ICON,
                           GetSystemMetrics(SM_CXSMICON),
                           GetSystemMetrics(SM_CYSMICON),
                           0);
			if(hIcon) {
				SendMessage(hwnd, WM_SETICON, ICON_SMALL, (LPARAM)hIcon);
			}

			// add characters to drop down list
			for(size_t i = 0; i < jabia_characters.size(); i++) {							
				SendMessageA(comboControl1,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)jabia_characters.at(i)->merc_name)); // merc names in structure are ASCII		
				//wsprintf(debugStrBuf, _T("In WM_INITDIALOG, character at 0x%X"), jabia_characters.at(i));	
				//OutputDebugString(debugStrBuf);
			}
				// select fist item in list
			SendMessage(comboControl1, CB_SETCURSEL, last_character_selected_index, 0);
			

			// add weapons slots to their combo box
			SendMessage(comboControl2,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)"1"));
			SendMessage(comboControl2,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)"2"));
			SendMessage(comboControl2,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)"3"));

			// select fist item in list
			SendMessage(comboControl2, CB_SETCURSEL, last_weaponslot_selected_index, 0);


			// add inventory slots to their combo box
			for(int i = 0; i < JABIA_CHARACTER_INV_SLOTS; i++) {
				wsprintf(debugStrBuf, _T("%i"), i);
				SendMessage(comboControl3,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)debugStrBuf));
			}

			// select fist item in list
			SendMessage(comboControl3, CB_SETCURSEL, 0, 0);

			// add weapons to inventory weapons combo box		
			for( std::map<int, JABIA_Weapon *>::iterator ii=jabia_weapons_map.begin(); ii!=jabia_weapons_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl4,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));					
			}
			SendMessage(comboControl4,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));
			
			// add weapons to active weapon combo box
			for( std::map<int, JABIA_Weapon *>::iterator ii=jabia_weapons_map.begin(); ii!=jabia_weapons_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				SendMessage(comboControl5,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl5,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add weapon mods to combo box
			for( std::map<int, JABIA_Attachment *>::iterator ii=jabia_attachments_map.begin(); ii!=jabia_attachments_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());				
				SendMessage(comboControl6,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl6,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add helmets to combo box
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_headgear_map.begin(); ii!=jabia_headgear_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl7,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl7,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add vests to combo box
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_vest_map.begin(); ii!=jabia_vest_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl8,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl8,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add shirts to combo box
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_torso_map.begin(); ii!=jabia_torso_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl9,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl9,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add pants to combo box
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_pants_map.begin(); ii!=jabia_pants_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl10,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl10,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add shoes to combo box
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_shoes_map.begin(); ii!=jabia_shoes_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl11,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl11,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add eyewear to combo box
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_eyewear_map.begin(); ii!=jabia_eyewear_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl12,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl12,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add ammo to combo box
			for( std::map<int, JABIA_Ammo *>::iterator ii=jabia_ammo_map.begin(); ii!=jabia_ammo_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl13,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl13,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			// add special item to combo box
			for( std::map<int, JABIA_Item *>::iterator ii=jabia_item_map.begin(); ii!=jabia_item_map.end(); ++ii) {
				wsprintf(debugStrBuf, _T("%i|%s"), (*ii).second->ID, ctx.string_map[(*ii).second->ID].c_str());
				//OutputDebugString(debugStrBuf);
				SendMessage(comboControl14,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)debugStrBuf));
			}
			SendMessage(comboControl14,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCWSTR)_T("None")));

			break;
        case WM_COMMAND:
            switch(LOWORD(wParam))
            {
				case IDC_COMBO_CHARACTER:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get a character out of the vector
							last_character_selected_index = SendMessage(comboControl1, CB_GETCURSEL, 0, 0);
							ptr = jabia_characters.at(last_character_selected_index);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_WEAPON_SLOT:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon from inventory
							last_weaponslot_selected_index = SendMessage(comboControl2, CB_GETCURSEL, 0, 0);
							ptr = jabia_characters.at(last_character_selected_index);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_INVENTORY_SLOT:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to item from inventory
							last_inventory_selected_index = SendMessage(comboControl3, CB_GETCURSEL, 0, 0);
							ptr = jabia_characters.at(last_character_selected_index);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_INVENTORY_WEAPON:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.inventory_weapon_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_EQUIPED_WEAPON:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.equiped_weapon_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
				case IDC_COMBO_WEAPON_MOD:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.attachment_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_HELMET:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.helmet_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_VEST:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.vest_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_SHIRT:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.torso_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_PANTS:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.pants_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_SHOES:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.shoes_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_EYEWEAR:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.eyewear_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_AMMO:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.ammo_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
				case IDC_COMBO_SPECIAL:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							// use combo box selected index to get weapon id
							ptr = jabia_characters.at(last_character_selected_index);
							ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
							inventory_combo_status.special_changed = true;
							setCharacter(hwnd, ptr);
							fillDialog(hwnd, ptr);
							break;
					}
					break;
                case IDSET:
					ptr = jabia_characters.at(last_character_selected_index);
					ZeroMemory((void *)&inventory_combo_status, sizeof(COMBO_BOX_STATUS));
					setCharacter(hwnd, ptr);
					setMoney(hwnd);
					break;
				case IDHEAL_CHARACTER:
				case IDM_HEAL_CHARACTER:					
					ptr = jabia_characters.at(last_character_selected_index);
					heal_character(ptr);
					fillDialog(hwnd, ptr);
					break;
				case IDM_KILL_CHARACTER:					
					ptr = jabia_characters.at(last_character_selected_index);
					kill_character(ptr);
					fillDialog(hwnd, ptr);
					break;
				case IDM_STUN_CHARACTER:
					ptr = jabia_characters.at(last_character_selected_index);
					stun_character(ptr);
					fillDialog(hwnd, ptr);
					break;
				case IDM_EQUIPMENT1:
					ptr = jabia_characters.at(last_character_selected_index);
					give_equipment1(ptr);
					fillDialog(hwnd, ptr);
					break;
				case IDM_DUMP_CHARACTER:					
					ptr = jabia_characters.at(last_character_selected_index);
					dump_current_character(hwnd, ptr);
					break;
				case IDM_DUMP_ALL:				
					dump_all_characters(hwnd);
					break;
				case IDSUPER:
					ptr = jabia_characters.at(last_character_selected_index);
					max_stats(ptr);
					fillDialog(hwnd, ptr);
					break;
				case IDFIXGEAR:
					ptr = jabia_characters.at(last_character_selected_index);
					fix_gear(ptr);
					fillDialog(hwnd, ptr);
					break;
				case IDMASTERKEY:
					ptr = jabia_characters.at(last_character_selected_index);
					fillDialog(hwnd, ptr);
					patchDoorKeyCheck();
					break;
                case IDCANCEL:
                    DestroyWindow(hwnd);
					PostQuitMessage(0);
					break;
            }
        break;
        default:
            return FALSE;
    }
    return FALSE;
}


void dump_current_character(HWND hwnd, JABIA_Character * ptr) {
	TCHAR debugStrBuf[100];
	JABIA_Character character;
	wsprintf(debugStrBuf, _T("Character address 0x%X | ptr address 0x%x"), &character, ptr);
	OutputDebugString(debugStrBuf);
	memcpy(&character, (void *)ptr, sizeof(JABIA_Character));		
	OutputDebugString(_T("Dump character"));
	
	OPENFILENAME ofn;
    TCHAR szFileName[MAX_PATH] = _T("");

    ZeroMemory(&ofn, sizeof(ofn));

    ofn.lStructSize = sizeof(ofn); // SEE NOTE BELOW
    ofn.hwndOwner = hwnd;
    ofn.lpstrFilter = _T("JABIA Character Dump (*.jcd)\0*.jcd\0All Files (*.*)\0*.*\0");
    ofn.lpstrFile = szFileName;
    ofn.nMaxFile = MAX_PATH;
    ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;
    ofn.lpstrDefExt = _T("jcd");
	
    if(GetSaveFileName(&ofn))
    {
        // Do something usefull with the filename stored in szFileName 
		dump_character(&character, szFileName);
    } else {
		//TODO show error message
	}
}

BOOL dump_all_characters(HWND hwnd) {
	TCHAR buf[100];
	
	LPITEMIDLIST pidl     = NULL;
	BROWSEINFO   bi       = { 0 };
	BOOL         bResult  = FALSE;

	bi.hwndOwner      = hwnd;
	bi.pszDisplayName = buf;
	bi.pidlRoot       = NULL;
	bi.lpszTitle      = _T("Select directory");
	bi.ulFlags        = BIF_RETURNONLYFSDIRS | BIF_USENEWUI;

	if ((pidl = SHBrowseForFolder(&bi)) != NULL)
	{
		bResult = SHGetPathFromIDList(pidl, buf);
		CoTaskMemFree(pidl);
	}

	if(bResult) {
		for(unsigned int i = 0; i < jabia_characters.size(); i++) {
			TCHAR full_path[100];
			wsprintf(full_path, _T("%s/%s"), buf, jabia_characters.at(i)->merc_name);
			dump_character(jabia_characters.at(i), full_path);
		}
	} else {
		//TODO show error
	}
	return bResult;
	
}

void fillDialog(HWND hwnd, JABIA_Character * ptr) {
	TCHAR buf[100];
	char nameBuf[100];
	JABIA_Character character;

	_itot_s(CurrentSaveGamePtr->money, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_MONEY, buf);

	if(ptr != NULL) {
		memcpy(&character, (void *)ptr, sizeof(JABIA_Character));		
		
		// add weapons to combo boxes
		HWND comboControl4;
		comboControl4=GetDlgItem(hwnd,IDC_COMBO_INVENTORY_WEAPON);			
		uint32_t selected_weapon_id = character.inventory.weapons[last_weaponslot_selected_index].weapon;		
		int weapon_id = 0;		
		if(selected_weapon_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Weapon *>::iterator ii=jabia_weapons_map.begin(); ii!=jabia_weapons_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(selected_weapon_id == id) {
					SendMessage(comboControl4, CB_SETCURSEL, weapon_id, 0);
					break;
				}
				weapon_id++;
			}		
		} else {
			SendMessage(comboControl4, CB_SETCURSEL, jabia_weapons_map.size(), 0);
		}
		
		HWND comboControl5;
		comboControl5=GetDlgItem(hwnd,IDC_COMBO_EQUIPED_WEAPON);			
		uint32_t equiped_weapon_id = character.inventory.weapon_in_hand;		
		weapon_id = 0;		
		if(equiped_weapon_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Weapon *>::iterator ii=jabia_weapons_map.begin(); ii!=jabia_weapons_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_weapon_id == id) {
					SendMessage(comboControl5, CB_SETCURSEL, weapon_id, 0);
					break;
				}
				weapon_id++;
			}		
		} else {
			SendMessage(comboControl5, CB_SETCURSEL, jabia_weapons_map.size(), 0);
		}		

		HWND comboControl6;
		comboControl6=GetDlgItem(hwnd,IDC_COMBO_WEAPON_MOD);			
		uint32_t equiped_attachment_id = character.inventory.weapon_attachment_removable;		
		int attachment_id = 0;		
		if(equiped_attachment_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Attachment *>::iterator ii=jabia_attachments_map.begin(); ii!=jabia_attachments_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_attachment_id == id) {
					SendMessage(comboControl6, CB_SETCURSEL, attachment_id, 0);
					break;
				}
				attachment_id++;
			}		
		} else {
			SendMessage(comboControl6, CB_SETCURSEL, jabia_attachments_map.size(), 0);
		}	
		
		HWND comboControl7;
		comboControl7=GetDlgItem(hwnd,IDC_COMBO_HELMET);			
		uint32_t equiped_helmet_id = character.inventory.cap_equiped;		
		int helmet_id = 0;
		if(equiped_helmet_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_headgear_map.begin(); ii!=jabia_headgear_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_helmet_id == id) {
					SendMessage(comboControl7, CB_SETCURSEL, helmet_id, 0);
					break;
				}
				helmet_id++;
			}		
		} else {
			SendMessage(comboControl7, CB_SETCURSEL, jabia_headgear_map.size(), 0);
		}

		HWND comboControl8;
		comboControl8=GetDlgItem(hwnd,IDC_COMBO_VEST);			
		uint32_t equiped_vest_id = character.inventory.vest_equiped;		
		int vest_id = 0;
		if(equiped_vest_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_vest_map.begin(); ii!=jabia_vest_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_vest_id == id) {
					SendMessage(comboControl8, CB_SETCURSEL, vest_id, 0);
					break;
				}
				vest_id++;
			}		
		} else {
			SendMessage(comboControl8, CB_SETCURSEL, jabia_vest_map.size(), 0);
		}
		
		HWND comboControl9;
		comboControl9=GetDlgItem(hwnd,IDC_COMBO_SHIRT);			
		uint32_t equiped_shirt_id = character.inventory.shirt_equiped;		
		int shirt_id = 0;
		if(equiped_shirt_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_torso_map.begin(); ii!=jabia_torso_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_shirt_id == id) {
					SendMessage(comboControl9, CB_SETCURSEL, shirt_id, 0);
					break;
				}
				shirt_id++;
			}		
		} else {
			SendMessage(comboControl9, CB_SETCURSEL, jabia_torso_map.size(), 0);
		}

		HWND comboControl10;
		comboControl10=GetDlgItem(hwnd,IDC_COMBO_PANTS);			
		uint32_t equiped_pants_id = character.inventory.pants_equiped;		
		int pants_id = 0;
		if(equiped_pants_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_pants_map.begin(); ii!=jabia_pants_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_pants_id == id) {
					SendMessage(comboControl10, CB_SETCURSEL, pants_id, 0);
					break;
				}
				pants_id++;
			}		
		} else {
			SendMessage(comboControl10, CB_SETCURSEL, jabia_pants_map.size(), 0);
		}

		HWND comboControl11;
		comboControl11=GetDlgItem(hwnd,IDC_COMBO_SHOES);			
		uint32_t equiped_shoes_id = character.inventory.shoes_equiped;		
		int shoes_id = 0;
		if(equiped_shoes_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_shoes_map.begin(); ii!=jabia_shoes_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_shoes_id == id) {
					SendMessage(comboControl11, CB_SETCURSEL, shoes_id, 0);
					break;
				}
				shoes_id++;
			}		
		} else {
			SendMessage(comboControl11, CB_SETCURSEL, jabia_shoes_map.size(), 0);
		}

		HWND comboControl12;
		comboControl12=GetDlgItem(hwnd,IDC_COMBO_EYEWEAR);			
		uint32_t equiped_eyewear_id = character.inventory.eyewear_equiped;		
		int eyewear_id = 0;
		if(equiped_eyewear_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_eyewear_map.begin(); ii!=jabia_eyewear_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_eyewear_id == id) {
					SendMessage(comboControl12, CB_SETCURSEL, eyewear_id, 0);
					break;
				}
				eyewear_id++;
			}		
		} else {
			SendMessage(comboControl12, CB_SETCURSEL, jabia_eyewear_map.size(), 0);
		}

		HWND comboControl13;
		comboControl13=GetDlgItem(hwnd,IDC_COMBO_AMMO);			
		uint32_t equiped_ammo_id = character.inventory.ammo_equiped;		
		int ammo_id = 0;
		if(equiped_ammo_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Ammo *>::iterator ii=jabia_ammo_map.begin(); ii!=jabia_ammo_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_ammo_id == id) {
					SendMessage(comboControl13, CB_SETCURSEL, ammo_id, 0);
					break;
				}
				ammo_id++;
			}		
		} else {
			SendMessage(comboControl13, CB_SETCURSEL, jabia_ammo_map.size(), 0);
		}

		HWND comboControl14;
		comboControl14=GetDlgItem(hwnd,IDC_COMBO_SPECIAL);			
		uint32_t equiped_special_id = character.inventory.special_equiped;		
		int special_id = 0;
		if(equiped_special_id != EMPTY_SLOT) {
			for( std::map<int, JABIA_Item *>::iterator ii=jabia_item_map.begin(); ii!=jabia_item_map.end(); ++ii) {
				uint32_t id = (*ii).second->ID;
				if(equiped_special_id == id) {
					SendMessage(comboControl14, CB_SETCURSEL, special_id, 0);
					break;
				}
				special_id++;
			}		
		} else {
			SendMessage(comboControl14, CB_SETCURSEL, jabia_item_map.size(), 0);
		}

		// address of character
		_itot_s((uint32_t)ptr, buf, 100, 16);
		SetDlgItemText(hwnd, IDC_ADDRESS, buf);	

		_itot_s(character.level, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_LEV, buf);

		_itot_s(character.experience, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_EX, buf);

		_itot_s(character.training_points, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_TP, buf);

		_itot_s(character.inventory.weapon_in_hand_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_WPN_EQ_DUR, buf);

		_itot_s(character.inventory.cap_equiped_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_HELM_EQ_DUR, buf);
		
		_itot_s(character.inventory.eyewear_equiped_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_EYE_EQ_DUR, buf);

		_itot_s(character.inventory.special_equiped_charges, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_SPC_EQ_LEFT, buf);
		
		_itot_s(character.inventory.shirt_equiped_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_SHRT_EQ_DUR, buf);
		
		_itot_s(character.inventory.vest_equiped_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_VEST_DUR, buf);
		
		_itot_s(character.inventory.shoes_equiped_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_SHOES_DUR, buf);

		_itot_s(character.inventory.pants_equiped_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_PANTS_DUR, buf);
		/*
		_itot_s(character.inventory.ammo_equiped, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_AMMO_EQ, buf);
		*/
		_itot_s(character.inventory.ammo_equiped_count, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_AMMO_EQ_CNT, buf);

		// health and stamina 	
		_stprintf_s(buf, _T("%.1f"), character.health, 4);
		//OutputDebugString(buf);
		SetDlgItemText(hwnd, IDC_HLTH, buf);

		_stprintf_s(buf, _T("%.1f"), character.stamina, 4);
		SetDlgItemText(hwnd, IDC_STAMINA, buf);

		// name
		memset(nameBuf, 0x00, 16);
		memcpy(nameBuf, character.merc_name, character.name_length);
		SetDlgItemTextA(hwnd, IDC_MERC_NAME, nameBuf);

		_itot_s(character.faction, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_MERC_FAC, buf);

		_itot_s(character.medical_condition, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_MED_COND, buf);

		// inventory
		_itot_s(character.inventory.weapons[last_weaponslot_selected_index].weapon_durability, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_WPN_INV_DUR, buf);

		_itot_s(character.inventory.weapons[last_weaponslot_selected_index].ammo_count, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_AMMO_INV_CNT, buf);
		/*
		_itot_s(character.inventory.inventory_items[last_inventory_selected_index].item_id, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_INV_ITEM_ID, buf);
		*/
		if(character.inventory.inventory_items[last_inventory_selected_index].item_id != EMPTY_SLOT) {
			wsprintf(buf, _T("%i|%s"), character.inventory.inventory_items[last_inventory_selected_index].item_id, ctx.string_map[character.inventory.inventory_items[last_inventory_selected_index].item_id].c_str());
			SetDlgItemText(hwnd, IDC_INV_ITEM_ID, buf);
		} else {
			SetDlgItemText(hwnd, IDC_INV_ITEM_ID, _T("None"));
		}


		// attributes
		_itot_s(character.agility, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_AG, buf);

		_itot_s(character.dexterity, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_DEX, buf);

		_itot_s(character.strength, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_STR, buf);

		_itot_s(character.intelligence, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_INT, buf);

		_itot_s(character.perception, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_PER, buf);

		// skills
		_itot_s(character.medical, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_MED, buf);

		_itot_s(character.explosives, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_EXPL, buf);

		_itot_s(character.marksmanship, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_MARK, buf);

		_itot_s(character.stealth, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_STEALTH, buf);

		_itot_s(character.mechanical, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_MECH, buf);

		_itot_s(character.bleed_rate, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_BLEED_RATE, buf);

		// stats
		_itot_s(character.total_days_in_service, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_DAYS_SERVICE, buf);

		_itot_s(character.melee_performed, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_MELEE_ATTACKS, buf);

		_itot_s(character.total_grenades_thrown, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_GRENADES_THROWN, buf);

		_itot_s(character.rockets_fired, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_ROCKETS_FIRED, buf);

		_itot_s(character.bullets_fired, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_BULLETS_SHOT, buf);

		_itot_s(character.total_damage_dealt, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_TOTAL_DAMAGE_DEALT, buf);

		_itot_s(character.enemies_killed, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_ENEMIES_KILLED, buf);

		_itot_s(character.total_damage_taken, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_TOTAL_DAMAGE_TAKEN, buf);

		_itot_s(character.times_bleeding, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_TIMES_BLEEDING, buf);

		_itot_s(character.times_wounded, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_TIMES_WOUNDED, buf);

		_itot_s(character.times_rescued_from_dying, buf, 100, 10);
		SetDlgItemText(hwnd, IDC_TIMES_RESCUED, buf);
	}	
}

void setCharacter(HWND hwnd, JABIA_Character * ptr) {
	TCHAR buf [100];
	char nameBuf[100];
	JABIA_Character * character_ptr = ptr;
	uint32_t level = 0;
	uint32_t experience;
	uint32_t training_points;
	uint16_t weapon_in_hand;
	uint16_t weapon_in_hand_durability;
	uint16_t cap_equiped;
	uint16_t cap_equiped_durability;
	uint16_t eyewear_equiped; 
	uint16_t eyewear_equiped_durability;
	uint16_t special_equiped; 
	uint16_t special_equiped_charges;
	uint16_t shirt_equiped;
	uint16_t shirt_equiped_durability;
	uint16_t vest_equiped;
	uint16_t vest_equiped_durability;
	uint16_t shoes_equiped;
	uint16_t shoes_equiped_durability;
	uint16_t pants_equiped;
	uint16_t pants_equiped_durability;	
	uint16_t ammo_equiped_count;
	uint16_t weapon_attachment_removable;

	uint16_t weapon;
	uint16_t weapon_durability;
	uint16_t ammo_count;

	float health;
	float stamina;
	uint32_t faction;
	uint32_t medical_condition;

	// attributes
	uint32_t agility;
	uint32_t dexterity;
	uint32_t strength;
	uint32_t intelligence;
	uint32_t perception;

	// skills
	uint32_t medical;
	uint32_t explosives;
	uint32_t marksmanship;
	uint32_t stealth;
	uint32_t mechanical;

	// health
	uint32_t bleed_rate;

	// stats
	uint32_t days_in_service;
	uint32_t melee_attacks;
	uint32_t total_grenades_thrown;
	uint32_t rockets_fired;
	uint32_t bullets_fired;
	uint32_t damage_dealt;
	uint32_t enemies_killed;
	uint32_t damage_taken;
	uint32_t times_bleeding;
	uint32_t times_wounded;
	uint32_t times_rescued;
	
	GetDlgItemText(hwnd, IDC_LEV, buf, 100);
	level = _ttoi(buf);
	character_ptr->level = level;

	GetDlgItemText(hwnd, IDC_EX, buf, 100);
	experience = _ttoi(buf);
	character_ptr->experience = experience;

	GetDlgItemText(hwnd, IDC_TP, buf, 100);
	training_points = _ttoi(buf);
	character_ptr->training_points = training_points;

	if(inventory_combo_status.equiped_weapon_changed) {		
		GetDlgItemText(hwnd, IDC_COMBO_EQUIPED_WEAPON, buf, 100);
		weapon_in_hand = getIdFromString(buf);
		if(weapon_in_hand != 0)
		{								
			character_ptr->inventory.weapon_in_hand = weapon_in_hand;
			character_ptr->inventory.weapon_in_hand_durability = jabia_weapons_map[weapon_in_hand]->Quality;
			uint16_t ammoType = jabia_weapons_map[weapon_in_hand]->AmmunitionType;
			for( std::map<int, JABIA_Ammo *>::iterator ii=jabia_ammo_map.begin(); ii!=jabia_ammo_map.end(); ++ii) {
				if(ammoType == (*ii).second->AmmunitionType) {
					character_ptr->inventory.ammo_equiped = (*ii).second->ID;
					break;
				}
			}
			character_ptr->inventory.ammo_equiped_count = jabia_weapons_map[weapon_in_hand]->ClipSize;
		} else {
			character_ptr->inventory.weapon_in_hand = EMPTY_SLOT;
			character_ptr->inventory.weapon_in_hand_durability = 0;
			character_ptr->inventory.ammo_equiped = EMPTY_SLOT;
			character_ptr->inventory.ammo_equiped_count = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_WPN_EQ_DUR, buf, 100);
		weapon_in_hand_durability = _ttoi(buf);
		character_ptr->inventory.weapon_in_hand_durability = weapon_in_hand_durability;

		GetDlgItemText(hwnd, IDC_AMMO_EQ_CNT, buf, 100);
		ammo_equiped_count = _ttoi(buf);
		character_ptr->inventory.ammo_equiped_count = ammo_equiped_count;

	}
	character_ptr->inventory.weapon_in_hand_removable = 1;
	
	if(inventory_combo_status.helmet_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_HELMET, buf, 100);	
		cap_equiped = getIdFromString(buf);
		if(cap_equiped != 0)
		{								
			character_ptr->inventory.cap_equiped = cap_equiped;
			character_ptr->inventory.cap_equiped_durability = 100;
		} else {
			character_ptr->inventory.cap_equiped = EMPTY_SLOT;
			character_ptr->inventory.cap_equiped_durability = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_HELM_EQ_DUR, buf, 100);
		cap_equiped_durability = _ttoi(buf);
		character_ptr->inventory.cap_equiped_durability = cap_equiped_durability;
	}
	character_ptr->inventory.cap_equiped_removable = 1;

	if(inventory_combo_status.vest_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_VEST, buf, 100);	
		vest_equiped = getIdFromString(buf);
		if(vest_equiped != 0)
		{								
			character_ptr->inventory.vest_equiped = vest_equiped;
			character_ptr->inventory.vest_equiped_durability = 100;
		} else {
			character_ptr->inventory.vest_equiped = EMPTY_SLOT;
			character_ptr->inventory.vest_equiped_durability = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_VEST_DUR, buf, 100);
		vest_equiped_durability = _ttoi(buf);
		character_ptr->inventory.vest_equiped_durability = vest_equiped_durability;
	}
	character_ptr->inventory.vest_equiped_status = 1;

	if(inventory_combo_status.torso_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_SHIRT, buf, 100);	
		shirt_equiped = getIdFromString(buf);
		if(shirt_equiped != 0)
		{								
			character_ptr->inventory.shirt_equiped = shirt_equiped;
			character_ptr->inventory.shirt_equiped_durability = 100;
		} else {
			character_ptr->inventory.shirt_equiped = EMPTY_SLOT;
			character_ptr->inventory.shirt_equiped_durability = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_SHRT_EQ_DUR, buf, 100);
		shirt_equiped_durability = _ttoi(buf);
		character_ptr->inventory.shirt_equiped_durability = shirt_equiped_durability;
	}
	character_ptr->inventory.shirt_equiped_status = 1;

	if(inventory_combo_status.pants_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_PANTS, buf, 100);	
		pants_equiped = getIdFromString(buf);
		if(pants_equiped != 0)
		{								
			character_ptr->inventory.pants_equiped = pants_equiped;
			character_ptr->inventory.pants_equiped_durability = 100;
		} else {
			character_ptr->inventory.pants_equiped = EMPTY_SLOT;
			character_ptr->inventory.pants_equiped_durability = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_PANTS_DUR, buf, 100);
		pants_equiped_durability = _ttoi(buf);
		character_ptr->inventory.pants_equiped_durability = pants_equiped_durability;
	}
	character_ptr->inventory.pants_equiped_status = 1;

	if(inventory_combo_status.shoes_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_SHOES, buf, 100);	
		shoes_equiped = getIdFromString(buf);
		if(shoes_equiped != 0)
		{								
			character_ptr->inventory.shoes_equiped = shoes_equiped;
			character_ptr->inventory.shoes_equiped_durability = 100;
		} else {
			character_ptr->inventory.shoes_equiped = EMPTY_SLOT;
			character_ptr->inventory.shoes_equiped_durability = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_SHOES_DUR, buf, 100);
		shoes_equiped_durability = _ttoi(buf);
		character_ptr->inventory.shoes_equiped_durability = shoes_equiped_durability;
	}
	character_ptr->inventory.shoes_equiped_status = 1;

	if(inventory_combo_status.eyewear_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_EYEWEAR, buf, 100);	
		eyewear_equiped = getIdFromString(buf);
		if(shoes_equiped != 0)
		{								
			character_ptr->inventory.eyewear_equiped = eyewear_equiped;
			character_ptr->inventory.eyewear_equiped_durability = 100;
		} else {
			character_ptr->inventory.eyewear_equiped = EMPTY_SLOT;
			character_ptr->inventory.eyewear_equiped_durability = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_EYE_EQ_DUR, buf, 100);
		eyewear_equiped_durability = _ttoi(buf);
		character_ptr->inventory.eyewear_equiped_durability = eyewear_equiped_durability;
	}
	character_ptr->inventory.eyewear_equiped_status = 1;

	if(inventory_combo_status.special_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_SPECIAL, buf, 100);	
		OutputDebugString(buf);
		special_equiped = getIdFromString(buf);
		TCHAR debugBuffer[100];
		wsprintf(debugBuffer, _T("%s %i"), buf, special_equiped);
		OutputDebugString(debugBuffer);
		if(special_equiped != 0)
		{								
			character_ptr->inventory.special_equiped = special_equiped;
			character_ptr->inventory.special_equiped_charges = jabia_item_map[special_equiped]->Charges;
			character_ptr->inventory.special_equiped_status = 1;
		} else {
			character_ptr->inventory.special_equiped = EMPTY_SLOT;
			character_ptr->inventory.special_equiped_charges = 0;
			character_ptr->inventory.special_equiped_status = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_SPC_EQ_LEFT, buf, 100);
		special_equiped_charges = _ttoi(buf);
		character_ptr->inventory.special_equiped_charges = special_equiped_charges;
	}	

	if(inventory_combo_status.attachment_changed) {		
		GetDlgItemText(hwnd, IDC_COMBO_WEAPON_MOD, buf, 100);
		weapon_attachment_removable = getIdFromString(buf);
		if(weapon_attachment_removable != 0)
		{								
			character_ptr->inventory.weapon_attachment_removable = weapon_attachment_removable;
			character_ptr->inventory.weapon_attachment_status = 1;
		} else {
			character_ptr->inventory.weapon_attachment_removable = 0xFFFF;
			character_ptr->inventory.weapon_attachment_status = 0;
		}
	} 

	character_ptr->inventory.weapon_attachment_status = 1;

	// get name and it's length
	memset(nameBuf, 0x0, JABIA_CHARACTER_MAX_NAME_LENGTH);
	GetDlgItemTextA(hwnd, IDC_MERC_NAME, nameBuf, JABIA_CHARACTER_MAX_NAME_LENGTH);
	memcpy(character_ptr->merc_name, nameBuf, JABIA_CHARACTER_MAX_NAME_LENGTH); // TODO read length of name from character struct
	character_ptr->name_length = (uint32_t)strlen(character_ptr->merc_name);

	// inventory
	if(inventory_combo_status.inventory_weapon_changed) {
		GetDlgItemText(hwnd, IDC_COMBO_INVENTORY_WEAPON, buf, 100);		
		weapon = getIdFromString(buf);
		if(weapon != 0)
		{								
			character_ptr->inventory.weapons[last_weaponslot_selected_index].weapon = weapon;
			character_ptr->inventory.weapons[last_weaponslot_selected_index].weapon_durability = jabia_weapons_map[weapon]->Quality;
			character_ptr->inventory.weapons[last_weaponslot_selected_index].ammo_count = jabia_weapons_map[weapon]->ClipSize;
		} else {
			character_ptr->inventory.weapons[last_weaponslot_selected_index].weapon = EMPTY_SLOT;
			character_ptr->inventory.weapons[last_weaponslot_selected_index].weapon_durability = 0;
			character_ptr->inventory.weapons[last_weaponslot_selected_index].ammo_count = 0;
		}
	} else {
		GetDlgItemText(hwnd, IDC_WPN_INV_DUR, buf, 100);
		weapon_durability = _ttoi(buf);
		character_ptr->inventory.weapons[last_weaponslot_selected_index].weapon_durability = weapon_durability;

		GetDlgItemText(hwnd, IDC_AMMO_INV_CNT, buf, 100);
		ammo_count = _ttoi(buf);
		character_ptr->inventory.weapons[last_weaponslot_selected_index].ammo_count = ammo_count;	
	}
	character_ptr->inventory.weapons[last_weaponslot_selected_index].removable = 1;

	// health and stamina
	GetDlgItemText(hwnd, IDC_HLTH, buf, 100);
	health = (float)_ttof(buf);
	character_ptr->health = health;

	GetDlgItemText(hwnd, IDC_STAMINA, buf, 100);
	stamina = (float)_ttof(buf);
	character_ptr->stamina = stamina;

	GetDlgItemText(hwnd, IDC_MERC_FAC, buf, 100);
	faction = _ttoi(buf);
	character_ptr->faction = faction;

	GetDlgItemText(hwnd, IDC_MED_COND, buf, 100);
	medical_condition = _ttoi(buf);
	character_ptr->medical_condition = medical_condition;

	// attributes
	GetDlgItemText(hwnd, IDC_AG, buf, 100);
	agility = _ttoi(buf);
	character_ptr->agility = agility;

	GetDlgItemText(hwnd, IDC_DEX, buf, 100);
	dexterity = _ttoi(buf);
	character_ptr->dexterity = dexterity;

	GetDlgItemText(hwnd, IDC_STR, buf, 100);
	strength = _ttoi(buf);
	character_ptr->strength = strength;

	GetDlgItemText(hwnd, IDC_INT, buf, 100);
	intelligence = _ttoi(buf);
	character_ptr->intelligence = intelligence;

	GetDlgItemText(hwnd, IDC_PER, buf, 100);
	perception = _ttoi(buf);
	character_ptr->perception = perception;

	// skills
	GetDlgItemText(hwnd, IDC_MED, buf, 100);
	medical = _ttoi(buf);
	character_ptr->medical = medical;

	GetDlgItemText(hwnd, IDC_EXPL, buf, 100);
	explosives = _ttoi(buf);
	character_ptr->explosives = explosives;

	GetDlgItemText(hwnd, IDC_MARK, buf, 100);
	marksmanship = _ttoi(buf);
	character_ptr->marksmanship = marksmanship;

	GetDlgItemText(hwnd, IDC_STEALTH, buf, 100);
	stealth = _ttoi(buf);
	character_ptr->stealth = stealth;

	GetDlgItemText(hwnd, IDC_MECH, buf, 100);
	mechanical = _ttoi(buf);
	character_ptr->mechanical = mechanical;

	GetDlgItemText(hwnd, IDC_BLEED_RATE, buf, 100);
	bleed_rate = _ttoi(buf);
	character_ptr->bleed_rate = bleed_rate;

	// stats
	GetDlgItemText(hwnd, IDC_DAYS_SERVICE, buf, 100);
	days_in_service = _ttoi(buf);
	character_ptr->total_days_in_service = days_in_service;	

	GetDlgItemText(hwnd, IDC_MELEE_ATTACKS, buf, 100);
	melee_attacks = _ttoi(buf);
	character_ptr->melee_performed = melee_attacks;

	GetDlgItemText(hwnd, IDC_GRENADES_THROWN, buf, 100);
	total_grenades_thrown = _ttoi(buf);
	character_ptr->total_grenades_thrown = total_grenades_thrown;

	GetDlgItemText(hwnd, IDC_ROCKETS_FIRED, buf, 100);
	rockets_fired = _ttoi(buf);
	character_ptr->rockets_fired = rockets_fired;

	GetDlgItemText(hwnd, IDC_BULLETS_SHOT, buf, 100);
	bullets_fired = _ttoi(buf);
	character_ptr->bullets_fired = bullets_fired;

	GetDlgItemText(hwnd, IDC_TOTAL_DAMAGE_DEALT, buf, 100);
	damage_dealt = _ttoi(buf);
	character_ptr->total_damage_dealt = damage_dealt;

	GetDlgItemText(hwnd, IDC_ENEMIES_KILLED, buf, 100);
	enemies_killed = _ttoi(buf);
	character_ptr->enemies_killed = enemies_killed;

	GetDlgItemText(hwnd, IDC_TOTAL_DAMAGE_TAKEN, buf, 100);
	damage_taken = _ttoi(buf);
	character_ptr->total_damage_taken = damage_taken;

	GetDlgItemText(hwnd, IDC_TIMES_BLEEDING, buf, 100);
	times_bleeding = _ttoi(buf);
	character_ptr->times_bleeding = times_bleeding;

	GetDlgItemText(hwnd, IDC_TIMES_WOUNDED, buf, 100);
	times_wounded = _ttoi(buf);
	character_ptr->times_wounded = times_wounded;

	GetDlgItemText(hwnd, IDC_TIMES_RESCUED, buf, 100);
	times_rescued = _ttoi(buf);
	character_ptr->times_rescued_from_dying = times_rescued;

}

int getIdFromString(TCHAR * buf) {
		std::wstring comboBoxString = std::wstring(buf);
		size_t next = comboBoxString.find_first_of(_T("|"));
		int id = _ttoi(comboBoxString.substr(0, next).c_str());
		std::wstring itemString = comboBoxString.substr(next+1, comboBoxString.length());		
		if(itemString.compare(L"None") != 0) {
			return id;
		} else {
			return 0;
		}
}

// begin hooks
void setMoney(HWND hwnd) {
	TCHAR buf[100];
	int money;
	GetDlgItemText(hwnd, IDC_MONEY, buf, 100);
	money = _ttoi(buf);
	CurrentSaveGamePtr->money = money;	
}

__declspec(naked) void* myCharacterConstReturn(){	
	// Character constructor uses thiscall calling convention and as an optimization passes something in EDX. I don't hook the call to the constructor.
	// Instead, I hook the return of the character constructor. The "this" pointer will be in EAX.

	__asm{
		push eax;
		mov ecx, eax;
		call recordCharacters;
		pop eax;
		retn 0x1C;
	}
}

void __fastcall recordCharacters(void* instance){
	//char buf [100];
	JABIA_Character * character_ptr;
	//OutputDebugString("Parsing character!");

	character_ptr = (JABIA_Character *)instance;

	//wsprintf(buf, "Character at 0x%X", character_ptr);
	//OutputDebugString(buf);
	jabia_characters.push_back(character_ptr);
	//wsprintf(buf, "Size %i", jabia_characters.size());
	//OutputDebugString(buf);
}

__declspec(naked) void* myCharacterDestReturn(){	
	__asm{
		push ebx; // something needs to be pushed	
		mov ecx, ebx; // saved
		call removeCharacter;
		pop ebx; // then poped
		pop     edi; // .text:00532BB8      
		pop     esi; // .text:00532BB9                   
		pop     ebx; // .text:00532BBA                 
        pop     ecx // .text:00532BBB
        retn    4 // .text:00532BBC
	}
}

int myCharacterDestructor(JABIA_Character * ptr) {
	//char buf[100];
	//wsprintf(buf, "Removing character at 0x%X", ptr);
	//OutputDebugString(buf);
	//wsprintf(buf, "Character is %s", ptr->merc_name);
	//OutputDebugString(buf);
	
	return CharacterDestructor(ptr);
}

void __fastcall removeCharacter(JABIA_Character * ptr){
	//char buf[100];
	//wsprintf(buf, "Removing character at 0x%X", ptr);
	//OutputDebugString(buf);
	//wsprintf(buf, "Character is %s", ptr->merc_name);
	//OutputDebugString(buf);
	std::vector<JABIA_Character *>::iterator position = std::find(jabia_characters.begin(), jabia_characters.end(), ptr);
	if (position != jabia_characters.end()) // == vector.end() means the element was not found
		jabia_characters.erase(position);
}


__declspec(naked) void* mySaveGameParseReturn(){	
	__asm{
		pushad;
		// pointer chase to get pointer to game state
		mov esi, DWORD PTR DS:[ebx + 0xA84];
		mov eax, [esi + 0x84];
		mov CurrentSaveGamePtr, eax;
		popad;
		pop ecx;
		pop edi;
		pop esi;
		pop ebp;
		pop ebx;
		add esp, 0x28;
		retn 8;
	}
}

__declspec(naked) void* myWeaponConstReturn(){	
	__asm{
		push eax;
		mov ecx, eax;
		call recordWeapons;
		pop eax;
		retn 8;
	}
}


void __fastcall recordWeapons(void* instance){
	TCHAR buf [100];
	JABIA_Weapon * weapon_ptr;

	weapon_ptr = (JABIA_Weapon *)instance;

	wsprintf(buf, _T("Weapon at 0x%X, ID: %i, AmmunitionType: %i"), weapon_ptr, weapon_ptr->ID, weapon_ptr->AmmunitionType);
	OutputDebugString(buf);
	jabia_weapons_map[weapon_ptr->ID] = weapon_ptr;
}

__declspec(naked) void* myAttachmentConstReturn(){	
	__asm{
		push eax;
		mov ecx, eax;
		call recordAttachments;
		pop eax;
		retn 8;
	}
}


void __fastcall recordAttachments(void* instance){
	TCHAR buf [100];
	JABIA_Attachment * attachment_ptr;

	attachment_ptr = (JABIA_Attachment *)instance;

	wsprintf(buf, _T("Attachment at 0x%X, ID: %i"), attachment_ptr, attachment_ptr->ID);
	OutputDebugString(buf);
	jabia_attachments_map[attachment_ptr->ID] = attachment_ptr;
}

__declspec(naked) void* myClothConstReturn(){	
	__asm{
		push eax;
		mov ecx, eax;
		call recordCloth;
		pop eax;
		retn 8;
	}
}


void __fastcall recordCloth(void* instance){
	TCHAR buf [100];
	JABIA_Cloth * cloth_ptr;

	cloth_ptr = (JABIA_Cloth *)instance;

	wsprintf(buf, _T("Clothing at 0x%X, ID: %i"), cloth_ptr, cloth_ptr->ID);
	OutputDebugString(buf);
	jabia_cloth_map[cloth_ptr->ID] = cloth_ptr;

	for( std::map<int, JABIA_Cloth *>::iterator ii=jabia_cloth_map.begin(); ii!=jabia_cloth_map.end(); ++ii) {
		if((*ii).second->Slot == Cap) {
			jabia_headgear_map[(*ii).second->ID] = (*ii).second;
		}
		if((*ii).second->Slot == Vest) {
			jabia_vest_map[(*ii).second->ID] = (*ii).second;
		}
		if((*ii).second->Slot == Torso) {
			jabia_torso_map[(*ii).second->ID] = (*ii).second;
		}
		if((*ii).second->Slot == Legs) {
			jabia_pants_map[(*ii).second->ID] = (*ii).second;
		}
		if((*ii).second->Slot == Feet) {
			jabia_shoes_map[(*ii).second->ID] = (*ii).second;
		}
		if((*ii).second->Slot == Glasses) {
			jabia_eyewear_map[(*ii).second->ID] = (*ii).second;
		}
	}
}

__declspec(naked) void* myItemConstReturn(){	
	__asm{
		push eax;
		mov ecx, eax;
		call recordItem;
		pop eax;
		retn 8;
	}
}

void __fastcall recordItem(void* instance){
	TCHAR buf [100];
	JABIA_Item * item_ptr;

	item_ptr = (JABIA_Item *)instance;

	wsprintf(buf, _T("Item at 0x%X, ID: %i"), item_ptr, item_ptr->ID);
	OutputDebugString(buf);
	jabia_item_map[item_ptr->ID] = item_ptr;
}

__declspec(naked) void* myAmmoConstReturn(){	
	__asm{
		push eax;
		mov ecx, eax;
		call recordAmmo;
		pop eax;
		retn 4;
	}
}

void __fastcall recordAmmo(void* instance){
	TCHAR buf [100];
	JABIA_Ammo * ammo_ptr;

	ammo_ptr = (JABIA_Ammo *)instance;

	wsprintf(buf, _T("Ammo at 0x%X, ID: %i, AmmunitionType: %i"), ammo_ptr, ammo_ptr->ID, ammo_ptr->AmmunitionType);
	OutputDebugString(buf);
	jabia_ammo_map[ammo_ptr->ID] = ammo_ptr;
}

void patchDoorKeyCheck(void) {	
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle);
	uint32_t * jmpAddressGui = (uint32_t *)((uint32_t)game_handle+DOOR_GUI_JMP_OFFSET);
	uint32_t * jmpAddressOpenAnim = (uint32_t *)((uint32_t)game_handle+DOOR_ANIMATION_JMP_OFFSET);
	uint32_t * jmpAddressCheck1 = (uint32_t *)((uint32_t)game_handle+DOOR_KEYCHECK1_JMP_OFFSET);
	uint32_t * jmpAddressCheck2 = (uint32_t *)((uint32_t)game_handle+DOOR_KEYCHECK2_JMP_OFFSET);
	TCHAR debugStrBuf[100];
	wsprintf(debugStrBuf, _T("Game handle 0x%x, offset 0x%x, masterkey patch address 0x%x"), game_handle, DOOR_GUI_JMP_OFFSET, jmpAddressGui);
	OutputDebugString(debugStrBuf);
	wsprintf(debugStrBuf, _T("Game handle 0x%x, offset 0x%x, masterkey patch address 0x%x"), game_handle, DOOR_ANIMATION_JMP_OFFSET, jmpAddressOpenAnim);
	OutputDebugString(debugStrBuf);
	wsprintf(debugStrBuf, _T("Game handle 0x%x, offset 0x%x, masterkey patch address 0x%x"), game_handle, DOOR_KEYCHECK1_JMP_OFFSET, jmpAddressCheck1);
	OutputDebugString(debugStrBuf);
	wsprintf(debugStrBuf, _T("Game handle 0x%x, offset 0x%x, masterkey patch address 0x%x"), game_handle, DOOR_KEYCHECK2_JMP_OFFSET, jmpAddressCheck2);
	OutputDebugString(debugStrBuf);


	uint16_t NOPpatch = 0x9090;
	DWORD oldProtection;
	// read + write
	VirtualProtect((LPVOID)jmpAddressGui, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	memcpy((void *)jmpAddressGui, &NOPpatch, sizeof(uint16_t)); 
	// restore protection
	VirtualProtect((LPVOID)jmpAddressGui, 6, oldProtection, NULL);
	VirtualProtect((LPVOID)jmpAddressOpenAnim, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	memcpy((void *)jmpAddressOpenAnim, &NOPpatch, sizeof(uint16_t)); 
	// restore protection
	VirtualProtect((LPVOID)jmpAddressOpenAnim, 6, oldProtection, NULL);
	VirtualProtect((LPVOID)jmpAddressCheck1, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
	memcpy((void *)jmpAddressCheck1, &NOPpatch, sizeof(uint16_t)); 
	memcpy((void *)jmpAddressCheck2, &NOPpatch, sizeof(uint16_t));
	// restore protection
    VirtualProtect((LPVOID)jmpAddressCheck1, 6, oldProtection, NULL);
	
}