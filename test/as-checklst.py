#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, checkListFilesEq


### Main test

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
            ("ascart.asm", ["-R"], "ASCART-L")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ["-L", Files.output, "-o", Files.reference])
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        checkListFilesEq(Files.output, Files.reference)

    for infile, opts, reffile in [
            ("ascopy.asm", [], "ASCOPY-L")
            #("ascopyn.asm", [], "ASCOPYN-L")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ["-L", Files.output, "-o", Files.reference])
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        checkListFilesEq(Files.output, Files.reference, ignoreLino=True)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
