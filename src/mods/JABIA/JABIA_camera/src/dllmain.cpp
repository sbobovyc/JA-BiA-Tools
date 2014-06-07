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
#include <stdint.h>
#include <stdio.h>
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/filesystem.hpp>
#include <iostream> 
#include <fstream> 

#include "game_version.h"
#include "camera.h"
#include "camera_mod.h"
#include "detours.h"
#include "resource.h"

#pragma comment(lib,"detours.lib")

DWORD WINAPI MyThread(LPVOID);
int _stdcall myCameraCallback(float, int);
void print_camera_info();
BOOL CALLBACK DialogProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
void fillDialog(HWND hwnd);

void setCamera(HWND hwnd);
void SetCameraGTA(void);
void SetCameraClose(void);
void SetCameraLowHigh(void);	
void SetCameraCustom(int);
void SetCameraDefault(void);


typedef int (_stdcall *CameraCallbackPtr)(float, int);

CameraCallbackPtr CameraCallback;
HMODULE game_handle; // address of GameJABiA.exe
DWORD g_threadID;
HMODULE g_hModule;
Camera * camera_ptr;
JABIA_camera_parameters camera_params;


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

DWORD WINAPI MyThread(LPVOID)
{
	
	char buf [100];
	// find base address of GameDemo.exe in memory
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, ProcessName, &game_handle);
	// find address of camera callback function
	CameraCallback = (CameraCallbackPtr)((uint32_t)game_handle+CAMERA_CALLBACK_OFFSET);
	wsprintf (buf, "Address of CameraCallback 0x%x", CameraCallback);
	OutputDebugString(buf);


	// start detour camera callback
	DetourRestoreAfterWith();
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)CameraCallback, myCameraCallback);
	DetourTransactionCommit();
	// end detour print xp function

	// sleep so that callback has a chance to execute
	while(camera_ptr == NULL) {
		Sleep(1000);
	}

	// restore camera callback
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
    DetourDetach(&(PVOID&)CameraCallback, myCameraCallback);
    DetourTransactionCommit();


	print_camera_info();

	// load custom camera settings from xml and set camera 
	load(PATH_TO_CAMERA_XML, camera_params);
	SetCameraCustom(camera_params.last_used);

	while(true)
	{
		if(GetAsyncKeyState(VK_ADD) & 1)
		{
				HWND hDialog = 0;
				
				hDialog = CreateDialog (g_hModule,
							MAKEINTRESOURCE (IDD_DIALOG1),
							0,
							DialogProc);

				//fillDialog(hDialog);
				
				if (!hDialog)
				{
					char buf [100];
					wsprintf (buf, "Error x%x", GetLastError ());
					MessageBox (0, buf, "CreateDialog", MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
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
			} else if(GetAsyncKeyState(VK_F8) &1) {
				OutputDebugString("Unloading JABIA_camera DLL");
				break;
			}
		Sleep(100);		
		//print_camera_info();
	}
	
	FreeLibraryAndExitThread(g_hModule, 0);
    return 0;
}

int _stdcall myCameraCallback(float u1, int u2) {
	__asm {
		mov camera_ptr, ecx 
	};
	return CameraCallback(u1, u2);
}

void print_camera_info() {
	char buf[1024];
	wsprintf(buf, "Camera at 0x%X", camera_ptr);
	OutputDebugString(buf);
	sprintf(buf, "Camera angle: %f\nCamera min: %f\nCamera max: %f\nCamera min angle: %f\nCamera max angle delta: %f\nCamera height: %f", 
		camera_ptr->current_angle,
		camera_ptr->camera_min, 
		camera_ptr->camera_max, 
		camera_ptr->min_angle, 
		camera_ptr->max_angle_delta,
		camera_ptr->current_height);
	OutputDebugString(buf);
}

BOOL CALLBACK DialogProc (HWND hwnd, 
                          UINT message, 
                          WPARAM wParam, 
                          LPARAM lParam)
{
	HMENU hMenu;
	int selected_custom = camera_params.last_used;
	char buf[100];

    switch (message)
    {
		case WM_INITDIALOG:
			BringWindowToTop(hwnd);
			
			// add menu
			hMenu = LoadMenu(g_hModule, MAKEINTRESOURCE(IDR_MENU1));
			SetMenu(hwnd,hMenu);

			wsprintf(buf, "Cst%i", selected_custom);
			SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);
			SetCameraCustom(selected_custom);
			fillDialog(hwnd);

			// add icon
			//HICON hIcon;

			//hIcon = (HICON)LoadImage(   g_hModule,
   //                        MAKEINTRESOURCE(IDI_ICON1),
   //                        IMAGE_ICON,
   //                        GetSystemMetrics(SM_CXSMICON),
   //                        GetSystemMetrics(SM_CYSMICON),
   //                        0);
			//if(hIcon) {
			//	SendMessage(hwnd, WM_SETICON, ICON_SMALL, (LPARAM)hIcon);
			//}
			return TRUE;
        case WM_COMMAND:
            switch(LOWORD(wParam))
            {				
				case IDM_GTA:
					wsprintf(buf, "GTA");
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);
					SetCameraGTA();
					fillDialog(hwnd);
					OutputDebugString("GTA");
					break;
				case IDM_CLOSE_UP:
					wsprintf(buf, "CU");
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);
					SetCameraClose();
					fillDialog(hwnd);
					OutputDebugString("CU");
					break;
				case IDM_LOW_AND_HIGH:
					wsprintf(buf, "L&H");
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);
					SetCameraLowHigh();
					OutputDebugString("L&H");
					break;
				case IDM_CUSTOM0:
					selected_custom = 0;
					wsprintf(buf, "Cst%i", selected_custom);
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);					
					SetCameraCustom(0);
					fillDialog(hwnd);
					OutputDebugString("CUSTOM0");
					break;
				case IDM_CUSTOM1:
					selected_custom = 1;
					wsprintf(buf, "Cst%i", selected_custom);
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);					
					SetCameraCustom(1);
					fillDialog(hwnd);
					OutputDebugString("CUSTOM1");
					break;
				case IDM_CUSTOM2:
					selected_custom = 2;
					wsprintf(buf, "Cst%i", selected_custom);
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);
					SetCameraCustom(2);
					fillDialog(hwnd);
					OutputDebugString("CUSTOM2");
					break;
				case IDM_CUSTOM3:
					selected_custom = 3;
					wsprintf(buf, "Cst%i", selected_custom);
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);		
					SetCameraCustom(3);
					fillDialog(hwnd);
					OutputDebugString("CUSTOM3");
					break;
				case IDM_DEFAULT:
					wsprintf(buf, "Def");
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);
					SetCameraDefault();
					fillDialog(hwnd);
					OutputDebugString("DEFAULT");
					break;
				case IDC_SAVE:
					wsprintf(buf, "Cst%i", selected_custom);
					SetDlgItemText(hwnd, IDC_SELECTED_STATE, buf);
					camera_params.camera_min[selected_custom] = camera_ptr->camera_min;
					camera_params.camera_max[selected_custom] = camera_ptr->camera_max;
					camera_params.min_angle[selected_custom] = camera_ptr->min_angle;
					camera_params.max_angle_delta[selected_custom] = camera_ptr->max_angle_delta;
					save(PATH_TO_CAMERA_XML, camera_params);
					SetCameraCustom(selected_custom);
					fillDialog(hwnd);
					OutputDebugString("SAVED");
					break;
                case IDOK:
					setCamera(hwnd);
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

void fillDialog(HWND hwnd) {
	char buf[100];
	sprintf_s(buf, "%.1f", camera_ptr->current_height, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_HEIGHT, buf);

	sprintf_s(buf, "%.1f", camera_ptr->current_angle, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_ANGLE, buf);

	sprintf_s(buf, "%.1f", camera_ptr->camera_min, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_MIN_HEIGHT, buf);

	sprintf_s(buf, "%.1f", camera_ptr->camera_max, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_MAX_HEIGHT, buf);

	sprintf_s(buf, "%.1f", camera_ptr->min_angle, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_MIN_ANGLE, buf);

	sprintf_s(buf, "%.1f", camera_ptr->max_angle_delta, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_ANGLE_DELTA, buf);
}

void setCamera(HWND hwnd) {
	char buf[100];
	float min;
	float max;
	float min_angle;
	float max_angle_delta;

	GetDlgItemText(hwnd, IDC_MIN_HEIGHT, buf, 100);
	min = (float)atof(buf);
	camera_ptr->camera_min = min;

	GetDlgItemText(hwnd, IDC_MAX_HEIGHT, buf, 100);
	max = (float)atof(buf);
	camera_ptr->camera_max = max;

	GetDlgItemText(hwnd, IDC_MIN_ANGLE, buf, 100);
	min_angle = (float)atof(buf);
	camera_ptr->min_angle = min_angle;

	GetDlgItemText(hwnd, IDC_ANGLE_DELTA, buf, 100);
	max_angle_delta = (float)atof(buf);
	camera_ptr->max_angle_delta = max_angle_delta;
}

void SetCameraGTA(void) {
	camera_ptr->camera_min = 50;
	camera_ptr->camera_max = 520;
	camera_ptr->min_angle = 2.0;
	camera_ptr->max_angle_delta = 0;
}

void SetCameraClose(void) {
	camera_ptr->camera_min = 50;
	camera_ptr->camera_max = 520;
	camera_ptr->min_angle = 1.5;
	camera_ptr->max_angle_delta = 0.9;
}

void SetCameraLowHigh(void) {
	camera_ptr->camera_min = 50.0;
	camera_ptr->camera_max = 700.0;
	camera_ptr->min_angle = 0.8;
	camera_ptr->max_angle_delta = 0.6;
}

void SetCameraCustom(int i) {
	camera_params.last_used = i;
	camera_ptr->camera_min = camera_params.camera_min[i];
	camera_ptr->camera_max = camera_params.camera_max[i];
	camera_ptr->min_angle = camera_params.min_angle[i];
	camera_ptr->max_angle_delta = camera_params.max_angle_delta[i];
}

void SetCameraDefault(void) {
	JABIA_camera_parameters default_params;
	camera_ptr->camera_min = default_params.camera_min[0];
	camera_ptr->camera_max = default_params.camera_max[0];
	camera_ptr->min_angle = default_params.min_angle[0];
	camera_ptr->max_angle_delta = default_params.max_angle_delta[0];
	camera_ptr->current_angle = camera_ptr->min_angle;
	camera_ptr->current_height = camera_ptr->camera_max;
}
