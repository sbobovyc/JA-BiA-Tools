"""
Created on June 18, 2014

@author: sbobovyc
"""
"""   
    Copyright (C) 2014 Stanislav Bobovych

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import struct 
import os
import sys
import cStringIO
import base64
import timeit
from multiprocessing.dummy import Pool
from multiprocessing import Manager
from itertools import repeat
from Crypto.Cipher import AES

PAK_SIGNATURE = 0x504B4C4501000000
AES_KEY_CIPHERED = {"JABIA_JAC" : "eFd1cnozbFBFVEVSMjUzeg==",
                    "DLC5" : "MTNIYW5zZWxuMTBFbGYlIQ==",
                    "DLC6" : "MTNIYW5zZWxuMTBFbGYlIQ=="}
PAK_filesize = 0 # in bytes
PAK_bytes_unpacked = 0

def unpack_helper(args):
    print "in unpack helper"
    data,q = args
    data.unpack()
    q.put(0)
    
class PAK_data:
    def __init_(self, dir):  
        self.file_pointer = None
        self.file_name_length = None    # includes '\0' 
        self.file_size = None   # in bytes
        self.file_offset = None # in bytes
        self.file_crc = None    # unknown crc
        self.file_name = None   # includes '\0'      
        self.path = None          
        self.data = None
    
    def parse(self, dir, file_pointer, dest_filepath, verbose=False):
        self.file_pointer = file_pointer
        self.file_directory = dir
        self.file_name_length, self.file_size, self.file_offset, self.file_crc = struct.unpack('<IQQQ', file_pointer.read(28))
        
        self.file_name = file_pointer.read(self.file_name_length)
        # strip the null
        self.file_name = self.file_name.replace("\00", "").strip()
        self.path = os.path.join(dest_filepath, self.file_directory)

        
        if verbose:
            print "File name: %s" % os.path.join(self.file_directory,self.file_name)
            print "File offset: %s" % hex(self.file_offset).rstrip('L')
            print "File Size: %s bytes" % hex(self.file_size).rstrip('L')
            print "File unknown crc: %s" % hex(self.file_crc).rstrip('L')
            #print "File Adler32 %s" % hex(zlib.adler32(self.data) & 0xffffffff )
            #print "File CRC32 %s" % hex(zlib.crc32(self.data) & 0xffffffff )
            print 

    def unpack(self):
        print "in unpack"
        self.file_pointer.seek(self.file_offset)
        self.data = self.file_pointer.read(self.file_size)
        
        with open(os.path.join(self.path, self.file_name), "wb") as f:
            f.write(self.data)
            
        return self.file_size
        
        
class PAK_dir:
    def __init__(self):
        self.dir_index = None           # start index is 1  
        self.dir_name_length = None     
        self.dir_number_files = None  
        self.dir_name = None
        self.file_list = []        
            
    
    def unpack(self, file_pointer, dest_filepath, verbose=False):        
        self.dir_index, self.dir_name_length, self.dir_number_files = struct.unpack('<IIQ', file_pointer.read(16))
        self.dir_name = file_pointer.read(self.dir_name_length)
        
        # strip the null and remove leading slash
        self.dir_name = self.dir_name.replace("\00", "").strip()[1:]
        if self.dir_number_files != 0:
            for i in range(0, self.dir_number_files):
                pF = PAK_data()
                pF.parse(self.dir_name, file_pointer, dest_filepath, verbose)
                self.file_list.append(pF)
        else:            
            return 
        
class PAK_header:
    def __init__(self):
        self.magic = None
        self.descriptor_size = None # in bytes
        self.num_dirs = None
        self.dir_list = []
    
    def unpack(self, file_pointer, dest_filepath, verbose=False):    
        self.magic, = struct.unpack(">Q", file_pointer.read(8))
        
        if self.magic != PAK_SIGNATURE:            
            # something bad happened
            print "File is not BiA pak"
            return
        
        self.descriptor_size, self.num_dirs = struct.unpack("<QQ", file_pointer.read(16))     
        global PAK_filesize   
        PAK_filesize -= self.descriptor_size
        
        if verbose:
            print "Descriptor size: %i bytes" % self.descriptor_size
            print "Content size: %i bytes" % PAK_filesize
            print "Number of directories in archive: %i" % self.num_dirs
            
        for i in range(0, self.num_dirs):
            pD = PAK_dir()
            pD.unpack(file_pointer, dest_filepath, verbose)
            self.dir_list.append(pD)

class PAK_file:
    def __init__(self, filepath=None, encrypted=False):
        self.filepath = filepath
        self.header = None     
        self.file_pointer = None
        self.encrypted = encrypted
        
        if self.filepath != None:
            global PAK_filesize
            PAK_filesize = os.path.getsize(filepath)
            self.open(filepath=self.filepath, encrypted=self.encrypted)
    
    def open(self, filepath=None, encrypted=False, peek=False):
        if filepath == None and self.filepath == None:
            print "File path is empty"
            return
        if self.filepath == None:
            self.filepath = filepath
        
        if encrypted:
            with open(self.filepath, "rb") as f:
                _, real_size, block_size = struct.unpack("<HII", f.read(0xa))
            
                buf = f.read(block_size)
    
                CIPHER = ""
                if os.path.splitext(os.path.basename(self.filepath))[0] == "dlc5_dlc5_configs_win32.pak":
                    CIPHER = "DLC5"
                elif os.path.splitext(os.path.basename(self.filepath))[0] == "dlc6_dlc6_configs_win32.pak":
                    CIPHER = "DLC6"                
                else:
                    CIPHER = "JABIA_JAC"
                
                aes = AES.new(base64.b64decode(AES_KEY_CIPHERED[CIPHER]), AES.MODE_ECB)
                self.file_pointer = cStringIO.StringIO(aes.decrypt(buf)[:real_size])
        else:
            self.file_pointer = open(self.filepath, "rb")
            
        self.header = PAK_header()

    #TODO add destructor that closes file handle
    def dump(self, dest_filepath=os.getcwd(), parallel=False,verbose=False):      
        if self.file_pointer != None:
            self.header.unpack(self.file_pointer, dest_filepath, verbose)
            for dir in self.header.dir_list:
                if not os.path.exists(dir.dir_name):
                    os.makedirs(dir.dir_name)
            if parallel:
                master_file_list = []
                for dir in self.header.dir_list:
                    master_file_list.extend(dir.file_list)
                p = Pool()
                m = Manager()
                q = m.Queue()
                args = [master_file_list, repeat(q)]
                result = p.map_async(PAK_data.unpack, master_file_list)
                #result = p.map_async(unpack_helper, args)
                p.close()
                p.join()
                """
                # monitor loop
                while True:
                    if result.ready():
                        break
                    else:
                        size = q.qsize()
                        print(size)
                """
            else:
                for dir in self.header.dir_list:
                    for data in dir.file_list:                    
                        global PAK_bytes_unpacked
                        PAK_bytes_unpacked += float(data.unpack())        
                        sys.stdout.write("%.0f%%\r" % (PAK_bytes_unpacked * 100/ PAK_filesize) )
         
                
def test():
    pF = PAK_file("C:\\Program Files (x86)\\Steam\\steamapps\\common\\JABIA\\data6_win32.pak") # 15 mb
    pF = PAK_file("C:\\Program Files (x86)\\Steam\\steamapps\\common\\JABIA\\data5_win32.pak") # 93 mb
    #pF = PAK_file("C:\\Program Files (x86)\\Steam\\steamapps\\common\\JABIA\\data_win32.pak") # 600 mb
    #pF = PAK_file("C:\\Program Files (x86)\\Steam\\steamapps\\common\\JABIA\\configs_win32.pak.crypt")
    pF.open(encrypted=False)    
    pF.dump(parallel=True, verbose=False)
    
if __name__ == "__main__":        
    print timeit.timeit(test, number=1)
