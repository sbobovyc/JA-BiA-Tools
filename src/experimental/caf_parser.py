import argparse
import struct
import os
import binascii

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for experimenting with BiA .caf files.')
    parser.add_argument('file', nargs='?', help='Input file')
    args = parser.parse_args()

    if args.file is not None:
        with open(args.file, "rb") as f:
            print args.file
            count1, = struct.unpack("<I", f.read(4))
            print "count1:", count1
            for i in range(0, count1):
                #print hex(f.tell())
                u1, = struct.unpack("<I", f.read(4))  # first transform in block
                u2, = struct.unpack("<I", f.read(4))  # number of transforms in block
                u3, = struct.unpack("<I", f.read(4))  # unknown
                u4, = struct.unpack("<I", f.read(4))  # possibly a timestamp
                print "\t", u1,u2,u3,hex(u4)
                if i == count1-1:
                    if u4 == 0xb34c17ab:
                        print "Good"
                    else:
                        print "Bad"
            print "########################################"

            count2, = struct.unpack("<I", f.read(4))
            print "count2:", count2
            # I think this is a list of 3x3 matrices representing transforms
            for i in range(0, count2):
                print hex(f.tell())
                row1 = struct.unpack("<fff", f.read(4*3))
                row2 = struct.unpack("<fff", f.read(4*3))
                row3 = struct.unpack("<fff", f.read(4*3))
                print "\t", row1
                print "\t", row2
                print "\t", row3
            print "########################################"

            frame_rate_mult, unk2 = struct.unpack("fI", f.read(8))
            print "Frame rate mult", frame_rate_mult
            print "Frame rate =", frame_rate_mult*30 
            print "Trailer", unk2 # unk2 is always either 0 or 1


            #file_size = os.path.getsize(args.file)
            #print "Remaining file size", file_size - f.tell()
            #print "Remaining word count", (file_size - f.tell())/4.0
            #while file_size - f.tell() > 0:
            #    print hex(f.tell())
            #    b = f.read(4)
            #    b_uint16_1 = struct.unpack("<H", b[0:2])
            #    b_uint16_2 = struct.unpack("<H", b[2:])
            #    b_uint32 = struct.unpack("<I", b)
            #    b_int32 = struct.unpack("<i", b)
            #    b_float = struct.unpack("f", b)
            #    print "\traw   ", "0x" + binascii.hexlify(b)
            #    print "\tuint16", b_uint16_1, b_uint16_2
            #    print "\tuint32", b_uint32
            #    print "\tint32 ", b_int32
            #    print "\tfloat ", b_float
            
