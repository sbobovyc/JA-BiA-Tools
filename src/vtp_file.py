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
from collections import OrderedDict
from jabia_file import JABIA_file

class VTP_constant:
    def __init__(self, name):
        self.name = name
        self.unknown3 = None
        self.unknown_params_list = None

    def get_packed_data(self): 
        import binascii       
        data_buffer = struct.pack("<I%isBB" % len(self.name), 
                                  len(self.name), self.name, self.unknown, len(self.path_list))
        for path in self.path_list:
            data_buffer += struct.pack("<I%is" % len(path), len(path), path)
        print binascii.hexlify(data_buffer)
        return data_buffer
        
class VTP_variable:
    def __init__(self, name, unknown):
        self.name = name
        self.unknown = unknown
        self.path_list = []
        
    def get_packed_data(self): 
        import binascii       
        data_buffer = struct.pack("<I%isBB" % len(self.name), 
                                  len(self.name), self.name, self.unknown, len(self.path_list))
        for path in self.path_list:
            data_buffer += struct.pack("<I%is" % len(path), len(path), path)
        print binascii.hexlify(data_buffer)
        return data_buffer
    
    def __repr__(self):
        return "%s(name=%r, id=%r, id_name=%r, path=%r)" % (
             self.__class__.__name__, self.id, self.id_name, self.path)
   
    def __str__(self):
        return "CTX ID: %s, %s = %s" % (self.id, self.id_name, self.path)
        
class VTP_item:
    def __init__(self, id, id_name):
        self.id = id
        self.unknown_const = 256
        self.id_name = id_name
        self.variable_list = []
        self.constant_list = []
        
    def get_packed_data(self, section): 
        import binascii       
        data_buffer = struct.pack("<IHI%is" % len(self.id_name), 
                                  self.id, self.unknown_const, len(self.id_name), self.id_name)
        data_buffer += struct.pack("<B", len(self.variable_list))
        for variable in self.variable_list:
            data_buffer += variable.get_packed_data()
        if section == 0 or section == 4:
            data_buffer += "\x00\x00"
        if section == 1 or section == 2:
            data_buffer += "\x00"
        print binascii.hexlify(data_buffer)
        return data_buffer
    
    def __repr__(self):
        return "%s(name=%r, id=%r, id_name=%r, path=%r)" % (
             self.__class__.__name__, self.id, self.id_name, self.path)
   
    def __str__(self):
        return "CTX ID: %s, %s = %s" % (self.id, self.id_name, self.path)
             
class VTP_data:
    def __init__(self):
        self.object_3d_list1 = []
        self.animation_list = []
        self.effects_list = []
        self.materials_list = []
        self.object_3d_list2 = []
    
    def parse(self, file_pointer, list):
        # section, number of entries
        self.section,self.num_items = struct.unpack("<BH", file_pointer.read(3))
        print
        print "Section %s, number of items %s" % (self.section, self.num_items)        
        for i in range(0, self.num_items):
            id1,id2,length = struct.unpack("<IHI", file_pointer.read(10))
            print 
            print "{"
            print "\tResource id",id1,id2
            varname, = struct.unpack("%ss" % length, file_pointer.read(length))
            num_types, = struct.unpack("<B", file_pointer.read(1))
            print "\tItem name", varname
            print "\tNumber of variables",num_types
            item = VTP_item(id1, varname)
            if num_types != 0:
                for i in range(0, num_types):
                    length, =struct.unpack("<I", file_pointer.read(4))
                    variable_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                    print "\tVariable", variable_name
                    unknown0, number_of_objects = struct.unpack("<BB", file_pointer.read(2))
                    print "\tUnknown",unknown0 
                    print "\tNumber of objects",number_of_objects
                    variable = VTP_variable(variable_name, unknown0)
                    for i in range(0, number_of_objects):
                        length, = struct.unpack("<I", file_pointer.read(4))                
                        file_path, = struct.unpack("%ss" %length, file_pointer.read(length))
                        print "\t\t",file_path
                        variable.path_list.append(file_path)
                    item.variable_list.append(variable)
            if self.section == 3:
                unknown1,num_constants,unknown2 = struct.unpack("<BBB", file_pointer.read(3))
                print "\tUnknown", unknown1
                print "\tNumber of constants",num_constants
                print "\tUnknown", unknown2
                
                for i in range(0, num_constants):                    
                    unknown3,length = struct.unpack("<BI", file_pointer.read(5))
                    material_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                    print "\tUnknown", unknown3
                    print "\tConstant", material_name,
                    prop = struct.unpack("<fffffffff", file_pointer.read(36))
                    print prop

            if self.section == 0 or self.section == 4:
                file_pointer.read(2)
            if self.section == 1 or self.section == 2:
                file_pointer.read(1)
            print "}"
            list.append(item)
        return 
    def unpack(self, file_pointer, peek=False, verbose=False):   
        self.num_sections, = struct.unpack("<xB", file_pointer.read(2))
        self.parse(file_pointer, self.object_3d_list1)    # read in static 3d objects
        self.parse(file_pointer, self.animation_list)    # read in animations
        self.parse(file_pointer, self.effects_list)    # read in effects
        self.parse(file_pointer, self.materials_list)    # read in material info
        self.parse(file_pointer, self.object_3d_list2)    # read in another set of 3d objects
        
        return 
#        # read in static 3d files
#        self.num_sections,self.section,self.num_items = struct.unpack("<xBBH", file_pointer.read(5))
#        print "Number of sections", self.num_sections, 
#        print "Number of static objects", self.num_items
#        for i in range(0, self.num_items):
#            id1,id2,length = struct.unpack("<IHI", file_pointer.read(10))
#            print "Resource id",id1,id2,length
#            varname, = struct.unpack("%ss" % length, file_pointer.read(length))
#            num_types, = struct.unpack("<B", file_pointer.read(1))
#            print "Varname", varname, num_types
#            for i in range(0, num_types):
#                length, =struct.unpack("<I", file_pointer.read(4))
#                object_type, = struct.unpack("%ss" % length, file_pointer.read(length))
#                print "Type", object_type
#                resource_id, number_of_objects = struct.unpack("<BB", file_pointer.read(2))
#                print resource_id, number_of_objects
#                for i in range(0, number_of_objects):
#                    length, = struct.unpack("<I", file_pointer.read(4))                
#                    file_path, = struct.unpack("%ss" %length, file_pointer.read(length))
#                    print file_path
#            # read in trailer
#            file_pointer.read(2)
#        print hex(file_pointer.tell())       
#        
#        
#        # read in animations        
#        self.section,self.num_animations, = struct.unpack("<BH", file_pointer.read(3))
#        print "Number of animations", hex(self.num_animations)
#        for i in range(0, self.num_animations):
#            id1,id2,length = struct.unpack("<HII", file_pointer.read(10))
#            print "Animation resource id",id1,id2,length
#            print i, self.num_animations
#            varname, = struct.unpack("%ss" % length, file_pointer.read(length))
#            num_animations, = struct.unpack("<B", file_pointer.read(1))
#            print "Varname", varname, num_animations
#            for i in range(0, num_animations):
#                length, = struct.unpack("<I", file_pointer.read(4))
#                print "length", length 
#                animation_name, = struct.unpack("%ss" % length, file_pointer.read(length))
#                print animation_name
#                unknown, num_files = struct.unpack("<BB", file_pointer.read(2))
#                print unknown, num_files
#                for i in range(0, num_files):
#                    length, = struct.unpack("<I", file_pointer.read(4))
#                    path_name, = struct.unpack("%ss" % length, file_pointer.read(length))
#                    print "Path name", path_name
#                    # read in animations
#            # read in trailer
#            file_pointer.read(1)
#        
#        
#        print hex(file_pointer.tell())
#        self.section, self.num_effects, = struct.unpack("<BH", file_pointer.read(3))
#        print "Number of effects", hex(self.num_effects)
#        for i in range(0, self.num_effects):
#            id1,id2,length = struct.unpack("<HII", file_pointer.read(10))
#            print "Effect resource id",id1,id2,length
#            print i, self.num_effects
#            varname, = struct.unpack("%ss" % length, file_pointer.read(length))
#            num_effects, = struct.unpack("<B", file_pointer.read(1))
#            print "Varname", varname, num_effects    
#            for i in range(0, num_effects):
#                length, = struct.unpack("<I", file_pointer.read(4))
#                print "length", length 
#                effect_name, = struct.unpack("%ss" % length, file_pointer.read(length))
#                print effect_name
#                unknown, num_files = struct.unpack("<BB", file_pointer.read(2))
#                print unknown, num_files  
#                for i in range(0, num_files):
#                    length, = struct.unpack("<I", file_pointer.read(4))
#                    path_name, = struct.unpack("%ss" % length, file_pointer.read(length))
#                    print "Path name", path_name          
#            # read in trailer
#            file_pointer.read(1)
#        
#        print hex(file_pointer.tell())           
#        self.num_objects, = struct.unpack("<xH", file_pointer.read(3))
#        print "Number of objects", hex(self.num_objects)
#        for i in range(0, self.num_objects):
#            id1,id2,length = struct.unpack("<HII", file_pointer.read(10))
#            print "Object resource id",id1,id2,length
#            print i, self.num_effects
#            varname, = struct.unpack("%ss" % length, file_pointer.read(length))
#            print "Varname", varname    
#            num_physics_files, = struct.unpack("B", file_pointer.read(1))
#            if num_physics_files > 0:
#                for i in range(0, num_physics_files):
#                    length, = struct.unpack("<I", file_pointer.read(4))
#                    print "length", length 
#                    effect_name, = struct.unpack("%ss" % length, file_pointer.read(length))
#                    print effect_name
#                    unknown, num_files = struct.unpack("<BB", file_pointer.read(2))
#                    print unknown, num_files  
#                    for i in range(0, num_files):
#                        length, = struct.unpack("<I", file_pointer.read(4))
#                        path_name, = struct.unpack("%ss" % length, file_pointer.read(length))
#                        print "Path name", path_name
#                    print hex(file_pointer.tell()) 
#            # check for non-files materials                                            
#            num_materials, = struct.unpack("<xBx", file_pointer.read(3))
#            print "Number of materials", num_materials
#            for i in range(0, num_materials):
#                length, = struct.unpack("<xI", file_pointer.read(5))
#                material_name, = struct.unpack("%ss" % length, file_pointer.read(length))
#                print "Material", material_name
#                a,b,c,d,e,f = struct.unpack("<ffffff", file_pointer.read(24))
#                print a,b,c,d,e,f
#                g,h,j = struct.unpack("<fff", file_pointer.read(12))
#                print g,h,j
#                print hex(file_pointer.tell()) 
#            
#            # read multi-crf objects
        if peek or verbose:
            pass
        if peek:
            return  
                    
    def get_packed_data(self):
        # header, 1 and number of sections
        data_buffer = "\x01\x05"
        
        # first section 3d objects
        data_buffer += "\x00"
        data_buffer += struct.pack("<H", len(self.object_3d_list1))
        for object in self.object_3d_list1:
            data_buffer += object.get_packed_data(0)            
        
        # second section animations
        data_buffer += "\x01"
        data_buffer += struct.pack("<H", len(self.animation_list))
        for object in self.animation_list:
            data_buffer += object.get_packed_data(1)
    
        # third section effects
        data_buffer += "\x02"
        data_buffer += struct.pack("<H", len(self.effects_list))
        for object in self.effects_list:
            data_buffer += object.get_packed_data(2)
#            
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
#    var = VTP_variable("default", 2)
#    var.path_list.append("environment/pipeline_02_edge_round_01.crf")
#    var.get_packed_data()
#    item = VTP_item(1, "pipeline_02_edge_round_01", 0)
#    item.variable_list.append(var)
#    item.get_packed_data()
    vtp = VTP_file("C:\\Program Files (x86)\\Jagged Alliance Back in Action Demo\\bin_win32\main.vtp")
    vtp.open()        
    vtp.unpack(verbose=False)    
    vtp.filepath = "test.bin"
    vtp.pack()
    #vtp.dump2yaml(".")
    pass

