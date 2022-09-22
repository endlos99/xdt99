#!/usr/bin/env python3

import os
import shutil
import re
import gzip

from config import Dirs, Disks, Files, XHM99_CONFIG
from utils import xhm, xdm, error, clear_env, delfile, check_files_eq, check_bin_text_eq, content_len, content_lines


# Check functions

def check_file_contains(infile, pattern):
    """check if text file contains at least one RE match"""
    try:
        with open(infile, 'r') as fin:
            for line in fin:
                if re.search(pattern, line):
                    return
    except IOError:
        pass
    error('HFE', f'{infile}: no match found')


# Main test

def runtest():
    """check command line interface"""

    clear_env(XHM99_CONFIG)

    # conversion HFE <-> disk pseudo-disks
    for n in ['rsssd', 'rdssd', 'rssdd', 'rdsdd', 'rsssd80t', 'rdssd80t', 'tiit80t']:
        refdsk = os.path.join(Dirs.hfe, n + '.dsk')
        refhfe = os.path.join(Dirs.hfe, n + '_dsk.hfe.gz')
        with gzip.open(refhfe, 'rb') as fin, open(Files.reference, 'wb') as fout:
            fout.write(fin.read())
        xhm('-T', refdsk, '-o', Files.input)
        check_files_eq('HFE', Files.input, Files.reference, 'PROGRAM')
        xhm('-F', Files.input, '-o', Files.output)
        check_files_eq('HFE', Files.output, refdsk, 'PROGRAM')

    # xdm99 delegation
    with gzip.open(Disks.hfe, 'rb') as fin, open(Disks.work, 'wb') as fout:
        fout.write(fin.read())
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, stdout=fout)
    check_file_contains(Files.output, 'HFEDISK.*1S/1D.*40')
    check_file_contains(Files.output, 'HFEFILE')

    # image manipulation
    ref = os.path.join(Dirs.refs, 'ti-text')
    xhm(Disks.work, '-a', ref, '-n', 'TESTFILE', '-f', 'DV60')
    xhm(Disks.work, '-e', 'TESTFILE', '-o', Files.output)
    xhm('-o', Files.output, Disks.work, '-e', 'TESTFILE')
    check_files_eq('HFE', Files.output, ref, 'DV')
    with open(Files.output, 'wb') as fout:
        xhm(Disks.work, '-p', 'TESTFILE', stdout=fout)
    check_bin_text_eq('HFE', Files.output, ref)

    ref = os.path.join(Dirs.refs, 'V10R.tfi')
    shutil.copyfile(ref, Files.reference)
    xhm(Disks.work, '-a', Files.reference, '-t')
    xhm(Disks.work, '-e', 'V10R', '-o', Files.output)
    xhm('-o', Files.output, Disks.work, '-e', 'V10R')
    ref = os.path.join(Dirs.refs, 'v10r.txt')
    check_bin_text_eq('HFE', Files.output, ref)

    # image resize
    with open(Files.output, 'w') as fout:
        xhm('--hfe-info', Disks.work, stdout=fout)
    check_file_contains(Files.output, 'Tracks: 40')
    check_file_contains(Files.output, 'Sides: 1')
    check_file_contains(Files.output, 'Encoding: 2')  # SD
    xhm(Disks.work, '-Z', 'dsdd')
    with open(Files.output, 'w') as fout:
        xhm('--hfe-info', Disks.work, stdout=fout)
    check_file_contains(Files.output, 'Tracks: 40')
    check_file_contains(Files.output, 'Sides: 2')
    check_file_contains(Files.output, 'Encoding: 0')  # DD

    # image creation
    xhm(Disks.work, '-X', 'dssd80t', '-a', ref, '-n', 'WALDO')
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, '-i', stdout=fout)
    check_file_contains(Files.output, r'2S/1D\s+80')
    check_file_contains(Files.output, r'WALDO.*PROGRAM')
    with open(Files.output, 'w') as fout:
        xhm('--hfe-info', Disks.work, stdout=fout)
    check_file_contains(Files.output, 'Tracks: 80')
    check_file_contains(Files.output, 'Sides: 2')
    check_file_contains(Files.output, 'Encoding: 2')  # SD

    xhm(Disks.work, '-X', 'sssd', '-n', 'DISKNAME')
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, '-i', stdout=fout)
    if content_lines(Files.output)[:10] != 'DISKNAME  ':
        error('init', 'Incorrect disk name when initializing')

    # messy stuff
    xdm(Disks.work, '-X', 'sssd')
    xdm(Disks.work, '-q', '--set-geometry', 'dssd')  # image too short now!
    xhm('-T', Disks.work, '-o', Files.input)
    with open(Files.output, 'w') as fout:
        xhm('--hfe-info', Files.input, stdout=fout)
    check_file_contains(Files.output, r'Tracks: 40')
    check_file_contains(Files.output, r'Sides: 2')  # DS
    check_file_contains(Files.output, r'Encoding: 2')  # SD
    with open(Files.error, 'w') as ferr:  # suppress error msg
        xhm(Files.input, stderr=ferr, rc=1)  # invalid track count

    # default options
    source = os.path.join(Dirs.disks, 'recsdis.dsk')
    shutil.copyfile(source, Files.input)
    os.environ[XHM99_CONFIG] = '-T non-existing-file'
    with open(Files.error, 'w') as ferr:
        xhm('-F', Files.input, '-o', Files.output, stderr=ferr, rc=2)  # system error

    delfile(Files.output)
    delfile(Files.error)
    with gzip.open(Disks.hfe, 'rb') as fin, open(Files.input, 'wb') as fout:
        fout.write(fin.read())
    os.environ[XHM99_CONFIG] = '-o ' + Files.error
    xhm(Files.input, '-e', 'HFEFILE', '-o', Files.output)
    if content_len(Files.error) > 0 or content_len(Files.output) <= 0:
        error('defaults', 'default options override not working')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
