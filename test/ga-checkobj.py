#!/usr/bin/env python

# How to update the gplsrcs.dsk:
# - replace source file DIS/VAR 80 (no ext)
# - start ti99 gpl gplsrcs.dsk
# - enter source name, then -O, then -L, options G3
# - start DSK2.LINK
# - enter -O, -P, options G3


import os

from config import Dirs, Disks, Files
from utils import xga, xdm, check_files_eq, check_gbc_files_eq, error
from zipfile import ZipFile


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    # object code
    for infile, opts, reffile in (
            ['gaops.gpl', [], 'GAOPS-Q'],
            ['gainst.gpl', [], 'GAINST-Q'],
            ['gabranch.gpl', [], 'GABRANCH-Q'],
            ['gamove.gpl', [], 'GAMOVE-Q'],
            ['gafmt.gpl', [], 'GAFMT-Q'],
            ['gadirs.gpl', [], 'GADIRS-Q'],
            ['gacopy.gpl', [], 'GACOPY-Q'],
            ['gaexts.gpl', [], 'GAEXTS-Q'],
            ['gapass.gpl', [], 'GAPASS-Q']
            ):
        source = os.path.join(Dirs.gplsources, infile)
        xdm(Disks.gplsrcs, '-e', reffile, '-o', Files.reference)
        xga(*[source] + opts + ['-q', '-o', Files.output])
        check_gbc_files_eq(infile, Files.output, Files.reference)

    # cart generation
    source = os.path.join(Dirs.gplsources, 'gahello.gpl')
    ref = os.path.join(Dirs.refs, 'gahello.rpk')
    xga(source, '-c', '-o', Files.output)
    with ZipFile(Files.output, 'r') as zout, ZipFile(ref, 'r') as zref:
        outdata = zout.read('GAHELLO.bin')
        refdata = zref.read('GAHELLO.bin')
        if outdata != refdata:
            error('GPL cart', 'Main file mismatch')
        if 'layout.xml' not in zout.namelist() or 'meta-inf.xml' not in zout.namelist():
            error('GPL cart', 'Missing layout or meta-inf files in RPK')

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == '__main__':
    runtest()
    print('OK')
