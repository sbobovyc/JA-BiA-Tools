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
import binascii
import struct
import math


try:
    from numpy import *
    from numpy.random import *
except ImportError, err:
    try: 
        from Numeric import *
        from RandomArray import *
    except ImportError, err:
        print "This library requires the numpy or Numeric extension, sorry"
        import sys
        sys.exit()
        
class CRF_data:
    def __init__(self):
        self.crf_magick = None
        self.vertex_xyz_data = []   # list of numpy arrays containing x,y,z
        self.vertex_uvw_data = []
        
    def unpack(self, file_pointer, peek=False, verbose=False):    
        self.crf_magick, = struct.unpack("<Q", file_pointer.read(8))    
        if self.crf_magick != 0x1636E6B66:
            print "Not a CRF file!"
            return 
        if peek or verbose:
            print "not implemented"
        if peek:
            print "not implemented" 
        self.footer_offset,self.magick2 = struct.unpack("<II", file_pointer.read(8))
        print self.footer_offset, hex(self.footer_offset)
        print self.magick2, hex(self.magick2)
        self.magick3, self.magick4, self.num_models_in_file = struct.unpack("<III", file_pointer.read(12))
        print self.magick3, self.magick4
        print "Number of models in file", self.num_models_in_file
        self.last_x, self.last_y, self.last_z = struct.unpack("<fff", file_pointer.read(12))        
        self.last_i, self.last_j, self.last_k = struct.unpack("<fff", file_pointer.read(12)) #root point?
        print "Last xyz", self.last_x, self.last_y, self.last_z
        print "Last xyz2", self.last_i, self.last_j, self.last_k
        self.number_of_point, = struct.unpack("<I", file_pointer.read(4))
        print "Number of verteces", self.number_of_point
        self.number_of_faces, = struct.unpack("<I", file_pointer.read(4))
        print "Number of faces", self.number_of_faces
        print "Position", hex(file_pointer.tell())
        self.faces = []
        for i in range(0, self.number_of_faces):
            v1, v2, v3 = struct.unpack("<HHH", file_pointer.read(6))
            self.faces.append([v1, v2, v3])
            print "Faces %s %s %s" % (v1+1, v2+1, v3+1)
        print "Position", hex(file_pointer.tell())
        self.start_token,null = struct.unpack("<QB", file_pointer.read(9)) 
        #0x0000200c01802102, 0x00
        print hex(self.start_token)
        
        #reading verteces
        for i in range(0, self.number_of_point):
            print hex(file_pointer.tell())
            # Sir_Kane    float x, y, z; dword diffuse, specular; short u0, v0, u1, v1; dword blendweights
            x, y, z, diffuse, specular, u0, v0, u1, v1, blendweights = struct.unpack("<fffIIHHHHI", file_pointer.read(32))
#            vertex = array([x,y,z])
            vertex = [x,y,z]
            self.vertex_xyz_data.append(vertex)
            print i, vertex, diffuse, specular, u0, v0, u1, v1, blendweights
            #print "v %s %s %s" % (x, y, z)
            
        # then 0x00 00 00 08 00 08 00 00 00
        # then data that does not seem to be used
        # then nm to signal end of data
        # then footer

        # dump to a simple wavfront object
        with open("crf_dump.obj", "w") as f:
            f.write("# Generated with crf_magick from JABIA Tools Project\n")
            f.write("o Dumped_Object\n")
            for i in range(0, self.number_of_point):
                f.write("v %s %s %s\n" % (self.vertex_xyz_data[i][0], self.vertex_xyz_data[i][1], self.vertex_xyz_data[i][2]))
            f.write("s off\n")
            for i in range(0, self.number_of_faces):
                f.write("f %s %s %s\n" % (self.faces[i][0]+1, self.faces[i][1]+1, self.faces[i][2]+1))
           
class CRF_file:
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
        
        self.data = CRF_data()
        
    def unpack(self, verbose=False):
        with open(self.filepath, "rb") as f:            
            self.data.unpack(f, verbose=verbose)
        
if __name__ == "__main__":
    #crf = CRF_file("C:\\Users\\sbobovyc\\Documents\\3DReaperDX\\folder_box_01.crf") 
    crf = CRF_file("C:\\Users\\sbobovyc\\Desktop\\bia\\1.11\\bin_win32\\weapons\\barret_m82_01.crf")
    crf.unpack()           