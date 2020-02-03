#!/usr/bin/env python

import os

from config import Dirs, Files
from utils import xdg, xas, error, content


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    source = os.path.join(Dirs.sources, 'dasource.asm')
    xas(source, '-b', '-R', '-q', '-o', Files.reference, '-E', Files.input)

    # bad command line arguments
    with open(Files.error, 'w') as ferr:
        xdg(Files.reference, '-a', 'foo', '-f', '6666', '-o', Files.output, stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badarg', 'Bad argument not caught')

    with open(Files.error, 'w') as ferr:
        xdg(Files.reference, '-a', 'fff', '-f', '600x', '-o', Files.output, stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badarg', 'Bad argument not caught')

    with open(Files.error, 'w') as ferr:
        xdg(Files.reference, '-a', '1000', '-f', '1000', '-e', '1100', '-o', Files.output, stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badarg', 'Bad argument not caught')

    with open(Files.error, 'w') as ferr:
        xdg(Files.reference, '-a', '1000', '-f', '1000', '-e', '1100-1-1', '-o', Files.output, stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badarg', 'Bad argument not caught')

    # skip all bytes
    with open(Files.error, 'w') as ferr:
        xdg(Files.reference, '-k', '>ffffffff', '-a', '1234', '-f', '1000', '-o', Files.output, stderr=ferr, rc=0)
    if (content(Files.output).strip()[:10] != b'grom >0000' or
            content(Files.output).strip()[-10:] != b'aorg >1234'):
        error('skipall', 'still unskipped content left')

    # missing files
    with open(Files.error, 'w') as ferr:
        xdg('asm/nosuchfile', '-a', '6000', '-f', '6666', '-o', Files.output, stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badfile', 'Bad input file not caught')

    with open(Files.error, 'w') as ferr:
        xdg(Files.reference, '-a', '6000', '-f', '6016', '-S', 'nosuchfile', '-o', Files.output, stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badfile', 'Bad input file not caught')

    # Cleanup
    os.remove(Files.input)
    os.remove(Files.error)
    os.remove(Files.reference)
    try:
        os.remove(Files.output)
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    runtest()
    print('OK')
