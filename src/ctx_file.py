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
        
class CTX_data:
    def __init__(self):
        self.num_items = None
        self.last_item_id = 0
        self.num_languages = None
        self.data_offset = 0 
        self.language_list = []
    
    def get_languages(self):
        return self.language_list
    
    def get_num_languages(self):
        return len(self.language_list)
    
    def insert_language(self, language):
        self.language_list.append(language)
    
    def unpack(self, file_pointer, peek=False, verbose=False):    
        self.num_items,self.last_item_id,self.num_languages = struct.unpack("<III", file_pointer.read(12))
        
        for i in range(0, self.num_languages):
            desc_length, = struct.unpack("<I", file_pointer.read(4))
            description_string = file_pointer.read(desc_length)
            data_offset, = struct.unpack("<I", file_pointer.read(4))
            self.insert_language(CTX_language(description_string, data_offset))
        
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
                item_text = unicode(item_raw_text, "utf-16le")                
                language.add_data(id, item_text)
                if verbose:
                    print id,item_text    
                    
    def get_packed_data(self):
        #1. check to see if all the language have the same amount of items
        #2. check that all languages have the same last item id
        self.num_languages = self.get_num_languages()
        self.num_items = self.language_list[0].get_num_items()
        self.last_item_id = self.language_list[0].get_last_item_id()        
        
        for i in range(1, len(self.language_list)):
            if self.language_list[i].get_num_items() != self.num_items:
                print "Languages do not contain same ammount of items!"
                return
            if self.language_list[i].get_last_item_id()  != self.last_item_id:
                print "The last item in each language is not the same!"
                return
            
        #3. pack each language into a byte string and create the data 
        header_buffer = struct.pack("<III", self.num_items, self.last_item_id, self.num_languages)
        data_buffer = ""
        previous_buffer_length = 0
        for language in self.language_list:
            length = language.get_description_length()
            description = language.get_description()
            header_buffer = header_buffer + struct.pack("<I%isI" % length, length, description, previous_buffer_length)
            #print binascii.hexlify(header_buffer)
            data_buffer = data_buffer + language.get_packed_data()
            previous_buffer_length = len(data_buffer)
            
        #4. concatenate the byte strings and return     
        return (header_buffer + data_buffer)            

    def __repr__(self):
        return "%s(name=%r, languages=%r)" % (
             self.__class__.__name__, self.language_list)
            
class CTX_file:
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
        
        self.data = CTX_data()
        
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
    pass
    cF = CTX_file("C:\Users\sbobovyc\Desktop\\test\\bin_win32\interface\equipment.ctx")
    #cF = CTX_file("/media/Acer/Users/sbobovyc/Desktop/test/bin_win32/interface/equipment.ctx")
    cF.open()        
    cF.unpack(verbose=False)    
    cF.dump2yaml(".")
#    cF.pack(verbose=False)
#    cFnew = CTX_file("new_equipment.ctx")
#    cFnew.yaml2ctx("equipment.ctx.txt")

    # create a file programmatically
#    cTest = CTX_file("test.ctx")
#    english = CTX_language("eng")
#    english.add_data(0, u"Officer's key")
#    cTest.data.insert_language(english)
#    cTest.dump2yaml(".")
