#!/usr/bin/env python
"""
Created on May 9, 2012

@author: sbobovyc
"""
"""
    Copyright (C) 2012 Stanislav Bobovych

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import os
from vtp_file import VTP_file

parser = argparse.ArgumentParser(
    description='Tool that can unpack/pack Jagged Alliance: BiA vtp files.',
    epilog='')

parser.add_argument('file', nargs='?', help='Input file')
parser.add_argument('outdir', nargs='?',
                    default=os.getcwd(), help='Output directory')
parser.add_argument('-i', '--info', default=False,
                    action='store_true', help='Output information about vtp file')
parser.add_argument('-d', '--debug', default=False,
                    action='store_true', help='Show debug messages.')


args = parser.parse_args()
infile = args.file
outdir = args.outdir
info = args.info
debug = args.debug

if infile is not None and os.path.splitext(infile)[1][1:].strip() == "vtp":
    vtp_filepath = os.path.abspath(infile)
    print("Unpacking %s" % vtp_filepath)
    vtp_file = VTP_file(filepath=vtp_filepath)
    vtp_file.open()
    vtp_file.unpack(peek=info, verbose=debug)

    if not info:
        output_filepath = os.path.abspath(outdir)
        vtp_file.dump2yaml(outdir)

elif infile is not None and os.path.splitext(infile)[1][1:].strip() == "txt":
    yaml_vtp_filepath = os.path.abspath(infile)
    vtp_file_name = os.path.basename(infile).split('.')[0] + ".vtp"
    vtp_filepath = os.path.join(os.path.abspath(outdir), vtp_file_name)

    print("Packing %s" % yaml_vtp_filepath)
    vtp_file = VTP_file(filepath=vtp_filepath)
    vtp_file.yaml2bin(yaml_vtp_filepath)

else:
    print("Nothing happened")
    parser.print_help()
