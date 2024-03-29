#!/usr/bin/env python3

import os

from config import Dirs, Disks, Files, XAS99_CONFIG
from utils import (xas, xdm, error, clear_env, delfile, check_obj_code_eq, check_image_set_eq, check_image_files_eq,
                   read_stderr, get_source_markers, check_errors, content, content_len, content_line_array)


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    clear_env(XAS99_CONFIG)

    # object code
    for inp_file, opts, ref_file, compr_file in [
        ('asdirs.asm', [], 'ASDIRS-O', 'ASDIRS-C'),
        ('asorgs.asm', [], 'ASORGS-O', 'ASORGS-C'),
        ('asopcs.asm', [], 'ASOPCS-O', 'ASOPCS-C'),
        ('asexprs.asm', [], 'ASEXPRS-O', None),
        ('asbss.asm', [], 'ASBSS-O', 'ASBSS-C'),
        ('asregs.asm', ['-R'], 'ASREGS-O', 'ASREGS-C'),
        ('ashellon.asm', ['-R'], 'ASHELLO-O', 'ASHELLO-C'),
        ('ascopy.asm', [], 'ASCOPY-O', None),
        ('ascopyn.asm', [], 'ASCOPYN-O', None),
        ('assize1.asm', [], 'ASSIZE1-O', 'ASSIZE1-C'),
        ('assize2.asm', [], 'ASSIZE2-O', None),
        ('assize3.asm', [], 'ASSIZE3-O', None),
        ('assize4.asm', [], 'ASSIZE4-O', None),
        ('asextsym.asm', [], 'ASEXTSYM-O', None),
        ('asdorg.asm', [], 'ASDORG-O', None),
        ('asrorg.asm', [], 'ASRORG-O', None),
        ('asimg1.asm', [], 'ASIMG1-O', 'ASIMG1-C'),
        ('asimg2.asm', [], 'ASIMG2-O', None),
        ('asimg3.asm', [], 'ASIMG3-OX', None),
        ('asreloc.asm', [], 'ASRELOC-O', None),
        ('asxorg.asm', [], 'ASXORG-O', None),
        ('ascart.asm', ['-R'], 'ASCART-O', 'ASCART-C')
    ]:
        source = os.path.join(Dirs.sources, inp_file)
        xdm(Disks.asmsrcs, '-e', ref_file, '-o', Files.reference)
        xas(*[source] + opts + ['-q', '-o', Files.output])
        check_obj_code_eq(Files.output, Files.reference)
        xas(*[source] + opts + ['--strict', '-q', '-o', Files.output])
        check_obj_code_eq(Files.output, Files.reference)
        if compr_file:
            # compressed object code
            xas(*[source] + opts + ['-C', '-q', '-o', Files.output])
            xdm(Disks.asmsrcs, '-e', compr_file, '-o', Files.reference)
            check_obj_code_eq(Files.output, Files.reference, compressed=True)

    # image files
    for inp_file, ref_file in [
            ('asimg1.asm', 'ASIMG1-I'),
            ('asimg2.asm', 'ASIMG2-I'),
            ('asimg3.asm', 'ASIMG3-I')
        ]:
        source = os.path.join(Dirs.sources, inp_file)
        xas(source, '-i', '-o', Files.output)
        xdm(Disks.asmsrcs, '-e', ref_file, '-o', Files.reference)
        check_image_files_eq(Files.output, Files.reference)

    for inp_file, reffiles in [
            ('aslimg.asm', ['ASLIMG-I', 'ASLIMG-J', 'ASLIMG-K']),
            ('assimg.asm', ['ASSIMG-I', 'ASSIMG-J', 'ASSIMG-K', 'ASSIMG-L']),
            ('asreloc.asm', ['ASRELOC-I'])
        ]:
        source = os.path.join(Dirs.sources, inp_file)
        xas(source, '-R', '-i', '-q', '-o', Files.output)
        gendata = []
        refdata = []
        for i, ref_file in enumerate(reffiles):
            xdm(Disks.asmimgs, '-e', ref_file, '-o', Files.reference)
            with open(Files.outputff[i], 'rb') as fgen, open(Files.reference, 'rb') as fref:
                gendata.append(fgen.read())
                refdata.append(fref.read())
        check_image_set_eq(gendata, refdata)

    # JMP instruction
    source = os.path.join(Dirs.sources, 'asjmp.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)
    xaserrors = read_stderr(Files.error)
    referrors = get_source_markers(source, r';ERROR(:....)?')
    check_errors(referrors, xaserrors)

    # valid labels (see also invalid and strict labels in as-checkerr.py)
    source = os.path.join(Dirs.sources, 'aslabel.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-q', '-o', Files.output, stderr=ferr, rc=0)
    if content_len(Files.error) > 0:
        error('labels', 'Valid label not accepted')

    # xas99-defined symbols
    source = os.path.join(Dirs.sources, 'asxassym.asm')
    xas(source, '-b', '-o', Files.output)
    with open(Files.output, 'rb') as f:
        data = f.read()
    for i in range(0, len(data), 2):
        if data[i:i + 2] == b'\x00\x00':
            error('symbols', 'Undefined xas99 symbol')

    # DORG special cases
    source = os.path.join(Dirs.sources, 'asdorg.asm')
    xas(source, '-a', '>2000', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asdorg-ti.asm')
    xas(ref, '-a', '>2000', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    # REF and built-ins
    source = os.path.join(Dirs.sources, 'asrefs.asm')
    xas(source, '-o', Files.output, '-L', Files.input)
    ref = os.path.join(Dirs.refs, 'asrefs.obj')
    check_obj_code_eq(Files.output, ref)
    words = ''.join(w[10:15] for w in content_line_array(Files.input)[1:] if w[10:15].strip())
    if words != '**** C820 8300 8C02 0620 0000e16FA 045B ':
        error('ref', 'Incorrect list file words')

    # new operators //, >>, <<
    source = os.path.join(Dirs.sources, 'asnewop.asm')
    xas(source, '-b', '-o', Files.output)
    if content(Files.output) != bytes((0x2f, 0x8d, 0xf1, 0xf8, 0x40, 0x00, 0x11, 0x11, 0x00, 0xcd, 0x12, 0x34, 0x43,
                                       0x21)):
        error('new ops', 'Incorrect results for new ops')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
