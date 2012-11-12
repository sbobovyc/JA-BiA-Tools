#ifndef JABIA_DEBUG
#define JABIA_DEBUG


#ifdef JABIA_EXPORTS
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __declspec(dllimport)
#endif

#define FULL
#define WITH_XP_MOD
//#define DEMO

#ifdef DEMO
#define CHARACTER_CONST_OFFSET 0x112450
#define CHARACTER_CONST_RETN_OFFSET 0x210
static ProcessName = "GameDemo.exe";
#else
#define CHARACTER_CONST_OFFSET 0x132880
#define CHARACTER_CONST_RETN_OFFSET 0x2D8
static char ProcessName[] = "GameJABiA.exe";
#endif


// modding exp function
#ifdef FULL
#define UPDATE_EXP_OFFSET 0x14C470
#endif


typedef void * (_stdcall *CharacterConstRetrunPtr)();
typedef void * (_stdcall *UpdateCharacterExpPtr)();

#ifdef __cplusplus
extern "C" {
#endif 

EXPORT BOOL CALLBACK DialogProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
#ifdef __cplusplus
}
#endif


DWORD WINAPI MyThread(LPVOID);
void* myCharacterConstRetrun();
void recordCharacters(void* instance);


void dump_current_character(HWND hwnd, uint32_t ptr);
BOOL dump_all_characters(HWND hwnd);
void fillDialog(HWND hwnd, uint32_t ptr);
void setCharacter(HWND hwnd, uint32_t ptr);


#endif /* JABIA_DEBUG */