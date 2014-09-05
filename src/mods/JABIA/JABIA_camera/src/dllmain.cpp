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

void setCamera(float, float, float, float);
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
bool defaultCamera = false;

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
		//if(defaultCamera) {
		//	SetCameraDefault();
		//	defaultCamera = false;
		//}
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
				/*
				// unloading is only for debugging
				OutputDebugString("Unloading JABIA_camera DLL");
				break;
				*/
			}
		Sleep(100);		
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
		camera_ptr->current_pitch_angle,
		camera_ptr->camera_min, 
		camera_ptr->camera_max, 
		camera_ptr->min_pitch_angle, 
		camera_ptr->max_pitch_angle_delta,
		camera_ptr->current_height);
	OutputDebugString(buf);
}

BOOL CALLBACK DialogProc (HWND hwnd, 
                          UINT message, 
                          WPARAM wParam, 
                          LPARAM lParam)
{
	HWND comboControl1;
	comboControl1=GetDlgItem(hwnd,IDOPTION);		
	char buf[100];

    switch (message)
    {
		case WM_INITDIALOG:
			BringWindowToTop(hwnd);			

			// add camera settings to drop down list
			SendMessageA(comboControl1,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)"Default"));
			SendMessageA(comboControl1,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)"GTA"));
			SendMessageA(comboControl1,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)"Close up"));
			SendMessageA(comboControl1,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)"Low and high"));		
			for(size_t i = 0; i < CAMERA_PARAMS_COUNT; i++) {		
				wsprintf(buf, "Custom%i", i);
				SendMessageA(comboControl1,CB_ADDSTRING,0,reinterpret_cast<LPARAM>((LPCTSTR)buf)); 		
			}										
			SendMessage(comboControl1, CB_SETCURSEL, camera_params.last_used, 0);
			fillDialog(hwnd);
			return TRUE;
        case WM_COMMAND:
            switch(LOWORD(wParam))
            {				
				case IDOPTION:
					switch(HIWORD(wParam))
					{
						case CBN_CLOSEUP:
							camera_params.last_used = SendMessage(comboControl1, CB_GETCURSEL, 0, 0);
							DestroyWindow(hwnd);
							PostQuitMessage(0);
							switch(camera_params.last_used) 
							{
								case 0:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
									SetCameraDefault();
									break;
								case 1:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
									SetCameraGTA();
									break;
								case 2:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
									SetCameraClose();
									break;
								case 3:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
									SetCameraLowHigh();
									break;
								case 4:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
									SetCameraCustom(0);
									break;
								case 5:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
									SetCameraCustom(1);
									break;
								case 6:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
									SetCameraCustom(2);
									break;
								case 7:
									EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
									SetCameraCustom(3);
									break;
							}
							break;
					}
					break;
				case IDC_SAVE:
					if(camera_params.last_used > 3) {
						int custom_selected = camera_params.last_used - 4;
						wsprintf(buf, "Saving to slot %i", custom_selected);
						OutputDebugString(buf);
						camera_params.camera_min[custom_selected] = camera_ptr->camera_min;
						camera_params.camera_max[custom_selected] = camera_ptr->camera_max;
						camera_params.min_pitch_angle[custom_selected] = camera_ptr->min_pitch_angle;
						camera_params.max_pitch_angle_delta[custom_selected] = camera_ptr->max_pitch_angle_delta;
						OutputDebugString("About to write xml");
						OutputDebugString(buf);
						DestroyWindow(hwnd);
						PostQuitMessage(0);
						save(PATH_TO_CAMERA_XML, camera_params);
						SetCameraCustom(camera_params.last_used - 4);
						OutputDebugString("SAVED");
					}
					break;
                case IDOK:
					float min;
					float max;
					float min_pitch_angle;
					float max_pitch_angle_delta;
					GetDlgItemText(hwnd, IDC_MIN_HEIGHT, buf, 100);
					min = (float)atof(buf);
					GetDlgItemText(hwnd, IDC_MAX_HEIGHT, buf, 100);
					max = (float)atof(buf);
					GetDlgItemText(hwnd, IDC_MIN_PITCH_ANGLE, buf, 100);
					min_pitch_angle = (float)atof(buf);
					GetDlgItemText(hwnd, IDC_PITCH_ANGLE_DELTA, buf, 100);
					max_pitch_angle_delta = (float)atof(buf);		
					DestroyWindow(hwnd);
					PostQuitMessage(0);
					if(max > min) {
						setCamera(min, max, min_pitch_angle, max_pitch_angle_delta);
					} else {
						wsprintf (buf, "Minimum height must be less than the maximum height.", GetLastError ());
						MessageBox (0, buf, "CreateDialog", MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
					}
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

	switch(camera_params.last_used) 
	{
		case 0:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
			break;
		case 1:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
			break;
		case 2:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
			break;
		case 3:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), FALSE);
			break;
		case 4:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
			break;
		case 5:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
			break;
		case 6:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
			break;
		case 7:
			EnableWindow( GetDlgItem( hwnd, IDC_SAVE ), TRUE);
			break;
	}
	char buf[100];
	sprintf_s(buf, "%.1f", camera_ptr->current_height, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_HEIGHT, buf);

	sprintf_s(buf, "%.1f", camera_ptr->current_pitch_angle, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_ANGLE, buf);

	sprintf_s(buf, "%.1f", camera_ptr->camera_min, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_MIN_HEIGHT, buf);

	sprintf_s(buf, "%.1f", camera_ptr->camera_max, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_MAX_HEIGHT, buf);

	sprintf_s(buf, "%.1f", camera_ptr->min_pitch_angle, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_MIN_PITCH_ANGLE, buf);

	sprintf_s(buf, "%.1f", camera_ptr->max_pitch_angle_delta, 4);
	//OutputDebugString(buf);
	SetDlgItemText(hwnd, IDC_PITCH_ANGLE_DELTA, buf);
}

void moveCameraToMin(float min) {
	char buf[100];
	sprintf(buf, "Moving to min: %.1f", min);
	OutputDebugString(buf);
	/* This function moves the camera to a height in small steps. If this is not done, the camera system breaks. */
	while(camera_ptr->current_height < min) {		
		camera_ptr->current_height += min/10.0f;		
		sprintf(buf, "At: %f", camera_ptr->current_height);
		OutputDebugString(buf);
		Sleep(100);
	}
}

void setCamera(float min, float max, float min_pitch_angle, float max_pitch_angle_delta) {
	moveCameraToMin(min);
	camera_ptr->camera_min = min;
	camera_ptr->camera_max = max;
	camera_ptr->min_pitch_angle = min_pitch_angle;
	camera_ptr->max_pitch_angle_delta = max_pitch_angle_delta;
	camera_ptr->current_height = max;
}

void SetCameraGTA(void) {
	float min = 50;
	moveCameraToMin(min);
	camera_ptr->camera_min = min;
	camera_ptr->camera_max = 520;
	camera_ptr->min_pitch_angle = 2.0;
	camera_ptr->max_pitch_angle_delta = 0;
	camera_ptr->current_height = camera_ptr->camera_max;
}

void SetCameraClose(void) {
	float min = 50;
	moveCameraToMin(min);
	camera_ptr->camera_min = min;
	camera_ptr->camera_max = 520;
	camera_ptr->min_pitch_angle = 1.5f;
	camera_ptr->max_pitch_angle_delta = 0.9f;
	camera_ptr->current_height = camera_ptr->camera_max;
}

void SetCameraLowHigh(void) {
	float min = 50;
	moveCameraToMin(min);
	camera_ptr->camera_min = min;
	camera_ptr->camera_max = 700.0;
	camera_ptr->min_pitch_angle = 0.8f;
	camera_ptr->max_pitch_angle_delta = 0.6f;
	camera_ptr->current_height = camera_ptr->camera_max;
}

void SetCameraCustom(int i) {
	camera_params.last_used = i + 4;
	moveCameraToMin(camera_params.camera_min[i]);
	camera_ptr->camera_min = camera_params.camera_min[i];
	camera_ptr->camera_max = camera_params.camera_max[i];
	camera_ptr->min_pitch_angle = camera_params.min_pitch_angle[i];
	camera_ptr->max_pitch_angle_delta = camera_params.max_pitch_angle_delta[i];
	camera_ptr->current_height = camera_ptr->camera_max;
}

void SetCameraDefault(void) {	
	JABIA_camera_parameters default_params;
	moveCameraToMin(camera_params.camera_min[0]);
	camera_ptr->camera_min = default_params.camera_min[0];
	camera_ptr->camera_max = default_params.camera_max[0];
	camera_ptr->min_pitch_angle = default_params.min_pitch_angle[0];
	camera_ptr->max_pitch_angle_delta = default_params.max_pitch_angle_delta[0];
	camera_ptr->current_pitch_angle = camera_ptr->min_pitch_angle;
	camera_ptr->current_height = camera_ptr->camera_max;
}
