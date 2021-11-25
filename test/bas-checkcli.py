#!/usr/bin/env python

import os

from config import Files, Dirs, XBAS99_CONFIG
from utils import xbas, check_binary_files_eq, error, clear_env, delfile, content_len


# Main test

def runtest():
    """check xbas99 CLI"""

    clear_env(XBAS99_CONFIG)

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

    # default options
    source = os.path.join(Dirs.basic, 'bashello.bas')
    os.environ[XBAS99_CONFIG] = '-c'
    xbas(source, '-o', Files.output, rc=0)

    delfile(Files.output)
    delfile(Files.error)
    os.environ[XBAS99_CONFIG] = '-o ' + Files.error
    xbas(source, '-c', '-o', Files.output)
    if content_len(Files.error) > 0 or content_len(Files.output) <= 0:
        error('defaults', 'default options override not working')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
