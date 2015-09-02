#!/usr/bin/env python
"""
Created on February 2, 2012

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
import sys
import multiprocessing
from pak_file import PAK_file

if __name__ == '__main__':
    # On Windows calling this function is necessary.
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    parser = argparse.ArgumentParser(description='Tool that can unpack Jagged Alliance: BiA pak/pak.crypt files.')

    parser.add_argument('file', nargs='?', help='Input file')
    parser.add_argument('outdir', nargs='?', help='Output directory')
    parser.add_argument('-i', '--info', default=False, action='store_true', help='Output information about pak file')
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='Show debug messages.')
    parser.add_argument('-p', '--parallel', default=False, action='store_true', help='Use multiple workers (This feature is experimental and will fail if not used from Python script)')

    args = parser.parse_args()
    infile = args.file
    outdir = args.outdir
    info = args.info
    debug = args.debug
    parallel = args.parallel

    if infile is not None and info is not False:
        info_filepath = os.path.abspath(infile)
        print "Not implemented yet."

    elif infile is not None:
        extension = os.path.splitext(infile)[1][1:].strip()
        pak_filepath = os.path.abspath(infile)

        print "Unpacking %s" % pak_filepath

        if extension == "pak":
            pak_file = PAK_file(filepath=pak_filepath, encrypted=False)
        elif extension == "crypt":
            pak_file = PAK_file(filepath=pak_filepath, encrypted=True)
        else:
            print "File not pak or pak.crypt"

        output_filepath = os.path.abspath('.')
        if outdir is not None:
            output_filepath = os.path.abspath(outdir)
        pak_file.dump(dest_filepath=output_filepath, verbose=debug, parallel=parallel)
    else:
        print "Nothing happened"
        parser.print_help()
