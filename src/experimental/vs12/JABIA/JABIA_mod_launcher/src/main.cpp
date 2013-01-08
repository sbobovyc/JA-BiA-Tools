#include <windows.h>
#include "libutils.h"
#include "resource.h"

#define LAUNCHER_VERSION_STRING "Version 0.2a\r\n"

#define LAUNCHER_NAME "JaggedAllianceBIA.exe"
#define EXE_NAME "GameJABiA.exe"

#define DEBUGGER_DLL_PATH "\\mods\\debugger\\JABIA_debug.dll"
#define XPMOD_DLL_PATH "\\mods\\xpmod\\JABIA_xpmod.dll"
#define LOOTDROP_DLL_PATH "\\mods\\loot_drop\\JABIA_loot_drop.dll"

BOOL CALLBACK DialogProc (HWND hwnd, 
                          UINT message, 
                          WPARAM wParam, 
                          LPARAM lParam);

void append_text(HWND hwnd, char * buf);
DWORD WINAPI launch_game(LPVOID);
void inject_dlls();

HINSTANCE TheInstance = 0;
UINT debug = 0;
UINT xpmod = 0;
UINT lootmod = 0;

HWND cancel_handle;
HWND dialog_handle;

int WINAPI WinMain
   (HINSTANCE hInst, HINSTANCE hPrevInst, char * cmdParam, int cmdShow)
{
    TheInstance = hInst;
    
	HWND hDialog = 0;
    hDialog = CreateDialog (hInst, 
                            MAKEINTRESOURCE (IDD_DIALOG1), 
                            0, 
                            DialogProc);

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

    return msg.wParam;
}

BOOL CALLBACK DialogProc (HWND hwnd, 
                          UINT message, 
                          WPARAM wParam, 
                          LPARAM lParam)
{
    switch (message)
    {
		case WM_INITDIALOG:
			BringWindowToTop(hwnd);
			
			// add icon
			HICON hIcon;

			hIcon = (HICON)LoadImage(   TheInstance,
                           MAKEINTRESOURCE(IDI_ICON1),
                           IMAGE_ICON,
                           GetSystemMetrics(SM_CXICONSPACING),
                           GetSystemMetrics(SM_CYICONSPACING),
                           0);
			if(hIcon) {
				SendMessage(hwnd, WM_SETICON, ICON_BIG, (LPARAM)hIcon);
			}
			
			cancel_handle = GetDlgItem(hwnd,IDCANCEL);
			dialog_handle = hwnd;

			append_text(hwnd, LAUNCHER_VERSION_STRING);

			break;
        case WM_COMMAND:
            switch(LOWORD(wParam))
            {			
                case IDOK:
					debug = IsDlgButtonChecked(hwnd, IDC_CHECKBOX1);
					xpmod = IsDlgButtonChecked(hwnd, IDC_CHECKBOX2);
					lootmod = IsDlgButtonChecked(hwnd, IDC_CHECKBOX3);

					// disable launch button
					EnableWindow( GetDlgItem( hwnd, IDOK ), FALSE );

					// create thread that launches the game
					DWORD g_threadID;
					CreateThread(NULL, NULL, &launch_game, NULL, NULL, &g_threadID);				

					break;
                case IDCANCEL:
					OutputDebugString("In Cancel");
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

void append_text(HWND hwnd, char * buf) {
	HWND hEdit;
	int ndx;
	hEdit = GetDlgItem (hwnd, IDC_EDIT1);
	ndx = GetWindowTextLength (hEdit);
	SetFocus (hEdit);
		   
	SendMessage (hEdit, EM_SETSEL, (WPARAM)ndx, (LPARAM)ndx);
	SendMessage (hEdit, EM_REPLACESEL, 0, (LPARAM) ((LPSTR) buf));
}


DWORD WINAPI launch_game(LPVOID) {
	BOOL status = FALSE;
	STARTUPINFO StartupInfo;	
	PROCESS_INFORMATION ProcessInformation;
	ZeroMemory(&StartupInfo, sizeof(StartupInfo));
	StartupInfo.cb = sizeof(StartupInfo);
	ZeroMemory(&ProcessInformation, sizeof(ProcessInformation));

	char buffer[] = "Starting JABIA launcher\r\n";
	append_text(dialog_handle, buffer);

	status = CreateProcessA(NULL, LAUNCHER_NAME, NULL, NULL, FALSE, 0, NULL, NULL, &StartupInfo, &ProcessInformation);
	if(!status) {
		char buf [100];
		wsprintf (buf, "Error x%x", GetLastError());
		MessageBox (0, buf, "CreateProcessA", MB_ICONEXCLAMATION | MB_OK);
	}

	inject_dlls();
	return TRUE;
}

void inject_dlls() {
	unsigned long pid = 0;
	int loopcount = 0;
	char buf[100];

	if(IsWindowsNT()) {
		while(pid == 0 && loopcount < 100) {
			pid = GetTargetProcessIdFromProcname(EXE_NAME);
			if(pid == 0) {
				loopcount++;				
			} else {
				if(debug) {					
					Sleep(1000);
					append_text(dialog_handle, "Injecting character debugger\r\n");
					LoadDll(EXE_NAME, DEBUGGER_DLL_PATH);
				}
				if(xpmod) {
					Sleep(1000);
					append_text(dialog_handle, "Injecting xpmod\r\n");
					LoadDll(EXE_NAME, XPMOD_DLL_PATH);
				}
				if(lootmod) {
					Sleep(1000);
					append_text(dialog_handle, "Injecting drop loot mod\r\n");
					LoadDll(EXE_NAME, LOOTDROP_DLL_PATH);
				}
			}
			Sleep(1000);
		}
	} else {
		MessageBox(0, "Your system does not support this method", "Error!", 0);
	}
	if(loopcount == 100) {
		MessageBox(0, "Process not found", "Error!", 0);
	}
	// exit the mod launcher
	append_text(dialog_handle, "Exiting\r\n");

	ExitProcess(0);
}