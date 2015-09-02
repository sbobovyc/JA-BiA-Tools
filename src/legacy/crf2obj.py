"""
Created on April 4, 2012

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
from crf_file import CRF_file

parser = argparse.ArgumentParser(description='Tool that can convert Jagged Alliance: BiA compiled resource (crf) files to Wavefront OBJ.', \
                                epilog='This is a tool for testing and will be replaced by a Blender plugin.')

parser.add_argument('file', nargs='?', help='Input file')

args = parser.parse_args()
file = args.file

if file != None and os.path.splitext(file)[1][1:].strip() == "crf":            
    crf_filepath = os.path.abspath(file)
    print "Converting %s" % crf_filepath
    crf_file = CRF_file(filepath=crf_filepath)
    crf_file.open()
    crf_file.unpack()

else:
    print "Nothing happened"
    parser.print_help()
        
