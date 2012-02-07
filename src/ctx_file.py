"""
Created on February 6, 2012

@author: sbobovyc
"""
"""   
    Copyright (C) 2011 Stanislav Bobovych

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
from collections import OrderedDict

class CTX_language:
    def __init__(self, description_string, data_offset):
        self.description_string = description_string
        self.data_offset = data_offset
        self.data_dictionary = OrderedDict()   # {text id : data} mapping
    
    def add_data(self, id, text):
        self.data_dictionary[id] = text
        
    def get_data(self):
        return self.data_dictionary
    
    def __str__(self):
        return "Language: %s, data offset: %s bytes" % (self.description_string, hex(self.data_offset).rstrip('L'))
        
class CTX_header:
    def __init__(self):
        self.num_items = None
        self.num_languages = None
        self.data_offset = 0 
        self.last_item_id = 0
        self.language_list = []
    
    def get_languages(self):
        return self.language_list
    
    def unpack(self, file_pointer, peek=False, verbose=False):    
        self.num_items,self.last_item_id,self.num_languages = struct.unpack("<III", file_pointer.read(12))
        
        for i in range(0, self.num_languages):
            desc_length, = struct.unpack("<I", file_pointer.read(4))
            description_string = file_pointer.read(desc_length)
            data_offset, = struct.unpack("<I", file_pointer.read(4))
            self.language_list.append( CTX_language(description_string, data_offset))
        
        self.data_offset = file_pointer.tell()
        
        if peek or verbose:
            print "Number of itmes: %s" % self.num_items
            print "Last item id: %i" % self.last_item_id
            print "Number of languages in file: %i" % self.num_languages
            print "Data offset: %s" % hex(self.data_offset).rstrip('L')
            for each in self.language_list:
                print each
        if peek:
            return 
        
        for language in self.language_list:
            file_pointer.seek(self.data_offset + language.data_offset)
            for i in range(0, self.num_items):
                id,item_length = struct.unpack("<II", file_pointer.read(8))
                item_length = 2 * item_length               # multiply by two to compensate for the "\0"
                item_raw_text = file_pointer.read(item_length)
                # swap bytes 
                #item_little_endian_text = struct.unpack("<%iH" %(item_length/2), item_raw_text)
                #swaped_text = struct.pack(">%iH" %(item_length/2), *item_little_endian_text)
                #print swaped_text
                item_text = unicode(item_raw_text, "utf-16")
                #item_text = item_text.replace("\00", "")
                language.add_data(id, item_text)
                if verbose:
                    print id,item_text                
            
class CTX_file:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.header = None
        if self.filepath != None:
            self.open(filepath)
    
    def open(self, filepath=None, peek=False):
        if filepath == None and self.filepath == None:
            print "File path is empty"
            return
        if self.filepath == None:
            self.filepath = filepath
        
        self.header = CTX_header()

    def unpack(self, verbose=False):
        with open(self.filepath, "rb") as f:            
            self.header.unpack(f, verbose=verbose)

    def dump2text(self):
        languages = self.header.get_languages()
        for language in languages:
            data = language.get_data()
            print "%s {" % language.description_string
            for key, value in data.items():
                print "\t", key, value
            print "}"

    def dump2file(self, dest_filepath=os.getcwd()): 
        file_name = os.path.join(dest_filepath, os.path.splitext(os.path.basename(self.filepath))[0])
        full_path = file_name + ".txt"
        print "Creating %s" % full_path 

        f = codecs.open(full_path, "w", "utf-16") 
        languages = self.header.get_languages()

        for language in languages:
            data = language.get_data()
            f.write("\n%s {\n" % language.description_string)
            for key, value in data.items():
                f.write("\t%i %s\n" % (key, value))
            f.write("}")
        f.close()

    def pack(self, dest_filepath=os.getcwd(), verbose=False):
        print "Not implemented yet."
#        with open(self.filepath, "rb") as f:            
#            self.header.unpack(f, dest_filepath, verbose)

if __name__ == "__main__":
    cF = CTX_file("C:\Users\sbobovyc\Desktop\\test\\bin_win32\interface\equipment.ctx")
    #cF = CTX_file("/media/Acer/Users/sbobovyc/Desktop/test/bin_win32/interface/equipment.ctx")
    cF.open()        
    cF.unpack(verbose=False)
    cF.dump2file(".")
                
