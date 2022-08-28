#!/usr/bin/env python3

import os

from config import Dirs, Disks, Files, XAS99_CONFIG
from utils import (xas, xdm, error, clear_env, delfile, check_list_files_eq, check_text_files_eq,
                   check_list_against_binary)


# Check functions

def check_end_equal(outfile, reffile):
    with open(outfile, 'r') as fout, open(reffile, 'r') as fref:
        otxt = [l.strip() for l in fout.readlines()]
        rtxt = [l.strip() for l in fref.readlines()]
    for i, rline in enumerate(rtxt):
        if rline.strip() != otxt[-len(rtxt) + i].strip():
            error('symbols', 'Symbols not as expected in line %d' % i)


def check_sym_equ_equiv(outfile, reffile):
    with open(outfile, 'r') as fout, open(reffile, 'r') as fref:
        otxt = [line for line in fout.readlines() if 'ref' not in line]
        rtxt = [l for l in fref.readlines() if '...' in l]
    if len(otxt) != 2 * len(rtxt):
        error('EQUs', 'Symbols/EQUs count mismatch')


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    clear_env(XAS99_CONFIG)

    # check if listings match E/A
    for infile, opts, reffile in [
            ('ashellon.asm', ['-R'], 'ASHELLO-L'),
            ('asdirs.asm', [], 'ASDIRS-L'),
            ('asorgs.asm', [], 'ASORGS-L'),
            ('asopcs.asm', [], 'ASOPCS-L'),
            ('asexprs.asm', [], 'ASEXPRS-L'),
            ('asbss.asm', [], 'ASBSS-L'),
            ('asregs.asm', ['-R'], 'ASREGS-L'),
            ('assize1.asm', [], 'ASSIZE1-L'),
            ('assize2.asm', [], 'ASSIZE2-L'),
            ('assize3.asm', [], 'ASSIZE3-L'),
            ('assize4.asm', [], 'ASSIZE4-L'),
            ('asextsym.asm', [], 'ASEXTSYM-L'),
            ('asimg1.asm', [], 'ASIMG1-L'),
            ('asimg2.asm', [], 'ASIMG2-L'),
            ('asimg3.asm', [], 'ASIMG3-L'),
            ('ascart.asm', ['-R', '-s'], 'ASCART-L')
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ['-q', '-L', Files.output, '-o', Files.input])
        xdm(Disks.asmsrcs, '-e', reffile, '-o', Files.reference)
        check_list_files_eq(Files.output, Files.reference)

    # check if listing words match actual words
    for infile, opts in [
            ('asdirs.asm', []),  # cannot use programs with many ?ORGs
            ('asopcs.asm', []),
            ('asbss.asm', []),
            ('asregs.asm', ['-R']),
            ('ascart.asm', ['-R', '-s']),
            ('aslist.asm', [])
        ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ['-b', '-q', '-L', Files.output, '-o', Files.reference])
        check_list_against_binary(Files.output, Files.reference)

    # changing sources
    for infile, opts, reffile in [
            ('ascopy.asm', [], 'ASCOPY-L')
            #('ascopyn.asm', [], 'ASCOPYN-L')  # TI version is not souce-equal to xas99 version
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ['-q', '-L', Files.output, '-o', Files.reference])
        xdm(Disks.asmsrcs, '-e', reffile, '-o', Files.reference)
        check_list_files_eq(Files.output, Files.reference, ignore_lino=True)

    # bytes and padding
    source = os.path.join(Dirs.sources, 'aslist.asm')
    xas(source, '-o', Files.input, '-L', Files.output)
    ref = os.path.join(Dirs.refs, 'aslist.lst')
    check_text_files_eq('listbytes', Files.output, ref, skip=1)

    # symbols
    source = os.path.join(Dirs.sources, 'ashello.asm')
    xas(source, '-R', '-L', Files.output, '-S', '-q', '-o', Files.input)
    reffile = os.path.join(Dirs.refs, 'ashello.sym')
    check_end_equal(Files.output, reffile)

    # EQUs
    source = os.path.join(Dirs.sources, 'ashello.asm')
    xas(source, '-R', '-E', Files.output, '-q', '-o', Files.input)
    reffile = os.path.join(Dirs.refs, 'ashello.sym')
    check_sym_equ_equiv(Files.output, reffile)

    # auto-generated constants
    source = os.path.join(Dirs.sources, 'asauto.asm')
    reffile = os.path.join(Dirs.refs, 'asauto.lst')
    with open(reffile, 'r') as fref:
        reflines = [line.rstrip() for line in fref.readlines()]
    xas(source, '-R', '-o', Files.error, '-S', '-L', Files.output)
    with open(Files.output, 'r') as fout:
        lines = [line.rstrip() for line in fout.readlines()
                 if line[:4] == '    '][-len(reflines):]
    if lines != reflines:
        error('auto', 'auto-const listing mismatch')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
