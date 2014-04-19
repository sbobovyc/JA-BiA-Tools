/*
@author: sbobovyc
*/

/*
Copyright (C) 2014 Stanislav Bobovych

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
#include "assembly_opcodes.h"

void returnHook(void * returnAddress, void * hookAddress, BYTE * savedReturn) {
		DWORD oldProtection;
		VirtualProtect(returnAddress, 6, PAGE_EXECUTE_READWRITE, &oldProtection);
		DWORD JMPSize = ((DWORD)hookAddress - (DWORD)returnAddress - 5);		
		BYTE JMP_hook[6] = {JMP, NOP, NOP, NOP, NOP, NOP}; 
		memcpy((void *)savedReturn, (void *)returnAddress, 6); // save retn
		memcpy(&JMP_hook[1], &JMPSize, 4);
		//wsprintf(buf, "JMP: %x%x%x%x%x", JMP[0], JMP[1], JMP[2], JMP[3], JMP[4], JMP[5]);
		//OutputDebugString(debugStrBuf);
		// overwrite retn with JMP_hook
		memcpy((void *)returnAddress, (void *)JMP_hook, 6);
		// restore protection
		VirtualProtect((LPVOID)returnAddress, 6, oldProtection, NULL);
}