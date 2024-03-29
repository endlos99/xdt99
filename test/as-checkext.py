#!/usr/bin/env python3

import os

from config import Dirs, Disks, Files, XAS99_CONFIG
from utils import (xas, xdm, r, error, clear_env, delfile, check_obj_code_eq, check_binary_files_eq, read_stderr,
                   check_errors, get_source_markers, check_dat_file_eq, content, content_lines, content_len,
                   content_line_array)


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


def check_symbols(fn, values):
    with open(fn, 'r') as f:
        for line in f:
            if line[:5] == '    W':
                exp = values[line[4:6]]
                found = int(line[26:30], 16)
                if exp != found:
                    error('symbols', f'Value mismatch: {found} != {exp}')


def check_timing(list_file, referece):
    with open(referece, 'r') as f:
        timings = [int(line[:4]) for line in f.readlines() if line[0] != ' ']
    i = 0
    with open(list_file, 'r') as f:
        for line in f.readlines():
            try:
                cycles = int(line[14:18])
            except ValueError:
                continue
            if timings[i] != cycles:
                error('xtime', f'Incorrect number of cycles for {i}th item')
            i += 1


# Main test

def runtest():
    """check xdt99 extensions"""

    clear_env(XAS99_CONFIG)

    # xdt99 extensions
    source = os.path.join(Dirs.sources, 'asxext.asm')
    xas(source, '-R', '-q', '-o', Files.output)
    xdm(Disks.asmsrcs, '-e', 'ASXEXT0-O', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)
    xas(source, '-R', '-D', 'sym2', '-q', '-o', Files.output)
    xdm(Disks.asmsrcs, '-e', 'ASXEXT1-O', '-o', Files.reference)
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

    # predefined target symbol _xas99_*
    source = os.path.join(Dirs.sources, 'asxtarg.asm')
    xas(source, '-b', '-o', Files.output)
    if content(Files.output) != b'\x11\x11\x33\x33\xff\xff':
        error('target', 'Binary mismatch')
    xas(source, '-i', '-o', Files.output)
    if content(Files.output)[6:] != b'\x11\x11\x44\x44\xff\xff':
        error('target', 'Image mismatch')

    # macro with text argument in listing
    source = os.path.join(Dirs.sources, 'asmactxt.asm')
    xas(source, 'vmbw.asm', '-R', '-b', '-o', Files.input, '-L', Files.output)
    if "'0'" in content_lines(Files.output):
        error('macro/listing', 'Macro arguments not escaped in listing')

    # SAVE directive
    source = os.path.join(Dirs.sources, 'asxsave.asm')
    xas(source, '-b', '-M', '--base', '0xb000', '-q', '-o', Files.output)
    for i, a in enumerate(['_b000', '_b023', '_b030', '_b080']):
        ref = os.path.join(Dirs.refs, f'asxsave_{i}.bin')
        check_binary_files_eq('SAVE', Files.output + a, ref)

    xas(source, '-t', 'a2', '-a', '0xb000', '-q', '-o', Files.output)
    for i, a in enumerate(['_b000', '_b023', '_b030', '_b080']):
        ref = r(f'asxsave_{i}.bin')
        check_dat_file_eq(Files.output + a, ref)

    source = os.path.join(Dirs.sources, 'asxsavee.asm')
    xas(source, '-b', '-M', '-a', '0x6000', '-q', '-o', Files.output)
    if content(Files.output) != b'\x22\x22\x22\x22':
        error('SAVE', 'Bad file name or contents')

    source = os.path.join(Dirs.sources, 'asxsaveo.asm')
    xas(source, '-b', '-M', '-o', Files.output)
    ref2 = os.path.join(Dirs.sources, 'asxsaveo2.asm')
    ref6 = os.path.join(Dirs.sources, 'asxsaveo6.asm')
    xas(ref2, '-b', '-o', Files.reference)
    check_binary_files_eq('SAVE', Files.output + '_2000', Files.reference)
    xas(ref6, '-b', '-o', Files.reference)
    check_binary_files_eq('SAVE', Files.output + '_6000', Files.reference)

    # remove front/back padding from saved binary (if minified)
    source = os.path.join(Dirs.sources, 'asxsavem.asm')
    # this padding could be avoided if saves would *enable* splitting of segments
    xas(source, '-b', '-M', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asxsavem0.asm')
    xas(ref, '-b', '-o', Files.reference)
    check_binary_files_eq('SAVE', Files.output, Files.reference)

    # minimized and maximized binaries
    source = os.path.join(Dirs.sources, 'asxbinmima.asm')
    xas(source, '-b', '-o', Files.reference)
    xas(source, '-b', '-M', '-o', Files.output)
    if content_len(Files.reference) != 0x2000:
        error('maximize', 'Max binary has wrong size')
    if content_len(Files.output) != 0x18:
        error('minimize', 'Min binary has wrong size')
    if content(Files.reference)[4:0x1c] != content(Files.output):
        error('minimize', 'Content mismatch')

    source = os.path.join(Dirs.sources, 'asxbinmaha.asm')
    xas(source, '-b', '-o', Files.output)
    if content_len(Files.output) != 0x1c:
        error('maximize', 'Max binary with open SAVE has wrong size')

    # bank switching: obsolete AORG addr, bank
    source = os.path.join(Dirs.sources, 'asxbank1.asm')
    xas(source, '-b', '-X', '-q', '-o', Files.output)
    save2s = [Files.output + '_b' + str(ext) for ext in range(3)]
    check_concat_eq(save2s, r('save2'))

    source = os.path.join(Dirs.sources, 'asxbank2.asm')
    xas(source, '-b', '-q', '-M', '-X', '-o', Files.output)
    for a in ['_c000_b0', '_d008_b0', '_e000_b0', '_c000_b1', '_d000_b1', '_e018_b1']:
        xas(os.path.join(Dirs.sources, 'asxbank2' + a + '.asm'), '-b', '-q', '-o', Files.reference)
        check_binary_files_eq('BANK+SAVE', Files.output + a, Files.reference)

    source = os.path.join(Dirs.sources, 'asxsegm.asm')
    xas(source, '-i', '-q', '-o', Files.output)
    check_file_sizes([(Files.outputff[i], size) for i, size in enumerate([26, 20, 14])])
    for i, val in enumerate([0x10, 0x20, 0x30]):
        check_image_values(Files.outputff[i], val)

    # BANK directive
    source = os.path.join(Dirs.sources, 'asdbank.asm')
    xas(source, '-b', '-R', '-M', '-X', '-o', Files.output)
    ref1 = os.path.join(Dirs.sources, 'asdbank_b0.asm')
    ref2 = os.path.join(Dirs.sources, 'asdbank_b1.asm')
    xas(ref1, '-b', '-R', '-X', '-o', Files.reference)
    check_binary_files_eq('BANK', Files.output + '_b0', Files.reference)
    xas(ref2, '-b', '-R', '-X', '-o', Files.reference)
    check_binary_files_eq('BANK', Files.output + '_b1', Files.reference)

    # equal length bank suffix
    source = os.path.join(Dirs.sources, 'asxbankf.asm')
    xas(source, '-b', '-o', Files.output)
    for i in range(10):
        if not os.path.isfile(Files.output + f'_b{i}'):
            error('bank format', 'bad bank suffix')
    xas(source, '-b', '-D', 'L2', '-o', Files.input)
    for i in range(12):
        if not os.path.isfile(Files.input + f'_b{i:02d}'):
            error('bank format', 'bad bank suffix')

    # cross-bank access
    source = os.path.join(Dirs.sources, 'asxbank.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-X', '-o', Files.output, stderr=ferr, rc=1)  # errors
    source = os.path.join(Dirs.sources, 'asxbankx.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-X', '-o', Files.output, stderr=ferr, rc=0)  # no error

    shared = os.path.join(Dirs.sources, 'asxbank_all.asm')
    xas(shared, '-b', '-R', '-o', Files.input)
    for n in range(2):
        source = os.path.join(Dirs.sources, f'asxbank_{n}.asm')
        xas(source, '-b', '-R', '-q', '-o', Files.reference)
        check_concat_eq((Files.input, Files.reference), Files.output + f'_b{n}')

    # sections shared across banks
    source = os.path.join(Dirs.sources, 'asshbank.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-X', '-o', Files.output, stderr=ferr, rc=1)  # with errors
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, r';ERROR(:....)?')
    check_errors(exp_errors, act_errors)

    source = os.path.join(Dirs.sources, 'asshbankx.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-X', '-o', Files.output, stderr=ferr, rc=0)  # no error

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
    check_lines_eq(save5s, r('asxtext'))

    # new EQU and WEQU semantics
    source = os.path.join(Dirs.sources, 'asxwequ.asm')
    xas(source, '-o', Files.input, '-q', '-S', '-L', Files.output)
    check_symbols(Files.output, {'W1': 3, 'W2': 2, 'W3': 0x2000})

    # auto-generated constants (b#, w#)
    source = os.path.join(Dirs.sources, 'asauto.asm')
    xas(source, '-R', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asauton.asm')
    xas(ref, '-R', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-R', '-a', '>2000', '-q', '-o', Files.output)
    xas(ref, '-R', '-a', '>2000', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)  # relocated

    xas(source, '-b', '-R', '-q', '-o', Files.output)
    xas(ref, '-b', '-R', '-o', Files.reference)
    check_binary_files_eq('auto-const', Files.output, Files.reference)  # as binary

    source = os.path.join(Dirs.sources, 'asautoa.asm')  # with AORG
    xas(source, '-R', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asautoan.asm')
    xas(ref, '-R', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, 'asauto2.asm')  # with AUTO
    xas(source, '-R', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asauto2n.asm')
    xas(ref, '-R', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, 'asxautobank.asm')  # with AUTO and BANKs
    xas(source, '-b', '-o', Files.output)
    for i in range(2):
        ref = os.path.join(Dirs.sources, f'asxautobank_{i}.asm')
        xas(ref, '-b', '-o', Files.reference)
        check_binary_files_eq('auto+bank', Files.output + f'_b{i}', Files.reference)

    source = os.path.join(Dirs.sources, 'asxautobanke.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-o', Files.output, stderr=ferr, rc=1)

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
    ref = r('asfloat.ref')
    check_binary_files_eq('float', Files.output, ref)

    # 9995, 99000 and F18A
    source1 = os.path.join(Dirs.sources, 'as9995.asm')
    xas(source1, '-R', '-b', '-5', '-o', Files.output)
    ref = r('as9995.ref')
    check_binary_files_eq('9995', Files.output, ref)

    source2 = os.path.join(Dirs.sources, 'asf18a.asm')
    xas(source2, '-R', '-b', '--f18a', '-o', Files.output)
    ref = r('asf18a.ref')
    check_binary_files_eq('f18a', Files.output, ref)

    with open(source1, 'r') as f1, open(source2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        with open(Files.input, 'w') as fout:
            fout.writelines(lines1 + lines2)
    xas(Files.input, '-R', '-5', '-18', '-o', Files.output, rc=0)

    source = os.path.join(Dirs.sources, 'as99000.asm')
    xas(source, '-b', '-R', '--99105', '-o', Files.output)  # also option -105
    ref = r('as99000.ref')
    check_binary_files_eq('99000', Files.output, ref)

    # cycle counting
    source = os.path.join(Dirs.sources, 'asxtime.asm')
    ref = r('asxtime.ref')
    xas(source, '-R', '-b', '-o', Files.output, '-L', Files.input)
    check_timing(Files.input, ref)

    # pragmas: cycle timing
    source = os.path.join(Dirs.sources, 'asxpragt.asm')
    xas(source, '-R', '-b', '-o', Files.output, '-L', Files.input)
    ref = r('asxpragt.ref')
    check_timing(Files.input, ref)

    # pragmas: warnings
    source = os.path.join(Dirs.sources, 'asxpragw.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '--quiet-unused-syms', '-o', Files.output, stderr=ferr, rc=0)
    expected = """> asxpragw.asm <2> 0005 - start  clr 0            ; WARN
 ***** Warning: Treating 0 as register, did you intend an @address?
 > asxpragw.asm <2> 0010 -        b   @start       ;: warn-opts = off, usage=on
 ***** Warning: Unknown pragma name: USAGE
 > asxpragw.asm <2> 0015 -        seto 2           ; WARN  ;: warn-usage=on, warn-opts=on
 ***** Warning: Treating 2 as register, did you intend an @address?
"""  # extra spaces for content_lines
    if content_lines(Files.error, skip=1) != expected:
        error('pragmas', 'Incorrect warnings shown')

    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '--quiet-usage', '-o', Files.output, stderr=ferr, rc=0)  # no error
    expected = """> asxpragw.asm <2> 0010 -        b   @start       ;: warn-opts = off, usage=on
 ***** Warning: Unknown pragma name: USAGE
 > asxpragw.asm <2> 0015 -        seto 2           ; WARN  ;: warn-usage=on, warn-opts=on
 ***** Warning: Treating 2 as register, did you intend an @address?
"""
    if content_lines(Files.error, skip=1) != expected:
        error('pragmas', 'Incorrect warnings shown with --quiet-usage')

    # pragmas: parsing error
    source = os.path.join(Dirs.sources, 'asxprage.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=0)
    if content_len(Files.error) > 0:
        error('pragmas', 'Incorrect parsing of non-pragma')

    # relaxed parsing
    source = os.path.join(Dirs.sources, 'asxrelax.asm')
    xas(source, '-R', '-b', '-r', '-o', Files.output, '-L', Files.input)
    if content(Files.output) != b'\x02\x01\x00\x10\x02\x02\x00\x0a\x00\x04':
        error('relaxed', 'Incorrect output')
    if len(content_line_array(Files.input)) != 13:
        error('relaxed', 'Incorrect listing size')

    # relaxed indexed addresses with parentheses
    source = os.path.join(Dirs.sources, 'asrelidx.asm')
    xas(source, '-R', '-q', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asrelidxr.asm')
    xas(ref, '-R', '-o', Files.reference)
    check_binary_files_eq('relindex', Files.output, Files.reference)

    # version string
    source = os.path.join(Dirs.sources, 'asxvers.asm')
    xas(source, '-b', '-q', '-o', Files.output, '-L', Files.input)
    binary = content(Files.output)
    if binary[:2] != b'\x07V' or binary[3:6:2] != b'..' or binary[-1] != 33 or not binary[2:7:2].decode().isdigit():
        error('version', 'Binary with version string mismatch')

    # register alias (3.5.1) [also see as-checkerr]
    source = os.path.join(Dirs.sources, 'asxrals.asm')
    xas(source, '-b', '-q', '-D', 'bin', '-o', Files.output)
    if content(Files.output) != bytes((0x04, 0xcf, 0x02, 0x0f, 0x00, 0x07, 0x04, 0xc7, 0x05, 0xaf, 0x00, 0x07,
                                       0x02, 0x01, 0x00, 0x2d)):
        error('ralias', 'Binary output mismatch')

    # .rept/.endr
    source = os.path.join(Dirs.sources, 'asxrept.asm')
    xas(source, '-b', '-L', Files.input, '-o', Files.output)
    if content(Files.output) != b'\x11' * 2 + b'\x22' * 6 + b'\x88' * 2 + b'\xff' * 2:
        error('rept', 'Binary output mismatch')
    listing = content_line_array(Files.input, strip=True)
    try:
        idx = listing.index('**** ****     > .rept') + 1
        for i in range(3):
            if listing[idx + i] != f'000{i + 1:d} 000{2*i + 2} 2222            data >2222':
                error('rept', 'List file mismatch')
    except ValueError:
        error('rept', 'List file .rept marker mismatch')

    # joined binary -B
    source = os.path.join(Dirs.sources, 'asxjoin.asm')
    xas(source, '-B', '-o', Files.output)
    result = content(Files.output)
    if (len(result) != 0x4000 or
            result[:0x40] != bytes(0x40) or
            result[0x40:0x46] != b'COMMON' or
            result[0x60:0x65] != bytes((1, 2, 3, 4, 5)) or
            result[0x1f00:0x1f04] != b'FINI' or
            result[0x2040:0x2046] != b'COMMON' or
            result[0x2090:0x2095] != bytes((255, 254, 253, 252, 251)) or
            result[0x3f00:0x3f04] != b'FINI' or
            any(result[i] != 0 for i in range(0x65, 0x1000)) or
            any(result[i] != 0 for i in range(0x2095, 0x3000))):
        error('join', 'Incorrect joined binary w/o saves')

    xas(source, '-B', '-o', Files.output, '-D', 'saves')
    result = content(Files.output)
    if (len(result) != 0x4000 or
            result[:0x40] != bytes(0x40) or
            result[0x40:0x46] != b'COMMON' or
            result[0x60:0x65] != bytes((1, 2, 3, 4, 5)) or
            result[0x1f00:0x1f04] != b'FINI' or
            result[0x2040:0x2046] != b'COMMON' or
            result[0x2090:0x2095] != bytes((255, 254, 253, 252, 251)) or
            result[0x3f00:0x3f04] != b'FINI' or
            any(result[i] != 0 for i in range(0x65, 0x1000)) or
            any(result[i] != 0 for i in range(0x2095, 0x3000))):
        error('join', 'Incorrect joined binary w/saves')

    source = os.path.join(Dirs.sources, 'asxjoinl.asm')
    xas(source, '-B', '-o', Files.output)
    result = content(Files.output)
    if (len(result) != 0x8000 or
            any(result[i] != 0 for i in range(0x2010, 0x5ff0)) or
            result[0x200f] != 0x10 or
            result[0x6008] != 0xff):
        error('join', 'Incorrect large joined binary')

    # macro call in list file
    source = os.path.join(Dirs.sources, 'asmaclst.asm')
    xas(source, '-R', '-b', '-S', '-o', Files.output, '-L', Files.input)
    listing = content_lines(Files.input)
    if 'lab    .push r2  ; save register' not in listing:
        error('mac list', 'Macro call not in list file')
    if 'lab.....' not in listing:
        error('mac list', 'Label missing in list file')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
