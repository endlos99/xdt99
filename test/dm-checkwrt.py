#!/usr/bin/env python

import os
import shutil
import random

from config import Dirs, Disks, Files
from utils import xdm, error, check_files_eq, check_text_files_eq


# Utility functions

def create_textline(length):
    """create line of random text with checksum"""
    vs = [random.randint(0, 79) for _ in range(length - 1)]
    cc = (- sum(vs)) % 80
    return ''.join(chr(v + 48) for v in vs + [cc])


def create_blob(size):
    """create random binary data with checksum"""
    vs = [random.randint(0, 255) for _ in range(size - 1)]
    cc = (- sum(vs)) % 256
    return bytes(vs + [cc])


def create_text_file(count, length, fixed, partial):
    """create text file with random records"""
    name = 'D%c%03dX%03d%s' % ('F' if fixed else 'V', length, count,
                               'P' if partial else '')
    path = os.path.join(Dirs.tmp, name.lower())
    lines = [create_textline(random.randint(0, length) if partial else length) for _ in range(count)]
    if fixed:
        data = ''.join([l + ' ' * (length - len(l)) for l in lines])
        fmt = 'DIS/FIX' + str(length)
    else:
        data = '\n'.join(lines) + '\n'
        fmt = 'DIS/VAR' + str(length)
    with open(path, 'w') as f:  # 'w' mangles \n into \r\n
        f.write(data)
    return name, path, fmt


def create_binary_file(size):
    """create binary file with random binary data"""
    name = 'PROG%05d' % size
    path = os.path.join(Dirs.tmp, name.lower())
    data = create_blob(size)
    with open(path, 'wb') as f:
        f.write(data)
    return name, path, 'PROGRAM'


# Check functions

def check_trunc(infile, lines, length):
    """check prefixes of lines"""
    with open(infile, 'r') as f:
        for i, inline in enumerate(f):
            if inline.rstrip() != lines[i].rstrip()[:length]:
                error('Truncated records', 'Record %d mismatch' % i)


# Main test

def runtest():
    """check reading and writing of random data"""
    
    # setup
    shutil.copyfile(Disks.blank, Disks.work)
    shutil.copyfile(Disks.blank, Disks.tifiles)

    # create files
    files = []
    for count, length in [
            (1, 2), (300, 2), (60, 10), (10, 63), (10, 64), (10, 126),
            (1, 127), (10, 127), (10, 128), (10, 129), (1, 254), (5, 254),
            (1, 255), (5, 255)
            ]:
        files.append(create_text_file(count, length, False, False))
        files.append(create_text_file(count, length, True, False))
    for count, length in [(20, 127), (15, 254), (15, 255)]:
        files.append(create_text_file(count, length, False, True))
        files.append(create_text_file(count, length, True, True))
    for size in [1, 2, 254, 255, 511, 513, 2560]:
        files.append(create_binary_file(size))

    bigFiles = []
    for count, length in [(200, 127), (100, 254), (100, 255)]:
        bigFiles.append(create_text_file(count, length, False, True))
        bigFiles.append(create_text_file(count, length, True, True))
    for size in [25600]:
        bigFiles.append(create_binary_file(size))

    # add files one by one and check
    for name, path, fmt in files:
        xdm(Disks.work, '-a', path, '-f', fmt)
        xdm(Disks.work, '-e', name, '-o', Files.output)
        check_files_eq('Write records', Files.output, path, fmt)

    # remove files one by one and check
    for name, path, fmt in files:
        xdm(Disks.work, '-e', name, '-o', Files.output)
        check_files_eq('Write records', Files.output, path, fmt)
        xdm(Disks.work, '-d', name)

    # add all files
    for name, path, fmt in files:
        xdm(Disks.work, '-a', path, '-f', fmt)

    # extract in and convert to/from TIFiles format
    for name, path, fmt in files:
        xdm(Disks.work, '-e', name, '-o', Files.reference)
        xdm(Disks.work, '-e', name, '-t', '-o', Files.tifile)
        xdm('-F', Files.tifile, '-o', Files.output)
        check_files_eq('Write records', Files.output, Files.reference, fmt)
        xdm('-T', Files.reference, '-o', Files.output, '-f', fmt, '-n', name)
        check_files_eq('Write records', Files.output, Files.tifile,
                     'PROGRAM', [(0x1e, 0x26)])

    # add and remove TIFiles files
    for name, path, fmt in files:
        xdm(Disks.work, '-e', name, '-t', '-o', Files.tifile)
        xdm(Disks.tifiles, '-t', '-a', Files.tifile)
    check_files_eq('Write records', Disks.tifiles, Disks.work, 'P')

    # convert to and from TIFiles cycle
    for name, fmt in [('intvar32v', 'IV32'), ('intfix32v', 'IF32'),
                      ('vardis', 'dv40')]:
        path = os.path.join(Dirs.refs, name)
        xdm(Disks.work, '-a', path, '-f', fmt, '-n', 'T')
        xdm(Disks.work, '-e', 'T', '-t', '-o', Files.output)
        xdm(Disks.work, '-d', 'T')
        xdm(Disks.work, '-a', Files.output, '-t')
        xdm(Disks.work, '-e', 'T', '-o', Files.output)
        check_text_files_eq('TIFiles', Files.output, path)

    # add and remove big files
    for name, path, fmt in bigFiles:
        xdm(Disks.work, '-a', path, '-f', fmt)
        xdm(Disks.work, '-e', name, '-o', Files.output)
        check_files_eq('Write records', Files.output, path, fmt)
        xdm(Disks.work, '-d', name)

    # check truncating of DIS/VAR files with long records
    path = os.path.join(Dirs.refs, 'vardis')
    with open(path, 'r') as f:
        reflines = f.readlines()
    for l in [8, 7, 4]:
        xdm(Disks.work, '-a', path, '-f', 'DV%d' % l, '-q')
        xdm(Disks.work, '-e', 'VARDIS', '-o', Files.output)
        check_trunc(Files.output, reflines, l)

    # create well-defined TI disk (checked-in state frozen)
    shutil.copyfile(Disks.recsgen, Disks.work)
    for name, path, fmt in files:
        xdm(Disks.work, '-a', path, '-f', fmt)

    # remove temporary files
    for name, path, fmt in files + bigFiles:
        os.remove(path)
    os.remove(Files.output)
    os.remove(Files.tifile)
    os.remove(Files.reference)
    os.remove(Disks.work)
    os.remove(Disks.tifiles)


if __name__ == '__main__':
    runtest()
    print('OK')
