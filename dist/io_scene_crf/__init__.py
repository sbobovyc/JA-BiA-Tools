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

bl_info = {
    "name": "JABIA CRF format",
    "author": "Stanislav Bobovych",
    "version": (0, 8),
    "blender": (2, 6, 8),
    "location": "File > Import-Export",
    "description": "Import-Export CRF, Import CRF mesh, UV's, "
                   "materials and textures",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": 'TESTING',
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if "import_crf" in locals():
        imp.reload(import_crf)
    if "export_crf" in locals():
        imp.reload(export_crf)


import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       )
from bpy_extras.io_utils import (ExportHelper,
                                 ImportHelper,
                                 path_reference_mode,
                                 axis_conversion,
                                 )


class ImportCRF(bpy.types.Operator, ImportHelper):
    '''Load a JABIA CRF File'''
    bl_idname = "import_scene.crf"
    bl_label = "Import CRF"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".crf"
    filter_glob = StringProperty(
            default="*.crf",
            options={'HIDDEN'},
            )
    
    use_verbose = BoolProperty(
            name="Verbose",
            description="Verbose output to console",
            default=False,
            )   
    use_shadeless = BoolProperty(
            name="Shadeless Materials",
            description="Use shadeless materials",
            default=False,
            )
    
    viz_normals = BoolProperty(
        name="Visualize Normals",
        description="Use vertex colors to visualize normals",
        default=True,
        )

    viz_blendweights = BoolProperty(
        name="Visualize Blendweights",
        description="Use vertex colors to visualize blendweights",
        default=True,
        )
        
    use_specular = BoolProperty(
        name="Specular Colors",
        description="Use vertex colors to visualize what may be specular colors",
        default=True,
        )

    use_uv_map = BoolProperty(
        name="Import UV map",
        description="Import UV map",
        default=True,
        )
    
    use_diffuse_texture = BoolProperty(
        name="Use diffuse texture",
        description="Search subdirs for any assosiated diffuse texture " \
                    "(Warning, may be slow)",
        default=True,
        )
    use_normal_texture = BoolProperty(
        name="Use normal texture",
        description="Search subdirs for any assosiated normals texture " \
                    "(Warning, may be slow)",
        default=True,
        )
    use_specular_texture = BoolProperty(
        name="Use specular texture",
        description="Search subdirs for any assosiated specular texture " \
                    "(Warning, may be slow)",
        default=True,
        )        
    use_computed_normals = BoolProperty(
        name="Precomputed Normals",
        description="Use vertex normals stored in CRF",
        default=False,
        )

    global_clamp_size = FloatProperty(
            name="Clamp Scale",
            description="Clamp the size to this maximum (Zero to Disable)",
            min=0.0, max=1000.0,
            soft_min=0.0, soft_max=1000.0,
            default=0.0,
            )
    axis_forward = EnumProperty(
            name="Forward",
            items=(('X', "X Forward", ""),
                   ('Y', "Y Forward", ""),
                   ('Z', "Z Forward", ""),
                   ('-X', "-X Forward", ""),
                   ('-Y', "-Y Forward", ""),
                   ('-Z', "-Z Forward", ""),
                   ),
            default='-Z',
            )

    axis_up = EnumProperty(
            name="Up",
            items=(('X', "X Up", ""),
                   ('Y', "Y Up", ""),
                   ('Z', "Z Up", ""),
                   ('-X', "-X Up", ""),
                   ('-Y', "-Y Up", ""),
                   ('-Z', "-Z Up", ""),
                   ),
            default='Y',
            )

    def execute(self, context):
        # print("Selected: " + context.active_object.name)
        from . import import_crf

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "split_mode",
                                            ))

        global_matrix = axis_conversion(from_forward=self.axis_forward,
                                        from_up=self.axis_up,
                                        ).to_4x4()
        keywords["global_matrix"] = global_matrix

        return import_crf.load(self, context, **keywords)

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "use_verbose")
        row = layout.split(percentage=0.67)
        row.prop(self, "use_shadeless")        

        row = layout.split(percentage=0.67)
        row.prop(self, "viz_normals")
        row = layout.split(percentage=0.67)
        row.prop(self, "viz_blendweights")
        row = layout.split(percentage=0.67)
        row.prop(self, "use_specular")
        layout.prop(self, "use_uv_map")        
        layout.prop(self, "use_diffuse_texture")
        layout.prop(self, "use_normal_texture")
        layout.prop(self, "use_specular_texture")        
        layout.prop(self, "use_computed_normals")

        row = layout.split(percentage=0.67)
        row.prop(self, "global_clamp_size")
        layout.prop(self, "axis_forward")
        layout.prop(self, "axis_up")



class ExportCRF(bpy.types.Operator, ExportHelper):
    '''Save a JABIA CRF File'''

    bl_idname = "export_scene.crf"
    bl_label = 'Export CRF'
    bl_options = {'PRESET'}

    filename_ext = ".crf"
    filter_glob = StringProperty(
            default="*.crf",
            options={'HIDDEN'},
            )
    use_verbose = BoolProperty(
            name="Verbose",
            description="Verbose output to console",
            default=False,
            )
    
##    # context group
##    use_selection = BoolProperty(
##            name="Selection Only",
##            description="Export selected objects only",
##            default=False,
##            )
##    use_animation = BoolProperty(
##            name="Animation",
##            description="Write out an OBJ for each frame",
##            default=False,
##            )
##
##    # object group
##    use_apply_modifiers = BoolProperty(
##            name="Apply Modifiers",
##            description="Apply modifiers (preview resolution)",
##            default=True,
##            )
##
##    # extra data group
##    use_edges = BoolProperty(
##            name="Include Edges",
##            description="",
##            default=True,
##            )
##    use_normals = BoolProperty(
##            name="Include Normals",
##            description="",
##            default=False,
##            )
##    use_uvs = BoolProperty(
##            name="Include UVs",
##            description="Write out the active UV coordinates",
##            default=True,
##            )
##    use_materials = BoolProperty(
##            name="Write Materials",
##            description="Write out the MTL file",
##            default=True,
##            )
##    use_triangles = BoolProperty(
##            name="Triangulate Faces",
##            description="Convert all faces to triangles",
##            default=False,
##            )
##    use_nurbs = BoolProperty(
##            name="Write Nurbs",
##            description="Write nurbs curves as OBJ nurbs rather then "
##                        "converting to geometry",
##            default=False,
##            )
##    use_vertex_groups = BoolProperty(
##            name="Polygroups",
##            description="",
##            default=False,
##            )
##
##    # grouping group
##    use_blen_objects = BoolProperty(
##            name="Objects as OBJ Objects",
##            description="",
##            default=True,
##            )
##    group_by_object = BoolProperty(
##            name="Objects as OBJ Groups ",
##            description="",
##            default=False,
##            )
##    group_by_material = BoolProperty(
##            name="Material Groups",
##            description="",
##            default=False,
##            )
##    keep_vertex_order = BoolProperty(
##            name="Keep Vertex Order",
##            description="",
##            default=False,
##            )
##
##    global_scale = FloatProperty(
##            name="Scale",
##            description="Scale all data",
##            min=0.01, max=1000.0,
##            soft_min=0.01,
##            soft_max=1000.0,
##            default=1.0,
##            )
##
##    axis_forward = EnumProperty(
##            name="Forward",
##            items=(('X', "X Forward", ""),
##                   ('Y', "Y Forward", ""),
##                   ('Z', "Z Forward", ""),
##                   ('-X', "-X Forward", ""),
##                   ('-Y', "-Y Forward", ""),
##                   ('-Z', "-Z Forward", ""),
##                   ),
##            default='-Z',
##            )
##
##    axis_up = EnumProperty(
##            name="Up",
##            items=(('X', "X Up", ""),
##                   ('Y', "Y Up", ""),
##                   ('Z', "Z Up", ""),
##                   ('-X', "-X Up", ""),
##                   ('-Y', "-Y Up", ""),
##                   ('-Z', "-Z Up", ""),
##                   ),
##            default='Y',
##            )

    path_mode = path_reference_mode

    check_extension = True

    def execute(self, context):
        from . import export_crf

        from mathutils import Matrix
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            ))

##        global_matrix = Matrix()
##
##        global_matrix[0][0] = \
##        global_matrix[1][1] = \
##        global_matrix[2][2] = self.global_scale
##
##        global_matrix = (global_matrix *
##                         axis_conversion(to_forward=self.axis_forward,
##                                         to_up=self.axis_up,
##                                         ).to_4x4())
##
##        keywords["global_matrix"] = global_matrix
        return export_crf.save(self, context, **keywords)


def menu_func_import(self, context):
    self.layout.operator(ImportCRF.bl_idname, text="Compiled Resource File (.crf)")


def menu_func_export(self, context):
    self.layout.operator(ExportCRF.bl_idname, text="Compiled Resource File (.crf)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
