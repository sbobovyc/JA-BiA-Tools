"""
Created on February 17, 2012

@author: sbobovyc
"""
"""   
    Copyright (C) 2012 Stanislav Bobovych

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
import codecs
import yaml
import binascii           
from collections import OrderedDict

DEG_entry_start = 0x0000

class DEG_entry:
    def __init__(self, name, color_file, normal_file, coords, mystery):
        self.name = name
        self.color_file = color_file
        self.normal_file = normal_file
        self.coords = coords    # ((ulx,uly),(width,height))
        self.mystery = mystery
    
    def get_name_lenth(self):
        return len(self.name)
    
    def get_c_length(self):
        return len(self.color_file)
    
    def get_n_length(self):
        return len(self.normal_file)
    
    def has_normals(self):
        if self.get_n_length() > 0:
            return True
        else:            
            return False
    def get_packed_data(self):
        data_buffer = struct.pack("<I%isI%isI%is" % (self.get_name_lenth(), self.get_c_length(), self.get_n_length()),
                             self.get_name_lenth(), self.name, 
                             self.get_c_length(), self.color_file, 
                             self.get_n_length(), self.normal_file)
        data_buffer += struct.pack("<IIII", self.coords[0][0], self.coords[0][1],
                              self.coords[1][0],self.coords[1][1])
        data_buffer += struct.pack("<II", self.mystery[0], self.mystery[1])
        binascii.hexlify(data_buffer)
        return data_buffer
    
    def __str__(self):
        string = "%s = %s and %s,\n(ulx,uly)=%s, (width,height)=%s, mystery=(%s,%s)\n" % ( 
            self.name, self.color_file, self.normal_file, self.coords[0], self.coords[1], 
            hex(self.mystery[0]), hex(self.mystery[1]))
        return string
        
class DEG_data:
    def __init__(self):
        self.entry_list = []
    
    def get_num_entries(self):
        return len(self.entry_list)
    
    def unpack(self, file_pointer, peek=False, verbose=False):    
        num_entries, = struct.unpack("<I", file_pointer.read(4))
        
        if peek:
            print "Peek not implemented"
            return 

        if verbose:
            print "Number of entries ", num_entries
        
        for i in range(0, num_entries):
            entry_separator,length = struct.unpack("<II", file_pointer.read(8))
            variable_name = file_pointer.read(length)
            c_file_length, = struct.unpack("<I", file_pointer.read(4))
            c_file = file_pointer.read(c_file_length)
            n_file_length, = struct.unpack("<I", file_pointer.read(4))
            n_file = file_pointer.read(n_file_length)
            ulx,uly,width,height = struct.unpack("<IIII", file_pointer.read(16))
            unknown1,unknown2 = struct.unpack("<II", file_pointer.read(8))
            # eat "0x01" or "0x00" flags (0x01 means has normals, 0x00 means doesn't)
            file_pointer.read(1)
            entry = DEG_entry(variable_name, c_file, n_file, ((ulx,uly),(width,height)), (unknown1, unknown2))
            if verbose:
                print entry
            self.entry_list.append(entry)
            

                    
    def get_packed_data(self):
        #1. get number of entries
        num_entries = self.get_num_entries()     
        header_buffer = struct.pack("<I", num_entries)
        
        #2. pack each entry 
        data_buffer = ""
        for entry in self.entry_list:                                                   
            data_buffer += struct.pack("<I", DEG_entry_start)
            data_buffer += entry.get_packed_data()
            if entry.has_normals():
                data_buffer += struct.pack("<B", 0x01)
            else:
                data_buffer += struct.pack("<B", 0x00)
            
        #3. concatenate the header and data   
        return (header_buffer + data_buffer)            

    def __repr__(self):
        return "%s(name=%r, languages=%r)" % (
             self.__class__.__name__, self.language_list)
            
class DEG_file:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.data = None
        if self.filepath != None:
            self.open(filepath)
    
    def open(self, filepath=None, peek=False):
        if filepath == None and self.filepath == None:
            print "File path is empty"
            return
        if self.filepath == None:
            self.filepath = filepath
        
        self.data = DEG_data()
        
    def get_data(self):
        return self.data
    
    def pack(self, verbose=False):
        if self.filepath == None:
            print "File path is empty. Open the file with a valid path."
            return
        
        print "Creating %s" % self.filepath
         
        with open(self.filepath, "wb") as f:            
            data = self.data.get_packed_data()
            f.write(data)

    def unpack(self, peek=False, verbose=False):
        with open(self.filepath, "rb") as f:            
            self.data.unpack(f, peek=peek, verbose=verbose)
                        
    def dump2yaml(self, dest_filepath=os.getcwd()): 
        file_name = os.path.join(dest_filepath, os.path.splitext(os.path.basename(self.filepath))[0])        

        full_path = file_name + ".deg.txt" 
        print "Creating %s" % full_path
        yaml.add_representer(unicode, lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:str', value))
        with codecs.open(full_path, "wb", "utf-16") as f:                                            
                yaml.dump(self.data, f, allow_unicode=True, encoding="utf-16")                                             
    
    def yaml2deg(self, yaml_file):
        filepath = os.path.abspath(yaml_file)
        with codecs.open(filepath, "r", "utf-16") as f:
            self.data = yaml.load(f)                   
        self.pack()

if __name__ == "__main__":    
#    dF = DEG_file("C:\Users\sbobovyc\Desktop\\bia\\1.06\\bin_win32\\configs\main.deg")
#    dF.open()        
#    dF.unpack(verbose=False)    
#    dF.dump2yaml()

    # packing
#    dF = DEG_file("main.deg")
#    dF.open()
#    dF.yaml2deg("main.deg.txt")
    pass