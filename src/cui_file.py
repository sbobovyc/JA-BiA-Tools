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

magick1 = "00000400000004000000020002000000030005000000060003000000"
magick2 = "00000400000011000000020010000000030012000000060003000000"
magick3 = "pad 2 bytes"
magick4 = "some unknown data"

class CUI_ui_screen_element:
    def __init__(self, type, name, count, unknown):
        pass
    
class CUI_ui_screen:
    def __init__(self, type, name, count, unknown):
        self.type = type
        self.name = name
        self.ui_count = count
        self.unknown = unknown
        self.element_list = []
        
    def get_packed_data(self):
        data_buffer = struct.pack("<II%isIx" % len(self.name), 
                                  self.id, len(self.name), self.name, self.unknown)
        return data_buffer
    
class CUI_ui_element_trailer:
    def __init__(self, unknown_data0, unknown_data1):
        self.unknonw_data0 = unknown_data0 # list of (id, data) 
        self.unknonw_data1 = unknown_data1
    
    def get_packed_data(self):
        data_buffer = struct.pack("<H", len(self.unknonw_data0))
        for each in self.unknonw_data0:
            data_buffer += struct.pack("<II", each[0], each[1])
        if len(self.unknonw_data1) == 0:
            data_buffer += struct.pack("xx")
        else:
            data_buffer += struct.pack("<H", len(self.unknonw_data1))
            for each in self.unknonw_data1:
                data_buffer += struct.pack("<HI", each[0], each[1])        

        return data_buffer

class CUI_ui_element_vertex:
    def __init__(self, vertex_id, color, data):
        self.vertex_id = vertex_id
        self.color = color
        self.data = data 
    
    def get_packed_data(self):
        data_buffer = struct.pack("<IIIB", self.vertex_id, self.color, *self.data)
        return data_buffer
    
    def __str__(self):
        return "id: %s, color: %s, data:%s" % (self.vertex_id, hex(self.color).rstrip('L'), self.data)
    
class CUI_ui_element: 
    def __init__(self, element_id, name, unknown0, unknown1, verteces, trailer):
        self.element_id = element_id
        self.name = name
        self.unknown0 = unknown0
        self.unknown1 = unknown1
        self.verteces = verteces    # list of CUI_ui_element_verteces
        self.trailer = trailer      # 

    def get_packed_data(self):        
        data_buffer = struct.pack("<II%isI" % (len(self.name)), 
                                  self.element_id, len(self.name), self.name, self.unknown0)
        data_buffer += struct.pack("<7Hx", *self.unknown1)
        data_buffer += struct.pack("<H", len(self.verteces))
        
        for vertex in self.verteces:
            data_buffer += vertex.get_packed_data()
            
        if self.trailer == "magick1":
            data_buffer += binascii.unhexlify(magick1)            
        elif self.trailer == "magick2":
            data_buffer += binascii.unhexlify(magick2)
        elif self.trailer == "magick3":
            data_buffer += struct.pack("Hxx", 0x0)
        else:
            data_buffer += self.trailer.get_packed_data()
#        print binascii.hexlify(data_buffer)
        return data_buffer
    
        
#    def __repr__(self):
#        return "%s(name=%r, icon_id=%r, resource=%r, ulx=%r, uly=%r, lrx=%r, lry=%s)" % (
#             self.__class__.__name__, self.icon_id, self.resource_id, self.ulx, self.uly, self.lrx, self.lry)
#   
    def __str__(self):
        string = ""
        string += "UI element id: %s, name: %s, type?: %s\n" % (self.element_id, self.name, hex(self.unknown0))
        string += "unknown data: (" + ', '.join(map(str, self.unknown1)) + ")\n"
        for vertex in self.verteces:
            string += vertex.__str__() + "\n"
        return string
#        return "UI icon ID: %s, resource %s, (%s,%s)(%s,%s)" % (self.icon_id, self.resource_id, self.ulx, self.uly, self.lrx, self.lry)

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
#        print binascii.hexlify(data_buffer)
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
#        print binascii.hexlify(data_buffer)
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
        self.ui_element_dict = OrderedDict()   # {element id : CUI_ui_element} mapping
        self.binary_ui_blob = ""
        
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
        
        file_count, = struct.unpack("<I", file_pointer.read(4))
        print "Sound file count:", file_count
        id = 0
        for i in range(0, file_count):
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
            ui_element_id,length = struct.unpack("<II", file_pointer.read(8))
            name = file_pointer.read(length)
            unknown0, = struct.unpack("<I", file_pointer.read(4))
            unknown1 = struct.unpack("<7Hx", file_pointer.read(15))
            
            num_verteces, = struct.unpack("<H", file_pointer.read(2))
            
            verteces = []
            for j in range(0, num_verteces):
                vertex_id, = struct.unpack("<I", file_pointer.read(4))
                color, = struct.unpack("<I", file_pointer.read(4))
                data = struct.unpack("<IB", file_pointer.read(5))
                verteces.append(CUI_ui_element_vertex(vertex_id, color, data))
            # this hack is here because I still don't know why some UI elements have traling data and some don't
            saved_position = file_pointer.tell()
            trailer = file_pointer.read(28)
            
            trailer_type = None
            unknown_data0 = []
            unknown_data1 = []
            if binascii.hexlify(trailer) == magick1:
                trailer_type = "magick1"
            elif binascii.hexlify(trailer) == magick2:
                trailer_type = "magick2"
            else:
                file_pointer.seek(saved_position)   # reset the address, very hacky
                trailer_length, = struct.unpack("<H", file_pointer.read(2))
                if(trailer_length == 0):
                    padding = file_pointer.read(2)
                    trailer_type = "magick3"
                else:
                    for i in range(0, trailer_length):
                        id,data = struct.unpack("<II", file_pointer.read(8))
                        unknown_data0.append((id,data))
                        
                    trailer_length, = struct.unpack("<H", file_pointer.read(2))
                    for i in range(0, trailer_length):
                        id,data = struct.unpack("<HI", file_pointer.read(6))
                        unknown_data1.append((id,data))                        
                        
                    trailer_type = CUI_ui_element_trailer(unknown_data0, unknown_data1)
            print 
            # construct object
            cui_ui_element = CUI_ui_element(ui_element_id, name, unknown0, unknown1, verteces, trailer_type)
            self.ui_element_dict[ui_element_id] = cui_ui_element
            print cui_ui_element
        
        self.binary_ui_blob = file_pointer.read()
#        count, = struct.unpack("<I", file_pointer.read(4))
#        print "Number of ui screens:", count        
#        for i in range(0, count):
#            ui_type,length = struct.unpack("<II", file_pointer.read(8))
#            name = file_pointer.read(length)
#            num_items, = struct.unpack("<I", file_pointer.read(4))
#            unknown, = struct.unpack("<Ix", file_pointer.read(5))
#            cui_ui_screen = CUI_ui_screen(ui_type, name, num_items, unknown)
#            print ui_type, name, num_items, unknown
#            for j in range(0, num_items):
#                ui_element_type, unknown, positioning, length = struct.unpack("<IIII", file_pointer.read(32))
#                name = file_pointer.read(length)
#                region, x_offset, y_offset = struct.unpack("<HHH", file_pointer.read(6))
#                print name, ui_element_type, hex(unknown)
#                print hex(region), x_offset, y_offset
                
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
        
        # merc, uint32 layer, 0x0000, uint32 ui type 0x26 (Pic_Background_white(solid)), 0x01c5 resource id, uint32, uint32 length, name, byte column, byte row, int16 x offset from grid center, 
        # int16 y offset from grid center, nonsense
        
    def get_packed_data(self):        
        last_ctx_id = self.ctx_id_list[-1].id     
        num_sounds = len(self.sound_list)
        num_binary = len(self.binary_blob_dictionary)
        num_fonts = len(self.font_list)
        num_ui_resources = len(self.ui_resource_dict)
        num_ui_icons = len(self.ui_icon_dict)
        num_ui_elements = len(self.ui_element_dict)
        
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
        
        # 7. compile ui elements
        data_buffer = data_buffer + struct.pack("<I", num_ui_elements)
        for key, value in self.ui_element_dict.items():
            data_buffer = data_buffer + value.get_packed_data()
        
        # 8. compile ui screen binary blob
        data_buffer = data_buffer + self.binary_ui_blob
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

#if __name__ == "__main__":    
#    cU = CUI_file("C:\Users\sbobovyc\Desktop\\bia\\1.06\\bin_win32\\interface\interface.cui")
#    #cF = CTX_file("/media/Acer/Users/sbobovyc/Desktop/test/bin_win32/interface/equipment.ctx")
#    cU.open()        
#    cU.unpack(verbose=False)   
#    cU.dump2yaml() 
#    cU.yaml2bin("interface.cui.txt")

