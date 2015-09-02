#!/usr/bin/env python
"""
Created on February 18, 2012

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
from cui_file import CUI_file

parser = argparse.ArgumentParser(description='Tool that can unpack/pack Jagged Alliance: BiA cui files.', epilog='')

parser.add_argument('file', nargs='?', help='Input file')
parser.add_argument('outdir', nargs='?', default=os.getcwd(), help='Output directory')
parser.add_argument('-i', '--info', default=False, action='store_true', help='Output information about cui file')
parser.add_argument('-d', '--debug', default=False, action='store_true', help='Show debug messages.')


args = parser.parse_args()
infile = args.file
outdir = args.outdir
info = args.info
debug = args.debug

if infile is not None and os.path.splitext(infile)[1][1:].strip() == "cui":
    cui_filepath = os.path.abspath(infile)
    print "Unpacking %s" % cui_filepath
    cui_file = CUI_file(filepath=cui_filepath)
    cui_file.open()
    cui_file.unpack(peek=info, verbose=debug)

    if not info:
        output_filepath = os.path.abspath(outdir)
        cui_file.dump2yaml(outdir)

elif infile is not None and os.path.splitext(infile)[1][1:].strip() == "txt":
    yaml_cui_filepath = os.path.abspath(infile)
    cui_file_name = os.path.basename(infile).split('.')[0] + ".cui"
    cui_filepath = os.path.join(os.path.abspath(outdir), cui_file_name)

    print "Packing %s" % yaml_cui_filepath
    cui_file = CUI_file(filepath=cui_filepath)
    cui_file.yaml2bin(yaml_cui_filepath)

else:
    print "Nothing happened"
    parser.print_help()
