"""
Created on February 6, 2012

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
from jabia_file import JABIA_file

class VTP_constant:
    def __init__(self, name):
        self.name = name
        self.unknown3 = None
        self.unknown_params_list = None

    def get_packed_data(self): 
        data_buffer = struct.pack("<BI%isfffffffff" % len(self.name), 
                                  self.unknown3, len(self.name), self.name, *self.unknown_params_list)
        #print binascii.hexlify(data_buffer)
        return data_buffer

    def __str__(self):
        return "Constant: %s = %s" % (self.name, self.unknown_params_list)
            
class VTP_variable:
    def __init__(self, name, unknown):
        self.name = name
        self.unknown = unknown
        self.path_list = []
        
    def get_packed_data(self): 
        data_buffer = struct.pack("<I%isBB" % len(self.name), 
                                  len(self.name), self.name, self.unknown, len(self.path_list))
        for path in self.path_list:
            data_buffer += struct.pack("<I%is" % len(path), len(path), path)
        #print binascii.hexlify(data_buffer)
        return data_buffer
    
#    def __repr__(self):
#        return "%s(name=%r, id=%r, id_name=%r, path=%r)" % (
#             self.__class__.__name__, self.id, self.id_name, self.path)
#   
    def __str__(self):     
        return "Variable: %s = %s" % (self.name, self.path_list)
        
class VTP_item:
    def __init__(self, id, id_name):
        self.id = id
        self.unknown_const = 256
        self.id_name = id_name
        self.variable_list = []
        self.unknown1 = None
        self.unknown2 = None
        self.constant_list = []
        
    def get_packed_data(self, section): 
        data_buffer = struct.pack("<IHI%is" % len(self.id_name), 
                                  self.id, self.unknown_const, len(self.id_name), self.id_name)
        data_buffer += struct.pack("<B", len(self.variable_list))
        for variable in self.variable_list:
            data_buffer += variable.get_packed_data()
        if section == 0 or section == 4:
            data_buffer += "\x00\x00"
        if section == 1 or section == 2:
            data_buffer += "\x00"
        if section == 3:
            data_buffer += struct.pack("<BBB", self.unknown1, len(self.constant_list), self.unknown2)
        for constant in self.constant_list:
            data_buffer += constant.get_packed_data()
        #print binascii.hexlify(data_buffer)
        return data_buffer
    
#    def __repr__(self):
#        return "%s(name=%r, id=%r, id_name=%r, path=%r)" % (
#             self.__class__.__name__, self.id, self.id_name, self.path)
#   
    def __str__(self):
        string = ""
        string += "VTP ID: %s, %s" % (self.id, self.id_name)
        for variable in self.variable_list:
            string += "\n"
            string += variable.__str__()
        for constant in self.constant_list:
            string += "\n"
            string += constant.__str__()
        return string
             
class VTP_data:
    def __init__(self):
        self.object_3d_list1 = []
        self.animation_list = []
        self.effects_list = []
        self.materials_list = []
        self.object_3d_list2 = []
    
    def parse(self, file_pointer, list_pointer, peek=False, verbose=False):
        # section, number of entries
        self.section,self.num_items = struct.unpack("<BH", file_pointer.read(3))
        if verbose:
            print "################################"
        print "Section %s, number of items %s" % (self.section, self.num_items)
        if verbose:
            print "################################"        
        for i in range(0, self.num_items):
            id1,id2,length = struct.unpack("<IHI", file_pointer.read(10))
            #print 
            #print "{"
            #print "\tResource id",id1,id2
            varname, = struct.unpack("%ss" % length, file_pointer.read(length))
            num_types, = struct.unpack("<B", file_pointer.read(1))
            #print "\tItem name", varname
            #print "\tNumber of variables",num_types
            item = VTP_item(id1, varname)
            if num_types != 0:
                for i in range(0, num_types):
                    length, =struct.unpack("<I", file_pointer.read(4))
                    variable_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                    #print "\tVariable", variable_name
                    unknown0, number_of_objects = struct.unpack("<BB", file_pointer.read(2))
                    #print "\tUnknown",unknown0 
                    #print "\tNumber of objects",number_of_objects
                    variable = VTP_variable(variable_name, unknown0)
                    for i in range(0, number_of_objects):
                        length, = struct.unpack("<I", file_pointer.read(4))                
                        file_path, = struct.unpack("%ss" %length, file_pointer.read(length))
                        #print "\t\t",file_path
                        variable.path_list.append(file_path)
                    item.variable_list.append(variable)
            if self.section == 3:
                unknown1,num_constants,unknown2 = struct.unpack("<BBB", file_pointer.read(3))
                #print "\tUnknown", unknown1
                #print "\tNumber of constants",num_constants
                #print "\tUnknown", unknown2
                item.unknown1 = unknown1
                item.unknown2 = unknown2
                
                for i in range(0, num_constants):                    
                    unknown3,length = struct.unpack("<BI", file_pointer.read(5))
                    material_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                    #print "\tUnknown", unknown3
                    #print "\tConstant", material_name,
                    prop = struct.unpack("<fffffffff", file_pointer.read(36))
                    #print prop
                    const = VTP_constant(material_name)
                    const.unknown3 = unknown3
                    const.unknown_params_list = prop
                    item.constant_list.append(const)
                    
            if self.section == 0 or self.section == 4:
                file_pointer.read(2)
            if self.section == 1 or self.section == 2:
                file_pointer.read(1)
            #print "}"
            
            list_pointer.append(item)
            if verbose:
                print
                print item
        return 
    
    def unpack(self, file_pointer, peek=False, verbose=False):   
        self.num_sections, = struct.unpack("<xB", file_pointer.read(2))
        self.parse(file_pointer, self.object_3d_list1, peek=peek, verbose=verbose)    # read in static 3d objects
        self.parse(file_pointer, self.animation_list, peek=peek, verbose=verbose)    # read in animations
        self.parse(file_pointer, self.effects_list, peek=peek, verbose=verbose)    # read in effects
        self.parse(file_pointer, self.materials_list, peek=peek, verbose=verbose)    # read in material info
        self.parse(file_pointer, self.object_3d_list2, peek=peek, verbose=verbose)    # read in another set of 3d objects
        
        return 
        if peek or verbose:
            pass
        if peek:
            return  
                    
    def get_packed_data(self):
        # header, 1 and number of sections
        data_buffer = "\x01\x05"
        
        # first section, 3d objects
        data_buffer += "\x00"
        data_buffer += struct.pack("<H", len(self.object_3d_list1))
        for object in self.object_3d_list1:
            data_buffer += object.get_packed_data(0)            
        
        # second section, animations
        data_buffer += "\x01"
        data_buffer += struct.pack("<H", len(self.animation_list))
        for object in self.animation_list:
            data_buffer += object.get_packed_data(1)
    
        # third section, effects
        data_buffer += "\x02"
        data_buffer += struct.pack("<H", len(self.effects_list))
        for object in self.effects_list:
            data_buffer += object.get_packed_data(2)
            
        # fourth section, materials
        data_buffer += "\x03"
        data_buffer += struct.pack("<H", len(self.materials_list))
        for object in self.materials_list:
            data_buffer += object.get_packed_data(3)
        
        # fifth section, second set of 3d objects
        data_buffer += "\x04"
        data_buffer += struct.pack("<H", len(self.object_3d_list2))
        for object in self.object_3d_list2:
            data_buffer += object.get_packed_data(4)    
                                
        # return     
        return data_buffer            

    def __repr__(self):
        return "%s(name=%r, languages=%r)" % (
             self.__class__.__name__, self.language_list)
            
class VTP_file(JABIA_file):    
    def __init__(self, filepath=None):
        super(VTP_file,self).__init__(filepath=filepath)
        self.yaml_extension = ".vtp.txt"
        
    def open(self, filepath=None, peek=False):
        super(VTP_file,self).open(filepath=filepath, peek=peek)  
        self.data = VTP_data()

if __name__ == "__main__":
    vtp = VTP_file("C:\\Program Files (x86)\\Jagged Alliance Back in Action Demo\\bin_win32\main.vtp")
    vtp.open()        
    vtp.unpack(verbose=False)        
    #vtp.pack()
    #vtp.dump2yaml(".")
    pass

