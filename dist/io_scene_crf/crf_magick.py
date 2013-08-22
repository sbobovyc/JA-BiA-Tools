import argparse
import sys
import os

import crf_objects

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool that can parse Jagged Alliance: BiA crf files.', \
                                epilog='Example: python crf_magick.py -s 10 -t 0 10 0 akm_01.crf new_akm.crf')    
    parser.add_argument('file', nargs='?', help='Input file')
    parser.add_argument('outfile', nargs='?', default='dump.crf', help='Output file')
    parser.add_argument('outdir', nargs='?', default=os.getcwd(), help='Output directory')
    parser.add_argument('-i', '--info', default=False, action='store_true', help='Print information about file')    
    parser.add_argument('-w', '--write', default=False, action='store_true', help='Write file')
    parser.add_argument('-s', '--scale', default=1.0, action='store', type=float, help='Uniform scale factor')
    parser.add_argument('-t', '--translate', nargs=3, default=[0, 0, 0], action='store', type=float, help='Translation')    

    args = parser.parse_args()
    file = args.file
    outfile = args.outfile
    outdir = args.outdir
    info = args.info
    write = args.write
    scale_factor = args.scale
    translation = args.translate
    
    path = os.path.abspath(file)
    outfile = os.path.abspath(outfile)
    print(path)
    
    file = open(path, "rb")    
    obj = crf_objects.CRF_object(file)
    file.close()

    if scale_factor != 1.0:
        obj.meshfile.scale(scale_factor)

    if translation != [0,0,0]:
        obj.meshfile.translate(translation)

    if info:
        print(obj.meshfile)
        
    if write:
        file = open(outfile, "wb")
        file.write(obj.get_bin())
        file.close()
