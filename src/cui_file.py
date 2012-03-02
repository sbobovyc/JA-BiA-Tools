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
import binascii           
from collections import OrderedDict
from jabia_file import JABIA_file
from jabia_object import JABIA_sound, JABIA_font
from ctx_file import CTX_ID

class CUI_ui_element:
    def __repr__(self):
        return "%s(name=%r, icon_id=%r, resource=%r, ulx=%r, uly=%r, lrx=%r, lry=%s)" % (
             self.__class__.__name__, self.icon_id, self.resource_id, self.ulx, self.uly, self.lrx, self.lry)
   
    def __str__(self):
        return "UI icon ID: %s, resource %s, (%s,%s)(%s,%s)" % (self.icon_id, self.resource_id, self.ulx, self.uly, self.lrx, self.lry)

class CUI_ui_icon:
    def __init__(self, icon_id, resource_id, ulx, uly, lrx, lry):
        self.icon_id = icon_id
        self.resource_id = resource_id    
        self.ulx = ulx
        self.uly = uly
        self.lrx = lrx
        self.lry = lry

    def get_packed_data(self):        
        data_buffer = struct.pack("<IIHHHH", 
                                  self.icon_id, self.resource_id, self.ulx, self.uly, self.lrx, self.lry)
        print binascii.hexlify(data_buffer)
        return data_buffer
        
    def __repr__(self):
        return "%s(name=%r, icon_id=%r, resource=%r, ulx=%r, uly=%r, lrx=%r, lry=%s)" % (
             self.__class__.__name__, self.icon_id, self.resource_id, self.ulx, self.uly, self.lrx, self.lry)
   
    def __str__(self):
        return "UI icon ID: %s, resource %s, (%s,%s)(%s,%s)" % (self.icon_id, self.resource_id, self.ulx, self.uly, self.lrx, self.lry)

class CUI_ui_resource:
    def __init__(self, id, ui_name, filename):
        self.id = id
        self.ui_name = ui_name
        self.filename = filename

    def get_packed_data(self):        
        data_buffer = struct.pack("<II%isI%is" % (len(self.ui_name), len(self.filename)), 
                                  self.id, len(self.ui_name), self.ui_name, len(self.filename), self.filename)
        print binascii.hexlify(data_buffer)
        return data_buffer
        
    def __repr__(self):
        return "%s(name=%r, id=%r, ui_name=%r, filename=%r)" % (
             self.__class__.__name__, self.id, self.ui_name, self.filename)
   
    def __str__(self):
        return "UI resource ID: %s, %s = %s" % (self.id, self.ui_name, self.filename)
    
class CUI_data:
    def __init__(self):
        self.ctx_id_list = [] 
        self.sound_list = [] 
        self.binary_blob_dictionary = {}  
        self.font_list = []
        self.ui_resource_dict = OrderedDict()   # {resource id : CUI_ui_resource} mapping
        self.ui_icon_dict = OrderedDict()   # {icon id : CUI_ui_icon} mapping
        
    def unpack(self, file_pointer, peek=False, verbose=False):    
        self.last_variable_id,unknown1 = struct.unpack("<II", file_pointer.read(8))

        if peek or verbose:
            print "Not implemented"
        if peek:
            return 
        
        print "Last variable picture_id:", self.last_variable_id
        
        id = 0
        while(id < self.last_variable_id):
            id,length = struct.unpack("<II", file_pointer.read(8))
            variable_name = file_pointer.read(length)
            length, = struct.unpack("<I", file_pointer.read(4))
            variable_value = file_pointer.read(length)
            ctx_id = CTX_ID(id, variable_name, variable_value)
            print ctx_id
            self.ctx_id_list.append(ctx_id)
        
        print
        
        self.file_count, = struct.unpack("<I", file_pointer.read(4))
        print "Sound file count:", self.file_count
        id = 0
        for i in range(0, self.file_count):
            id,length = struct.unpack("<II", file_pointer.read(8))
            filename = file_pointer.read(length)
            jabia_sound = JABIA_sound(id, filename)            
            print jabia_sound
            self.sound_list.append(jabia_sound)
        
        print 
        
        self.binary_count, = struct.unpack("<I", file_pointer.read(4))
        print "Binary sound info blob count:", self.binary_count
        for i in range(0, self.binary_count):
            id, = struct.unpack("<I", file_pointer.read(4))
            raw_data = file_pointer.read(9)            
            print id,binascii.hexlify(raw_data)
            self.binary_blob_dictionary[id] = raw_data
        
        print
        
        self.font_count, = struct.unpack("<I", file_pointer.read(4))
        print "Font count:", self.font_count
        for i in range(0, self.font_count):
            id,length = struct.unpack("<II", file_pointer.read(8))
            font_name = file_pointer.read(length)
            length, = struct.unpack("<I", file_pointer.read(4))
            filename = file_pointer.read(length)
            jabia_font = JABIA_font(id, font_name, filename)
            print jabia_font
            self.font_list.append(jabia_font)
            
        print
        
        self.ui_file_count, = struct.unpack("<I", file_pointer.read(4))
        print "UI file count:", self.ui_file_count
        for i in range(0, self.ui_file_count):
            id,length = struct.unpack("<II", file_pointer.read(8))
            ui_name = file_pointer.read(length)
            length, = struct.unpack("<I", file_pointer.read(4))
            filename = file_pointer.read(length)
            ui_resource = CUI_ui_resource(id, ui_name, filename)
            print ui_resource
            self.ui_resource_dict[id]= ui_resource
        print 
        
        self.ui_count, = struct.unpack("<I", file_pointer.read(4))
        print "UI icon count:", self.ui_count
        for i in range(0, self.ui_count):
            icon_id,resource_id = struct.unpack("<II", file_pointer.read(8))
            ulx,uly,lrx,lry = struct.unpack("<HHHH", file_pointer.read(8))
            icon = CUI_ui_icon(icon_id, resource_id, ulx, uly, lrx, lry)
            self.ui_icon_dict[icon_id] = icon
            print icon
            
        print 
        
        count, = struct.unpack("<I", file_pointer.read(4))
        print "Number of ui elements:", count
        for i in range(0, count):
            ui_id,length = struct.unpack("<II", file_pointer.read(8))
            text = file_pointer.read(length)
            unknown0, = struct.unpack("<I", file_pointer.read(4))
            unknown1 = struct.unpack("<7H", file_pointer.read(14))
            padding = struct.unpack("<B", file_pointer.read(1))
            
            num_verteces, = struct.unpack("<H", file_pointer.read(2))
            
            for j in range(0, num_verteces):
                vertex_id, = struct.unpack("<I", file_pointer.read(4))
                color, = struct.unpack("<I", file_pointer.read(4))
                data = struct.unpack("<IB", file_pointer.read(5))
            # this hack is here because I still don't know why some UI elements have traling data and some don't
            saved_position = file_pointer.tell()
            trailer = file_pointer.read(28)
            magick1 = "00000400000004000000020002000000030005000000060003000000"
            magick2 = "00000400000011000000020010000000030012000000060003000000"
            if binascii.hexlify(trailer) == magick1:
                print "magick1"
            elif binascii.hexlify(trailer) == magick2:
                print "magick2"
            else:
                file_pointer.seek(saved_position)   # reset the address, very hacky
                trailer_length, = struct.unpack("<H", file_pointer.read(2))
                if(trailer_length == 0):
                    padding = file_pointer.read(2)
                else:
                    for i in range(0, trailer_length):
                        id,data = struct.unpack("<II", file_pointer.read(8))
                    trailer_length, = struct.unpack("<H", file_pointer.read(2))
                    for i in range(0, trailer_length):
                        id,data = struct.unpack("<HI", file_pointer.read(6))
            print "UI id: %i," % ui_id, "UI name: %s," % text, "UI type?:%s" % hex(unknown0)
            print "Unknown data:",unknown1
            print "Number of vertex descriptions?:",num_verteces
            print 
        
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
        last_ctx_id = self.ctx_id_list[-1].id     
        num_sounds = len(self.sound_list)
        num_binary = len(self.binary_blob_dictionary)
        num_fonts = len(self.font_list)
        num_ui_resources = len(self.ui_resource_dict)
        num_ui_icons = len(self.ui_icon_dict)
        
        # 1. compile ctx mappings
        data_buffer = struct.pack("<II", last_ctx_id, 0xFFFFFFFF)      
        for ctx_id in self.ctx_id_list:
            data_buffer = data_buffer + ctx_id.get_packed_data()

        # 2. compile sound mappings
        data_buffer = data_buffer + struct.pack("<I", num_sounds)
        for sound in self.sound_list:
            data_buffer = data_buffer + sound.get_packed_data()
        
        # 3. compile unknown binary data
        data_buffer = data_buffer + struct.pack("<I", num_binary)
        for key, value in self.binary_blob_dictionary.items():        
            data_packed = struct.pack("<I%is" % len(value), key, value)
            data_buffer = data_buffer + data_packed                
        
        # 4. compile fonts
        data_buffer = data_buffer + struct.pack("<I", num_fonts)
        for font in self.font_list:
            data_buffer = data_buffer + font.get_packed_data()
        
        # 5. compile ui resources
        data_buffer = data_buffer + struct.pack("<I", num_ui_resources)
        for key, value in self.ui_resource_dict.items():
            data_buffer = data_buffer + value.get_packed_data()
        
        # 6. compile ui icons
        data_buffer = data_buffer + struct.pack("<I", num_ui_icons)
        for key, value in self.ui_icon_dict.items():
            data_buffer = data_buffer + value.get_packed_data()
            
        return (data_buffer)  
    
    def __repr__(self):
        return "%s(name=%r)" % (
             self.__class__.__name__, self.language_list)
            
class CUI_file(JABIA_file):
    def __init__(self, filepath=None):
        super(CUI_file,self).__init__(filepath=filepath)
        self.yaml_extension = ".cui.txt"
        
    def open(self, filepath=None, peek=False):
        super(CUI_file,self).open(filepath=filepath, peek=peek)
        self.data = CUI_data()   

if __name__ == "__main__":    
    cU = CUI_file("C:\Users\sbobovyc\Desktop\\bia\\1.06\\bin_win32\\interface\interface.cui")
    #cF = CTX_file("/media/Acer/Users/sbobovyc/Desktop/test/bin_win32/interface/equipment.ctx")
    cU.open()        
    cU.unpack(verbose=False)   
    cU.dump2yaml() 
    cU.yaml2bin("interface.cui.txt")

