#include <windows.h>
#include <string.h>
#include <stdint.h>
#include <detours.h>
#include "resource.h"
#include "character.h"

#pragma comment(lib, "detours.lib")

#define MYFUNC_ADDR 0x01341FF0
#define SHOW_INVENTORY_FUNC 0x00D39B70    
typedef int (_stdcall *ShowInventoryPtr)(void * unknown1, void * character_ptr, void * unknown2, int unknown3);


BOOL CALLBACK DialogProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
DWORD WINAPI MyThread(LPVOID);
int myShowInventory(void * unknown1, void * character_ptr, void * unknown2, int unknown3);
void fillDialog(HWND hwnd, uint32_t ptr);
void setCharacter(HWND hwnd, uint32_t ptr);

ShowInventoryPtr ShowInventory = (ShowInventoryPtr)SHOW_INVENTORY_FUNC;
DWORD g_threadID;
HMODULE g_hModule;
//void __stdcall CallFunction(void);
HINSTANCE TheInstance = 0;
uint32_t address = 0; // character address

INT APIENTRY DllMain(HMODULE hDLL, DWORD Reason, LPVOID Reserved)
{
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
	// hook ShowInventory	
	//DetourTransactionBegin();
 //   DetourUpdateThread(GetCurrentThread());
 //   DetourAttach(&(PVOID&)ShowInventory, myShowInventory);
 //   DetourTransactionCommit();
    while(true)
    {
        if(GetAsyncKeyState(VK_F7) & 1)
        {

			    HWND hDialog = 0;
				
			    hDialog = CreateDialog (g_hModule,
                            MAKEINTRESOURCE (IDD_DIALOG1),
                            0,
                            DialogProc);
				HMODULE game_handle;
				GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, "GameDemo.exe", &game_handle);
				uint32_t temp_addr;
				temp_addr = (uint32_t)game_handle;
				char buf [100];

				temp_addr = *(uint32_t *)(temp_addr + 0x003C64E8)+ 0x6E0;
				wsprintf (buf, "base ptr 0x%x", temp_addr);
				OutputDebugString(buf);		
				temp_addr = *(uint32_t *)temp_addr + 0xD4;
				wsprintf (buf, "second ptr 0x%x", temp_addr);
				OutputDebugString(buf);
				temp_addr = *(uint32_t *)temp_addr + 0x5C0;
				wsprintf (buf, "second ptr 0x%x", temp_addr);
				OutputDebugString(buf);
				temp_addr = *(uint32_t *)temp_addr + 0x34;
				wsprintf (buf, "second ptr 0x%x", temp_addr);
				OutputDebugString(buf);
				temp_addr = *(uint32_t *)temp_addr + 0x118;
				wsprintf (buf, "second ptr 0x%x", temp_addr);
				OutputDebugString(buf);

				address = temp_addr;
				if(address) {
					fillDialog(hDialog, address);
				}
				if (!hDialog)
				{
					char buf [100];
					wsprintf (buf, "Error x%x", GetLastError ());
					MessageBox (0, buf, "CreateDialog", MB_ICONEXCLAMATION | MB_OK);
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
        else if(GetAsyncKeyState(VK_F8) &1) {
			OutputDebugString("Unloading DLL");
            break;
		}
    Sleep(100);
    }
	//DetourTransactionBegin();
 //   DetourUpdateThread(GetCurrentThread());
 //   DetourDetach(&(PVOID&)ShowInventory, myShowInventory);
 //   DetourTransactionCommit();
    FreeLibraryAndExitThread(g_hModule, 0);
    return 0;
}

//void __stdcall CallFunction(void)
//{
//    typedef void (__stdcall *pFunctionAddress)(void);
//    pFunctionAddress pMySecretFunction = (pFunctionAddress)(MYFUNC_ADDR);
//    pMySecretFunction();
//}

BOOL CALLBACK DialogProc (HWND hwnd, 
                          UINT message, 
                          WPARAM wParam, 
                          LPARAM lParam)
{
	BOOL status = FALSE;
	char address_string[50];	
	char buf [100];

    switch (message)
    {
        case WM_COMMAND:
            switch(LOWORD(wParam))
            {
				case IDGET:
					GetDlgItemText(hwnd, IDC_ADDRESS, address_string, 50);
					OutputDebugString(address_string);
					address = strtoul(address_string, NULL, 16);
					wsprintf (buf, "%li", address);
					OutputDebugString(buf);
					fillDialog(hwnd, address);
					break;
                case IDSET:
					GetDlgItemText(hwnd, IDC_ADDRESS, address_string, 50);
					address = strtoul(address_string, NULL, 16);
					setCharacter(hwnd, address);
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

void fillDialog(HWND hwnd, uint32_t ptr) {
	char buf[100];
	JABIA_Character character;
	memcpy(&character, (void *)ptr, sizeof(JABIA_Character));
	
	_itoa_s(ptr, buf, 100, 16);
	SetDlgItemText(hwnd, IDC_ADDRESS, buf);

	_itoa_s(character.level, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_LEV, buf);

	_itoa_s(character.experience, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_EX, buf);

	_itoa_s(character.training_points, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_TP, buf);

	_itoa_s(character.weapon_in_hand, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_WPN_EQ, buf);

	_itoa_s(character.weapon_in_hand_durability, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_WPN_EQ_DUR, buf);

	_itoa_s(character.helmet_equiped, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_HELM_EQ, buf);

	_itoa_s(character.helmet_equiped_durability, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_HELM_EQ_DUR, buf);

	_itoa_s(character.special_equiped, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_SPC_EQ, buf);

	_itoa_s(character.special_equiped_charges, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_SPC_EQ_LEFT, buf);

	_itoa_s(character.shirt_equiped, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_SHRT_EQ, buf);

	_itoa_s(character.shirt_equiped_durability, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_SHRT_EQ_DUR, buf);

	_itoa_s(character.vest_equiped, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_VEST_EQ, buf);

	_itoa_s(character.vest_equiped_durability, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_VEST_DUR, buf);

	_itoa_s(character.shoes_equiped, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_SHOES_EQ, buf);

	_itoa_s(character.shoes_equiped_durability, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_SHOES_DUR, buf);

	_itoa_s(character.pants_equiped, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_PANTS_EQ, buf);

	_itoa_s(character.pants_equiped_durability, buf, 100, 10);
	SetDlgItemText(hwnd, IDC_PANTS_DUR, buf);
}

void setCharacter(HWND hwnd, uint32_t ptr) {
	char buf [100];
	JABIA_Character * character_ptr = (JABIA_Character *)ptr;
	uint32_t level = 0;
	uint32_t experience;
	uint32_t training_points;
	uint16_t weapon_in_hand;
	uint16_t weapon_in_hand_durability;
	uint16_t helmet_equiped;
	uint16_t helmet_equiped_durability;
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

	GetDlgItemText(hwnd, IDC_LEV, buf, 100);
	level = atoi(buf);
	character_ptr->level = level;

	GetDlgItemText(hwnd, IDC_EX, buf, 100);
	experience = atoi(buf);
	character_ptr->experience = experience;

	GetDlgItemText(hwnd, IDC_TP, buf, 100);
	training_points = atoi(buf);
	character_ptr->training_points = training_points;

	GetDlgItemText(hwnd, IDC_WPN_EQ, buf, 100);
	weapon_in_hand = atoi(buf);
	character_ptr->weapon_in_hand = weapon_in_hand;

	GetDlgItemText(hwnd, IDC_WPN_EQ_DUR, buf, 100);
	weapon_in_hand_durability = atoi(buf);
	character_ptr->weapon_in_hand_durability = weapon_in_hand_durability;

	GetDlgItemText(hwnd, IDC_HELM_EQ, buf, 100);
	helmet_equiped = atoi(buf);
	character_ptr->helmet_equiped = helmet_equiped;

	GetDlgItemText(hwnd, IDC_HELM_EQ_DUR, buf, 100);
	helmet_equiped_durability = atoi(buf);
	character_ptr->helmet_equiped_durability = helmet_equiped_durability;

	GetDlgItemText(hwnd, IDC_SPC_EQ, buf, 100);
	special_equiped = atoi(buf);
	character_ptr->special_equiped = special_equiped;

	GetDlgItemText(hwnd, IDC_SPC_EQ_LEFT, buf, 100);
	special_equiped_charges = atoi(buf);
	character_ptr->special_equiped_charges = special_equiped_charges;

	GetDlgItemText(hwnd, IDC_SHRT_EQ, buf, 100);
	shirt_equiped = atoi(buf);
	character_ptr->shirt_equiped = shirt_equiped;

	GetDlgItemText(hwnd, IDC_SHRT_EQ_DUR, buf, 100);
	shirt_equiped_durability = atoi(buf);
	character_ptr->shirt_equiped_durability = shirt_equiped_durability;

	GetDlgItemText(hwnd, IDC_VEST_EQ, buf, 100);
	vest_equiped = atoi(buf);
	character_ptr->vest_equiped = vest_equiped;

	GetDlgItemText(hwnd, IDC_VEST_DUR, buf, 100);
	vest_equiped_durability = atoi(buf);
	character_ptr->vest_equiped_durability = vest_equiped_durability;

	GetDlgItemText(hwnd, IDC_SHOES_EQ, buf, 100);
	shoes_equiped = atoi(buf);
	character_ptr->shoes_equiped = shoes_equiped;

	GetDlgItemText(hwnd, IDC_SHOES_DUR, buf, 100);
	shoes_equiped_durability = atoi(buf);
	character_ptr->vest_equiped_durability = shoes_equiped_durability;

	GetDlgItemText(hwnd, IDC_PANTS_EQ, buf, 100);
	pants_equiped = atoi(buf);
	character_ptr->pants_equiped = pants_equiped;

	GetDlgItemText(hwnd, IDC_PANTS_DUR, buf, 100);
	pants_equiped_durability = atoi(buf);
	character_ptr->pants_equiped_durability = pants_equiped_durability;
}

int myShowInventory(void * unknown1, void * character_ptr, void * unknown2, int unknown3) {
	OutputDebugString("Showing the inventory!");
	int retVal;
	address = (uint32_t) character_ptr;
	retVal = ShowInventory(unknown1, character_ptr, unknown2, unknown3);
	return retVal;

}