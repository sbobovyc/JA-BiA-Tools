""" Graphs CRF bone structure in file bones.bin. Pydot is required if you want to generate a graph.
http://code.google.com/p/pydot/
"""

import struct

with_graph = True
try:
    import pydot 
except ImportError, err:
    print "Pydot not installed, will not create graph."
    with_graph = False

def uint2float(uint_number):
    if uint_number > 128:
        return float(uint_number / 127.0)
    elif uint_number < 128:
        return float(-uint_number / 128.0)
    else:
        return 0.0
    
class Tree(object):
    def __init__(self):
        self.tree = {}

    def insert(self, node):
        if node.id in self.tree:
            return
        else:
            pass
        
class Node(object):
    def __init__(self, bone_id, name):
        self.id = bone_id
        self.name = name
        self.data = None
        self.children = []

    def get_data_raw(self):
        return self.data
    
    def get_data_scaled_255(self):
        quaternion = map(lambda x: x/255.0, self.data)
        return quaternion

    def get_data_scaled_128(self):
        quaternion = map(uint2float, self.data)
        return quaternion
        
    def add_child(self, child_id):
        self.children.append(child_id)

    def get_children(self, bone_dict):
        edge_list = []
        for child in self.children:
            parent = str(self.id) + "\n" + str(self.name) + "\n" + str(self.get_data_raw())
            child = str(child) + "\n" + str(bone_dict[child].name) + "\n" + str(bone_dict[child].get_data_raw())
            edge_list.append(pydot.Edge(parent, child))
        return edge_list
    
def graph(bones):
    graph = pydot.Dot(graph_type='digraph')

    for key,value in bones.items():
        for edge in value.get_children(bones):
            graph.add_edge(edge)

    graph.write_png('crf_bonegraph.png')

def read_bones():
    bone_dict = {}    
    with open("bones.bin", "rb") as f:
            bone_count, = struct.unpack("<I", f.read(4))
            print "Bone count", bone_count

##            print struct.unpack("<fff", f.read(12))
##            bone_count, = struct.unpack("<I", f.read(4))
##            print struct.unpack("<fff", f.read(12))
            for i in range(0, bone_count):
                print "Bone id:", i
                f11, f12, f13 = struct.unpack("<fff", f.read(12))
                uint1, = struct.unpack("<I", f.read(4))                
                f21, f22, f23 = struct.unpack("<fff", f.read(12))
                uint2, = struct.unpack("<I", f.read(4))                
                f31, f32, f33 = struct.unpack("<fff", f.read(12))
                uint3, = struct.unpack("<I", f.read(4))
                f41, f42, f43 = struct.unpack("<fff", f.read(12))
                uint4, = struct.unpack("<I", f.read(4))
                
                print f11, f12, f13
                print uint1
                print f21, f22, f23
                print uint2
                print f31, f32, f33
                print uint3
                print f41, f42, f43
                print uint4                
                print
                
            bone_count, = struct.unpack("<I", f.read(4))            
            print "Bone count", bone_count
            unknown, = struct.unpack("<I", f.read(4))
            #print unknown
            print
            
            for i in range(0, bone_count):
                bone_id,bone_name_length = struct.unpack("<II", f.read(8))
                bone_name, = struct.unpack("%is" % bone_name_length, f.read(bone_name_length))

                #print bone_name, "ID:", bone_id
                num_children, = struct.unpack("<I", f.read(4))
                #print "Number of children", num_children
                
                bone = Node(bone_id, bone_name)
                bone_dict[bone.id] = bone
                
                for i in range(0, num_children):
                    child, = struct.unpack("<I", f.read(4))
                    #print "Child", child
                    bone.add_child(child)
                #unknown, = struct.unpack("<f", f.read(4))
                unknown = struct.unpack("BBBB", f.read(4))
                bone.data = unknown
                

    return bone_dict

def print_bones(bone_dict):
    for key,value in bone_dict.items():
        print "ID:",key,"Name:",value.name
        print "{"
        print "//Unknown data, possibly a quaternion? Printing out in multiple scales."
        print "Raw:", ["%i" % val for val in value.get_data_raw()] 
        print "0 to 1:", ["%.4f" % val for val in value.get_data_scaled_255()]
        print "-1 to 1:", ["%.4f" % val for val in value.get_data_scaled_128()]
        
        print "Children bones:"
        for child in value.children:
            print "\t", bone_dict[child].name
        print "}"
        print
            
def read_animation():
    with open("animation.bin", "rb") as f:
        f.read(16)
        for i in range(0, 255):
            print hex(f.tell())
            byte, x, y, z, w, short, int1, int2 = struct.unpack("<BBBBBHxII", f.read(16))
            x = x/255.0
            y = y/255.0
            z = z/255.0
            w = w/255.0
            print byte, "%.3f %.3f %.3f %.3f" % (x, y, z, w), short, int1, int2

if __name__ == '__main__':    
    bones = read_bones()
    print_bones(bones)

    if with_graph:
        graph(bones)

    #read_animation()
