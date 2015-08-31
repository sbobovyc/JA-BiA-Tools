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

import os
import time
import struct
import bpy
import mathutils
import bpy_extras.io_utils

from .crf_objects import CRF_object,CRF_header,CRF_meshfile,CRF_mesh,CRF_vertex,CRF_vertex_blend,CRF_materials,CRF_entry,CRF_entry_descriptor


def _write(context, filepath,
              EXPORT_USE_VERBOSE,
              EXPORT_TRI,  # ok
              EXPORT_EDGES,
              EXPORT_NORMALS,  # not yet
              EXPORT_UV,  # ok
              EXPORT_MTL,
              EXPORT_APPLY_MODIFIERS,  # ok
              EXPORT_BLEN_OBS,
              EXPORT_GROUP_BY_OB,
              EXPORT_GROUP_BY_MAT,
              EXPORT_KEEP_VERT_ORDER,
              EXPORT_POLYGROUPS,
              EXPORT_CURVE_AS_NURBS,
              EXPORT_SEL_ONLY,  # ok
              EXPORT_ANIMATION,
              EXPORT_GLOBAL_MATRIX,
              EXPORT_PATH_MODE,
              ):  # Not used

    verbose = EXPORT_USE_VERBOSE
    base_name, ext = os.path.splitext(filepath)
    context_name = [base_name, '', '', ext]  # Base name, scene name, frame number, extension
    file = open(filepath, "wb")

    scene = context.scene
    orig_frame = scene.frame_current


    print('\nexporting crf %r' % filepath)
    time1 = time.time()
    num_meshes = len(bpy.context.selected_objects)
    if num_meshes < 1:
        raise Exception("Must select at least one object to export CRF")
    print("Number of meshes", num_meshes)
    ob_primary = bpy.context.selected_objects[0]
    print(ob_primary)

    # Exit edit mode before exporting, so current object states are exported properly.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
        

    matrix_world = ob_primary.matrix_basis # world matrix so we can transform from local to global coordinates
    
    meshfile = CRF_meshfile()
    LoX = -ob_primary.bound_box[4][0]    
    LoY = ob_primary.bound_box[4][1]
    LoZ = ob_primary.bound_box[4][2]
    HiX = -ob_primary.bound_box[2][0]
    HiY = ob_primary.bound_box[2][1]
    HiZ = ob_primary.bound_box[2][2]
    meshfile.num_meshes = len(bpy.context.selected_objects)
    meshfile.model_bounding_box = ((LoX, LoY, LoZ), (HiX, HiY, HiZ))
    print("Bounding box (%f, %f, %f) (%f, %f, %f)" % (LoX, LoY, LoZ, HiX, HiY, HiZ))

    
    # start mesh export loop
    mesh_number = 0
    for ob in bpy.context.selected_objects:
        # get blender data
        blender_mesh = ob.data
        
        crf_mesh = CRF_mesh()
        crf_mesh.mesh_number = mesh_number
        mesh_number = mesh_number + 1

        crf_mesh.number_of_vertices = len(blender_mesh.vertices)
        crf_mesh.number_of_faces = len(blender_mesh.polygons)
        
        # mesh bounding box
        LoX = -ob.bound_box[4][0]
        LoY = ob.bound_box[4][1]
        LoZ = ob.bound_box[4][2]
        HiX = -ob.bound_box[2][0]
        HiY = ob.bound_box[2][1]
        HiZ = ob.bound_box[2][2]
        crf_mesh.bounding_box = ((LoX, LoY, LoZ), (HiX, HiY, HiZ))

        crf_mesh.stream_count = 2
        layout = 0xc018021 #TODO magic number
        stride = 32
        crf_mesh.vertex_stream0_layout = [layout, stride]
        layout = 0x80000 #TODO magic number
        stride = 8
        crf_mesh.vertex_stream1_layout = [layout, stride]
        print(crf_mesh)                
        
        # face/vertex index list
        #TODO, the first face always has the first two vertices switched. Don't know if this will affect
        # anything. Need to verify that this does not cause a problem.
        
        for face in blender_mesh.polygons:
            verts_in_face = (face.vertices[2],face.vertices[1],face.vertices[0])
            if verbose:
                print("face index %s, verts %s" % (face.index, verts_in_face))
            crf_mesh.face_list.append(verts_in_face)
                    
        
        # make sure to create uv texture layers before vertex color layers, otherwise uv layer will overwrite a vertex color layer
        if len(blender_mesh.uv_textures) == 2:
            uv_tex0 = blender_mesh.uv_textures[0]
            uv_tex1 = blender_mesh.uv_textures[1]
        elif len(blender_mesh.uv_textures) == 1:
            uv_tex0 = blender_mesh.uv_textures[0]
            uv_tex1 = blender_mesh.uv_textures.new()
            uv_tex1.name = "UV_Secondary"
        else:
            uv_tex0 = blender_mesh.uv_textures.new()
            uv_tex0.name = "UV_Main"
            uv_tex1 = blender_mesh.uv_textures.new()
            uv_tex1.name = "UV_Secondary"
        
        blender_mesh.update(calc_tessface=True)
        uv_tex0 = blender_mesh.tessface_uv_textures[0]
        uv_tex1 = blender_mesh.tessface_uv_textures[1]
        
        # vertices, normals, ks, and UVs
        if "vertex_specular_colors" in blender_mesh.tessface_vertex_colors:
            vtex_specular_colors = blender_mesh.tessface_vertex_colors["vertex_specular_colors"]
        else:
            vtex_specular_colors_m = blender_mesh.vertex_colors.new()
            vtex_specular_colors_m.name = "vertex_specular_colors"
            blender_mesh.update(calc_tessface=True)
            vtex_specular_colors = blender_mesh.tessface_vertex_colors["vertex_specular_colors"]

        if "vertex_specular_alpha" in blender_mesh.tessface_vertex_colors:
            vtex_specular_alpha = blender_mesh.tessface_vertex_colors["vertex_specular_alpha"]
        else:
            vtex_specular_alpha_m = blender_mesh.vertex_colors.new()
            vtex_specular_alpha_m.name = "vertex_specular_alpha"
            blender_mesh.update(calc_tessface=True)
            vtex_specular_alpha = blender_mesh.tessface_vertex_colors["vertex_specular_alpha"]

        if "vertex_blendweight_xyz" in blender_mesh.tessface_vertex_colors:
            vtex_blendweights_xyz = blender_mesh.tessface_vertex_colors["vertex_blendweight_xyz"]
        else:
            vtex_blendweights_xyz_m = blender_mesh.vertex_colors.new()
            vtex_blendweights_xyz_m.name = "vertex_blendweight_xyz"
            blender_mesh.update(calc_tessface=True)
            vtex_blendweights_xyz = blender_mesh.tessface_vertex_colors["vertex_blendweight_xyz"]

        if "vertex_blendweight_w" in blender_mesh.tessface_vertex_colors:
            vtex_blendweights_w = blender_mesh.tessface_vertex_colors["vertex_blendweight_w"]
        else:
            vtex_blendweights_w_m = blender_mesh.vertex_colors.new()
            vtex_blendweights_w_m.name = "vertex_blendweight_w"
            blender_mesh.update(calc_tessface=True)
            vtex_blendweights_w = blender_mesh.tessface_vertex_colors["vertex_blendweight_w"]        

        vert_dict = {} # will store CRF_vertex objects
        for face in blender_mesh.tessfaces:
            verts_in_face = face.vertices[:]
            if not verts_in_face[0] in vert_dict:
                vert = CRF_vertex()
                vert.index = verts_in_face[0]
                # get vertex coords and make sure to translate from local to global
                vert.x_blend, vert.y_blend, vert.z_blend = matrix_world * blender_mesh.vertices[verts_in_face[0]].co.xyz 
                vert.normal_x_blend, vert.normal_y_blend, vert.normal_z_blend = blender_mesh.vertices[verts_in_face[0]].normal
                vert.normal_w_blend = 1.0
                vert.specular_blue_blend = vtex_specular_colors.data[face.index].color1[2] 
                vert.specular_green_blend = vtex_specular_colors.data[face.index].color1[1] 
                vert.specular_red_blend = vtex_specular_colors.data[face.index].color1[0] 
                vert.specular_alpha_blend = vtex_specular_alpha.data[face.index].color1[0] # only use the first color for alpha       
                vert.u0_blend = uv_tex0.data[face.index].uv1[0] 
                vert.v0_blend = uv_tex0.data[face.index].uv1[1]
                vert.u1_blend = uv_tex1.data[face.index].uv1[0] 
                vert.v1_blend = uv_tex1.data[face.index].uv1[1]
                vert.blendweights1_x_blend = vtex_blendweights_xyz.data[face.index].color1[0]
                vert.blendweights1_y_blend = vtex_blendweights_xyz.data[face.index].color1[1]
                vert.blendweights1_z_blend = vtex_blendweights_xyz.data[face.index].color1[2]
                vert.blendweights1_w_blend = vtex_blendweights_w.data[face.index].color1[0] # only use the first color for w       
                vert.blend2raw()
                vert_dict[verts_in_face[0]] = vert # put object in dictionary
                if verbose:
                    print(vert)

            if not verts_in_face[1] in vert_dict:
                vert = CRF_vertex()
                vert.index = verts_in_face[1]
                # get vertex coords and make sure to translate from local to global
                vert.x_blend, vert.y_blend, vert.z_blend = matrix_world * blender_mesh.vertices[verts_in_face[1]].co.xyz
                vert.normal_x_blend, vert.normal_y_blend, vert.normal_z_blend = blender_mesh.vertices[verts_in_face[1]].normal
                vert.normal_w_blend = 1.0
                vert.specular_blue_blend = vtex_specular_colors.data[face.index].color2[2] 
                vert.specular_green_blend = vtex_specular_colors.data[face.index].color2[1] 
                vert.specular_red_blend = vtex_specular_colors.data[face.index].color2[0] 
                vert.specular_alpha_blend = vtex_specular_alpha.data[face.index].color1[0] # only use the first color for alpha              
                vert.u0_blend = uv_tex0.data[face.index].uv2[0] 
                vert.v0_blend = uv_tex0.data[face.index].uv2[1]
                vert.u1_blend = uv_tex1.data[face.index].uv2[0] 
                vert.v1_blend = uv_tex1.data[face.index].uv2[1]
                vert.blendweights1_x_blend = vtex_blendweights_xyz.data[face.index].color1[0]
                vert.blendweights1_y_blend = vtex_blendweights_xyz.data[face.index].color1[1]
                vert.blendweights1_z_blend = vtex_blendweights_xyz.data[face.index].color1[2]
                vert.blendweights1_w_blend = vtex_blendweights_w.data[face.index].color1[0] # only use the first color for w
                vert.blend2raw()
                vert_dict[verts_in_face[1]] = vert # put object in dictionary
                if verbose:
                    print(vert)     

            if not verts_in_face[2] in vert_dict:
                vert = CRF_vertex()
                vert.index = verts_in_face[2]
                # get vertex coords and make sure to translate from local to global
                vert.x_blend, vert.y_blend, vert.z_blend = matrix_world * blender_mesh.vertices[verts_in_face[2]].co.xyz
                vert.normal_x_blend, vert.normal_y_blend, vert.normal_z_blend = blender_mesh.vertices[verts_in_face[2]].normal     
                vert.normal_w_blend = 1.0
                vert.specular_blue_blend = vtex_specular_colors.data[face.index].color3[2] 
                vert.specular_green_blend = vtex_specular_colors.data[face.index].color3[1] 
                vert.specular_red_blend = vtex_specular_colors.data[face.index].color3[0] 
                vert.specular_alpha_blend = vtex_specular_alpha.data[face.index].color1[0] # only use the first color for alpha              
                vert.u0_blend = uv_tex0.data[face.index].uv3[0] 
                vert.v0_blend = uv_tex0.data[face.index].uv3[1]
                vert.u1_blend = uv_tex1.data[face.index].uv3[0] 
                vert.v1_blend = uv_tex1.data[face.index].uv3[1]
                vert.blendweights1_x_blend = vtex_blendweights_xyz.data[face.index].color1[0]
                vert.blendweights1_y_blend = vtex_blendweights_xyz.data[face.index].color1[1]
                vert.blendweights1_z_blend = vtex_blendweights_xyz.data[face.index].color1[2]
                vert.blendweights1_w_blend = vtex_blendweights_w.data[face.index].color1[0] # only use the first color for w
                vert.blend2raw()
                vert_dict[verts_in_face[2]] = vert # put object in dictionary
                if verbose:
                    print(vert)    
        
        for key, vertex in vert_dict.items():
            if verbose:
                print(vertex)
            crf_mesh.vertices0.append(vertex)
            crf_mesh.vertices1.append(CRF_vertex_blend()) #TODO this works with static models
        # end mesh geometry and UVs

        # begin materials
        diffuse_texture_file = None
        normals_texture_file = None
        specular_texture_file = None
                
        print(blender_mesh.materials[0].texture_slots[0])
        print(blender_mesh.materials[0].texture_slots[1])        
        if blender_mesh.materials[0].texture_slots[0] == None and blender_mesh.materials[0].texture_slots[1] == None:
               raise Exception("Missing a diffuse or normal texture")
        else:
            diffuse_texture_file = blender_mesh.materials[0].texture_slots[0].texture.image.name
            normals_texture_file = blender_mesh.materials[0].texture_slots[1].texture.image.name
            
        if blender_mesh.materials[0].texture_slots[2] == None:
            print("Using a constant specular value")
        else:
            specular_texture_file = blender_mesh.materials[0].texture_slots[2].texture.image.name


        # strip extension from filenames
        diffuse_texture_file = os.path.splitext(diffuse_texture_file)[0]
        normals_texture_file = os.path.splitext(normals_texture_file)[0]
        if specular_texture_file != None:
            specular_texture_file = os.path.splitext(specular_texture_file)[0]

        # get diffuse and specular material color
        diffuse_material_color = blender_mesh.materials[0].diffuse_color
        specular_material_color = blender_mesh.materials[0].specular_color
        print("Textures:", diffuse_texture_file, normals_texture_file, specular_texture_file)

        materials = CRF_materials()
        materials.material_type = b'nm' #TODO magic number
        materials.material_subtype = 0x100000004000000 #TODO magic number 
        materials.diffuse_texture = str.encode(diffuse_texture_file)
        materials.normal_texture = str.encode(normals_texture_file)
        materials.specular_constant = specular_material_color
                
        if specular_texture_file != None:
            materials.custom_data_count = 2
            materials.custom1_1 = (0,0,0,1) #TODO magic number
            materials.specular_texture = str.encode(specular_texture_file)            
        else:
            materials.custom_data_count = 1
        crf_mesh.materials = materials
        # end of materials
        
        meshfile.meshes.append(crf_mesh)
    # end of all meshes
    
    # create object and fill in data structures    
    crf_object = CRF_object()
    
    footer_root_entry = CRF_entry()
    footer_root_entry.create_rootnode()
    footer_meshfile_entry = CRF_entry()
    footer_meshfile_entry.create_meshfile(len(meshfile.get_bin()))    
    crf_object.footer.entries.append(footer_root_entry)
    crf_object.footer.entries.append(footer_meshfile_entry)
        
    footer_root_entry_descriptor = CRF_entry_descriptor()
    footer_root_entry_descriptor.create_rootnode()
    footer_meshfile_entry_descriptor = CRF_entry_descriptor()
    footer_meshfile_entry_descriptor.create_meshfile() 
    crf_object.footer.entry_descriptors.append(footer_root_entry_descriptor)
    crf_object.footer.entry_descriptors.append(footer_meshfile_entry_descriptor)
    
    crf_object.meshfile = meshfile
    
    
    # end of header
    
    file.write(crf_object.get_bin())
    """
    # entries describing what's in the file
    trailer_1 = file.tell() 
    meshfile_size = trailer_1 - 0x14 # calculate size of meshfile 
    root_node_entry = CRF_entry()
    root_node_entry.create_rootnode()
    file.write(root_node_entry.get_bin())
    meshfile_entry = CRF_entry()
    meshfile_entry.create_meshfile(meshfile_size)
    file.write(meshfile_entry.get_bin())
    
    trailer_1_end = file.tell()

    # put trailer1 and trailer2 offsets into the file header
    file.seek(0x08)
    file.write(struct.pack("<I", trailer_1)) # trailer1 file offset
    file.write(struct.pack("<I", trailer_1_end)) # trailer2 file offset

    # entry descriptions    
    file.seek(trailer_1_end)
    root_node_entry_description = CRF_entry_descriptor()
    root_node_entry_description.create_rootnode()
    file.write(root_node_entry_description.get_bin())
    meshfile_entry_description = CRF_entry_descriptor()
    meshfile_entry_description.create_meshfile()
    file.write(meshfile_entry_description.get_bin())
    """
    file.close()
    print("CRF Export time: %.2f" % (time.time() - time1))
    # Restore old active scene.
#   orig_scene.makeCurrent()
#   Window.WaitCursor(0)


'''
Currently the exporter lacks these features:
* multiple scene export (only active scene is written)
* particles
'''


def save(operator, context, filepath="",
         use_verbose=False,
         use_triangles=False,
         use_edges=True,
         use_normals=False,
         use_uvs=True,
         use_materials=True,
         use_apply_modifiers=True,
         use_blen_objects=True,
         group_by_object=False,
         group_by_material=False,
         keep_vertex_order=False,
         use_vertex_groups=False,
         use_nurbs=True,
         use_selection=True,
         use_animation=False,
         global_matrix=None,
         path_mode='AUTO'
         ):

    _write(context, filepath,
           EXPORT_USE_VERBOSE=use_verbose,
           EXPORT_TRI=use_triangles,
           EXPORT_EDGES=use_edges,
           EXPORT_NORMALS=use_normals,
           EXPORT_UV=use_uvs,
           EXPORT_MTL=use_materials,
           EXPORT_APPLY_MODIFIERS=use_apply_modifiers,
           EXPORT_BLEN_OBS=use_blen_objects,
           EXPORT_GROUP_BY_OB=group_by_object,
           EXPORT_GROUP_BY_MAT=group_by_material,
           EXPORT_KEEP_VERT_ORDER=keep_vertex_order,
           EXPORT_POLYGROUPS=use_vertex_groups,
           EXPORT_CURVE_AS_NURBS=use_nurbs,
           EXPORT_SEL_ONLY=use_selection,
           EXPORT_ANIMATION=use_animation,
           EXPORT_GLOBAL_MATRIX=global_matrix,
           EXPORT_PATH_MODE=path_mode,
           )

    return {'FINISHED'}
