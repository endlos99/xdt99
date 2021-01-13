#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import (xas, xdm, error, check_files_eq, check_obj_code_eq, check_image_files_eq, read_stderr,
                   get_source_markers, check_binary_files_eq, check_errors, content_len, check_file_empty)


# Main test

def runtest():
    """check linked files object code against non-linked equivalent file object code
       NOTE: Programs commented out contain multiple xORGs, so the relocation of segments
             will lead to different object codes.
    """

    for inp_file, opts, ref_file, compr_file, relaxed_check in [
            ('asdirs.asm', [], 'ASDIRS-O', 'ASDIRS-C', False),
            ('asorg2.asm', [], 'ASORG2-O', None, False),
            ('asorg3.asm', [], 'ASORG3-O', None, False),
            ('asopcs.asm', [], 'ASOPCS-O', 'ASOPCS-C', False),
            ('asbss.asm', [], 'ASBSS-O', 'ASBSS-C', False),
            ('asbss2.asm', [], 'ASBSS2-O', None, False),
            ('asbss3.asm', [], 'ASBSS3-O', None, False),
            ('asbss4.asm', [], 'ASBSS4-O', None, False),
            ('ashellon.asm', ['-R'], 'ASHELLO-O', 'ASHELLO-C', False),
            ('ascopy.asm', [], 'ASCOPY-O', None, False),
            ('assize1.asm', [], 'ASSIZE1-O', 'ASSIZE1-C', False),
            ('asextsym.asm', [], 'ASEXTSYM-O', 'ASEXTSYM-C', False),
            #('asimg1.asm', [], 'ASIMG1-O', 'ASIMG1-C', False),
            ('asimg2.asm', [], 'ASIMG2-O', None, False),
            #('asimg3.asm', [], 'ASIMG3-OX', None, False),
            ('asreloc.asm', [], 'ASRELOC-O', None, False),
            ('asxorg.asm', [], 'ASXORG-O', None, True),  # TODO: slightly different structure for linked code
            ('ascart.asm', ['-R'], 'ASCART-O', 'ASCART-C', False),
            ]:
        source = os.path.join(Dirs.sources, inp_file)
        xas(*[source] + opts + ['-q', '-o', Files.input])
        xas('-l', Files.input, '-o', Files.output)
        xdm(Disks.asmsrcs, '-e', ref_file, '-o', Files.reference)
        tagfilter = b'BC' if relaxed_check else None  # compare only B and C tags
        check_obj_code_eq(Files.output, Files.reference, tagfilter=tagfilter)  # default

        xas('-ll', Files.input, '-o', Files.output)
        check_obj_code_eq(Files.output, Files.reference, tagfilter=tagfilter)  # resolve conflicts

        if compr_file:
            # compressed object code
            xas(*[source] + opts + ['-C', '-q', '-o', Files.input])
            xas('-l', Files.input, '-C', '-o', Files.output)
            xdm(Disks.asmsrcs, '-e', compr_file, '-o', Files.reference)
            check_obj_code_eq(Files.output, Files.reference, compressed=True)

    # parsing of object code
    source = os.path.join(Dirs.sources, 'asbssorg.asm')
    xas(source, '-o', Files.reference)
    xas('-l', Files.reference, '-o', Files.output)
    check_obj_code_eq(Files.output, Files.reference)

    # link multiple files
    library = os.path.join(Dirs.sources, 'aslink0b.asm')
    xas(library, '-q', '-o', Files.input)
    source = os.path.join(Dirs.sources, 'aslink0a.asm')
    xas(source, '-l', Files.input, '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslink0.asm')
    xas(ref, '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-ll', Files.input, '-q', '-o', Files.output)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, library)  # name should be source.obj
    objname = 'aslink0a.obj'
    if not os.path.isfile(objname):
        error('multi-files', 'Bad output file for multiple inputs')

    library = os.path.join(Dirs.sources, 'aslink1b.asm')
    xas(library, '-R', '-D', 'x=1', '-q', '-o', Files.input)
    source = os.path.join(Dirs.sources, 'aslink1a.asm')
    xas(source, '-l', Files.input, '-R', '-D', 'x=1', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslink1.asm')
    xas(ref, '-R', '-D', 'x=1', '-q', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    # link 3 files
    for x in ('a', 'b', 'c'):
        xas(os.path.join(Dirs.sources, 'aslink2' + x + '.asm'), '-q', '-o', Files.input + x)
    xas('-l', Files.input + 'a', Files.input + 'b', Files.input + 'c', '-q', '-b', '-o', Files.output)
    xas(os.path.join(Dirs.sources, 'aslink2.asm'), '-q', '-b', '-o', Files.reference)
    check_binary_files_eq('link', Files.output, Files.reference)

    xas('-ll', Files.input + 'a', Files.input + 'b', Files.input + 'c', '-q', '-b', '-o', Files.output)
    xas(os.path.join(Dirs.sources, 'aslink2.asm'), '-q', '-b', '-o', Files.reference)
    check_binary_files_eq('link', Files.output, Files.reference)

    # ditto with multiple source files
    sources = [os.path.join(Dirs.sources, f'aslink1{x}.asm') for x in ('a', 'b')]
    xas(*sources, '-R', '-D', 'x=1', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslink1.asm')
    xas(ref, '-R', '-D', 'x=1', '-q', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    sources = [os.path.join(Dirs.sources, f'aslink2{x}.asm') for x in ('a', 'b', 'c')]
    xas(*sources, '-b', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslink2.asm')
    xas(ref, '-b', '-q', '-o', Files.reference)
    check_binary_files_eq('multi-source', Files.output, Files.reference)

    # link and multi-files with conflict
    source1 = os.path.join(Dirs.sources, 'aslink3a.asm')
    source2 = os.path.join(Dirs.sources, 'aslink3b.asm')
    xas(source1, source2, '-b', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslink3.asm')
    xas(ref, '-b', '-o', Files.reference)
    check_binary_files_eq('link', Files.output, Files.reference)

    xas(source2, '-o', Files.input)
    xas(source1, '-l', Files.input, '-b', '-o', Files.output)
    check_binary_files_eq('multi-source', Files.output, Files.reference)

    # link file with auto-generated constants
    source = os.path.join(Dirs.sources, 'asauto.asm')
    xas(source, '-R', '-o', Files.input)
    xas('-R', '-l', Files.input, '-b', '-o', Files.output)
    xas(source, '-R', '-b', '-o', Files.reference)
    check_binary_files_eq('link', Files.output, Files.reference)

    # link w/o name
    xas('-l', Files.input, '-R')
    if not os.path.isfile('a.obj'):
        error('link', 'Objcode code file with default name not found')

    # link and rebase
    source = os.path.join(Dirs.sources, 'aslinkr.asm')
    xas(source, '-q', '-o', Files.input)
    xas('-l', Files.input, '-a', '>2000', '-b', '-q', '-o', Files.output)
    xas(source, '-b', '-a', '>2000', '-o', Files.reference)
    check_binary_files_eq('link/base', Files.output, Files.reference)

    xas('-ll', Files.input, '-a', '>2000', '-b', '-q', '-o', Files.output)
    check_binary_files_eq('link/base', Files.output, Files.reference)

    # link and rorg/aorg
    lib = os.path.join(Dirs.sources, 'aslinkob.asm')
    xas(lib, '-o', Files.input)
    source = os.path.join(Dirs.sources, 'aslinkoa.asm')
    xas(source, '-a', '>4000', '-l', Files.input, '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslinko.asm')
    xas(ref, '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, lib, '-a', '>4000', '-o', Files.output)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-a', '>4000', '-ll', Files.input, '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslinkor.asm')
    xas(ref, '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    # link and xorg
    lib = os.path.join(Dirs.sources, 'aslinkxb.asm')
    xas(lib, '-q', '-o', Files.input)
    source = os.path.join(Dirs.sources, 'aslinkxa.asm')
    xas(source, '-l', Files.input, '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslinkx.asm')
    xas(ref, '-q', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-ll', Files.input, '-q', '-o', Files.output)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-l', Files.input, '-a', '>e000', '-b', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslinkxe.asm')
    xas(ref, '-b', '-q', '-o', Files.reference)
    check_binary_files_eq('link/xorg', Files.output, Files.reference)

    xas(source, '-ll', Files.input, '-a', '>e000', '-b', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'aslinkxer.asm')
    xas(ref, '-b', '-q', '-o', Files.reference)
    check_binary_files_eq('link/xorg', Files.output, Files.reference)

    # link and -D
    lib = os.path.join(Dirs.sources, 'aslink4b.asm')
    xas(lib, '-q', '-o', Files.input)
    source = os.path.join(Dirs.sources, 'aslink4a.asm')
    xas(source, '-l', Files.input, '-D', 'x=69', '-o', Files.output)  # no need for -ll case
    ref = os.path.join(Dirs.sources, 'aslink4.asm')
    xas(ref, '-D', 'x=69', '-q', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    # in-unit conflict resolution
    # NOTE: For one program unit, internal conflicts may still be resolved
    #       against the absolute segments, yielding a non-zero offset for that
    #       single unit.  Inter-reloc conflicts cannot be resolved.
    source = os.path.join(Dirs.sources, 'asorgx.asm')
    xas(source, '-o', Files.input)
    xas('-ll', Files.input, '-b', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asorgxn.asm')
    xas(ref, '-b', '-o', Files.reference)
    check_binary_files_eq('in-file conflict', Files.output, Files.reference)

    # symbol conflicts
    source1 = os.path.join(Dirs.sources, 'aslinks1a.asm')
    source2 = os.path.join(Dirs.sources, 'aslinks1b.asm')
    with open(Files.error, 'w') as ferr:
        xas(source1, source2, '-o', Files.output, rc=1, stderr=ferr)

    xas(source2, '-o', Files.input)
    with open(Files.error, 'w') as ferr:
        xas(source1, '-l', Files.input, '-o', Files.output, rc=1, stderr=ferr)

    source1 = os.path.join(Dirs.sources, 'aslinks2a.asm')
    xas(source1, source2, '-o', Files.output, rc=0)
    source2 = os.path.join(Dirs.sources, 'aslinks2b.asm')
    xas(source1, source2, '-o', Files.output, rc=0)

    xas(source2, '-o', Files.input)
    xas(source1, '-l', Files.input, '-o', Files.output, rc=0)

    # entry conflict
    source1 = os.path.join(Dirs.sources, 'aslinkea.asm')
    source2 = os.path.join(Dirs.sources, 'aslinkeb.asm')
    with open(Files.error, 'w') as ferr:
        xas(source1, source2, '-o', Files.output, rc=1, stderr=ferr)

    xas(source2, '-o', Files.input)
    with open(Files.error, 'w') as ferr:
        xas(source1, '-l', Files.input, '-o', Files.output, rc=1, stderr=ferr)

    # practical example
    source =  os.path.join(Dirs.sources, 'asstdlib.asm')
    libs = ['vmbw.asm', 'vsbr.asm', 'vwbt.asm']
    with open(Files.error, 'w') as ferr:
        xas(source, *libs, '-R', '-o', Files.output, rc=0, stderr=ferr)
    check_file_empty(Files.error)

    # cleanup
    os.remove(Files.input)
    os.remove(Files.input + 'a')
    os.remove(Files.input + 'b')
    os.remove(Files.input + 'c')
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(objname)
    os.remove('a.obj')


if __name__ == '__main__':
    runtest()
    print('OK')
