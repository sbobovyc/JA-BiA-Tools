from __future__ import print_function
import argparse
import sys
import os

with_graph = True
try:
    import pydot
except ImportError, err:
    print("Pydot not installed, will not create graph.")
    with_graph = False
    

import crf_objects

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool that can parse Jagged Alliance: BiA crf files.', \
                                epilog='Example: python crf_magick.py --write -s 10 -t 0 10 0 akm_01.crf new_akm.crf')    
    parser.add_argument('file', nargs='?', help='Input file')
    parser.add_argument('outfile', nargs='?', default='dump.crf', help='Output file')
    parser.add_argument('outdir', nargs='?', default=os.getcwd(), help='Output directory')
    parser.add_argument('-i', '--info', default=False, action='store_true', help='Print information about file')
    parser.add_argument('-d', '--diff', default=False, action='store_true', help='Diff two files')
    parser.add_argument('-b', '--boneinfo', default=False, action='store_true', help='Print information about bones and if pydot/graphiz are installed create graph.')
    parser.add_argument('-w', '--write', default=False, action='store_true', help='Write file')
    parser.add_argument('-s', '--scale', default=1.0, action='store', type=float, help='Uniform scale factor')
    parser.add_argument('-t', '--translate', nargs=3, default=[0, 0, 0], action='store', type=float, help='Translation')    
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='Print verbose information.')
    
    args = parser.parse_args()
    infile1 = args.file
    outfile = args.outfile
    outdir = args.outdir
    info = args.info
    diff = args.diff
    boneinfo = args.boneinfo
    write = args.write
    scale_factor = args.scale
    translation = args.translate
    verbose = args.verbose
    
    path = os.path.abspath(infile1)
    outfile = os.path.abspath(outfile)
    print("File:",path)
    
    fp = open(path, "rb")    
    obj = crf_objects.CRF_object()
    obj.parse_bin(fp, verbose)
    fp.close()

    if diff:
    	fp = open(outfile, "rb")
    	obj2 = crf_objects.CRF_object()
    	obj2.parse_bin(fp, verbose)
    	fp.close()
    
        for mesh1, mesh2 in zip(obj.meshfile.meshes, obj2.meshfile.meshes):
            formatter_header = "{0:<10s} {1:<10s} {2:<10s} {3:<10s} {4:<10s} {5:<10s} {6:<10s}\n"
            formatter = "{0:<10s} {1:<10f} {2:<10f} {3:<10f} {4:<10s} {5:<10s} {6:<10s}\n"
            for v_ob1,v_ob2 in zip(mesh1.vertices0, mesh2.vertices0):
    	        string = ""
    	        string += formatter_header.format("index", "x_delta", "y_delta", "z_delta", "nx_delta","ny_delta", "nz_delta")
    	        string += formatter.format(str(v_ob1.index), v_ob1.x - v_ob2.x, v_ob1.y - v_ob2.y, v_ob1.z - v_ob2.z,
                                            str(v_ob1.normal_x - v_ob2.normal_x), str(v_ob1.normal_y - v_ob2.normal_y), str(v_ob1.normal_z - v_ob2.normal_z))
    	        print(string)
        sys.exit()

    if scale_factor != 1.0:
        obj.meshfile.scale(scale_factor)

    if translation != [0,0,0]:
        obj.meshfile.translate(translation)

    if info:
        print(obj.meshfile)
        sys.exit(0)
        
    if boneinfo:
        if obj.skeleton != None:
            print(obj.jointmap)
            print(obj.skeleton)
            if with_graph:
                graph = pydot.Dot(graph_type='digraph')
                for key in obj.jointmap.bone_dict:
                    parent = "%s : %s" % (obj.jointmap.bone_dict[key].bone_name, key)
                    child_ids = obj.jointmap.bone_dict[key].child_list
                    children = map(lambda x: "%s : %s" % (obj.jointmap.bone_dict[x].bone_name, x), child_ids)
                    for child in children:                    
                        graph.add_edge(pydot.Edge(parent, child))
                graph.write_png(os.path.basename(infile1).split('.')[0] + "_bonegraph.png")

    if write:
        fp = open(outfile, "wb")
        fp.write(obj.get_bin())
        fp.close()
