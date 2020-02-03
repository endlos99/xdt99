#!/usr/bin/env python

import os

from config import Dirs, Files
from utils import xga, error, read_stderr, get_source_markers, check_errors


# Main test

def runtest():
    """run regression tests"""

    # check for errors
    source = os.path.join(Dirs.gplsources, 'gaerrs.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=1)
    act_errors = read_stderr(Files.error, include_warnings=False)
    exp_errors = get_source_markers(source, tag=r';ERROR')
    check_errors(exp_errors, act_errors)

    # error messages in pass 0 and 1
    for s in ['gaerrs0.gpl', 'gaerrs1.gpl']:
        source = os.path.join(Dirs.gplsources, s)
        with open(Files.error, 'w') as ferr:
            xga(source, '-o', Files.output, stderr=ferr, rc=1)
        act_errors = read_stderr(Files.error, include_warnings=False)
        exp_errors = get_source_markers(source, tag=r'\* ERROR')
        check_errors(exp_errors, act_errors)

    # open .if-.endif or .defm-.endm
    source = os.path.join(Dirs.gplsources, 'gaopenif.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=1)
    with open(Files.error, 'r') as fin:
        msgs = ' '.join(fin.readlines())
    if 'Missing .endif' not in msgs:
        error('open', 'Missing error for open .if/.endif')

    source = os.path.join(Dirs.gplsources, 'gaopenmac.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=1)
    with open(Files.error, 'r') as fin:
        msgs = ' '.join(fin.readlines())
    if 'Missing .endm' not in msgs:
        error('open', 'Missing error for open .defm/.endm')

    # warnings
    source = os.path.join(Dirs.gplsources, 'gawarn.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=0)
    act_errors = read_stderr(Files.error, include_warnings=True)
    exp_errors = get_source_markers(source, tag=r';WARN')
    check_errors(exp_errors, act_errors)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.error)


if __name__ == '__main__':
    runtest()
    print('OK')
