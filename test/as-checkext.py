#!/usr/bin/env python

import os
import glob

from config import Dirs, Disks, Files
from utils import (xas, xdm, check_obj_code_eq, check_binary_files_eq, read_stderr, check_errors, concat,
                   get_source_markers, check_dat_file_eq, content, content_lines, error)


# Check functions

def check_concat_eq(infiles, reffile):
    data = b''
    for fn in infiles:
        with open(fn, 'rb') as f:
            data += f.read()
    with open(reffile, 'rb') as f:
        ref = f.read()
    if data != ref:
        error('Files', 'Incorrect binary data')


def check_lines_eq(infiles, reffile):
    lines = []
    for fn in infiles:
        with open(fn, 'r') as f:
            lines.extend(f.readlines())
    with open(reffile, 'r') as f:
        ref = f.readlines()
    if lines != ref:
        error('Files', 'Incorrect text lines')


def check_no_files(files):
    for fn in files:
        if os.path.isfile(fn):
            error('Files', 'Extraneous file ' + fn)


def check_file_sizes(files):
    for fn, fs in files:
        size = None
        with open(fn, 'rb') as f:
            size = len(f.read())
        if fs != size:
            error('Files', 'Incorrect file size ' + fn + ': ' + str(size))


def check_numeric_eq(output, ref):
    idx = 0
    with open(output, 'r') as fout, open(ref, 'rb') as fref:
        data = fref.read()
        for l in fout:
            line = l.strip()
            if not line or line[0] == '*' or line[0] == ';':
                continue
            if line[:4].lower() != 'byte':
                error('Files', 'Bad format: ' + l)
            toks = [x.strip() for x in line[4:].split(',')]
            vals = [int(x[1:], 16) if x[0] == '>' else int(x)
                    for x in toks]
            for v in vals:
                if v != data[idx]:
                    error('Files', f'Unexpected data: {v}/{data[idx]} at {idx}')
                idx += 1


def check_image_values(fn, val):
    with open(fn, 'rb') as f:
        data = f.read()[6:]
    for n in data[::2]:
        if n != val:
            error('image', 'Bad value in image data')
            print(n, val)


# Main test

def runtest():
    """check xdt99 extensions"""

    # xdt99 extensions
    source = os.path.join(Dirs.sources, 'asxext.asm')
    xas(source, '-R', '-q', '-o', Files.output)
    xdm(Disks.asmsrcs, '-e', 'ASXEXT0-O', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)
    xas(source, '-R', '-D', 'sym2', '-q', '-o', Files.output)
    xdm(Disks.asmsrcs, '-e', 'ASXEXT1-O', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)
    xas(source, '-R', '-D', 'sym2=2', 'sym3=2', '-q', '-o', Files.output)
    xdm(Disks.asmsrcs, '-e', 'ASXEXT2-O', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)
    xas(source, '-R', '-D', 'sym2=2,sym3=2', '-q', '-o', Files.output)
    xdm(Disks.asmsrcs, '-e', 'ASXEXT2-O', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    # some CLI options
    source = os.path.join(Dirs.sources, 'ascart.asm')
    xas(source, '--embed', '-R', '-o', Files.output)

    # misc new features
    for infile, opts, reffile in [
            ('asxnew.asm', ['-18'], 'ASXNEW-O'),
            ('asmacs.asm', [], 'ASMACS-O')
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(source, *opts, '-q', '-o', Files.output)
        xdm(Disks.asmsrcs, '-e', reffile, '-o', Files.reference)
        check_obj_code_eq(Files.output, Files.reference)

    # macro with text argument in listing
    source = os.path.join(Dirs.sources, 'asmactxt.asm')
    xas(source, 'vmbw.a99', '-R', '-b', '-o', Files.input, '-L', Files.output)
    if "'0'" in content_lines(Files.output):
        error('macro/listing', 'Macro arguments not escaped in listing')

    # SAVE directive
    source = os.path.join(Dirs.sources, 'asxsave.asm')
    xas(source, '-b', '--base', '0xb000', '-q', '-o', Files.output)
    for i, a in enumerate(['_b000', '_b020', '_b030', '_b080']):
        ref = os.path.join(Dirs.refs, f'asxsave_{i}.bin')
        check_binary_files_eq('SAVE', Files.output + a, ref)

    xas(source, '-t', 'a2', '-a', '0xb000', '-q', '-o', Files.output)
    for i, a in enumerate(['_b000', '_b020', '_b030', '_b080']):
        ref = os.path.join(Dirs.refs, f'asxsave_{i}.bin')
        check_dat_file_eq(Files.output + a, ref)

    source = os.path.join(Dirs.sources, 'asxsavee.asm')
    xas(source, '-b', '-a', '0x6000', '-q', '-o', Files.output)
    if content(Files.output) != b'\x22\x22\x22\x22':
        error('SAVE', 'Bad file contents')

    source = os.path.join(Dirs.sources, 'asxsaveo.asm')
    xas(source, '-b', '-o', Files.output)
    ref2 = os.path.join(Dirs.sources, 'asxsaveo2.asm')
    ref6 = os.path.join(Dirs.sources, 'asxsaveo6.asm')
    xas(ref2, '-b', '-o', Files.reference)
    check_binary_files_eq('SAVE', Files.output + '_2000', Files.reference)
    xas(ref6, '-b', '-o', Files.reference)
    check_binary_files_eq('SAVE', Files.output + '_6000', Files.reference)

    # remove front/back padding from saved binary
    source = os.path.join(Dirs.sources, 'asxsavem.asm')
    # this padding could be avoided if saves would *enable* splitting of segments
    xas(source, '-b', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asxsavem0.asm')
    xas(ref, '-b', '-o', Files.reference)
    check_binary_files_eq('SAVE', Files.output, Files.reference)

    # bank switching: obsolete AORG addr, bank
    source = os.path.join(Dirs.sources, 'asxbank1.asm')
    xas(source, '-b', '-a', '>6030', '-q', '-o', Files.output)
    save2s = [Files.output + '_b' + str(ext) for ext in range(3)]
    check_concat_eq(save2s, os.path.join(Dirs.refs, 'save2'))

    source = os.path.join(Dirs.sources, 'asxbank2.asm')
    xas(source, '-b', '-q', '-o', Files.output)
    for i, a in enumerate(['_c000_b0', '_d000_b0', '_e000_b0', '_c000_b1', '_d000_b1', '_e000_b1']):
        xas(os.path.join(Dirs.sources, 'asxbank2' + a + '.asm'), '-b', '-q', '-o', Files.reference)
        check_binary_files_eq('BANK+SAVE', Files.output + a, Files.reference)

    source = os.path.join(Dirs.sources, 'asxsegm.asm')
    xas(source, '-i', '-q', '-o', Files.output)
    check_file_sizes([(Files.outputff[i], size) for i, size in enumerate([26, 20, 14])])
    for i, val in enumerate([0x10, 0x20, 0x30]):
        check_image_values(Files.outputff[i], val)

    # BANK directive
    source = os.path.join(Dirs.sources, 'asdbank.asm')
    xas(source, '-b', '-R', '-o', Files.output)
    ref1 = os.path.join(Dirs.sources, 'asdbank_b0.asm')
    ref2 = os.path.join(Dirs.sources, 'asdbank_b1.asm')
    xas(ref1, '-b', '-R', '-o', Files.reference)
    check_binary_files_eq('BANK', Files.output + '_b0', Files.reference)
    xas(ref2, '-b', '-R', '-o', Files.reference)
    check_binary_files_eq('BANK', Files.output + '_b1', Files.reference)

    # cross-bank access
    source = os.path.join(Dirs.sources, 'asxbank.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-o', Files.output, stderr=ferr, rc=0)  # no error

    source = os.path.join(Dirs.sources, 'asnxbank.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-o', Files.output, stderr=ferr, rc=1)  # with errors

    # sections shared across banks
    source = os.path.join(Dirs.sources, 'asshbank.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-o', Files.output, stderr=ferr, rc=1)  # with errors
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, r';ERROR(:....)?')
    check_errors(exp_errors, act_errors)

    source = os.path.join(Dirs.sources, 'asshbankx.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-o', Files.output, stderr=ferr, rc=0)  # no error

    # data output (-t)
    source = os.path.join(Dirs.sources, 'ashexdat.asm')
    xas(source, '-t', 'a2', '-R', '-o', Files.output)
    xas(source, '-b', '-R', '-o', Files.reference)
    check_numeric_eq(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, 'asxtext.asm')
    xas(source, '-t', 'a2', '-o', Files.output + '1')
    xas(source, '-t', 'c4', '-o', Files.output + '2')
    xas(source, '-t', 'b', '-o', Files.output + '3')
    xas(source, '-t', 'a4', '-o', Files.output + '4')
    xas(source, '-t', 'c', '-o', Files.output + '5')
    save5s = [Files.output + ext
              for ext in ['1', '2', '3', '4', '5']]
    check_lines_eq(save5s, os.path.join(Dirs.refs, 'asxtext'))

    # auto-generated constants (b#, w#)
    source = os.path.join(Dirs.sources, 'asauto.asm')
    xas(source, '-R', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asauton.asm')
    xas(ref, '-R', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-R', '-a', '>2000', '-o', Files.output)
    xas(ref, '-R', '-a', '>2000', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)  # relocated

    xas(source, '-b', '-R', '-o', Files.output)
    xas(ref, '-b', '-R', '-o', Files.reference)
    check_binary_files_eq('auto-const', Files.output, Files.reference)  # as binary

    # size modifier (s#)
    source = os.path.join(Dirs.sources, 'assmod.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-o', Files.output, stderr=ferr, rc=0)
    ref = os.path.join(Dirs.sources, 'assmodn.asm')
    xas(ref, '-b', '-R', '-q', '-o', Files.reference)
    check_binary_files_eq('s#', Files.output, Files.reference)

    source = os.path.join(Dirs.sources, 'assmode.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-o', Files.output, stderr=ferr, rc=1)
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, tag=r';ERROR')
    check_errors(exp_errors, act_errors)

    # floating-point numbers
    source = os.path.join(Dirs.sources, 'asfloat.asm')
    xas(source, '-b', '-o', Files.output)
    ref = os.path.join(Dirs.refs, 'asfloat.ref')
    check_binary_files_eq('float', Files.output, ref)

    # 9995 and F18A
    source1 = os.path.join(Dirs.sources, 'as9995.asm')
    xas(source1, '-R', '-b', '-5', '-o', Files.output)
    ref = os.path.join(Dirs.refs, 'as9995.ref')
    check_binary_files_eq('9995', Files.output, ref)

    source2 = os.path.join(Dirs.sources, 'asf18a.asm')
    xas(source2, '-R', '-b', '--f18a', '-o', Files.output)
    ref = os.path.join(Dirs.refs, 'asf18a.ref')
    check_binary_files_eq('f18a', Files.output, ref)

    with open(source1, 'r') as f1, open(source2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        with open(Files.input, 'w') as fout:
            fout.writelines(lines1 + lines2)
    xas(Files.input, '-R', '-5', '-18', '-o', Files.output, rc=0)

    # cleanup
    for fn in glob.glob("tmp/outpu*"):
        os.remove(fn)
    os.remove(Files.input)
    os.remove(Files.reference)


if __name__ == '__main__':
    runtest()
    print('OK')
