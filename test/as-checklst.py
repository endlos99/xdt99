#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, error, check_list_files_eq


# Check functions

def check_end_equal(outfile, reffile):
    with open(outfile, "r") as fout, open(reffile, "r") as fref:
        otxt = [l.strip() for l in fout.readlines()]
        rtxt = [l.strip() for l in fref.readlines()]
    for i, rline in enumerate(rtxt):
        if rline.strip() != otxt[-len(rtxt) + i].strip():
            error("symbols", "Symbols not as expected in line %d" % i)


def check_sym_equ_equiv(outfile, reffile):
    with open(outfile, "r") as fout, open(reffile, "r") as fref:
        otxt = fout.readlines()
        rtxt = [l for l in fref.readlines() if "..." in l]
    if len(otxt) != 2 * len(rtxt):
        error("EQUs", "Symbols/EQUs count mismatch")


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    for infile, opts, reffile in [
            ("ashello.asm", ["-R"], "ASHELLO-L"),
            ("asdirs.asm", [], "ASDIRS-L"),
            ("asorgs.asm", [], "ASORGS-L"),
            ("asopcs.asm", [], "ASOPCS-L"),
            ("asexprs.asm", [], "ASEXPRS-L"),
            ("asbss.asm", [], "ASBSS-L"),
            ("asregs.asm", ["-R"], "ASREGS-L"),
            ("assize1.asm", [], "ASSIZE1-L"),
            ("assize2.asm", [], "ASSIZE2-L"),
            ("assize3.asm", [], "ASSIZE3-L"),
            ("assize4.asm", [], "ASSIZE4-L"),
            ("astisym.asm", [], "ASTISYM-L"),
            ("asimg1.asm", [], "ASIMG1-L"),
            ("asimg2.asm", [], "ASIMG2-L"),
            ("asimg3.asm", [], "ASIMG3-L"),
            ("ascart.asm", ["-R", "-s"], "ASCART-L")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ["-L", Files.output, "-o", Files.reference])
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        check_list_files_eq(Files.output, Files.reference)

    for infile, opts, reffile in [
            ("ascopy.asm", [], "ASCOPY-L")
            #("ascopyn.asm", [], "ASCOPYN-L")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ["-L", Files.output, "-o", Files.reference])
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        check_list_files_eq(Files.output, Files.reference, ignoreLino=True)

    # symbols
    source = os.path.join(Dirs.sources, "ashello.asm")
    xas(source, "-R", "-L", Files.output, "-S", "-o", Files.input)
    reffile = os.path.join(Dirs.refs, "ashello.sym")
    check_end_equal(Files.output, reffile)

    # EQUs
    source = os.path.join(Dirs.sources, "ashello.asm")
    xas(source, "-R", "-E", Files.output, "-o", Files.input)
    reffile = os.path.join(Dirs.refs, "ashello.sym")
    check_sym_equ_equiv(Files.output, reffile)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
