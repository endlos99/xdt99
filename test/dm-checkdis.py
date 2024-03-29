#!/usr/bin/env python3

import os
import shutil
import re

from config import Dirs, Disks, Files, XDM99_CONFIG
from utils import xdm, r, error, clear_env, delfile, check_bin_text_eq


# Check functions

def check_records_by_checksum(infile):
    """check records by checksum"""
    with open(infile, 'r') as f:
        for i, line in enumerate(f):
            l = line[:-1] if line[-1] == '\n' else line
            s = 0
            for c in l:
                s = (s + ord(c) - 48) % 80
            if s != 0:
                error('VAR Records', f'{infile}: Record {i} checksum mismatch: {s} != 0')


def check_records_by_len(infile, fixed=None):
    """check records by encoded length"""
    refline = b'*'.join([bytes((list(range(64, 127)))) for _ in range(4)])
    if fixed is None:
        with open(infile, 'r') as f:
            records = [line.encode() for line in f]
    else:
        with open(infile, 'rb') as f:
            data = f.read()
            records = [data[i:i + fixed] for i in range(0, len(data), fixed)]
    for i, line in enumerate(records):
        if fixed and len(line) != fixed:
            error('VAR Records', f'{infile}: Record {i} length mismatch: {len(l)} != {fixed}')
        line = line.rstrip()
        s = b'!' + refline[:len(line) - 2] + bytes((i + 49,)) if len(line) > 1 else b''
        if line != s:
            error('VAR Records', f'{infile}: Record {i} content mismatch')


# Main test

def runtest():
    """extract VAR record files generated by DMWRVAR.xb"""

    clear_env(XDM99_CONFIG)

    # setup
    shutil.copyfile(Disks.recsdis, Disks.work)

    # read full-size records
    for reclen in [16, 127, 128, 129, 254, 255]:
        xdm(Disks.work, '-e', 'F' + str(reclen), '-o', Files.output)
        check_records_by_checksum(Files.output)
    for reclen in [16, 126, 127, 128, 254, 255]:
        xdm(Disks.work, '-e', 'V' + str(reclen), '-o', Files.output)
        check_records_by_checksum(Files.output)

    # read partially filled records
    for reclen in [64]:
        xdm(Disks.work, '-e', 'F' + str(reclen) + 'V', '-o', Files.output)
        check_records_by_len(Files.output, fixed=reclen)
    for recid in [
            '64V', '255V1', '255V2', '255V3', '255V4', '255V4', '255V5'
            ]:
        xdm(Disks.work, '-e', 'V' + recid, '-o', Files.output)
        check_records_by_len(Files.output)

    # read special records
    xdm(Disks.work, '-e', 'F10R', '-o', Files.output)
    check_bin_text_eq('VAR Records', Files.output, r('f10r.txt'))
    xdm(Disks.work, '-e', 'V10R', '-o', Files.output)
    check_bin_text_eq('VAR Records', Files.output, r('v10r.txt'))

    # re-write extracted records and check
    for fn in [
            'V1', 'V16', 'V126', 'V127', 'V128', 'V254', 'V64V', 'V255V1',
            'V255V2', 'V255V3', 'V255V4', 'V255V5', 'V10R', 'F10R',
            'F1', 'F16', 'F127', 'F128', 'F129', 'F254', 'F255', 'F64V'
            ]:
        rectype = 'DIS/VAR' if fn[0] == 'V' else 'DIS/FIX'
        reclen = re.search(r'\d+', fn).group(0)
        fmt = rectype + reclen
        xdm(Disks.work, '-e', fn, '-o', Files.reference)
        xdm(Disks.work, '-a', Files.reference, '-n', 'COPY', '-f', fmt)
        xdm(Disks.work, '-e', 'COPY', '-o', Files.output)
        check_bin_text_eq('VAR Records', Files.output, Files.reference)

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
