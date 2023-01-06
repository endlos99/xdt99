#!/usr/bin/env python3

import os

from config import Dirs, Files, XGA99_CONFIG
from utils import xga, error, clear_env, delfile, read_stderr, get_source_markers, check_errors, content


# Main test

def runtest():
    """run regression tests"""

    clear_env(XGA99_CONFIG)

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
    if 'Missing .ENDIF' not in msgs:
        error('open', 'Missing error for open .if/.endif')

    source = os.path.join(Dirs.gplsources, 'gaopenmac.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=1)
    with open(Files.error, 'r') as fin:
        msgs = ' '.join(fin.readlines())
    if 'Missing .ENDM' not in msgs:
        error('open', 'Missing error for open .defm/.endm')

    # warnings
    source = os.path.join(Dirs.gplsources, 'gawarn.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=0)
    act_errors = read_stderr(Files.error, include_warnings=True)
    exp_errors = get_source_markers(source, tag=r';WARN')
    check_errors(exp_errors, act_errors)

    # warning about arith expressions relying on non-standard precedence
    source = os.path.join(Dirs.gplsources, 'gaaprec.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '--color', 'off', '-o', Files.output, stderr=ferr, rc=0)
    warnings = read_stderr(Files.error, include_warnings=True)
    markers = get_source_markers(source, r';WARN')
    check_errors(markers, warnings)

    # label continuation errors
    source = os.path.join(Dirs.gplsources, 'gapasse.gpl')  # only in pass 0
    with open(Files.error, 'w') as ferr:
        xga(source, '--color', 'off', '-o', Files.output, stderr=ferr, rc=1)
    errs = content(Files.error, mode='r')
    if '<0>' not in errs or '<1>' in errs or '<2>' in errs:
        error('label:', 'Incorrect pass for label continuation error message')

    source = os.path.join(Dirs.gplsources, 'gaxlabe.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '--color', 'off', '-o', Files.output, stderr=ferr, rc=1)
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, tag=r';ERROR')
    check_errors(exp_errors, act_errors)

    # .rept/.endr
    source = os.path.join(Dirs.gplsources, 'gaxrepte.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=1)
    errors = read_stderr(Files.error)
    markers = get_source_markers(source, r';ERROR')
    check_errors(markers, errors)

    source = os.path.join(Dirs.gplsources, 'gaxrepte2.gpl')
    with open(Files.error, 'w') as ferr:
        xga(source, '-o', Files.output, stderr=ferr, rc=1)

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
