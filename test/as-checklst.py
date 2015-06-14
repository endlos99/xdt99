#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, error


### Check function

def ordw(word):
    return ord(word[0]) << 8 | ord(word[1])


def checkListFilesEq(genfile, reffile, ignoreLino=False):
    """check if list files are equivalent"""
    with open(genfile, "rb") as fg, open(reffile, "rb") as fr:
        genlist = [l.rstrip() for l in fg.readlines()]
        reflist = [l[2:].rstrip() for l in fr.readlines() if l[:2] == "  "]
    gi, ri = 1, 0
    mincol, maxcol = 4 if ignoreLino else 0, 74
    while gi < len(genlist):
        gl, rl = genlist[gi], reflist[ri]
        # ignore deliberate changes
        try:
            if gl[10] in ".X":
                rl = rl[:10] + gl[10:15] + rl[15:]  # no data
            if gl[14] == "r":
                rl = rl[:14] + "r" + rl[15:]
            if "ORG" in rl[16:] or "BES" in rl[16:]:
                rl = rl[:5] + gl[5:9] + rl[9:]  # no address
            # ignore list directives
            if ("TITL" in gl[16:] or "PAGE" in gl[16:] or "UNL" in gl[16:] or
                    "LIST" in gl[16:]):
                gi += 1
                continue
            # ignore BYTE sections
            if "BYTE" in gl[16:] and "BYTE" in rl[16:]:
                gi += 1
                while not genlist[gi][16:].rstrip():
                    gi += 1
                ri += 1
                while not reflist[ri][16:].rstrip():
                    ri += 1
                continue
        except IndexError:
            pass
        if gl[mincol:maxcol] != rl[mincol:maxcol]:
            error("List file", "Line mismatch in %d/%d" % (gi, ri))
        gi, ri = gi + 1, ri + 1


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
