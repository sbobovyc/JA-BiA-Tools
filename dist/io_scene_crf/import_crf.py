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

# Script copyright (C) Campbell Barton
# Contributors: Campbell Barton, Jiri Hnidek, Paolo Ciccone

"""
This script imports a Wavefront OBJ files to Blender.

Usage:
Run this script from "File->Import" menu and then load the desired OBJ file.
Note, This loads mesh objects and materials only, nurbs and curves are not supported.

http://wiki.blender.org/index.php/Scripts/Manual/Import/wavefront_obj
"""

import os
import time
import bpy
import mathutils
import struct
from bpy_extras.io_utils import unpack_list, unpack_face_list
from bpy_extras.image_utils import load_image

def load(operator, context, filepath,
         global_clamp_size=0.0,
         use_ngons=True,
         use_smooth_groups=True,
         use_edges=True,
         use_split_objects=True,
         use_split_groups=True,
         use_image_search=True,
         use_groups_as_vgroups=False,
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

    if use_split_objects or use_split_groups:
        use_groups_as_vgroups = False

    time_main = time.time()

    verts_loc = []
    verts_tex = []
    faces = []  # tuples of the faces
    material_libs = []  # filanems to material libs this uses
    vertex_groups = {}  # when use_groups_as_vgroups is true

    # Context variables
    context_material = None
    context_smooth_group = None
    context_object = None
    context_vgroup = None

    # Nurbs
    context_nurbs = {}
    nurbs = []
    context_parm = b''  # used by nurbs too but could be used elsewhere

    has_ngons = False
    # has_smoothgroups= False - is explicit with len(unique_smooth_groups) being > 0

    # Until we can use sets
    unique_materials = {}
    unique_material_images = {}
    unique_smooth_groups = {}
    # unique_obects= {} - no use for this variable since the objects are stored in the face.

    # when there are faces that end with \
    # it means they are multiline-
    # since we use xreadline we cant skip to the next line
    # so we need to know whether
    context_multi_line = b''

    print("\tparsing obj file...")
    time_sub = time.time()
#     time_sub= sys.time()

    file = open(filepath, "rb")
    crf_magick, = struct.unpack("<Q", file.read(8))    
    if crf_magick != 0x1636E6B66:
        print("Not a CRF file!")
        return 

    footer_offset,magick2 = struct.unpack("<II", file.read(8))
    magick3, magick4, num_models_in_file = struct.unpack("<III", file.read(12))

    last_x, last_y, last_z = struct.unpack("<fff", file.read(12))        
    last_i, last_j, last_k = struct.unpack("<fff", file.read(12)) #root point?
    number_of_point, = struct.unpack("<I", file.read(4))
    number_of_faces, = struct.unpack("<I", file.read(4))
    for i in range(0, number_of_faces):
            v1, v2, v3 = struct.unpack("<HHH", file.read(6))
            face_vert_loc_indices = [v1, v2, v3]
            face_vert_tex_indices = [v1, v2, v3]
            context_material = b'office_assets_01_c.dds'
            context_smooth_group = None
            context_object = b'Dumped_Object'
            unique_materials[context_material] = None
            faces.append((v1, v2, v3, v1))


    start_token,null = struct.unpack("<QB", file.read(9)) 
    #0x0000200c01802102, 0x00

    for i in range(0, number_of_point):
        x, y, z, diffuse, specular, u0, v0, u1, v1, blendweights = struct.unpack("<fffIIHHHHI", file.read(32))
        verts_loc.append((x,y,z))

        
    
    time_new = time.time()
    print("%.4f sec" % (time_new - time_sub))
    time_sub = time_new

    print('\tloading materials and images...')
    material_libs = [b'default_library']
    use_image_search = True
    print(material_libs)
    print(unique_materials)
    print(unique_material_images)
    print(use_image_search)

    time_new = time.time()
    print("%.4f sec" % (time_new - time_sub))
    time_sub = time_new

    # deselect all
    if bpy.ops.object.select_all.poll():
        bpy.ops.object.select_all(action='DESELECT')

    scene = context.scene
#     scn.objects.selected = []
    new_objects = []  # put new objects here

    me = bpy.data.meshes.new("DumpedObject_Mesh")   # create a new mesh
    ob = bpy.data.objects.new("DumpedObject", me)
    # Fill the mesh with verts, edges, faces 
    me.from_pydata(verts_loc,[],faces)   # edges or faces should be [], or you ask for problems
    me.update(calc_edges=True)    # Update mesh with new data
                         
    new_objects.append(ob)

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


