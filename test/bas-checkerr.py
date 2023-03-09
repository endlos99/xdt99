#!/usr/bin/env python3

import os

from config import Files, Dirs, XBAS99_CONFIG
from utils import xbas, error, clear_env, delfile, content_line_array, content_cat


# Main test

def runtest():
    """check xbas99 error handling"""

    clear_env(XBAS99_CONFIG)

    for filename, opts, rc, errortext, n in (
            ('baserr1.bas', ('-l', '-c'), 1, 'Error: Unknown label HONK', 2),
            ('baserr2.bas', ('-l', '-c'), 1, 'Error: Label END conflicts with reserved keyword', 0),
            ('baserr3.bas', ('-c',), 1, 'Error: Syntax error after GO', 2)
    ):
        source = os.path.join(Dirs.basic, filename)
        with open(Files.error, 'w') as ferr:
            xbas(source, *opts, '--color', 'off', '-o', Files.output, stderr=ferr, rc=rc)
        errors = content_line_array(Files.error)
        if len(errors) < n + 1 or errors[n].rstrip() != errortext:
            error('errors', 'Bad error message')

    # bad labels
    source = os.path.join(Dirs.basic, 'baserr4.bas')
    with open(Files.error, 'w') as ferr:
        xbas(source, '-c', '-l', '--color', 'off', '-o', Files.output, stderr=ferr, rc=1)
    if (content_cat(Files.error)[24:] !=  # skip version string
            '[8]  GOTO @LOOX Error: Unknown label LOOX Warning: Unused labels: OUT DONE 1 Error found.'):
        error('labels', 'Bad/missing errors')

    source = os.path.join(Dirs.basic, 'baslabe2.bas')
    with open(Files.error, 'w') as ferr:
        xbas(source, '-l', '--color', 'off', '-o', Files.output, stderr=ferr, rc=1)
    if (content_line_array(Files.error)[0] !=
            'Error: Label RND conflicts with reserved keyword\n'):
        error('labels', 'Reserved keyword')

    source = os.path.join(Dirs.basic, 'duplaberr.bas')
    with open(Files.error, 'w') as ferr:
        xbas(source, '-l', '--color', 'off', '-o', Files.output, stderr=ferr, rc=1)
    if 'Duplicate label DUP_LABEL' not in content_line_array(Files.error)[0]:
        error('labels', 'Incorrect duplicate label error message')

    # bad local labels
    source = os.path.join(Dirs.basic, 'localerr1.bas')
    with open(Files.error, 'w') as ferr:
        xbas(source, '-l', '-q', '--color', 'off', '-o', Files.output, stderr=ferr, rc=1)
    err = content_line_array(Files.error, strip=True)
    if err[1][-6:] != '!ERROR' or err[3][-6:] != '!ERROR':
        error('local labels', 'Incorrect error messages')

    source = os.path.join(Dirs.basic, 'localerr2.bas')
    with open(Files.error, 'w') as ferr:
        xbas(source, '-l', '--color', 'off', '-o', Files.output, stderr=ferr, rc=1)
    if content_line_array(Files.error)[0] != 'Error: Duplicate label A%LABEL\n':
        error('local labels', 'Missed duplicate local label')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
