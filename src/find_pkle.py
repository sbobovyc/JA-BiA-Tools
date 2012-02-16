# http://msdn.microsoft.com/en-us/library/windows/desktop/aa366907%28v=vs.85%29.aspx
# http://msdn.microsoft.com/en-us/library/windows/desktop/ee175820%28v=vs.85%29.aspx
# http://msdn.microsoft.com/en-us/library/windows/desktop/ee175819%28v=vs.85%29.aspx

import win32con
import winappdbg
from ctypes import *
from ctypes.wintypes import *
from win32com.client import GetObject   
import binascii
from matplotlib.mlab import ma

MEM_MIN = 0x00400000
MEM_MAX = 0x7FFFFFFF

def get_pid_by_name(exe_name):
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    len(processes)
#    print [process.Properties_('Name').Value for process in processes]
    p = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % exe_name)
#    print [prop.Name for prop in p[0].Properties_]
    pid = p[0].Properties_('ProcessId').Value # get our ProcessId
    
    return pid

def get_segment_size(pid, lpAddress):   
    hProcess =  windll.kernel32.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, int(pid))
    
    lpBuffer  = winappdbg.win32.MEMORY_BASIC_INFORMATION()
    dwLength  = sizeof(lpBuffer)     
    status = windll.kernel32.VirtualQueryEx(hProcess, lpAddress, byref(lpBuffer), dwLength)
    if status == 0:
        print "Error"
        return
#    print hex(lpBuffer.BaseAddress)
#    print hex(lpBuffer.RegionSize) 
    size = (lpBuffer.BaseAddress + lpBuffer.RegionSize) - lpAddress
#    print hex(size) 
    return size
    
def search_proc_memory(pid, search_data, match_limit=None, min=MEM_MIN, max=MEM_MAX):    
    hProcess = windll.kernel32.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, int(pid))
    
    if not hProcess: #Just in case error occurs.
                raise IOError, "Couldn't acquire a handle to PID: %s" % pid
#    print hProcess  
    
#    VIRTUAL_MEM = win32con.MEM_COMMIT | win32con.MEM_RESERVE
#    argument_address = windll.kernel32.VirtualAllocEx( hProcess, 0, len(str(search_data)), VIRTUAL_MEM, win32con.PAGE_READWRITE)
#    print hex(argument_address)
#    memory_addresses = map(int, range(argument_address)) #Program Memory Range.
#    print "First memory address", hex(memory_addresses[0])
    read_buffer = create_string_buffer(len(str(search_data)))
    count = c_ulong(0)
    
    match_address = []
    j = min
    while j < max:
        windll.kernel32.ReadProcessMemory(hProcess, j, read_buffer, len(search_data), byref(count))
        data = read_buffer.raw
        if data == search_data:
            match_address.append(j)
            print "Found %s at" % search_data, hex(j)
        j += 32 #word alignment
        if len(match_address) == match_limit:
            break        
        
    return match_address

def read_mem(pid, lpAddress, size):
    hProcess = windll.kernel32.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, int(pid))
    buffer = create_string_buffer(size)    
    count = c_ulong(0)
    status = windll.kernel32.ReadProcessMemory(hProcess, lpAddress, buffer, size, byref(count))
    
    return buffer.raw

if __name__ == "__main__":
    bin_name = "GameJaBiA.exe"
    print "Searching %s" % bin_name
    pid = get_pid_by_name(bin_name)
    print "Found process ID:", pid
    data = "PKLE"
    match_address = search_proc_memory(pid, data, match_limit=2)
    size_list = []
    for address in match_address:
        size_list.append(get_segment_size(pid, address))
    f = open("configs_win32.pak", "wb")
    data = read_mem(pid, match_address[0], size_list[0])    
    f.write(data)    
    f.close()
    
    f = open("interface_win32.pak", "wb")
    data = read_mem(pid, match_address[1], size_list[1])    
    f.write(data)    
    f.close()
    
    
