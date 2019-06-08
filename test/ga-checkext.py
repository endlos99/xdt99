#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xga, xdm, error, check_binary_files_eq, check_gbc_files_eq


# Main test

def runtest():
    """run regression tests"""

    # preprocessor
    source = os.path.join(Dirs.gplsources, "gaxprep.gpl")
    xga(source, "-D", "isdef=2", "-o", Files.output)
    xdm(Disks.gplsrcs, "-e", "GAXPREP-Q", "-o", Files.reference)
    check_gbc_files_eq(source, Files.output, Files.reference)

    # directives
    source = os.path.join(Dirs.gplsources, "gaxbcopy.gpl")
    xga(source, "-I", "gpl", "-o", Files.output)
    source = os.path.join(Dirs.gplsources, "gaxbcopyn.gpl")
    xga(source, "-o", Files.reference)
    check_binary_files_eq("bcopy", Files.output, Files.reference)

    # local labels
    source = os.path.join(Dirs.gplsources, "gaxlocal.gpl")
    xga(source, "-o", Files.output)
    ref = os.path.join(Dirs.gplsources, "gaxlocaln.gpl")
    xga(ref, "-o", Files.reference)
    check_binary_files_eq("locals", Files.output, Files.reference)

    # floating-point numbers
    source = os.path.join(Dirs.gplsources, "gafloat.gpl")
    xga(source, "-o", Files.output)
    ref = os.path.join(Dirs.refs, "asfloat.ref")
    check_binary_files_eq("float", Files.output, ref)

    # GROM n or address
    for source in (" GROM >6000\n DATA $", " GROM 3\n DATA $"):
        with open(Files.input, "w") as fout:
            fout.writelines(source)
        xga(Files.input, "-o", Files.output)
        with open(Files.output, "rb") as fin:
            if fin.read()[:4] != "\x60\x00":
                error("GROM", "Incorrect address after GROM directive")

    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    os.remove(Files.reference)
    #os.remove(Files.error)


if __name__ == "__main__":
    runtest()
    print "OK"
