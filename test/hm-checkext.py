#!/usr/bin/env python3

import re

from config import Dirs, Disks, Files, Masks, XHM99_CONFIG
from utils import (xhm, error, t, r, clear_env, delfile, content, content_len, content_cat, content_line_array,
                   check_binary_files_eq)


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

    # archive
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, '-X', 'dssd', '-K', 'ARK', '-Y', stdout=fout, rc=0)
    if content_len(Files.output) > 0:
        error('archive', 'Initialization not silent')

    with open(Files.output, 'w') as fout:
        xhm(Disks.work, '-X', 'dssd', '-K', 'ARK', '-Y', '-t', '-a', r('F16.tfi'), r('V64V.tfi'), stdout=fout, rc=0)
    if content_len(Files.output) > 0:
        error('archive', 'Initialization and adding files not silent')
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, stdout=fout, rc=0)
    if len(content_line_array(Files.output)) != 3:
        error('archive', 'Catalog disk incorrect')
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, '-K', 'ARK', stdout=fout, rc=0)
    if len(content_line_array(Files.output)) != 4:
        error('archive', 'Catalog archive incorrect')

    xhm(Disks.work, '-e', 'ARK', '-9', '-o', Files.output)
    if content(Files.output)[:10] != b'ARK       ':
        error('archive', 'Error getting file from disk')
    xhm(Disks.work, '-e', '*V', '-K', 'ARK', '-t', '-o', Files.output)
    check_binary_files_eq('archive', Files.output, r('V64V.tfi'), mask=Masks.tifiles_date)

    xhm(Disks.work, '-X', 'dssd', '-a', r('arkfileall_ark'), '-f', 'IF128', '-n', 'ZIP')
    xhm(Disks.work, '-K', 'ZIP', '-E', '*T')
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, stdout=fout)
    catalog = content_line_array(Files.output)
    expected = ['ZIP       :     202 used  518 free   180 KB  2S',
                '-----------------------------------------------',
                'ARKFILE1T     5  DIS/VAR 80     841 B   18 recs',
                'ARKFILE2T    72  DIS/VAR 80   18001 B  237 recs',
                'ARKFILE5T     2  DIS/VAR 30     128 B    5 recs',
                'ZIP         121  INT/FIX 128  30720 B  240 recs']
    for i in range(len(catalog)):
        if catalog[i][:47] != expected[i]:
            error('exark', 'Incorrect catalog')

    xhm(Disks.work, '-Y', '-K', 'ALLTHEFILES', '-A', '*')
    with open(Files.output, 'w') as fout:
        xhm(Disks.work, stdout=fout)
    catalog = content_line_array(Files.output)
    expected = ['ZIP       :     394 used  326 free   180 KB  2S',
                '-----------------------------------------------',
                'ALLTHEFILE  192  INT/FIX 128  48768 B  381 recs',
                'ARKFILE1T     5  DIS/VAR 80     841 B   18 recs',
                'ARKFILE2T    72  DIS/VAR 80   18001 B  237 recs',
                'ARKFILE5T     2  DIS/VAR 30     128 B    5 recs',
                'ZIP         121  INT/FIX 128  30720 B  240 recs']
    for i in range(len(catalog)):
        if catalog[i][:47] != expected[i]:
            error('addark', 'Incorrect catalog')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
