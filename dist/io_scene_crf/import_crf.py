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
from bpy_extras.io_utils import unpack_list, unpack_face_list, axis_conversion
from bpy_extras.image_utils import load_image

from .crf_objects import CRF_object

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

def createMaterial(name, use_shadeless, use_vertex_color_paint):        
    # Create shadeless or shaded material and MTex
    mat = bpy.data.materials.new(name)
    mat.use_shadeless = use_shadeless
    mat.use_vertex_color_paint = use_vertex_color_paint   # support per vertex    
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
    mtex.use_map_alpha = True

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
    

def createSimpleMaterial(use_shadeless, viz_normals):        
    # Create shadeless or shaded material and MTex
    mat = bpy.data.materials.new('SimpleMat')
    mat.use_shadeless = use_shadeless
    mat.use_vertex_color_paint = viz_normals   # support per vertex 
    return mat

def createTextureLayer(name, me, texFaces):
    uvtex = me.tessface_uv_textures.new()
    uvtex.name = name
    for n,tf in enumerate(texFaces):        
        datum = uvtex.data[n]
        datum.uv1 = tf[0]
        datum.uv2 = tf[1]
        datum.uv3 = tf[2]
    return uvtex

def setVertexNormalsColors(me, faces, vertex_normals):
    vtex_normals = me.tessface_vertex_colors.new()
    vtex_normals.name = "vertex_normal_xyz"
    for face in faces:
        verts_in_face = face.vertices[:]
        vtex_normals.data[face.index].color1 = vertex_normals[verts_in_face[0]][0:3]
        vtex_normals.data[face.index].color2 = vertex_normals[verts_in_face[1]][0:3]
        vtex_normals.data[face.index].color3 = vertex_normals[verts_in_face[2]][0:3]
    
    vtex_normals = me.tessface_vertex_colors.new()
    vtex_normals.name = "vertex_normal_w"
    for face in faces:
        verts_in_face = face.vertices[:]
        alpha0 = (vertex_normals[verts_in_face[0]][3], vertex_normals[verts_in_face[0]][3], vertex_normals[verts_in_face[0]][3])
        alpha1 = (vertex_normals[verts_in_face[1]][3], vertex_normals[verts_in_face[1]][3], vertex_normals[verts_in_face[1]][3])
        alpha2 = (vertex_normals[verts_in_face[2]][3], vertex_normals[verts_in_face[2]][3], vertex_normals[verts_in_face[2]][3])
        vtex_normals.data[face.index].color1 = alpha0
        vtex_normals.data[face.index].color2 = alpha1
        vtex_normals.data[face.index].color3 = alpha2

def setVertexSpecularColors(me, faces, vertex_specular):
    vtex_specular = me.tessface_vertex_colors.new()
    vtex_specular.name = "vertex_specular_colors"
    for face in faces:
        verts_in_face = face.vertices[:]
        vtex_specular.data[face.index].color1 = vertex_specular[verts_in_face[0]][0:3]
        vtex_specular.data[face.index].color2 = vertex_specular[verts_in_face[1]][0:3]
        vtex_specular.data[face.index].color3 = vertex_specular[verts_in_face[2]][0:3]
        
    vtex_specular = me.tessface_vertex_colors.new()
    vtex_specular.name = "vertex_specular_alpha"
    for face in faces:
        verts_in_face = face.vertices[:]
        alpha0 = (vertex_specular[verts_in_face[0]][3], vertex_specular[verts_in_face[0]][3], vertex_specular[verts_in_face[0]][3])
        alpha1 = (vertex_specular[verts_in_face[1]][3], vertex_specular[verts_in_face[1]][3], vertex_specular[verts_in_face[1]][3])
        alpha2 = (vertex_specular[verts_in_face[2]][3], vertex_specular[verts_in_face[2]][3], vertex_specular[verts_in_face[2]][3])
        vtex_specular.data[face.index].color1 = alpha0
        vtex_specular.data[face.index].color2 = alpha1
        vtex_specular.data[face.index].color3 = alpha2

def setVertexBlendweightColors(me, faces, vertex_blendweight):
    vtex_blendweight = me.tessface_vertex_colors.new()
    vtex_blendweight.name = "vertex_blendweight_xyz"
    for face in faces:
        verts_in_face = face.vertices[:]
        vtex_blendweight.data[face.index].color1 = vertex_blendweight[verts_in_face[0]][0:3]
        vtex_blendweight.data[face.index].color2 = vertex_blendweight[verts_in_face[1]][0:3]
        vtex_blendweight.data[face.index].color3 = vertex_blendweight[verts_in_face[2]][0:3]
        
    vtex_blendweight = me.tessface_vertex_colors.new()
    vtex_blendweight.name = "vertex_blendweight_w"
    for face in faces:
        verts_in_face = face.vertices[:]
        alpha0 = (vertex_blendweight[verts_in_face[0]][3], vertex_blendweight[verts_in_face[0]][3], vertex_blendweight[verts_in_face[0]][3])
        alpha1 = (vertex_blendweight[verts_in_face[1]][3], vertex_blendweight[verts_in_face[1]][3], vertex_blendweight[verts_in_face[1]][3])
        alpha2 = (vertex_blendweight[verts_in_face[2]][3], vertex_blendweight[verts_in_face[2]][3], vertex_blendweight[verts_in_face[2]][3])
        vtex_blendweight.data[face.index].color1 = alpha0
        vtex_blendweight.data[face.index].color2 = alpha1
        vtex_blendweight.data[face.index].color3 = alpha2        


def bone_transform(joint_matrix):
    m = mathutils.Matrix(joint_matrix)
    m = m.inverted().transposed()
    rot = axis_conversion(from_forward='-Z', from_up='Y').to_4x4()
    m = rot * m
    return m

def make_skel(amt, crf_jointmap, parent_id):
    crf_joint = crf_jointmap.joint_list[parent_id]
    crf_bone = crf_jointmap.bone_dict[parent_id]
    m = bone_transform(crf_joint.matrix)
    
    if len(crf_bone.child_list) == 0:
        return
    if parent_id == 0: #if root bone
        bone = amt.edit_bones.new(crf_bone.bone_name.decode('UTF-8'))            
        bone.head = (0,0,0)
        bone.tail = (0,-1,0)
        bone.transform(m)
        head = bone.head.copy()
        tail = bone.tail.copy() 
        bone.tail = (0,0,0)
        bone.tail = head
        bone.head = tail

    for child_id in crf_bone.child_list:
        crf_joint = crf_jointmap.joint_list[child_id]
        m = bone_transform(crf_joint.matrix)
        parent_name = crf_jointmap.bone_dict[parent_id].bone_name.decode('UTF-8')
        child_name = crf_jointmap.bone_dict[child_id].bone_name.decode('UTF-8')
        bone = amt.edit_bones.new(child_name)
        bone.head = (0,0,0)
        bone.tail = (0,0,0.2)
        bone.transform(m)
        bone.parent = amt.edit_bones[parent_name]        
        head = bone.head.copy()
        tail = bone.tail.copy() 
        bone.tail = (0,0,0)                
        amt.edit_bones[child_name].head = amt.edit_bones[parent_name].tail
        amt.edit_bones[child_name].tail = head
        bone.use_connect = True
        make_skel(amt, crf_jointmap, child_id)
              
def load(operator, context, filepath,
         global_clamp_size=0.0,
         use_verbose=False,
         dump_first_only=False,
         use_uv_map=True,
         use_diffuse_texture=True,
         use_normal_texture=True,
         use_specular_texture=True,         
         use_computed_normals=False,
         use_shadeless=True,
         viz_normals=True,
         viz_blendweights=False,
         use_specular=True,
         global_matrix=None,
         ):
    '''
    Called by the user interface or another script.
    load_obj(path) - should give acceptable results.
    This function passes the file and sends the data off
        to be split into objects and then converted into mesh objects
    '''
    print('\nimporting crf %r' % filepath)

    filepath = os.fsencode(filepath)

    if global_matrix is None:
        global_matrix = mathutils.Matrix()

    new_objects = []  # put new objects here
    
    time_main = time.time()
    print("\tparsing crf file...")
    time_sub = time.time()

    file = open(filepath, "rb")
    CRF = CRF_object()    
    CRF.parse_bin(file)
    meshfile = CRF.meshfile

    bad_vertex_list = []
    
    # start importing meshes
    for i in range(0, meshfile.num_meshes):
        verts_loc = []
        verts_tex0 = []
        verts_tex1 = []
        faces = []  # tuples of the faces
        face_tex = [] # tuples of uv coordinates for faces
        vertex_normals = []
        vertex_specular = []
        vertex_blendweights1 = []        
        
        mesh = meshfile.meshes[i]
        faces = mesh.face_list
        
        #convert from DirectX to Blender face vertex ordering
        bad_mesh_vertex_list = []
        for i in range(0, len(faces)):
            v1,v2,v3 = faces[i]
            # if there are duplicated vertices in triangle, delete that face by making all vertices the same
            if v1 == v2 or v1 == v3 or v2 == v3:
                print("Found a bad face %i, eliminating %i,%i,%i" % (i,v1,v2,v3))
                faces[i] = (v3,v3,v3)
                bad_mesh_vertex_list.append(v1)
                bad_mesh_vertex_list.append(v2)
                bad_mesh_vertex_list.append(v3)
            else:
                faces[i] = (v3,v2,v1)
        bad_vertex_list.append(bad_mesh_vertex_list)
        
        for vertex in mesh.vertices0:
            verts_loc.append( (vertex.x_blend, vertex.y_blend, vertex.z_blend) )            
            verts_tex0.append( (vertex.u0_blend, vertex.v0_blend) )        

            vertex_normals.append( (vertex.normal_x_blend, vertex.normal_y_blend, vertex.normal_z_blend, vertex.normal_w_blend) )
            vertex_specular.append( (vertex.specular_red_blend, vertex.specular_green_blend, vertex.specular_blue_blend, vertex.specular_alpha_blend) )
            vertex_blendweights1.append( (vertex.blendweights1_x_blend, vertex.blendweights1_y_blend, vertex.blendweights1_z_blend, vertex.blendweights1_w_blend) )
        
        # deselect all
        if bpy.ops.object.select_all.poll():
            bpy.ops.object.select_all(action='DESELECT')

        # create blender mesh
        me = bpy.data.meshes.new("Dumped_Mesh")   # create a new mesh
        object_name = os.path.splitext(os.path.basename(filepath))[0]
        ob = bpy.data.objects.new(os.fsdecode(object_name) + "_%i" % mesh.mesh_number, me)
        # Fill the mesh with verts, edges, faces
        me.vertices.add(len(verts_loc))
        me.vertices.foreach_set("co", unpack_list(verts_loc))
        me.tessfaces.add(len(faces))
        me.tessfaces.foreach_set("vertices_raw", unpack_face_list(faces))
        
        
        # use computed normals
        if use_computed_normals:
            for vertex, vertex_normal in zip(me.vertices, vertex_normals):
                print("vertex index", vertex.index, vertex_normal)
                vertex.normal = vertex_normal[0:3]
                
        # fill face uv texture array
        for face in ob.data.tessfaces:
            verts_in_face = face.vertices[:]
            if use_verbose:
                print("face index", face.index)  
                print("normal", face.normal)  
                for vert in verts_in_face:  
                    print("vert", vert, " vert co", ob.data.vertices[vert].co)
                    print("Normal X:%s Y:%s Z:%s " % (vertex_normals[vert][0], vertex_normals[vert][1], vertex_normals[vert][2]))
                    print("specular R:%s G:%s B:%s " % (vertex_specular[vert][0], vertex_specular[vert][1], vertex_specular[vert][2]))
                    print("UV0: ", verts_tex0[vert])
                    print()
            i = face.index
            v1 = verts_in_face[0]
            v2 = verts_in_face[1]
            v3 = verts_in_face[2]
            face_tex.append([ verts_tex0[v1], verts_tex0[v2], verts_tex0[v3] ]) 
        
        # start all optional tasks        
        # add uv map
        if use_uv_map:
            uvMain = createTextureLayer("UV_Main", me, face_tex)

        # add texture
        if use_diffuse_texture or use_normal_texture or use_specular_texture:
            # create a material to which textures can be added
            mat = createMaterial('TexMat', use_shadeless, viz_normals)
            if use_diffuse_texture:
                diffuse_texture = mesh.materials.diffuse_texture            
                diffuse_texture_filepath = findTextureFile(os.fsdecode(filepath),  diffuse_texture.decode(sys.stdout.encoding))
                print("Adding diffuse texture ", diffuse_texture_filepath)        
                if diffuse_texture_filepath != None and diffuse_texture_filepath != "":
                    addDiffuseTexture(diffuse_texture_filepath, mat)
                    mat.use_transparency = True
                    mat.alpha = 0 #TODO check model data for this param
            if use_normal_texture:
                normal_texture = mesh.materials.normal_texture            
                normal_texture_filepath = findTextureFile(os.fsdecode(filepath),  normal_texture.decode(sys.stdout.encoding))
                print("Adding normals texture ", normal_texture_filepath)        
                if normal_texture_filepath != None and normal_texture_filepath != "":
                    addNormalTexture(normal_texture_filepath, mat)
            if use_specular_texture:
                specular_texture = mesh.materials.specular_texture            
                specular_texture_filepath = findTextureFile(os.fsdecode(filepath),  specular_texture.decode(sys.stdout.encoding))
                print("Adding normals texture ", specular_texture_filepath)        
                if specular_texture_filepath != None and specular_texture_filepath != "":
                    addSpecularTexture(specular_texture_filepath, mat)                            
            ob.data.materials.append(mat)

        # viz normals
                
        # add specular constant
        if use_specular:
            vertex_specular = []
            for vertex in mesh.vertices0:
                vertex_specular.append((vertex.specular_red_blend, vertex.specular_green_blend, vertex.specular_blue_blend, vertex.specular_alpha_blend))
                
            setVertexSpecularColors(me, ob.data.tessfaces, vertex_specular)
            # if no materials exist, create one+
            if len(ob.data.materials) == 0:
                mat = createMaterial('Specular', use_shadeless, viz_normals)
                mat.specular_color = mesh.materials.specular_constant
                ob.data.materials.append(mat)
            else:
                if mesh.materials.specular_constant != None:
                    ob.data.materials[0].specular_color = mesh.materials.specular_constant
                else:
                    ob.data.materials[0].specular_color = (1, 0, 0)
                    print("Failed to find specular constnat! FIXME")
                print(ob.data.materials[0].specular_color)
                      
        # viz blendweights
        
        # end all optional tasks
        
        me.update(calc_tessface=True, calc_edges=True)
        new_objects.append(ob)
    # end loop for importing meshes
    
    # import bones
    #TODO add bone weights
    #TODO attach armature to all meshes
    if CRF.footer.get_jointmap() != None:
        amt = bpy.data.armatures.new("Armature")
        amt_ob = bpy.data.objects.new("Armature", amt)
        scn = bpy.context.scene
        scn.objects.link(amt_ob)
        scn.objects.active = amt_ob
        amt_ob.select = True
        
        bpy.ops.object.mode_set(mode='EDIT')        
        make_skel(amt, CRF.jointmap, 0)
        """
        for key,value in CRF.jointmap.bone_dict.items():
            crf_joint = CRF.jointmap.joint_list[key]            
            m = mathutils.Matrix(crf_joint.matrix)
            m = m.inverted().transposed()
            print("Bone %i\n" % key, m, "parent", crf_joint.parent_id)
            rot = axis_conversion(from_forward='-Z', from_up='Y').to_4x4()
            m = rot * m
            crf_joint = CRF.jointmap.joint_list[key]
            bpy.ops.mesh.primitive_uv_sphere_add(size=0.1, location=(0,0,0))
            bpy.context.object.matrix_world = m
            bpy.context.object.name = "joint_%s" % key
        """            
        bpy.ops.object.mode_set(mode='OBJECT')
    #TODO add skinning
    #select object and armature, parent armature to object
    ob.select = True
    amt_ob.select = True
    bpy.ops.object.parent_set(type='ARMATURE_NAME')
    """
    bpy.context.selected_objects        
    SWITCH to edit mode
    assign vertex to vertex group
    bpy.ops.object.vertex_group_assign()
    Name vertex group after bone.
    """
        
            
    time_new = time.time()
    print("%.4f sec" % (time_new - time_sub))
    time_sub = time_new

    print('\tloading materials and images...')


    time_new = time.time()
    print("%.4f sec" % (time_new - time_sub))
    time_sub = time_new
    
    # Create new obj
    scene = context.scene    
    for ob,bad_vertices in zip(new_objects,bad_vertex_list):
        base = scene.objects.link(ob)
        base.select = True

        # we could apply this anywhere before scaling.
        ob.matrix_world = global_matrix
        
        #delete bad vertices
        bpy.context.scene.objects.active = ob 
        ob.select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for v in bad_vertices:
            print("Deleting vertex %i in %s" % (v, ob.name))
            ob.data.vertices[v].select = True        
        bpy.ops.object.mode_set(mode='EDIT')        
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        

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


