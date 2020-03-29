#!/usr/bin/env python

import os

from config import Files, Dirs
from utils import xbas, check_binary_files_eq, error


# Main test

def runtest():
    """check xbas99 CLI"""

    # -o
    source = os.path.join(Dirs.basic, 'bashello.bas')
    xbas(source, '-c', '-o', Files.reference)
    with open(Files.output, 'wb') as fout:
        xbas(source, '-c', '-o', '-', rc=0, stdout=fout)
    check_binary_files_eq('stdout', Files.output, Files.reference)

    xbas(source, '-c', '-o', Dirs.tmp)
    if not os.path.isfile(os.path.join(Dirs.tmp, 'bashello.prg')):
        error('output', '-o <dir> failed')

    # join
    source = os.path.join(Dirs.basic, 'basjoin.bas')
    xbas(source, '-c', '-j', '1,10', '-o', Files.output, rc=0)
    xbas(source, '-c', '-j', ',10', '-o', Files.output, rc=0)
    xbas(source, '-c', '-j', '1,', '-o', Files.output, rc=0)
    with open(Files.error, 'w') as ferr:
        xbas(source, '-c', '-j', '10', '-o', Files.output, rc=1, stderr=ferr)  # incorrect

    # invalid option combinations
    source = os.path.join(Dirs.basic, 'bashello.bas')
    with open(Files.error, 'w') as ferr:
        xbas(source, '-c', '-j', '1,1', '-l', rc=2, stderr=ferr)
        xbas(source, '-d', '-l', rc=2, stderr=ferr)
        xbas(source, '-d', '-j', '9,9', rc=2, stderr=ferr)
        xbas(source, '-d', '--protect', rc=2, stderr=ferr)

    program = os.path.join(Dirs.basic, 'sample-l.bin')
    xbas(program, '-d', '-L', '-o', Files.output, rc=0)  # useless. but OK

    # cleanup
    os.remove(Files.output)
    os.remove(Files.error)


if __name__ == '__main__':
    runtest()
    print('OK')
