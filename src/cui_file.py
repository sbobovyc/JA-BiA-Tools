"""
Created on February 16, 2012

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

class CTX_language:
    def __init__(self, description_string, data_offset=0):
        self.description_string = description_string
        self.data_offset = data_offset
        self.data_dictionary = OrderedDict()   # {text id : data} mapping
    
    def add_data(self, id, text):
        self.data_dictionary[id] = text
    
    def get_description(self):
        return self.description_string
    
    def get_data(self):
        return self.data_dictionary
    
    def get_num_items(self):
        return len(self.data_dictionary)
    
    def get_last_item_id(self):
        last_item = self.data_dictionary.popitem()  # get last item in ordered dictionary        
        # put item back
        self.add_data(last_item[0], last_item[1])
        last_item_id = last_item[0]
        return last_item_id
    
    def get_description_length(self):
        return len(self.description_string)
    
    def get_packed_data(self):        
        buffer = ""
        for key, value in self.data_dictionary.items():       
            encoded_value = value.encode('utf-16le')     
            encoded_size = len(encoded_value)         
            data_packed = struct.pack("<II%is" % encoded_size, key, encoded_size/2, encoded_value)
            #print binascii.hexlify(data_packed)
            buffer = buffer + data_packed
            #print binascii.hexlify(buffer)
        return buffer
    
    def __repr__(self):
        return "%s(name=%r, language=%r, data=%r)" % (
             self.__class__.__name__, self.description_string, self.data_dictionary)
   
    def __str__(self):
        return "Language: %s, data offset: %s bytes" % (self.description_string, hex(self.data_offset).rstrip('L'))
        
class CUI_data:
    def __init__(self):
        pass
    
    def unpack(self, file_pointer, peek=False, verbose=False):    
        self.last_variable_id,self.unknown2 = struct.unpack("<II", file_pointer.read(8))

        if peek or verbose:
            print "Not implemented"
        if peek:
            return 
        
        print "Last variable picture_id:", self.last_variable_id
        picture_id = 0
        while(picture_id < self.last_variable_id):
            picture_id,length = struct.unpack("<II", file_pointer.read(8))
            variable_name = file_pointer.read(length)
            length, = struct.unpack("<I", file_pointer.read(4))
            variable_value = file_pointer.read(length)
            print picture_id,variable_name, "=", variable_value
            self.data_offset = file_pointer.tell()
        
        print
        
        self.file_count, = struct.unpack("<I", file_pointer.read(4))
        print "File count:", self.file_count
        picture_id = 0
        for i in range(0, self.file_count):
            picture_id,length = struct.unpack("<II", file_pointer.read(8))
            file_name = file_pointer.read(length)
            print picture_id, file_name
        
        self.binary_count, = struct.unpack("<I", file_pointer.read(4))
        print "Binary sound info blob count:", self.binary_count
        for i in range(0, self.binary_count):
            id, = struct.unpack("<I", file_pointer.read(4))
            raw_data = file_pointer.read(9)
            print id,binascii.hexlify(raw_data)
        
        print
        
        self.font_count, = struct.unpack("<I", file_pointer.read(4))
        print "Font count:", self.font_count
        for i in range(0, self.font_count):
            picture_id,length = struct.unpack("<II", file_pointer.read(8))
            font_name = file_pointer.read(length)
            length, = struct.unpack("<I", file_pointer.read(4))
            font_file = file_pointer.read(length)
            print picture_id,font_name,font_file
            
        print
        
        self.ui_file_count, = struct.unpack("<I", file_pointer.read(4))
        print "UI file count:", self.ui_file_count
        for i in range(0, self.ui_file_count):
            picture_id,length = struct.unpack("<II", file_pointer.read(8))
            ui_name = file_pointer.read(length)
            length, = struct.unpack("<I", file_pointer.read(4))
            ui_file = file_pointer.read(length)
            print picture_id,ui_name,ui_file
        
        print 
        
        self.ui_count, = struct.unpack("<I", file_pointer.read(4))
        print "UI element count:", self.ui_count
        print "resource ID, picture ID, ulx, uly, lrx, lry"
        for i in range(0, self.ui_count):
            picture_id,resource_id = struct.unpack("<II", file_pointer.read(8))
            ulx,uly,lrx,lry = struct.unpack("<HHHH", file_pointer.read(8))
            print picture_id,resource_id,ulx,uly,lrx,lry
            
        print 
        
        count, = struct.unpack("<I", file_pointer.read(4))
        print "Number of ui elements:", count
        for i in range(0, count):
            id,length = struct.unpack("<II", file_pointer.read(8))
            text = file_pointer.read(length)
            unknown0, = struct.unpack("<I", file_pointer.read(4))
            unknown1 = struct.unpack("<7H", file_pointer.read(14))
            padding = struct.unpack("<B", file_pointer.read(1))
            
            num_verteces, = struct.unpack("<H", file_pointer.read(2))
            
            for j in range(0, num_verteces):
                vertex_id, = struct.unpack("<I", file_pointer.read(4))
                color, = struct.unpack("<I", file_pointer.read(4))
                data = struct.unpack("<IB", file_pointer.read(5))
                
            trailer_length = struct.unpack("<H", file_pointer.read(2))
            if(trailer_length == 0):
                padding = file_pointer.read(2)
            else:
                pass
            print id, text, hex(unknown0), unknown1, num_verteces
            print hex(file_pointer.tell())
        
        # Background_Overlapping_Inactive, uint32 id, unint32 length, name, 
        
        # Pic_Background_white(transparent), uint32 id, unint32 length, name, 
        # 0x1000, 0x10 00 13 00 02 01 00 00 00 00 00 02 00 02 00,
        # 0x06 number of vertex definitions, uint32 vertex id?, 9 bytes of vertex definition
        # 7D 7D 7D 64 (RGBA) diffuse (D3DDECLTYPE_D3DCOLOR) color, 7F 7F 7F C8 specular? (it's unused),
    
        
        # Pic_Background_white(solid), uint32 id, unint32 length, name, 19 bytes of stuff,
        # 7D 7D 7D 0A (RGBA) diffuse color, 7F 7F 7F C8 specular? (it's unused),
        
        # ButtonBitIcon_CheckButton is the last ui type
        
        # MainMenu Start, uint32 UI type (0xA9, Pic_Background_lightgreen), uint32 length of name, name, 
        # uint32 number of ui elements, uint32 unknown, 0x00
        # MAIN_LoadGame, uint32 UI type(0xA7), 0xFFFFFFFF, 0x03030000, uint32 length of name, name, 
        
        # MAIN_PlayTutorial, 0x03 UI_type (button with text),
        # 0x03 (center the text), 0x0000, length, name, byte column, byte row, 
        # int16 x offset from grid center, int16 y offset from grid center,
        # 0x18012400 (type?, only exists in main menu), uint32 ctx id (which text to use), uint32 length in bytes of next command,
        # command (play tutorial, new game, exit, etc) {memory address?}, nonsense
        
        # merc, uint32 layer, 0x0000, uint32 ui type (Pic_Background_white(solid)), 0x01c5 resource id, uint32, uint32 length, name, byte column, byte row, int16 x offset from grid center, 
        # int16 y offset from grid center, nonsense
        
    def get_packed_data(self):
        return None
        #1. check to see if all the language have the same amount of items
        #2. check that all languages have the same last item id
#        self.num_languages = self.get_num_languages()
#        self.num_items = self.language_list[0].get_num_items()
#        self.last_item_id = self.language_list[0].get_last_item_id()        
#        
#        for i in range(1, len(self.language_list)):
#            if self.language_list[i].get_num_items() != self.num_items:
#                print "Languages do not contain same ammount of items!"
#                return
#            if self.language_list[i].get_last_item_id()  != self.last_item_id:
#                print "The last item in each language is not the same!"
#                return
#            
#        #3. pack each language into a byte string and create the data 
#        header_buffer = struct.pack("<III", self.num_items, self.last_item_id, self.num_languages)
#        data_buffer = ""
#        previous_buffer_length = 0
#        for language in self.language_list:
#            length = language.get_description_length()
#            description = language.get_description()
#            header_buffer = header_buffer + struct.pack("<I%isI" % length, length, description, previous_buffer_length)
#            #print binascii.hexlify(header_buffer)
#            data_buffer = data_buffer + language.get_packed_data()
#            previous_buffer_length = len(data_buffer)
#            
#        #4. concatenate the byte strings and return     
#        return (header_buffer + data_buffer)            

    def __repr__(self):
        return "%s(name=%r, languages=%r)" % (
             self.__class__.__name__, self.language_list)
            
class CUI_file:
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
        
        self.data = CUI_data()
        
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

        full_path = file_name + ".ctx.txt" 
        print "Creating %s" % full_path
        yaml.add_representer(unicode, lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:str', value))
        with codecs.open(full_path, "wb", "utf-16") as f:                                            
                yaml.dump(self.data, f, allow_unicode=True, encoding="utf-16")                                             
    
    def yaml2ctx(self, yaml_file):
        filepath = os.path.abspath(yaml_file)
        with codecs.open(filepath, "r", "utf-16") as f:
            self.data = yaml.load(f)                   
        self.pack()

if __name__ == "__main__":    
    cU = CUI_file("C:\Users\sbobovyc\Desktop\\bia\\1.06\\bin_win32\\interface\interface.cui")
    #cF = CTX_file("/media/Acer/Users/sbobovyc/Desktop/test/bin_win32/interface/equipment.ctx")
    cU.open()        
    cU.unpack(verbose=False)    

