#!/usr/bin/env python3

import os
import re
import zipfile

from config import Dirs, Files, XGA99_CONFIG
from utils import (xga, t, error, clear_env, delfile, check_files_eq, check_binary_files_eq, content, content_len,
                   content_line_array, read_stderr, get_source_markers, check_errors)


# check functions

def check_bin_text_equal_c(outfile, reffile):
    with open(outfile, 'r') as fout, open(reffile, 'rb') as fref:
        txt = ' '.join([line for line in fout if ';' not in line])
        bin = fref.read()
    if len(bin) % 2 != 0:
        bin += bytes(1)
    words = [(bin[i + 1] << 8) + bin[i] for i in range(0, len(bin), 2)]
    texts = [int(m, 16) for m in re.findall(r'0x([0-9a-f]{4})', txt)]
    if words != texts:
        error('0x', '0x/word mismatch')


def check_bin_text_equal_basic(outfile, reffile):
    with open(outfile, 'r') as fout, open(reffile, 'rb') as fref:
        txt = ' '.join(fout.readlines())
        bin = fref.read()
    if len(bin) % 2 != 0:
        bin += b'\x00'
    words = [(bin[i] << 8) + bin[i + 1] for i in range(0, len(bin), 2)]
    texts = [int(m) % 0x10000 for m in re.findall(r'(-?[0-9]{1,5})', txt)]
    if words != texts:
        error('DATA', 'DATA/word mismatch')


def check_text_eq(outfile, reffile):
    lino = 0
    with open(outfile, 'r') as fout, open(reffile, 'r') as fref:
        lino += 1
        outline = fout.readline().strip()
        refline = fref.readline().strip()
        if outline != refline:
            error('listing', f"Text lines don't match in line {lino:d}")


def check_list_addr_data(infile, reffile, addr):
    code_lines = {}
    with open(infile, 'r') as fin, open(reffile, 'rb') as fref:
        lines = fin.readlines()
        data = fref.read()
    for line in lines:
        m = re.search(r'^(?:\w{4}|    ) (\w{4}) (\w{2})', line)
        if m:
            idx = int(m.group(1), 16)
            if idx in code_lines:
                error('listing', f'Duplicate address >{idx:x}')
            code_lines[idx] = int(m.group(2), 16)
    for byte_ in data:
        try:
            if code_lines[addr] != byte_:
                error('listing', f'Address/data mismatch at address >{addr:x}')
        except KeyError:
            error('listing', f'Missing address >{addr:x} in listing file')
        addr += 1


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    clear_env(XGA99_CONFIG)

    # input and output files
    source = os.path.join(Dirs.gplsources, 'gacart.gpl')
    with open(Files.output, 'wb') as f:
        xga(source, '-o', '-', stdout=f)
    xga(source, '-o', Files.reference)
    check_files_eq('stdout', Files.output, Files.reference, 'P')

    xga(source, '-o', Dirs.tmp)
    if not os.path.isfile(t('gacart.gbc')):
        error('output', '-o <dir> failed')

    with open(Files.output, 'wb') as f:
        xga(source, '-G', '>6000', '-A', '>0030', '-o', '-', stdout=f)
    xga(source, '-G', '>6000', '-A', '>0030', '-o', Files.reference)
    check_files_eq('stdout', Files.output, Files.reference, 'P')

    with open(Files.output, 'w') as f:
        xga(source, '-o', Files.input, '-L', '-', stdout=f)
    xga(source, '-o', Files.input, '-L', Files.reference)
    check_text_eq(Files.output, Files.reference)

    source = os.path.join(Dirs.gplsources, 'nonexisting')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, '--color', 'off', stderr=ferr, rc=1)
    with open(Files.error, 'r') as ferr:
        errs = ferr.readlines()
    if len(errs) != 1 or errs[0].strip() != 'Error: File not found: nonexisting':
        error('File error', 'Incorrect file error message')

    # text -t
    source = os.path.join(Dirs.gplsources, 'gacart.gpl')
    xga(source, '-o', Files.reference)
    xga(source, '-t', 'c4r', '-o', Files.output)
    check_bin_text_equal_c(Files.output, Files.reference)

    xga(source, '-t', 'b4', '-o', Files.output)
    check_bin_text_equal_basic(Files.output, Files.reference)

    # listing and symbols -L
    source = os.path.join(Dirs.gplsources, 'gahello.gpl')
    xga(source, '-o', Files.error, '-L', Files.input)
    xga(source, '-o', Files.reference)
    with open(Files.input, 'r') as flist, open(Files.error, 'w') as fout:
        listfile = [line[14:] for line in flist.readlines() if line[0:4].isdigit()]
        fout.writelines(listfile)
    xga(Files.error, '-o', Files.output)
    check_binary_files_eq('listing', Files.output, Files.reference)  # checks code
    check_list_addr_data(Files.input, Files.reference, 0x0030)  # checks addr and data

    # macro errors
    source = os.path.join(Dirs.gplsources, 'gamacse.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=1)
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, tag=r';ERROR')
    check_errors(exp_errors, act_errors)

    # color
    source = os.path.join(Dirs.gplsources, 'gaerrs1.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '--color', 'on', '-o', Files.output, stderr=ferr, rc=1)
    errors = content(Files.error, mode='r')
    if '\x1b[31m' not in errors or '\x1b[33m' not in errors:
        error('color', 'Missing color in errors and warnings')

    # relaxed syntax
    source = os.path.join(Dirs.gplsources, 'gaxrelax.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-r', '-o', Files.output, stderr=ferr, rc=0)

    # default options
    delfile(Files.input)
    source = os.path.join(Dirs.gplsources, 'gahello.gpl')
    os.environ[XGA99_CONFIG] = '-L ' + Files.input
    xga(source, '-o', Files.output)
    if content_len(Files.input) <= 0:
        error('defaults', 'default options not working')

    delfile(Files.input)
    delfile(Files.error)
    os.environ[XGA99_CONFIG] = '-L ' + Files.error
    xga(source, '-o', Files.output, '-L', Files.input)
    if content_len(Files.error) > 0:
        error('defaults', 'default options override not working')

    # platform-agnostic paths
    source = os.path.join(Dirs.gplsources, 'gawin.gpl')
    xga(source, '-o', Files.output)
    if content(Files.output) != bytes((0, 1, 0, 2, 0, 2, 0, 1)):
        error('wincopy', 'File with Windows paths mismatch')

    # paths as filenames for -o, -L, -E
    source = os.path.join(Dirs.gplsources, 'gamulf.gpl')
    xga(source, '-g', '-o', Dirs.tmp)
    if (content(t('gamulf_g1.gbc')) != b'\x01' * 10 or
            content(t('gamulf_g5.gbc')) != b'\x02' * 16 or
            content(t('gamulf_g7.gbc')) != b'\x03' * 32):
        error('path output', 'Image contents mismatch')

    xga(source, '-o', Files.output, '-L', Dirs.tmp)
    if content_line_array(t('gamulf.lst'))[0][:31] != 'XGA99 CROSS-ASSEMBLER   VERSION':
        error('path output', 'List file contents mismatch')

    xga(source, '-o', Files.output, '-L', Files.input, '-E', Dirs.tmp)
    if len(content_line_array(t('gamulf.equ'))) != 6:
        error('path output', 'Equ file contents mismatch')

    # new cart
    source = os.path.join(Dirs.gplsources, 'ganalign.gpl')  # prerequisite: proper padding between GROMs
    xga(source, '-o', Files.output)
    data = content(Files.output)
    if data[0] != 5 or data[0x1800] != 6 or data[0x4f00] != 7:
        error('padding', 'Incorrect non-aligned byte code')

    xga(source, '-B', '-o', Files.output)
    data = content(Files.output)
    if len(data) != 0x6000 or data[0x1000] != 5 or data[0x2800] != 6 or data[0x5f00] != 7:
        error('padding', 'Incorrect GROM padding')

    source = os.path.join(Dirs.gplsources, 'gacart.gpl')
    xga(source, '-c', '-o', Files.output)  # assumes GROM 3
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('GACART.bin')
    if data[0] != 0xaa or data[0x12:0x14] != b'\x60\x1b' or data[0x30] == 0xaa:
        error('cart', 'Incorrect GPL header')

    source = os.path.join(Dirs.gplsources, 'gacarthdr.gpl')
    xga(source, '-c', '-o', Files.output)
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('GACARTHDR.bin')
    if len(data) != 0x2031 or data[0x1000] != 1 or data[0] != 0xaa or data[0x2000] == 0xaa:
        error('cart', 'Incorrect GPL header')

    source = os.path.join(Dirs.gplsources, 'gacarthdr.gpl')
    xga(source, '-c', '-D', 'AA', '-o', Files.output)
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('GACARTHDR.bin')
    if len(data) != 0x2031 or data[0x1000] != 1 or data[0] == 0xaa or data[0x2000] != 0xaa:
        error('cart', 'Incorrect GPL header')

    source = os.path.join(Dirs.gplsources, 'gacarthi.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-c', '-o', Files.output, stderr=ferr, rc=0)
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('GACARTHI.bin')
    if len(data) != 0x4020 or data[0] != 0xaa or data[0x3000] != 3 or data[0x2000] == 0xaa or data[0x4000] != 0x2e:
        error('cart', 'Incorrect cart without GPL header')
    if not content(Files.error):
        error('cart', 'Missing warning about overwriting data')

    xga(source, '-c', '-D', 'AA', '-o', Files.output)
    with zipfile.ZipFile(Files.output, 'r') as archive:
        data = archive.read('GACARTHI.bin')
    if (len(data) != 0x4021 or data[0] == 0xaa or data[0x3000] != 3 or data[0x2000] == 0xaa or data[0x4000] != 0xaa or
            data[0x4001] != 0x2e):
        error('cart', 'Incorrect cart with GPL header')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
