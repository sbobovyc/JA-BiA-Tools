import bpy


def main(context):
    obj = bpy.context.active_object
    print(obj)
    mesh = obj.data
    print(mesh)
    print()
    
    old_verts = {}
    new_verts = {}
    faces = {}
    
    for vert in mesh.vertices:
        print("Vertex index", vert.index, vert.co)
        old_verts[vert.index] = vert.co
        print(old_verts[vert.index])
    print()
    
    for face in mesh.faces:
        print("Face index", face.index, face.vertices[:])
    print()
    
    for face in mesh.faces:
        print("Face index", face.index, face.vertices[:])
        create_new_v1 = False
        create_new_v2 = False
        create_new_v3 = False
        if face.vertices[0] in new_verts:
            create_new_v1 = True
        if face.vertices[1] in new_verts:
            create_new_v2 = True            
        if face.vertices[2] in new_verts:
            create_new_v3 = True            
            
        if create_new_v1 or create_new_v2 or create_new_v3:
            print("True")
            new_v1 = face.vertices[0]
            new_v2 = face.vertices[1]            
            new_v3 = face.vertices[2]            
            if create_new_v1:
                new_verts[len(new_verts)+1] = old_verts[new_v1]
                print("Created vertex", old_verts[new_v1])
            if create_new_v2:
                new_verts[len(new_verts)+1] = old_verts[new_v2]
                print("Created vertex", old_verts[new_v2])                
            if create_new_v1:
                new_verts[len(new_verts)+1] = old_verts[new_v3]
                print("Created vertex", old_verts[new_v3])                     
            print("Created face", new_v1, new_v2, new_v3)
            faces[len(faces)+1] = (new_v1, new_v2, new_v3)      
        else:
            print("False")
            new_verts[face.vertices[0]] = face.vertices[0] 
            new_verts[face.vertices[1]] = face.vertices[1]
            new_verts[face.vertices[1]] = face.vertices[1]
            faces[face.index] = (face.vertices[0], face.vertices[1], face.vertices[2])  

    print()            
    print(new_verts)
    print()                
    print(faces)


    

class SimpleOperator(bpy.types.Operator):
    '''Tooltip'''
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
