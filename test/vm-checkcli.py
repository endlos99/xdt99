#!/usr/bin/env python3

import os
import shutil

from config import Dirs, Disks, Files, XVM99_CONFIG
from utils import xvm, xdm, error, clear_env, delfile, check_files_eq, content_len


# Check functions

def check_file_len(infile, minlines=-1, maxlines=99999):
    """check if file has certain length"""
    try:
        with open(infile, 'r') as f:
            line_count = len(f.readlines())
    except IOError:
        line_count = 0
    if not minlines <= line_count <= maxlines:
        error('CLI',
              f'{infile}: Line count mismatch: found {line_count:d} lines, expected {minlines:d} to {maxlines:d}')


# Main test

def runtest():
    """check command line interface"""

    clear_env(XVM99_CONFIG)

    # setup
    with open(Disks.volumes, 'wb') as v:
        for i in range(4 * 1600):
            v.write(bytes(2 * 256))  # Disk.bytes_per_sector plus padding
    shutil.copyfile(Disks.recsgen, Disks.work)

    # volume operations
    xvm(Disks.volumes, '2', '-w', Disks.recsgen, '--keep-size')
    xvm(Disks.volumes, '1,3-4', '-w', Disks.recsdis, '--keep-size')

    with open(Files.error, 'w') as fout:
        xvm(Disks.volumes, '1-5', stdout=fout)
        xvm(Disks.volumes, '4', stdout=fout)
        xvm(Disks.volumes, '5', '-i', stderr=fout, rc=1)

    xvm(Disks.volumes, '2', '-r', Files.output)
    check_files_eq('xvm', Files.output, Disks.recsgen, 'P')
    xvm(Disks.volumes, '1', '-r', Files.output)
    check_files_eq('xvm', Files.output, Disks.recsdis, 'P')
    xvm(Disks.volumes, '4', '-r', Files.output)
    check_files_eq('xvm', Files.output, Disks.recsdis, 'P')
    xvm(Disks.volumes, '4', '-r', Files.output, '--keep-size')
    check_files_eq('xvm', Files.output, Disks.recsdis, 'P', mask=[(360 * 256, 1600 * 256)])

    # file operations
    xvm(Disks.volumes, '2', '-e', 'DF254X015P', '-o', Files.output)
    xdm(Disks.recsgen, '-e', 'DF254X015P', '-o', Files.reference)
    check_files_eq('xvm', Files.output, Files.reference, 'P')

    xvm(Disks.volumes, '1', '-w', Disks.work, '--keep-size')
    ref = os.path.join(Dirs.refs, 'sector1')
    xdm(Disks.work, '-a', ref, '-f', 'DF80')
    xvm(Disks.volumes, '1', '-a', ref, '-f', 'DF80')
    xvm(Disks.volumes, '1', '-r', Files.output)
    check_files_eq('xvm', Files.output, Disks.work, 'P')

    xvm(Disks.volumes, '3', '-w', Disks.work)
    xvm(Disks.volumes, '3', '-a', ref, '-f', 'DF80', '-n', 'REFFILE')
    xvm(Disks.volumes, '3', '-r', Files.output)
    xdm(Files.output, '-e', 'REFFILE', '-q', '-o', Files.reference)

    ref = os.path.join(Dirs.refs, 'glob')
    xvm(Disks.volumes, '1', '-a', ref + '?', '-n', 'GLOBA1', shell=True)
    xvm(Disks.volumes, '1', '-e', 'GLOBA1', '-o', Files.output)
    xvm(Disks.volumes, '1', '-e', 'GLOBA2', '-o', Files.output)
    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, '1', '-e', 'GLOBA3', '-o', Files.output, stderr=ferr, rc=1)
    xvm(Disks.volumes, '1', '-d', 'GLOB*', '-o', Files.output)
    xvm(Disks.volumes, '1', '-a', ref + '*', '-n', 'GLOBB1', shell=True)
    xvm(Disks.volumes, '1', '-e', 'GLOBB1', '-o', Files.output)
    xvm(Disks.volumes, '1', '-e', 'GLOBB2', '-o', Files.output)
    xvm(Disks.volumes, '1', '-e', 'GLOBB3', '-o', Files.output)

    # default options
    xdm(Files.output, '-q', '-X', 'CF')
    with open(Files.reference, 'w') as f:
        f.write('contents')
    xdm(Files.output, '-a', Files.reference, '-n', 'FILE', '-q')
    with open(Files.output, 'rb') as fin, open(Files.input, 'wb') as fout:
        disk = fin.read()
        fout.write(b''.join(bytes((b, 0)) for b in disk))  # spread disk image

    os.environ[XVM99_CONFIG] = '-Z-non-existing'
    with open(Files.output, 'w') as fout, open(Files.error, 'w') as ferr:
        xvm(Files.input, '1', stdout=fout, stderr=ferr, rc=2)

    delfile(Files.output)
    delfile(Files.error)
    os.environ[XVM99_CONFIG] = '-o ' + Files.error
    with open(Files.output, 'w') as fout, open(Files.error, 'w') as ferr:
        xvm(Files.input, '1', '-e', 'FILE', '-o', Files.output, rc=0)
    if content_len(Files.error) > 0 or content_len(Files.output) <= 0:
        error('defaults', 'default options override not working')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
