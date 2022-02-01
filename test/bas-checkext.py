#!/usr/bin/env python3

import os

from config import Files, Dirs, XBAS99_CONFIG
from utils import xbas, error, delfile, check_binary_files_eq


# Check functions

def check_errors(errfile):
    with open(errfile, 'r') as f:
        errlines = f.readlines()[:-1][::2]
    errlinos = ''.join(line[:3] for line in errlines)
    if errlinos != '[2][5][7]':
        error('labels', 'Bad error messages')


def check_unused_labels(errfile):
    with open(errfile, 'r') as f:
        unusedline = f.readlines()[-1]
    labels = unusedline[24:-1]
    if labels != 'LOOP PRINT EVEN DONE':
        error('unused labels', 'Incorrect list of unused labels')


# Main test

def runtest():
    """check extensions to BASIC editor"""

    os.environ[XBAS99_CONFIG] = '--color off'

    # labels
    for name in ('baslab1', 'baslab2', 'baslab3'):
        source = os.path.join(Dirs.basic, name + '.bas')
        ref = os.path.join(Dirs.basic, name + 'n.bas')
        xbas(source, '-l', '-c', '-q', '-o', Files.output)
        xbas(ref, '-c', '-q', '-o', Files.reference)
        check_binary_files_eq('labels', Files.output, Files.reference)

    source = os.path.join(Dirs.basic, 'niml.bas')
    xbas(source, '-c', '-l', '-o', Files.output)
    ref = os.path.join(Dirs.basic, 'nim.bas')
    xbas(ref, '-c', '-o', Files.reference)
    check_binary_files_eq('labels', Files.output, Files.reference)

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
