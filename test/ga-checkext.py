#!/usr/bin/env python

import os

from config import Dirs, Disks, Files, XGA99_CONFIG
from utils import (xga, xdm, error, clear_env, delfile, check_binary_files_eq, check_gbc_files_eq, content,
                   content_lines, content_line_array)


# check functions

def check_split_groms(base_grom, grom_count):
    for i in range(grom_count):
        grom = base_grom + i
        fn = Files.output + '_g' + str(grom)
        with open(fn, 'rb') as f:
            data = f.read()
            if any(b != grom for b in data if b):
                error('split grom', 'Bad GROM contents')
        os.remove(fn)
    if os.path.isfile(Files.output + '_g' + str(base_grom + grom_count)):
        error('split grom', 'Too many GROM files')


# Main test

def runtest():
    """run regression tests"""

    clear_env(XGA99_CONFIG)

    # other syntax
    source = os.path.join(Dirs.gplsources, 'gahello_timt.gpl')
    xga(source, '-y', 'mizapf', '-o', Files.output)
    ref = os.path.join(Dirs.gplsources, 'gahello.gpl')
    xga(ref, '-o', Files.reference)
    check_binary_files_eq('syntax', Files.output, Files.reference)

    # preprocessor
    source = os.path.join(Dirs.gplsources, 'gaxprep.gpl')
    xga(source, '-D', 'isdef=2', '-q', '-o', Files.output)
    xdm(Disks.gplsrcs, '-e', 'GAXPREP-Q', '-o', Files.reference)
    check_gbc_files_eq(source, Files.output, Files.reference)

    # directives
    source = os.path.join(Dirs.gplsources, 'gaxbcopy.gpl')
    xga(source, '-I', 'gpl', '-o', Files.output)
    source = os.path.join(Dirs.gplsources, 'gaxbcopyn.gpl')
    xga(source, '-o', Files.reference)
    check_binary_files_eq('bcopy', Files.output, Files.reference)

    # local labels
    source = os.path.join(Dirs.gplsources, 'gaxlocal.gpl')
    xga(source, '-o', Files.output)
    ref = os.path.join(Dirs.gplsources, 'gaxlocaln.gpl')
    xga(ref, '-o', Files.reference)
    check_binary_files_eq('locals', Files.output, Files.reference)

    # floating-point numbers
    source = os.path.join(Dirs.gplsources, 'gafloat.gpl')
    xga(source, '-o', Files.output)
    ref = os.path.join(Dirs.refs, 'asfloat.ref')
    check_binary_files_eq('float', Files.output, ref)

    # GROM n or address
    for source in (' GROM >6000\n DATA $', ' GROM 3\n DATA $'):
        with open(Files.input, 'w') as fout:
            fout.writelines(source)
        xga(Files.input, '-o', Files.output)
        with open(Files.output, 'rb') as fin:
            if fin.read()[:4] != b'\x60\x00':
                error('GROM', 'Incorrect address after GROM directive')

    # split GROMs
    source = os.path.join(Dirs.gplsources, 'gasplit.gpl')
    xga(source, '-g', '-o', Files.output)
    check_split_groms(3, 3)

    # unused symbols
    source = os.path.join(Dirs.gplsources, 'gauusym.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '--color', 'off', '-o', Files.output, stderr=ferr, rc=0)
    expected = """> gauusym.gpl <1> **** - 
 ***** Warning: Unused constants: s1:5
 > gauusymi.gpl <1> **** - 
 ***** Warning: Unused constants: si:1
"""
    if content_lines(Files.error) != expected:
        error('unused', 'Incorrect warnings')

    # relaxed parsing
    source = os.path.join(Dirs.gplsources, 'gaxrelax.gpl')
    xga(source, '-r', '-o', Files.output, '-L', Files.input)
    if content(Files.output) != b'\xbe\x00\x0b\xbe\x8f\xa0\x0b\x00\x00\x03':
        error('relaxed', 'Incorrect output')
    if len(content_line_array(Files.input)) != 18:
        error('relaxed', 'Incorrect list file length')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
