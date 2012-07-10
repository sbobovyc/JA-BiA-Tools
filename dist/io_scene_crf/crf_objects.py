import math
import struct

class CRF_vertex(object):
    """
        Common variables:
        CRF_vertex.index
        
        Raw CRF variables:
        CRF_vertex.x, vert.y, vert.z 
        CRF_vertex.normal_x 
        CRF_vertex.normal_y 
        CRF_vertex.normal_z 
        CRF_vertex.normal_w 
        CRF_vertex.specular_blue 
        CRF_vertex.specular_green
        CRF_vertex.specular_red 
        CRF_vertex.specular_alpha      
        CRF_vertex.u0 
        CRF_vertex.v0 
        CRF_vertex.u1 
        CRF_vertex.v1 
        CRF_vertex.blendweights1_x
        CRF_vertex.blendweights1_y
        CRF_vertex.blendweights1_z
        CRF_vertex.blendweights1_w

        Blender variables
        CRF_vertex.x_blend, vert.y_blend, vert.z_blend 
        CRF_vertex.normal_x_blend 
        CRF_vertex.normal_y_blend 
        CRF_vertex.normal_z_blend 
        CRF_vertex.normal_w_blend 
        CRF_vertex.specular_blue_blend 
        CRF_vertex.specular_green_blend
        CRF_vertex.specular_red_blend 
        CRF_vertex.specular_alpha_blend #Not iplemented      
        CRF_vertex.u0_blend 
        CRF_vertex.v0_blend 
        CRF_vertex.u1_blend 
        CRF_vertex.v1_blend 
        CRF_vertex.blendweights1_blend
        CRF_vertex.blendweights1_x_blend
        CRF_vertex.blendweights1_y_blend
        CRF_vertex.blendweights1_z_blend
        CRF_vertex.blendweights1_w_blend  

            
    """
    def __str__(self):
        string = "Vertex index = %s\n" % (self.index)
        string += "Blender values:\n"
        string += "xyz = %f %f %f\n" % (self.x_blend, self.y_blend, self.z_blend)
        string += "\tvertex normal XYZW  = %f %f %f %f\n" % (self.normal_x_blend, self.normal_y_blend, self.normal_z_blend, self.normal_w_blend)                                                                    
        string += "\tspecular BGRA  = %f %f %f %f\n" % (self.normal_x_blend, self.normal_y_blend, self.normal_z_blend, self.normal_w_blend)                                                 
        string += "\tuv0 = %f %f\n" % (self.u0_blend, self.v0_blend)
        string += "\tuv1 = %f %f\n" % (self.u1_blend, self.v1_blend)
        string += "\tblendeweight = %f %f %f %f\n" % (self.blendweights1_x_blend, self.blendweights1_y_blend, self.blendweights1_z_blend, self.blendweights1_w_blend)     

        string += "CRF values:\n"
        string += "xyz = %f %f %f\n" % (self.x, self.y, self.z)        
        string += "\tvertex normal XYZW  = %i %i %i %i, %s %s %s %s\n" % (self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                                     hex(self.normal_x), hex(self.normal_y), hex(self.normal_z), hex(self.normal_w))
        string += "\tspecular BGRA  = %i %i %i %i, %s %s %s %s\n" % (self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                                     hex(self.specular_blue), hex(self.specular_green), hex(self.specular_red), hex(self.specular_alpha))
        string += "\tuv0 = %i %i, 0x%x 0x%x\n" % (self.u0, self.v0, self.u0, self.v0)
        string += "\tuv1 = %i %i, 0x%x 0x%x\n" % (self.u1, self.v1, self.u1, self.v1)        
        string += "\tblendeweight = 0x%x 0x%x 0x%x 0x%x\n" % (self.blendweights1_x & 0xff, self.blendweights1_y & 0xff, self.blendweights1_z & 0xff, self.blendweights1_w & 0xff)       
        return string

    def float2uint(self, f_number):
        if f_number > 0.0:
            return int(128 + f_number * 127)
        elif f_number < 0.0:
            return int(128 - math.fabs(f_number) * 128)
        else:
            return 128
        
    def uint2float(self, uint_number):
        if uint_number > 128:
            return float(uint_number / 127.0)
        elif uint_number < 128:
            return float(-uint_number / 128.0)
        else:
            return 0.0

    def raw2blend(self):
        """ Convert raw values to blender values """
        #TODO find out how CRF object coordinates work (global or local)
        self.x_blend = self.x
        self.y_blend = self.y
        self.z_blend = self.z
        self.x_blend = -self.x_blend # mirror vertex across x axis

        self.normal_x_blend = self.uint2float(self.normal_x)
        self.normal_y_blend = self.uint2float(self.normal_y) 
        self.normal_z_blend = self.uint2float(self.normal_z) 
        self.normal_w_blend = self.uint2float(self.normal_w)

        self.specular_blue_blend = self.specular_blue / 255
        self.specular_green_blend = self.specular_green / 255
        self.specular_red_blend = self.specular_red / 255
        self.specular_alpha_blend = self.specular_alpha / 255

        self.u0_blend = 0.5+(self.u0 / 32768)/2.0
        self.v0_blend = 0.5-(self.v0 / 32768)/2.0
        self.u1_blend = 0.5+(self.u1 / 32768)/2.0
        self.v1_blend = 0.5-(self.v1 / 32768)/2.0
        
        self.blendweights1_x_blend = self.blendweights1_x / 255
        self.blendweights1_y_blend = self.blendweights1_y / 255
        self.blendweights1_z_blend = self.blendweights1_z / 255
        self.blendweights1_w_blend = self.blendweights1_w / 255        
        
        
    def blend2raw(self):
        """ Convert blender values to raw values """
        #TODO find out how CRF object coordinates work (global or local)
        self.x = self.x_blend
        self.y = self.z_blend
        self.z = self.y_blend
        self.x = -self.x # mirror vertex across x axis
        self.z = -self.z # mirror vertex across z axis
        
        self.normal_x = self.float2uint(self.normal_x_blend)
        self.normal_y = self.float2uint(-self.normal_y_blend) # flip y direction
        self.normal_z = self.float2uint(-self.normal_z_blend) # flip z direction
        self.normal_w = self.float2uint(self.normal_w_blend)
        
        self.specular_blue = int(self.specular_blue_blend * 255)
        self.specular_green = int(self.specular_green_blend * 255)
        self.specular_red = int(self.specular_red_blend * 255)
        self.specular_alpha = int(self.specular_alpha_blend * 255)
        
        self.u0 = int(((self.u0_blend - 0.5) * 2) * 32768)
        self.v0 = int(((self.v0_blend - 0.5) * -2) * 32768)
        self.u1 = int(((self.u1_blend - 0.5) * 2) * 32768)
        self.v1 = int(((self.v1_blend - 0.5) * -2) * 32768)

        self.blendweights1_x = int(self.blendweights1_x_blend * 255)
        self.blendweights1_y = int(self.blendweights1_y_blend * 255)
        self.blendweights1_z = int(self.blendweights1_z_blend * 255)
        self.blendweights1_w = int(self.blendweights1_w_blend * 255)

        # clamp uv values to be <= 32768 and >=-32768
        if self.u0 >= 32768:
            self.u0 = 32767
        if self.v0 >= 32767:
            self.v0 = 32767
        if self.u1 >= 32768:
            self.u1 = 32767
        if self.v1 >= 32768:
            self.v1 = 32767
        if self.u0 <= -32768:
            self.u0 = -32767
        if self.v0 <= -32768:
            self.v0 = -32767
        if self.u1 <= -32768:
            self.u1 = -32767
        if self.v1 <= -32768:
            self.v1 = -32767               
        
    def convert2bin(self):        
        binstring = struct.pack("<fffBBBBBBBBhhhhBBBB", self.x, self.y, self.z,
                                                         self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                         self.specular_blue, self.specular_green, self.specular_red, self.specular_alpha,
                                                         self.u0, self.v0, self.u1, self.v1,
                                                         self.blendweights1_x, self.blendweights1_y,
                                                        self.blendweights1_z, self.blendweights1_w)                                                
        return binstring
    
