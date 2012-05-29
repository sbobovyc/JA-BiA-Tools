# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# Script copyright (C) Stanislav Bobovych

"""
This script imports a JABIA CRF files to Blender.

Usage:
Run this script from "File->Import" menu and then load the desired CRF file.
Note, This loads mesh objects and materials only, nurbs and curves are not supported.

https://github.com/sbobovyc/JA-BiA-Tools/wiki

Useful docs:
http://msdn.microsoft.com/en-us/library/windows/desktop/bb173349%28v=vs.85%29.aspx
"""

import sys
import os
import fnmatch
import time
import bpy
import mathutils
import struct
from bpy_extras.io_utils import unpack_list, unpack_face_list
from bpy_extras.image_utils import load_image

def find_files(base, pattern):
    '''Return list of files matching pattern in base folder.'''
    try:
        return [n for n in fnmatch.filter(os.listdir(base), pattern) if
            os.path.isfile(os.path.join(base, n))]
    except:
        print("File not found")

def findTextureFile(path, name):
    obj_dir = os.path.dirname(path)
    #search several locations
    possible_locations = [obj_dir, os.path.join(os.path.dirname(obj_dir), "textures"),
                          os.path.join(os.path.dirname(obj_dir), "textures", "items"),
                          os.path.join(os.path.dirname(obj_dir), "textures", "interface"),
                          os.path.join(os.path.dirname(obj_dir), "textures", "characters")]
    for location in possible_locations:
        filenames = find_files(location, "%s.*" % name)
        # relying on lazy evaluation of if statement to not cause a problem if filenames is None
        if  filenames != None and len(filenames) != 0:
            file_path = os.path.join(location, filenames[0])
            return file_path
    
##def createMaterial(filepath):    
##    # Create image texture from image. Change here if the snippet 
##    # folder is not located in you home directory.
##    realpath = os.path.expanduser(filepath)
##    tex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
##    tex.image = bpy.data.images.load(realpath)
##    tex.use_alpha = True
## 
##    # Create shadeless material and MTex
##    mat = bpy.data.materials.new('TexMat')
##    mat.use_shadeless = True
##    mtex = mat.texture_slots.add()
##    mtex.texture = tex
##    mtex.texture_coords = 'UV'
##    mtex.use_map_color_diffuse = True 
##    return mat

def createMaterial(name, use_shadeless, use_vertex_colors):        
    # Create shadeless or shaded material and MTex
    mat = bpy.data.materials.new(name)
    mat.use_shadeless = use_shadeless
    mat.use_vertex_color_paint = use_vertex_colors   # support per vertex    
    return mat

def addDiffuseTexture(color_filepath, mat):
    # Create image texture from image. Change here if the snippet 
    # folder is not located in you home directory.
    realpath = os.path.expanduser(color_filepath)
    tex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
    tex.image = bpy.data.images.load(realpath)
    tex.use_alpha = True
    mtex = mat.texture_slots.add()
    mtex.texture = tex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True

def addNormalTexture(normals_filepath, mat):
    realpath = os.path.expanduser(normals_filepath)
    norm = bpy.data.textures.new('NormalsTex', type = 'IMAGE')
    norm.image = bpy.data.images.load(realpath)
    norm.use_alpha = True
    norm.use_normal_map = True
    mnorm = mat.texture_slots.add()
    mnorm.texture = norm
    mnorm.texture_coords = 'UV'
    mnorm.use_map_color_diffuse = False
    mnorm.use_map_normal = True
    mnorm.normal_factor = 0.2

def addSpecularTexture(specular_filepath, mat):
    realpath = os.path.expanduser(specular_filepath)
    spec = bpy.data.textures.new('SpecularTex', type = 'IMAGE')
    spec.image = bpy.data.images.load(realpath)
    spec.use_alpha = True
    mspec = mat.texture_slots.add()
    mspec.texture = spec
    mspec.texture_coords = 'UV'
    mspec.use_map_color_diffuse = False
    mspec.use_map_normal = False
    mspec.use_map_specular = True
    

def createSimpleMaterial(use_shadeless, use_vertex_colors):        
    # Create shadeless or shaded material and MTex
    mat = bpy.data.materials.new('SimpleMat')
    mat.use_shadeless = use_shadeless
    mat.use_vertex_color_paint = use_vertex_colors   # support per vertex 
    return mat

def createTextureLayer(name, me, texFaces):
    uvtex = me.uv_textures.new()
    uvtex.name = name
    for n,tf in enumerate(texFaces):        
        datum = uvtex.data[n]
        datum.uv1 = tf[0]
        datum.uv2 = tf[1]
        datum.uv3 = tf[2]
    return uvtex

def setVertexDiffuseColors(me, faces, vertex_diffuse):
    vtex_diffuse = me.vertex_colors.new()
    vtex_diffuse.name = "vertex_diffuse_colors"
    for face in faces:
        verts_in_face = face.vertices[:]
        vtex_diffuse.data[face.index].color1 = vertex_diffuse[verts_in_face[0]]
        vtex_diffuse.data[face.index].color2 = vertex_diffuse[verts_in_face[1]]
        vtex_diffuse.data[face.index].color3 = vertex_diffuse[verts_in_face[2]]

##    for n in vtex_diffuse.data:
##        print(n.color1, n.color2, n.color3)
        
    return vtex_diffuse

def setVertexSpecularColors(me, faces, vertex_specular):
    vtex_specular = me.vertex_colors.new()
    vtex_specular.name = "vertex_specular_colors"
    for face in faces:
        verts_in_face = face.vertices[:]
        vtex_specular.data[face.index].color1 = vertex_specular[verts_in_face[0]]
        vtex_specular.data[face.index].color2 = vertex_specular[verts_in_face[1]]
        vtex_specular.data[face.index].color3 = vertex_specular[verts_in_face[2]]

##    for n in vtex_diffuse.data:
##        print(n.color1, n.color2, n.color3)
        
    return vtex_specular


def parseShaderInfo(file, specular_list):
    texture_name = b''
    normals_name = b''
    specular_name = b''
    state = 0
    flag = 0
    #read in material information
    print("Reading materials", hex(file.tell()))
    materials, = struct.unpack("2s", file.read(2))
    if materials == b'nm':
        unknown, = struct.unpack("<I", file.read(4))
        unknown, = struct.unpack("<I", file.read(4))
    else:
        state = -1

    running = True
    while running:
        if state == 0:
            print("STATE 0", flag)
            variable, = struct.unpack("4s", file.read(4))
            print(variable)
            if variable == b'sffd':
                state = 1
                flag = "dffs"
            elif variable == b'smrn':
                state = 1
                flag = "nrms"
            elif variable == b'lcps':
                state = 1
                flag = "spcl"
            elif variable == b'1tsc':
                state = 3
            else:
                state = -1
            
        if state == 1:
            print("STATE 1", flag)
            length, = struct.unpack("<I", file.read(4))
            if length > 0 and flag == "dffs":
                state = 2
            elif length > 0 and flag == "nrms":
                state = 2
            elif length > 0 and flag == "spcl":
                state = 2
            elif length == 0 and flag == "spcl":
                state = 4
            else:
                state = -1

        if state == 2:
            print("STATE 2", flag)
            if flag == "dffs":
                texture_name, = struct.unpack("%ss" % length, file.read(length))
                file.read(4)
                flag = 0
                state = 0                
            elif flag == "nrms":
                normals_name, = struct.unpack("%ss" % length, file.read(length))
                file.read(4)
                flag = 0
                state = 0                
            elif flag == "spcl":
                specular_name, = struct.unpack("%ss" % length, file.read(length))
                state = 4

        if state == 3:
            print("STATE 3", flag)
            int1, int2 = struct.unpack("<II", file.read(8))
            if int1 == 0 and int2 == 0:
                variable, = struct.unpack("4s", file.read(4))
                print(variable, hex(file.tell()))
                if variable == b'lcps':
                    length, = struct.unpack("<I", file.read(4))
                    print("length", length)
                    if length != 0:
                        flag = "spcl"
                        state = 2
                    else:
                        state = 4

        if state == 4:
            print("STATE 4", flag)
            int1, int2 = struct.unpack("<II", file.read(8))            
            variable, = struct.unpack("4s", file.read(4))
            print(variable, hex(file.tell()))
            if variable == b'lcps':
                red,green,blue = struct.unpack("<fff", file.read(12))
                specular_list.append( (red, green, blue) )
                if int2 == 2:
                    variable, = struct.unpack("4s", file.read(4))
                    file.read(16)
                    variable, = struct.unpack("4s", file.read(4))
                    # read trailer
                    file.read(24)
                    state = 99
                if int2 == 1:
                    # read trailer
                    file.read(24)
                    print("Int is one", hex(file.tell()))
                    state = 99                            
                
        # specular constant        
##        if state == 4:
##            print("STATE 4", flag)
##            if flag == "spcl":
##                garbage,const = struct.unpack("<II", file.read(8))
##                variable, = struct.unpack("4s", file.read(4))
##                if variable == b'lcps':
##                    red,green,blue = struct.read("<fff", file.read(12))
##                    specular_list.append( (red, green, blue) )
##                    state = 99
##                else:
##                    print("Error in state 4")
##                    return

        if state == 99:
            return texture_name, normals_name, specular_name
        
        if state == -1:
            print("This object's materials format is unsupported")
            return    
        

def load(operator, context, filepath,
         global_clamp_size=0.0,
         use_verbose=False,
         use_image_search=True,
         use_shadeless=True,
         use_vertex_colors=True,
         use_specular=True,
         global_matrix=None,
         ):
    '''
    Called by the user interface or another script.
    load_obj(path) - should give acceptable results.
    This function passes the file and sends the data off
        to be split into objects and then converted into mesh objects
    '''
    print('\nimporting obj %r' % filepath)

    filepath = os.fsencode(filepath)

    if global_matrix is None:
        global_matrix = mathutils.Matrix()

    new_objects = []  # put new objects here
    
    time_main = time.time()
    print("\tparsing crf file...")
    time_sub = time.time()
#     time_sub= sys.time()

    file = open(filepath, "rb")
    crf_magick, = struct.unpack("<Q", file.read(8))    
    if crf_magick != 0x1636E6B66:
        print("Not a CRF file!")
        return 

    footer_offset1,footer_offset2 = struct.unpack("<II", file.read(8))
    # so far found model type 0x2 and 0x4
    object_type, magick4, num_meshes_in_file = struct.unpack("<III", file.read(12))
    LoX, LoY, LoZ = struct.unpack("<fff", file.read(12))        
    HiX, HiY, HiZ = struct.unpack("<fff", file.read(12)) #bounding box?
    print("(%f, %f, %f) (%f, %f, %f)" % (LoX, LoY, LoZ, HiX, HiY, HiZ))
    print("Object type", hex(object_type))

    # start unpacking loop here
    for model_number in range(0, num_meshes_in_file):
        verts_loc = []
        verts_tex0 = []
        verts_tex1 = []
        faces = []  # tuples of the faces
        face_tex = [] # tuples of uv coordinates for faces
        vertex_diffuse = []
        vertex_specular = []

        number_of_verteces, = struct.unpack("<I", file.read(4))
        number_of_faces, = struct.unpack("<I", file.read(4))
        print("Model: %i, verteces: %i, faces: %i" % (model_number, number_of_verteces, number_of_faces))
        # read in face/vertex index list
        for i in range(0, number_of_faces):
                v1, v2, v3 = struct.unpack("<HHH", file.read(6))
                face_vert_loc_indices = [v1, v2, v3]
                face_vert_tex_indices = [v1, v2, v3]
                faces.append((v1, v2, v3))
                if use_verbose:
                    print("face index %s, verts (%s, %s, %s)" % (i, v1, v2, v3))


        #read start token     #0x0000200c01802102, 0x00
        start_token, = struct.unpack("<Qx", file.read(9)) 


        if use_verbose:
            print("Loading file, printing raw vertex information.")
        # read in verteces, kd, ks, and UVs
        for i in range(0, number_of_verteces):
            x, y, z, \
                diffuse_blue, diffuse_green, diffuse_red, diffuse_alpha, \
                specular_blue, specular_green, specular_red, specular_alpha, \
                u0, v0, u1, v1, blendweights1 = struct.unpack("<fffBBBBBBBBhhhhI", file.read(32))
            
            if use_verbose:                
                print("vert index=%s, xyz=(%s %s %s), Kd=(%s, %s, %s, %s), Ks=(%s, %s, %s, %s), uv0=(%s, %s), uv1=(%s, %s)" % (i, x,y,z, \
                                    hex(diffuse_alpha), hex(diffuse_red), hex(diffuse_green), hex(diffuse_blue), \
                                    hex(specular_alpha), hex(specular_red), hex(specular_green), hex(specular_blue), \
                                    hex(u0), hex(v0), hex(u1), hex(v1)))
            # convert signed short to float
            # distortions due to rounding by directx and not python
            u0 /= 32768
            v0 /= 32768
            u1 /= 32768
            v1 /= 32768
            
            # mirror vertex across x axis
            verts_loc.append((-x,y,z))
            
            # rectify UV map
            uv0 = (0.5+u0/2.0, 0.5-v0/2.0)

            verts_tex0.append(uv0)
            
            #TODO, add support for the second UV map
            if use_verbose:
                print("Rectified uv0:", uv0)
                print()

            # convert 8 bit to float
            # notice that I don't include alpha
            #TODO Add alpha support
            vertex_diffuse.append( (diffuse_red/255.0, diffuse_green/255.0, diffuse_blue/255.0) )
            vertex_specular.append( (specular_red/255.0, specular_green/255.0, specular_blue/255.0) )

        #read in separator 0x000000080008000000
        print("Separator at", hex(file.tell()))
        separator = struct.unpack("<8B", file.read(8))

        if use_verbose:
            print("Second vertex data stream at", hex(file.tell()))
        #read in second vertex stream, but don't use it for anything
        #TODO figure out why this is here
        for i in range(0, number_of_verteces):
            unknown0, unknown1 = struct.unpack("<ff", file.read(8))
            if use_verbose:
                print("vert index=%s, x?=%s, y?=%s" % (i, unknown0, unknown1))

        #if object type is 0x4, read in second set of blendweights
        #TODO not sure how this data is used
        if object_type == 0x4:
            if use_verbose:
                print("Second blendweight? list at", hex(file.tell()))
            for i in range(0, number_of_verteces):
                blendweights2, unknown = struct.unpack("<II", file.read(8))
            # read in one more int
            file.read(8)
            print("Yay", hex(file.tell()))
            
        #read in bounding box?
        bounding_box = struct.unpack("<6f", file.read(24))
        if use_verbose:
            print("Bounding box? ", bounding_box)
                
        #read in material information
        texture_name = b''
        normal_name = b''
        specular_name = b''
        specular_list = []
        texture_name, normal_name, specular_name = parseShaderInfo(file, specular_list)        
        print(texture_name, normal_name, specular_name, specular_list)    
        #next is object bone information, not parsed
        

        # fill face texture array
##        for i in range(0, len(faces)):
##            face_tex.append([ verts_tex0[faces[i][0]], verts_tex0[faces[i][1]], verts_tex0[faces[i][2]] ] )
        
        # deselect all
        if bpy.ops.object.select_all.poll():
            bpy.ops.object.select_all(action='DESELECT')

        scene = context.scene
    #     scn.objects.selected = []

        me = bpy.data.meshes.new("DumpedObject%i_Mesh" % model_number)   # create a new mesh
        ob = bpy.data.objects.new("DumpedObject%i" % model_number, me)
        # Fill the mesh with verts, edges, faces 
        me.from_pydata(verts_loc,[],faces)   # edges or faces should be [], or you ask for problems
        me.update(calc_edges=True)    # Update mesh with new data

        # fill face uv texture array
        for face in ob.data.faces:
            verts_in_face = face.vertices[:]
            if use_verbose:
                print("face index", face.index)  
                print("normal", face.normal)  
                for vert in verts_in_face:  
                    print("vert", vert, " vert co", ob.data.vertices[vert].co)
                    print("diffuse R:%s G:%s B:%s " % (vertex_diffuse[vert][0], vertex_diffuse[vert][1], vertex_diffuse[vert][2]))
                    print("specular R:%s G:%s B:%s " % (vertex_specular[vert][0], vertex_specular[vert][1], vertex_specular[vert][2]))
                    print("UV0: ", verts_tex0[vert])
                    print()
            i = face.index
            v1 = verts_in_face[0]
            v2 = verts_in_face[1]
            v3 = verts_in_face[2]
            face_tex.append([ verts_tex0[v1], verts_tex0[v2], verts_tex0[v3] ] )

        if use_image_search:
            uvMain = createTextureLayer("UV_Main", me, face_tex)
            texture_filepath = findTextureFile(os.fsdecode(filepath),  texture_name.decode(sys.stdout.encoding))
            normals_filepath = findTextureFile(os.fsdecode(filepath),  normal_name.decode(sys.stdout.encoding))
            specular_filepath = findTextureFile(os.fsdecode(filepath),  specular_name.decode(sys.stdout.encoding))            
            print(texture_filepath, normals_filepath, specular_filepath)            
            mat = createMaterial('TexMat', use_shadeless, use_vertex_colors)
            if texture_filepath != None and texture_filepath != "":
                addDiffuseTexture(texture_filepath, mat)
            if normals_filepath != None and normals_filepath != "":
                addNormalTexture(normals_filepath, mat)
            if use_specular and specular_filepath != None and specular_filepath != "":
                addSpecularTexture(specular_filepath, mat)                
            ob.data.materials.append(mat)

        if use_vertex_colors:
            setVertexDiffuseColors(me, ob.data.faces, vertex_diffuse)
            # if no materials exists, create one+
            if len(ob.data.materials) == 0 and not use_image_search:
                mat = createMaterial('SimpleMat', use_shadeless, use_vertex_colors)
                ob.data.materials.append(mat)
                
        if use_specular:
            setVertexSpecularColors(me, ob.data.faces, vertex_specular)
            # if no materials exists, create one+
            if len(ob.data.materials) == 0 and not use_image_search:
                mat = createMaterial('Specular', use_shadeless, use_vertex_colors)
                mat.specular_color = specular_list[0]
                ob.data.materials.append(mat)
            else:
                #ob.data.materials[0] = specular_list[0]
                ob.data.materials[0].specular_color = specular_list[0]
                print(ob.data.materials[0].specular_color)
        new_objects.append(ob)

    # end loop
    
    time_new = time.time()
    print("%.4f sec" % (time_new - time_sub))
    time_sub = time_new

    print('\tloading materials and images...')


    time_new = time.time()
    print("%.4f sec" % (time_new - time_sub))
    time_sub = time_new
    
    # Create new obj
    for obj in new_objects:
        base = scene.objects.link(obj)
        base.select = True

        # we could apply this anywhere before scaling.
        obj.matrix_world = global_matrix

    scene.update()

    axis_min = [1000000000] * 3
    axis_max = [-1000000000] * 3

    if global_clamp_size:
        # Get all object bounds
        for ob in new_objects:
            for v in ob.bound_box:
                for axis, value in enumerate(v):
                    if axis_min[axis] > value:
                        axis_min[axis] = value
                    if axis_max[axis] < value:
                        axis_max[axis] = value

        # Scale objects
        max_axis = max(axis_max[0] - axis_min[0], axis_max[1] - axis_min[1], axis_max[2] - axis_min[2])
        scale = 1.0

        while global_clamp_size < max_axis * scale:
            scale = scale / 10.0

        for obj in new_objects:
            obj.scale = scale, scale, scale

    time_new = time.time()

    print("finished importing: %r in %.4f sec." % (filepath, (time_new - time_main)))
    return {'FINISHED'}


