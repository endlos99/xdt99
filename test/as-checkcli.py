#!/usr/bin/env python

import os
import re

from config import Dirs, Disks, Files, XAS99_CONFIG
from utils import (chrw, ordw, xas, xdm, error, clear_env, delfile, content, content_len, check_obj_code_eq,
                   check_binary_files_eq, check_image_files_eq, check_list_files_eq)


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


def check_symbols(outfile, symspec):
    """check if all symbol/value pairs are in symfile"""
    with open(outfile, 'r') as fout:
        source = fout.readlines()
    equs = {}
    eref = []
    refs, symbols = symspec
    for line in source:
        if line.strip()[:3] == 'ref':
            eref.extend([s.strip().upper() for s in line.strip()[3:].split(',')])
    for i in range(0, len(source), 2):
        if source[i].strip()[:3] == 'ref':
            continue
        sym = source[i].split(':')[0]
        val = source[i + 1].upper().split('EQU', 1)[1].strip().split()[0]
        equs[sym] = val

    for ref in refs:
        if ref not in eref:
            error('symbols', f'Missing reference {ref}')
        del eref[eref.index(ref)]
    if eref:
        error('symbols', f'Extraneous references {eref}')
    for sym, val in symbols:
        if equs.get(sym) != val:
            error('symbols', f'Symbol mismatch for {sym}={val}/{equs.get(sym)}')


# Main test

def runtest():
    """check command line interface"""

    clear_env(XAS99_CONFIG)

    # input and output files
    source = os.path.join(Dirs.sources, 'ashellon.asm')
    with open(Files.output, 'wb') as f:
        xas(source, '-R', '-o', '-', stdout=f)
    xdm(Disks.asmsrcs, '-e', 'ASHELLO-O', '-q', '-o', Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

    xas(source, '-R', '-o', Dirs.tmp)  # -o <dir>
    if not os.path.isfile(os.path.join(Dirs.tmp, 'ashellon.obj')):
        error('output', '-o <dir> failed')

    with open(Files.output, 'wb') as f:
        xas(source, '-R', '-i', '-D', 'VSBW=>210C', 'VMBW=>2110', 'VWTR=>211C', 'KSCAN=>2108', '-o', '-', stdout=f)
    xdm(Disks.asmsrcs, '-e', 'ASHELLO-I', '-o', Files.reference)
    check_image_files_eq(Files.output, Files.reference)

    with open(Files.output, 'w') as f:
        xas(source, '-R', '-q', '-o', Files.output, '-L', '-', stdout=f)
    xdm(Disks.asmsrcs, '-e', 'ASHELLO-L', '-o', Files.reference)
    check_list_files_eq(Files.output, Files.reference)

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
    xas(source, '-b', '-D', 's1=1', 's3=3', 's2=4', '-o', Files.output)
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
    xas(source, '-b', '-R', '-o', Files.reference, '-E', Files.output)
    check_symbols(Files.output,
                  (('VDPWA', 'SCAN'),  # references
                   (('START', '>0000'), ('S1', '>0001'), ('S2', '>0018'))))  # symbols

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
        error('warn', 'warnings, even though disabled')

    # linker
    source1 = os.path.join(Dirs.sources, 'aslink0a.asm')
    source2 = os.path.join(Dirs.sources, 'aslink0b.asm')
    xas(source1, '-q', '-o', Files.input)
    xas(source2, '-q', '-o', Files.output)
    with open(Files.error, "w") as ferr:
        xas('-l', Files.input, '-ll', Files.output, '-o', Files.reference, rc=2, stderr=ferr)  # mutually exclusive

    # default options
    delfile(Files.input)
    source = os.path.join(Dirs.sources, 'ashello.asm')
    os.environ[XAS99_CONFIG] = '-L ' + Files.input
    xas(source, '-R', '-o', Files.output)
    if content_len(Files.input) <= 0:
        error('defaults', 'default options not working')

    delfile(Files.input)
    delfile(Files.error)
    os.environ[XAS99_CONFIG] = '-L ' + Files.error
    xas(source, '-R', '-o', Files.output, '-L', Files.input)
    if content_len(Files.error) > 0:
        error('defaults', 'default options override not working')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
