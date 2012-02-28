"""
Created on February 27, 2012

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

import yaml 
import codecs
import os

class JABIA_file(object):
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
    
    def yaml2bin(self, yaml_file):
        filepath = os.path.abspath(yaml_file)
        with codecs.open(filepath, "r", "utf-16") as f:
            self.data = yaml.load(f)                   
        self.pack()
