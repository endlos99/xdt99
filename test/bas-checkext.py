#!/usr/bin/env python3

import os
import re

from config import Files, Dirs, XBAS99_CONFIG
from utils import xbas, error, delfile, check_binary_files_eq, content_line_array


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


def check_source_escs_eq(sf1, sf2):
    source1 = content_line_array(sf1)
    source2 = content_line_array(sf2)
    if len(source1) != len(source2):
        error('esc codes', 'Program lengths differ')
    for i, l in enumerate(source1):
        line1 = l.strip()
        line2 = source2[i].strip()
        if line1 != line2:
            line1n = re.sub(r'\\d(...)',
                            lambda m: f'\\x{int(m.group(1)):02x}',
                            line1)
            if line1n != line2:
                line1nn = re.sub(r'\\x(..)',
                                 lambda m: s + s if (s := chr(int(m.group(1), 16))) == '"' else s,
                                 line1n)
                if line1nn != line2:
                    error('esc codes', f'Lines {i} differ:\n' + line1nn + '\n' + line2)


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

    # character escape codes
    source = os.path.join(Dirs.basic, 'escapes.bas')
    xbas(source, '-c', '-o', Files.input)
    ref = os.path.join(Dirs.refs, 'escapes.prg')
    check_binary_files_eq('esc codes', Files.input, ref)

    xbas(Files.input, '-d', '-o', Files.output)
    check_source_escs_eq(source, Files.output)

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
