#!/usr/bin/env python3

import os
import re
import zipfile

from config import Dirs, Disks, Files, XAS99_CONFIG
from utils import (chrws, ordw, xas, xdm, t, r, error, clear_env, delfile, content, content_len, content_line_array,
                   check_obj_code_eq, check_binary_files_eq, check_image_files_eq, check_list_files_eq)


def remove(files):
    for fn in files:
        if os.path.exists(fn):
            os.remove(fn)


# Check functions

def check_exists(files):
    for fn in files:
        try:
            with open(fn, 'rb') as f:
                x = f.read()[0]
        except (IOError, IndexError):
            error('Files', 'File missing or empty: ' + fn)


def check_bin_text_equal_bytes(outfile, reffile):
    with open(outfile, 'r') as fout, open(reffile, 'rb') as fref:
        txt = ' '.join(fout.readlines())
        bin = fref.read()
    data = [b for b in bin]
    dirs = [int(m, 16) for m in re.findall('>([0-9A-Fa-f]{2})', txt)][1:]  # skip AORG
    if data != dirs:
        error('DATA', 'DATA/word mismatch')


def check_bin_text_equal_words(outfile, reffile):
    with open(outfile, 'r') as fout, open(reffile, 'rb') as fref:
        txt = ' '.join(fout.readlines())
        bin = fref.read()
    if len(bin) % 2 == 1:
        bin += b'\x00'
    data = [ordw(bin[i:i + 2]) for i in range(0, len(bin), 2)]
    dirs = [int(m, 16) for m in re.findall('>([0-9A-Fa-f]{4})', txt)][1:]  # skip AORG
    if data != dirs:
        error('DATA', 'DATA/word mismatch')


def check_symbols(equ_file, symspec, strict=False):
    """check if all symbol/value pairs are in symfile"""
    with open(equ_file, 'r') as fout:
        equ_list = fout.readlines()
    equs = {}
    eref = []
    refs, symbols = symspec
    label = None
    for l in equ_list:
        line = l.strip()
        if line[:3].lower() == 'ref':
            eref.extend([s.strip().upper() for s in line[3:].split(',')])
        elif l[0] != ' ':
            if strict:
                sym, _, op = re.split(r'\s+', line, maxsplit=2)
                try:
                    val, _ = op.split('*', maxsplit=1)
                except ValueError:
                    val = op
                equs[sym.strip()] = val.strip()
            else:
                if label:
                    equs[label] = line[4:].strip()
                    label = None
                else:
                    label, _ = line.split(':', maxsplit=1)
    for ref in refs:
        if ref not in eref:
            error('symbols', f'Missing reference {ref}')
        del eref[eref.index(ref)]
    if eref:
        error('symbols', f'Extraneous references {eref}')
    for sym, val in symbols:
        if equs.get(sym) != val:
            error('symbols', f'Symbol mismatch for {sym}={val}/{equs.get(sym)}')


def check_parsing(args):
    """check parsing of positional arguments after list options"""
    import sys
    sys.path.append('..')
    from xas99 import Xas99Processor
    print(f'PP: (\'{args}\')')
    sys.argv = ('xxx ' + args).split()
    processor = Xas99Processor()
    processor.parse()
    return processor.opts.sources


def runtest():
    """check command line interface"""

    clear_env(XAS99_CONFIG)

    # parsing of positional arguments after list options
    if check_parsing('-I foo bar -D x,y,z main1 main2 -l dummy'):  # should be empty list
        error('parse', 'Parsed sources mismatch')

    if check_parsing('-I foo bar; main1 main2') != ['main1', 'main2']:
        error('parse', 'Parsed sources mismatch')

    if check_parsing('-D x y z ; main1 main2') != ['main1', 'main2']:
        error('parse', 'Parsed sources mismatch')

    if check_parsing('main1 -I foo; -D x; main2') != ['main1', 'main2']:
        error('parse', 'Parsed sources mismatch')

    # input and output files
    source = os.path.join(Dirs.sources, 'ashellon.asm')
    with open(Files.output, 'wb') as f:
        xas(source, '-R', '-o', '-', stdout=f)
    xdm(Disks.asmsrcs, '-e', 'ASHELLO-O', '-q', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-R', '-o', Dirs.tmp)  # -o <dir>
    if not os.path.isfile(t('ashellon.obj')):
        error('output', '-o <dir> failed')

    with open(Files.output, 'wb') as f:
        xas(source, '-R', '-i', '-D', 'VSBW=>210C,VMBW=>2110,VWTR=>211C,KSCAN=>2108', '-o', '-', stdout=f)
    xdm(Disks.asmsrcs, '-e', 'ASHELLO-I', '-o', Files.reference)
    check_image_files_eq(Files.output, Files.reference)

    with open(Files.output, 'w') as f:
        xas(source, '-R', '-q', '-o', Files.output, '-L', '-', stdout=f)
    xdm(Disks.asmsrcs, '-e', 'ASHELLO-L', '-o', Files.reference)
    check_list_files_eq(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, 'assyms.asm')
    reference = os.path.join(Dirs.refs, 'assyms.equ')
    with open(Files.output, 'w') as f:
        xas(source, '-R', '-o', Files.input, '-E', '-', stdout=f)
    if content(Files.output) != content(reference):
        error('stdout', 'EQU file mismatch')

    source = os.path.join(Dirs.sources, 'nonexisting')
    with open(Files.error, 'w') as ferr:
        xas(source, '-i', '-R', '-o', Files.output, stderr=ferr, rc=1)
    with open(Files.error, 'r') as ferr:
        errs = ferr.readlines()
    if len(errs) != 1 or 'File not found' not in errs[0] or 'nonexisting' not in errs[0]:
        error('File error', 'Incorrect file error message')

    # include path
    source = os.path.join(Dirs.sources, 'ascopyi.asm')
    incls = os.path.join(Dirs.sources, 'test') + ',' + os.path.join(Dirs.sources, 'test', 'test')
    xas(source, '-i', '-I', incls, '-o', Files.output)
    with open(Files.output, 'rb') as f:
        data = f.read()
    if len(data) != 6 + 20:
        error('Include paths', 'Incorrect image length')

    # command-line definitions
    source = os.path.join(Dirs.sources, 'asdef.asm')
    xas(source, '-b', '-D', 's1=1,s3=3,s2=4', '-o', Files.output)
    if content(Files.output) != b'\x01\x03':
        error('-D', 'Content mismatch')
    xas(source, '-b', '-D', 's1=2,s2=2,s3=3', '-o', Files.output)
    if content(Files.output) != b'\x02\x03':
        error('-D', 'Content mismatch')

    # rebase -a
    source = os.path.join(Dirs.sources, 'asrebase.asm')
    xas(source, '-b', '-a', '>2000', '-o', Files.output)
    ref = os.path.join(Dirs.sources, 'asrebasen.asm')
    xas(ref, '-b', '-o', Files.reference)
    check_binary_files_eq('rebase', Files.output, Files.reference)

    # various parameter combinations
    source = os.path.join(Dirs.sources, 'asxbank1.asm')
    remove([Files.reference])
    xas(source, '-b', '-q', '-o', Files.output, '-L', Files.reference)
    check_exists([Files.reference])

    # text data output
    source = os.path.join(Dirs.sources, 'ascart.asm')
    xas(source, '-b', '-R', '-o', Files.reference)
    xas(source, '-t', 'a2', '-R', '-o', Files.output)
    check_bin_text_equal_bytes(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, 'asmtext.asm')
    xas(source, '-t', 'a2', '-R', '-o', Files.output)
    dat = content(Files.output, mode='r')
    if (not 'aorg >1000' in dat or 'aorg >1010' in dat or
            'data' in dat or not 'byte' in dat or
            '0x' in dat or not '>' in dat):
        error('dat', 'Invalid .dat file contents')

    # symbols
    source = os.path.join(Dirs.sources, 'assyms.asm')
    xas(source, '-b', '-s', '-R', '-o', Files.reference, '-E', Files.output)
    check_symbols(Files.output,
                  (('Z',),  # references
                   (('START', '>0000'), ('S1', '>0001'), ('S2', '>0018'), ('SCAN', '>000E'), ('VDPWA', '>8C02'))),
                  strict=True)  # expected symbols

    reference = r('assyms-s.equ')
    xas(source, '-s', '-R', '-o', Files.reference, '-E', Files.output)
    if content(Files.output) != content(reference):
        error('equs', 'Strict EQU file mismatch')

    reference = r('assyms.equ')
    xas(source, '-R', '-o', Files.reference, '-E', Files.output)
    if content(Files.output) != content(reference):
        error('equs', 'Relaxed EQU file mismatch')

    # color
    source = os.path.join(Dirs.sources, 'aserrs.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'on', '-o', Files.output, stderr=ferr, rc=1)
    errors = content(Files.error, mode='r')
    if '\x1b[31m' not in errors or '\x1b[33m' not in errors:
        error('color', 'Missing color in errors and warnings')

    # relaxed syntax
    source = os.path.join(Dirs.sources, 'asxrelax.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-r', '-o', Files.output, stderr=ferr, rc=0)

    # disable warnings
    source = os.path.join(Dirs.sources, 'aswarn.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-q', '-o', Files.output, stderr=ferr, rc=0)
    if content_len(Files.error) > 0:
        error('warn', 'Warnings, even though disabled')

    # linker
    source1 = os.path.join(Dirs.sources, 'aslink0a.asm')
    source2 = os.path.join(Dirs.sources, 'aslink0b.asm')
    xas(source1, '-q', '-o', Files.input)
    xas(source2, '-q', '-o', Files.output)
    with open(Files.error, "w") as ferr:
        xas('-l', Files.input, '-ll', Files.output, '-o', Files.reference, rc=2, stderr=ferr)  # mutually exclusive

    # multiple sources and errors
    source = os.path.join(Dirs.sources, 'aserrsim.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, source, '-R', '-o', Files.output, stderr=ferr, rc=0)
    errs = content_line_array(Files.error)
    if len(errs) != 5 or 'Warning' not in errs[2] or 'Warning' not in errs[4]:
        error('multi source', 'Incorrect warnings')

    with open(Files.error, 'w') as ferr:
        xas(source, source, '-R', '-D', 'err', '-o', Files.output, stderr=ferr, rc=1)
    errs = content_line_array(Files.error)
    if len(errs) != 6 or 'Warning' not in errs[2] or 'Error' not in errs[4]:  # includes "1 error found" message
        error('multi source', 'Incorrect errors')

    # default options
    delfile(Files.input)
    source = os.path.join(Dirs.sources, 'ashello.asm')
    os.environ[XAS99_CONFIG] = '-L ' + Files.input
    xas(source, '-R', '-o', Files.output)
    if content_len(Files.input) <= 0:
        error('defaults', 'Default options not working')

    delfile(Files.input)
    delfile(Files.error)
    os.environ[XAS99_CONFIG] = '-L ' + Files.error
    xas(source, '-R', '-o', Files.output, '-L', Files.input)
    if content_len(Files.error) > 0:
        error('defaults', 'Default options override not working')
    del os.environ[XAS99_CONFIG]

    # platform-agnostic paths
    source = os.path.join(Dirs.sources, 'aswin.asm')
    xas(source, '-b', '-o', Files.output)
    if content(Files.output) != bytes((0, 1, 0, 2, 0, 2, 0, 1)):
        error('wincopy', 'File with Windows paths mismatch')

    # paths as filenames for -o, -L, -E
    source = os.path.join(Dirs.sources, 'asmulf.asm')
    xas(source, '-i', '-o', Dirs.tmp)
    if (content(t('asmulf.img')) != chrws(0xffff, 0x10, 0x2000) + b'\x01' * 10 or
            content(t('asmulg.img')) != chrws(0xffff, 0x16, 0xa000) + b'\x02' * 16 or
            content(t('asmulh.img')) != chrws(0, 0x26, 0xe000) + b'\x03' * 32):
        error('path output', 'Image contents mismatch')

    xas(source, '-o', Files.output, '-L', Dirs.tmp)
    if content_line_array(t('asmulf.lst'))[0][:31] != 'XAS99 CROSS-ASSEMBLER   VERSION':
        error('path output', 'List file contents mismatch')

    xas(source, '-o', Files.output, '-L', Files.input, '-E', Dirs.tmp, '-s')
    if len(content_line_array(t('asmulf.equ'))) != 3:
        error('path output', 'Equ file contents mismatch')

    # joined binary
    source = os.path.join(Dirs.sources, 'asjoin.asm')
    xas(source, '-B', '-o', Files.output)
    data = content(Files.output)
    if (data[0x10] != 1 or data[0x1020] != 2 or data[0x2030] != 3 or data[0x3040] != 4 or
            data[0x4050] != 5 or data[0x5060] != 6):
        error('joined', 'Incorrect data in joined binary')
    if len(data) != 0x6000:
        error('joined', 'Incorrect joined binary size')

    xas(source, '-B', '-M', '-o', Files.output)
    data = content(Files.output)
    if (data[0x10] != 1 or data[0x1020] != 2 or data[0x2030] != 3 or data[0x3040] != 4 or
            data[0x4050] != 5 or data[0x5060] != 6):
        error('joined', 'Incorrect data in minimized joined binary')
    if len(data) != 0x5061:
        error('joined', 'Incorrect minimized joined binary size')

    # new cart
    source = os.path.join(Dirs.sources, 'ascart.asm')
    reference = r('ASCART.bin')
    xas(source, '-R', '-c', '-o', Files.output)
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('ASCART.bin')
        layout = archive.read('layout.xml')
        _metainf = archive.read('meta-inf.xml')
    if data != content(reference):
        error('cart', 'Incorrect data in cart')
    if b"pcb type='standard'" not in layout:
        error('cart', 'Incorrect paging in layout.xml')

    source = os.path.join(Dirs.sources, 'ascarthd.asm')
    reference = r('ASCARTHD.bin')
    xas(source, '-R', '-c', '-o', Files.output)
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('ASCARTHD.bin')
    if data != content(reference):
        error('cart', 'Incorrect data in cart')

    source = os.path.join(Dirs.sources, 'ascartrel.asm')
    for x in (['-q'], ['-D', 'SIXM']):
        xas(source, '-R', '-c', *x, '-o', Files.output)
        with zipfile.ZipFile(Files.output, 'r') as archive:
            data = archive.read('ASCARTREL.bin')
        if data[0] != 0xaa or data[0x30] == 0xaa or data[0x12:0x14] != b'\x60\x16':
            error('cart', 'Incorrect header in cart')

    source = os.path.join(Dirs.sources, 'ascartbnk.asm')
    xas(source, '-c', '-o', Files.output)
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('ASCARTBNK.bin')
        layout = archive.read('layout.xml')
    if data[0] != 0xaa or data[0x30] == 0xaa:
        error('cart', 'Incorrect data in cart')
    if b"pcb type='paged378'" not in layout:
        error('cart', 'Incorrect paging in layout.xml')

    # cleanup
    delfile(Dirs.tmp)


# Main test

if __name__ == '__main__':
    runtest()
    print('OK')
