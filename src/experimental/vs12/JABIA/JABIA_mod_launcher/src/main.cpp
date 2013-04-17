#include <windows.h>
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/filesystem.hpp>
#include <iostream> 
#include <fstream> 

#include "mod_launcher.h"
#include "libutils.h"
#include "resource.h"



BOOL CALLBACK DialogProc (HWND hwnd, 
                          UINT message, 
                          WPARAM wParam, 
                          LPARAM lParam);

void append_text(HWND hwnd, char * buf);
DWORD WINAPI launch_game(LPVOID);
void inject_dlls();

JABIA_mod_launcher_parameters params;

HINSTANCE TheInstance = 0;
UINT debug = 0;
UINT xpmod = 0;
UINT lootmod = 0;
UINT cameramod = 0;
UINT pathmod = 0;

HWND cancel_handle;
HWND dialog_handle;


void save(JABIA_mod_launcher_parameters * dr) 
{ 	
	boost::filesystem::path working_dir = boost::filesystem::current_path();
	boost::filesystem::path modpath(PATH_TO_MOD_LAUNCHER_XML);
	boost::filesystem::path fullpath = working_dir / modpath;
	OutputDebugString(fullpath.string().c_str());
	std::ofstream file(fullpath.string()); 	
	boost::archive::xml_oarchive oa(file); 
	OutputDebugString("Done saving xml");
	oa & BOOST_SERIALIZATION_NVP(dr); 
} 

JABIA_mod_launcher_parameters load() 
{ 
	JABIA_mod_launcher_parameters param;
	boost::filesystem::path working_dir = boost::filesystem::current_path();
	boost::filesystem::path modpath(PATH_TO_MOD_LAUNCHER_XML);
	boost::filesystem::path fullpath = working_dir / modpath;
	if ( !(boost::filesystem::exists(fullpath) && boost::filesystem::is_regular_file(fullpath)) )    // does p actually exist and is p a regular file?   
	{
		save(&param);
	}
	OutputDebugString(fullpath.string().c_str());
	std::ifstream file(fullpath.string()); 
	boost::archive::xml_iarchive ia(file);   
	
	ia >> BOOST_SERIALIZATION_NVP(param); 
	OutputDebugString("Done loading xml");
	return param;
}


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

			// initialize checkboxes			
			params = load();
			if(params.debug_mod) {		
				SendDlgItemMessage(hwnd, IDC_CHECKBOX1, BM_SETCHECK, BST_CHECKED, 0);
			}
			if(params.xp_mod) {
				SendDlgItemMessage(hwnd, IDC_CHECKBOX2, BM_SETCHECK, BST_CHECKED, 0);
			}
			if(params.loot_drop_mod) {
				SendDlgItemMessage(hwnd, IDC_CHECKBOX3, BM_SETCHECK, BST_CHECKED, 0);
			}
			if(params.camera_mod) {
				SendDlgItemMessage(hwnd, IDC_CHECKBOX4, BM_SETCHECK, BST_CHECKED, 0);
			}

			//if(params.path_mod) {
			//	SendDlgItemMessage(hwnd, IDC_CHECKBOX5, BM_SETCHECK, BST_CHECKED, 0);
			//}

			cancel_handle = GetDlgItem(hwnd,IDCANCEL);
			dialog_handle = hwnd;

			append_text(hwnd, LAUNCHER_VERSION_STRING);
			append_text(hwnd, MOTD);

			break;
        case WM_COMMAND:
            switch(LOWORD(wParam))
            {			
                case IDOK:
					debug = IsDlgButtonChecked(hwnd, IDC_CHECKBOX1);
					xpmod = IsDlgButtonChecked(hwnd, IDC_CHECKBOX2);
					lootmod = IsDlgButtonChecked(hwnd, IDC_CHECKBOX3);
					cameramod = IsDlgButtonChecked(hwnd, IDC_CHECKBOX4);
					pathmod = IsDlgButtonChecked(hwnd, IDC_CHECKBOX5);

					// save params
					params.debug_mod = debug;
					params.xp_mod = xpmod;
					params.loot_drop_mod = lootmod;
					params.camera_mod = cameramod;
					params.path_mod = pathmod;
					save(&params);

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

	append_text(dialog_handle, "Starting JABIA launcher\r\n");

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

	if(IsWindowsNT()) {
		while(pid == 0 && loopcount < 100) {
			pid = GetTargetProcessIdFromProcname(EXE_NAME);
			if(pid == 0) {
				loopcount++;				
			} else {
				if(pathmod) {					
					//Sleep(1000);
					DebugSetProcessKillOnExit(FALSE);
					DebugActiveProcess(pid);
					LoadDll(EXE_NAME, PATHMOD_DLL_PATH);
					append_text(dialog_handle, "Injecting path mod\r\n");
					DebugActiveProcessStop(pid);

				}
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
				if(cameramod) {
					Sleep(1000);
					append_text(dialog_handle, "Injecting camera mod\r\n");
					LoadDll(EXE_NAME, CAMERA_DLL_PATH);
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