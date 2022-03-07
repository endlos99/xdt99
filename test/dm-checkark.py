#!/usr/bin/env python3

import os
import shutil
import re

from xdm import Bitstream, LZW  # linked into test/ dir as a kludge
from config import Dirs, Disks, Files, Masks, XDM99_CONFIG
from utils import (r, t, xdm, error, clear_env, delfile, content, content_lines, content_line_array,
                   check_binary_files_eq)


# Check functions

def check_tifiles(outfile, reffile):
    """tifiles dates may differ, as archive has no date info"""
    # TIFILES date is [0x1e:0x26]
    with open(outfile, 'rb') as fout, open(reffile, 'rb') as fref:
        outdata = fout.read()
        refdata = fref.read()
    if outdata[:0x1e] != refdata[:0x1e] or outdata[0x26:] != refdata[0x26:]:
        error('archive files', 'TIFILES Files differ')


def check_archive(outfile, reffile):
    """archives may differ in zero-padding"""
    with open(outfile, 'rb') as fout, open(reffile, 'rb') as fref:
        outdata = fout.read()
        refdata = fref.read()
    outdata += bytes(len(refdata) - len(outdata))


def check_disk_files(outfile, reffile):
    """outfile uses >e5 to pad unused sectors, reffile uses >00
       compare everythin outside those differences
    """
    with open(outfile, 'rb') as fout, open(reffile, 'rb') as fref:
        outdata = fout.read()
        refdata = fref.read()
    start = 0
    for m in re.finditer(rb'\xe5{5,}', outdata):
        outchunk = outdata[start:m.start()]
        refchunk = refdata[start:m.start()]
        start = m.end()
        if outchunk != refchunk:
            error('Boone archive', 'Archive chunk differs')
        zeroes = refdata[m.start():m.end()]
        if zeroes != bytes(len(zeroes)):
            error('Boone archive', 'Archive chunk is not zero')


# Main test

def runtest():
    """check handling of ARK archives"""

    clear_env(XDM99_CONFIG)

    # bitstreams
    print('XX: Bitstream')
    bstream = Bitstream(b'\xab\xcd\xef', 3)
    bits = []
    while True:
        try:
            bits.append(bstream.read())
        except StopIteration:
            break
    if bits != [5, 2, 7, 4, 6, 7, 5, 7]:
        error('bitstream', 'Bad bitstream bits (width 3)')

    bstream = Bitstream(b'\x12\x34\x56\x78\x90\xab\xcd\xef\x00', 11)
    bits = []
    while True:
        try:
            bits.append(bstream.read())
        except StopIteration:
            break
    if bits != [145, 1301, 1265, 266, 1510, 1980]:
        error('bitstream', 'Bad bitstream bits (width 11)')

    bstream = Bitstream(b'\x5a\x96\x0f', 1)
    bits = []
    while True:
        try:
            bits.append(bstream.read())
        except StopIteration:
            break
    if bits != [0, 1, 0, 1,  1, 0, 1, 0,  1, 0, 0, 1,  0, 1, 1, 0,  0, 0, 0, 0,  1, 1, 1, 1]:
        error('bitstream', 'Bad bitstream bits (width 1)')

    bstream = Bitstream(width=3)
    for bits in [7, 0, 3, 6, 1, 1, 5, 2, 7, 7, 3, 5, 0, 1]:
        bstream.write(bits)
    if bstream.array() != bytes((0xe1, 0xe2, 0x6a, 0xfd, 0xd0, 0x40)):
        error('bitstream', 'Bad bitstream bytes (width 3)')

    bstream = Bitstream(width=11)
    for bits in [0xa5, 0x1e7, 0x44, 0x7ff, 0x5aa, 0x311, 0x200]:
        bstream.write(bits)
    if bstream.array() != bytes((0x14, 0xa7, 0x9c, 0x22, 0x7f, 0xfb, 0x54, 0xc4, 0x50, 0x00)):
        error('bitstream', 'Bad bitstream bytes (width 11)')

    # LZW
    lzw = LZW()
    text = b"""xdt99 is free software: you can redistribute it and/or modify
it under the terms of the GNU general Public license as published by
the free software foundation, either version 3 of the license, or
at your option any later version.

This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
merchantability or fitness for a particular purpose.  See the
GNU general public license for more details.

You should have received a copy of the GNU general public license
along with this program.  If not, see https www gnu org licenses."""

    print('XX: LZW')
    text_c = lzw.compress(text)
    text_cd = lzw.decompress(text_c)
    text_cdc = lzw.compress(text_cd)
    text_cdcd = lzw.decompress(text_cdc)
    if text_c != text_cdc or text != text_cd or text_cd != text_cdcd:
        error('LZW', 'error in compression/decompression')

    # Archive

    # create
    with open(Files.output, 'w') as fout:
        xdm('-Y', '-K', Files.reference, '-i', stdout=fout, rc=0)
    if len(content_line_array(Files.output)) != 2:
        error('archive', 'creation of empty archive failed')

    os.remove(Files.reference)
    with open(Files.error, 'w') as ferr:
        xdm('-K', Files.reference, '-i', stderr=ferr, rc=1)

    # references

    # single file archive
    shutil.copyfile(Disks.ark1, Disks.work)
    for i, suffix in enumerate(('1T', '2T', '3B', '4B', '5T')):
        ref = r(f'arkfile{suffix.lower()}.tfi')
        xdm(Disks.work, '-K', f'FILE{i + 1}_ARK', '-t', '-e', f'ARKFILE{suffix}', '-o', Files.output)
        check_tifiles(Files.output, ref)
        xdm(Disks.work, '-e', f'FILE{i + 1}_ARK', '-t', '-o', Files.input)
        xdm('-K', Files.input, '-t', '-e', f'ARKFILE{suffix}', '-o', Files.output)
        check_tifiles(Files.output, ref)

    xdm('-X', 'dssd', Disks.work)
    for i, suffix in enumerate(('1T', '2T', '3B', '4B', '5T')):
        ref = r(f'arkfile{suffix.lower()}_ark')
        xdm('-Y', '-K', Files.output, '-t', '-a', r(f'arkfile{suffix.lower()}.tfi'))
        check_archive(Files.output, ref)
        xdm(Disks.work, '-Y', '-K', f'ARC{i}', '-t', '-a', r(f'arkfile{suffix.lower()}.tfi'))
        xdm(Disks.work, '-e', f'ARC{i}', '-o', Files.output)
        check_archive(Files.output, ref)

    # multi file archive
    xdm('-Y', '-K', Files.output)
    ref = r('arkfileall_ark')
    for i, suffix in enumerate(('1T', '2T', '3B', '4B', '5T')):
        xdm('-K', Files.output, '-t', '-a', r(f'arkfile{suffix.lower()}.tfi'))
    check_archive(Files.output, ref)

    xdm('-K', Files.output, '-e', '*', '-t', '-o', Dirs.tmp)
    for i, suffix in enumerate(('1t', '2t', '3b', '4b', '5t')):
        check_tifiles(t(f'arkfile{suffix}.tfi'), r(f'arkfile{suffix}.tfi'))

    delfile(Dirs.tmp)

    xdm('-X', 'dsdd', Disks.work)
    xdm(Disks.work, '-Y', '-K', 'ARK')
    for i, suffix in enumerate(('1T', '2T', '3B', '4B', '5T')):
        xdm(Disks.work, '-K', 'ARK', '-t', '-a', r(f'arkfile{suffix.lower()}.tfi'))
    xdm(Disks.work, '-e', 'ARK', '-o', Files.output)
    shutil.copyfile(Disks.ark2, Disks.work)
    xdm(Disks.work, '-e', 'ALL_ARK', '-o', Files.reference)
    check_archive(Files.output, Files.reference)

    xdm('-K', Files.output, '-t', '-e', '*', '-o', Dirs.tmp)
    for i, suffix in enumerate(('1t', '2t', '3b', '4b', '5t')):
        check_tifiles(t(f'arkfile{suffix}.tfi'), r(f'arkfile{suffix}.tfi'))

    # Boone's archive
    shutil.copyfile(Disks.arkb, Disks.work)
    xdm(Disks.work, '-Y', '-K', 'XARK', '-A', 'F128', 'F129', 'F16', 'V128', 'V64V', 'V254')
    xdm(Disks.work, '-e', 'BARK', 'XARK', '-o', Dirs.tmp)
    xdm('--decompress', t('bark'), '-o', Files.reference)
    xdm('--decompress', t('xark'), '-o', Files.output)
    check_disk_files(Files.output, Files.reference)

    # operations

    # info
    xdm('-Y', '-K', Files.archive, '-t', '-a', r('F127.tfi'), r('V127.tfi'), r('F64V.tfi'), r('V64V.tfi'))
    with open(Files.output, 'w') as fout:
        xdm('-K', Files.archive, '-i', stdout=fout)
    catalog = content_lines(Files.output)
    if 'F127' not in catalog or 'V127' not in catalog or 'F64V' not in catalog or 'V64V' not in catalog:
        error('extract', 'missing entries in archive catalog')

    # add
    xdm(Disks.work, '-X', 'dssd')
    xdm(Disks.work, '-Y', '-K', 'ARC1', '-t', '-a', r('F127.tfi'), r('F16.tfi'), r('F1.tfi'))
    xdm(Disks.work, '-Y', '-K', 'ARC2', '-t', '-a', r('V127.tfi'), r('V16.tfi'), r('V1.tfi'))
    xdm(Disks.work, '-K', 'ARC1', '-t', '-a', r('F64V.tfi'))
    xdm(Disks.work, '-K', 'ARC2', '-t', '-a', r('V64V.tfi'))
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-K', 'ARC1', stdout=fout)
    with open(Files.input, 'w') as fout:
        xdm(Disks.work, '-K', 'ARC2', stdout=fout)
    if len(content_line_array(Files.output)) != 2+4 or len(content_line_array(Files.input)) != 2+4:
        error('add', 'bad catalog after adding files')

    xdm('-X', 'dssd', Disks.work, '-Y', '-K', 'ARCHIVE', '-a', r('F16.tfi'), '-t')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, stdout=fout, rc=0)
    if content_line_array(Files.output)[-1][:10] != 'ARCHIVE   ':
        error('init^2', 'Missing archive on disk')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-K', 'ARCHIVE', stdout=fout, rc=0)
    if content_line_array(Files.output)[-1][:10] != 'F16       ':
        error('init^2', 'Missing file in archive')

    xdm('-X', 'dssd', Disks.work, '-Y', '-K', 'ARCHIVE', '-a', r('F16.tfi'), '-t', '-o', Disks.work2)
    check_binary_files_eq('init^2-o', Disks.work, Disks.work2, mask=Masks.disk_dates(1))

    xdm('-Y', '-K', Files.archive, '-a', r('F129.tfi'), '-t')
    xdm('-K', Files.archive, '-e', 'F129', '-o', Files.reference)
    xdm('-Y', '-K', Files.archive, '-a', r('F129.v9t9'), '-9')
    xdm('-K', Files.archive, '-e', 'F129', '-o', Files.output)
    check_binary_files_eq('archive v9t9', Files.output, Files.reference)

    # addark
    shutil.copyfile(Disks.recsdis, Disks.work)
    xdm(Disks.work, '-Y', '-K', 'ARC', '-A', 'F127', 'F128', 'F129', 'V16', 'V254', 'V64V')
    xdm(Disks.work, '-e', 'ARC', '-o', Files.output)
    xdm('-K', Files.output, '-t', '-e', 'F127', 'F128', 'F129', 'V16', 'V254', 'V64V', '-o', Dirs.tmp)
    check_tifiles(t('f127.tfi'), r('F127.tfi'))
    check_tifiles(t('f128.tfi'), r('F128.tfi'))
    check_tifiles(t('f129.tfi'), r('F129.tfi'))
    check_tifiles(t('v16.tfi'), r('V16.tfi'))
    check_tifiles(t('v254.tfi'), r('V254.tfi'))
    check_tifiles(t('v64v.tfi'), r('V64V.tfi'))
    xdm('-K', Files.archive, '-Y', '-t', '-a', t('f127.tfi'), t('f128.tfi'), t('f129.tfi'), t('v16.tfi'),
        t('v254.tfi'), t('v64v.tfi'))
    check_archive(Files.archive, Files.output)

    # exark
    xdm(Disks.work, '-X', 'dssd', '-a', Files.archive, '-n', 'ARC', '-f', 'DIS/FIX128')
    xdm(Disks.work, '-K', 'ARC', '-E', 'F129', 'V16', 'V254')
    xdm(Disks.work, '-t', '-e', 'F129', 'V16', 'V254')
    for name in ('f129', 'v16', 'v254'):
        check_tifiles(t(name) + '.tfi', r(name.upper() + '.tfi'))

    # other operations
    xdm('-X', 'DSSD', Disks.work, '-n', 'DISK')
    xdm(Disks.work, '-Y', '-K', 'ARK', '-a', r('F16.tfi'), r('V16.tfi'), '-t')
    xdm(Disks.work, '-K', 'ARK', '-r', 'F16:FIX', 'V16:VAR')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-K', 'ARK', stdout=fout)
    cat = content(Files.output)
    if b'F16' in cat or b'V16' in cat or b'FIX' not in cat or b'VAR' not in cat:
        error('archive ops', 'Bad catalog after renaming')

    xdm(Disks.work, '-K', 'ARK', '-w', 'VAR')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-K', 'ARK', stdout=fout)
    if 'P' not in content_line_array(Files.output)[-1]:
        error('protect', 'File not protected')

    xdm(Disks.work, '-K', 'ARK', '-d', 'FIX')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-K', 'ARK', stdout=fout)
    cat = content(Files.output)
    if b'FIX' in cat or b'VAR' not in cat:
        error('archive ops', 'Bad catalog after deleting')

    # details checks
    xdm('-X', 'dssd', Disks.work, '-Y', '-K', 'ARKIVE', '-a', r('F64V.tfi'), r('V64V.tfi'), '-t')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, stdout=fout)
    if len(content_line_array(Files.output)) != 3:
        error('initialize', 'Error initializing both disk and archive')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-K', 'ARKIVE', stdout=fout)
    if len(content_line_array(Files.output)) != 4:
        error('initialize', 'Error initializing both disk and archive')

    # remove temporary files
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
