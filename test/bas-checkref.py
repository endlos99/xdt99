#!/usr/bin/env python

import os
import re

from config import Disks, Files, Dirs, XBAS99_CONFIG
from utils import xdm, xbas, error, clear_env, delfile, check_binary_files_eq


# Check functions

def check_listing_eq(infile, reffile):
    """check if TI BASIC listings are equal"""
    ref_list, prev_lino = [], 0
    with open(reffile, 'r') as f:
        for line in f:
            line = line.rstrip('\n\r')
            if not line.strip():
                continue
            m = re.match('(\d+)\s+', line)
            curr_lino = int(m.group(1)) if m else -1
            if 0 <= curr_lino - prev_lino < 3:
                ref_list.append(line)
                prev_lino = curr_lino
            else:
                # continuation of previous source line
                ref_list[-1] += line
    with open(infile, 'r') as f:
        for i, line in enumerate(f):
            if line.rstrip() != ref_list[i].rstrip():
                error('Listing', 'Source mismatch on line %d:\nexpected: %sactual: %s' % (
                    i + 1, ref_list[i], line))


def gen_listing(infile, outfile):
    lino = 1
    with open(infile, 'r') as fin, open(outfile, 'w') as fout:
        for line in fin:
            if line.strip():
                fout.write('%d %s' % (lino, line))
                lino += 1


def check_line_numbers(file, linos):
    """check if non-empty line counts match"""
    with open(file, 'r') as f:
        lines = [l for l in f.readlines() if l.rstrip()]
    for line, lino in zip(lines, linos):
        m = re.match(r'(\d+) ', line)
        if m.group(1) != str(lino):
            error('line count', f'Could not find line number {lino}')


# Main test

def runtest():
    """compare xbas99 generation to TI references"""

    clear_env(XBAS99_CONFIG)

    for fn in ('KEYWORDS', 'STATMNTS', 'NUMBERS', 'COMMENTS', 'LOWRCASE', 'GIBBRISH'):
        # compare generated xbas99 listing with TI BASIC reference
        xdm(Disks.basic1, '-e', fn, '-o', Files.input)
        xdm(Disks.basic1, '-e', fn + '-L', '-o', Files.reference)
        xbas(Files.input, '-d', '-o', Files.output)
        check_listing_eq(Files.output, Files.reference)

        # ditto with MERGE format
        xdm(Disks.basic1, '-e', fn + '-M', '-o', Files.input)
        xbas(Files.input, '-d', '--merge', '-o', Files.output)
        check_listing_eq(Files.output, Files.reference)

        # compare generated xbas99 basic program with TI BASIC reference
        xdm(Disks.basic1, '-e', fn + '-L', '-o', Files.input)
        xdm(Disks.basic1, '-e', fn, '-o', Files.reference)
        xbas(Files.input, '-c', '-o', Files.output)
        check_binary_files_eq('Tokenization', Files.output, Files.reference)

        # ditto with non-canonically formatted original source
        rawlist = os.path.join(Dirs.basic, fn.lower() + '.txt')
        gen_listing(rawlist, Files.input)
        xbas(Files.input, '-c', '-o', Files.output)
        check_binary_files_eq('Tokenization', Files.output, Files.reference)

    # check using randomized listings
    for i in range(8):
        fn = 'RAND%02d' % i
        xdm(Disks.basic2, '-e', fn, '-o', Files.input)
        xdm(Disks.basic2, '-e', fn + '-L', '-o', Files.reference)

        # compare generated xbas99 listing with TI BASIC reference
        xbas(Files.input, '-d', '-o', Files.output)
        check_listing_eq(Files.output, Files.reference)

        # compare generated xbas99 basic program with TI BASIC reference
        xbas(Files.reference, '-c', '-j', ',2', '-o', Files.output)  # some linos missing in listing
        check_binary_files_eq('Tokenization', Files.output, Files.input)

    # check long format
    path = os.path.join(Dirs.basic, 'sample-l.bin')
    xbas(path, '-d', '-o', Files.output)
    path = os.path.join(Dirs.basic, 'sample-n.bin')
    xbas(path, '-d', '-o', Files.reference)
    check_binary_files_eq('Long Format', Files.output, Files.reference)

    # check listing protection
    xdm(Disks.basic1, '-e', 'STATMNTS-L', '-o', Files.input)
    xbas(Files.input, '-c', '-j', '3,5', '--protect', '-o', Files.output)
    xbas(Files.input, '-c', '-j', '3,1', '-o', Files.reference)
    check_binary_files_eq('Protection', Files.output, Files.reference, mask=[(0, 2)])

    # join
    source = os.path.join(Dirs.basic, 'basjoin.bas')
    xbas(source, '-c', '-j', '5,10', '-o', Files.input)
    xbas(Files.input, '-d', '-o', Files.output)
    check_line_numbers(Files.output, [100, 110, 120, 125])

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
