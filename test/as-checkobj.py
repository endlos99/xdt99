#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, checkFilesEq, checkObjCodeEq, checkImageFilesEq


### Main test

def runtest():
    """check cross-generated output against native reference files"""

    # object code
    for infile, opts, reffile, cprfile in [
            ("asdirs.asm", [], "ASDIRS-O", "ASDIRS-C"),
            ("asorgs.asm", [], "ASORGS-O", "ASORGS-C"),
            ("asopcs.asm", [], "ASOPCS-O", "ASOPCS-C"),
            ("asexprs.asm", [], "ASEXPRS-O", "ASEXPRS-C"),
            ("asbss.asm", [], "ASBSS-O", "ASBSS-C"),
            ("asregs.asm", ["-R"], "ASREGS-O", "ASREGS-C"),
            ("ashello.asm", ["-R"], "ASHELLO-O", "ASHELLO-C"),
            ("ascopy.asm", [], "ASCOPY-O", None),
            ("ascopyn.asm", [], "ASCOPYN-O", None),
            ("assize1.asm", [], "ASSIZE1-O", "ASSIZE1-C"),
            ("assize2.asm", [], "ASSIZE2-O", None),
            ("assize3.asm", [], "ASSIZE3-O", None),
            ("assize4.asm", [], "ASSIZE4-O", None),
            ("astisym.asm", [], "ASTISYM-O", "ASTISYM-C"),
            ("asimg1.asm", [], "ASIMG1-O", "ASIMG1-C"),
            ("asimg2.asm", [], "ASIMG2-O", None),
            ("asimg3.asm", [], "ASIMG3-OX", None),
            #("asreloc.asm", [], "ASRELOC-O", None),
            ("ascart.asm", ["-R"], "ASCART-O", "ASCART-C")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        xas(*[source] + opts + ["-o", Files.output])
        checkObjCodeEq(Files.output, Files.reference)
        xas(*[source] + opts + ["--strict", "-o", Files.output])
        checkObjCodeEq(Files.output, Files.reference)
        if cprfile:
            # compressed object code
            xas(*[source] + opts + ["-C", "-o", Files.output])
            xdm(Disks.asmsrcs, "-e", cprfile, "-o", Files.reference)
            checkObjCodeEq(Files.output, Files.reference)

    # xdt99 extensions
    source = os.path.join(Dirs.sources, "asxext.asm")
    xas(source, "-R", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT0-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT1-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2=2", "sym3=2", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT2-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)

    # image files
    for infile, opts, reffile in [
            ("ashello.asm", ["-R"], "ASHELLO-I"),
            ("astisym.asm", [], "ASTISYM-I"),
            ("asimg1.asm", [], "ASIMG1-I"),
            ("asimg2.asm", [], "ASIMG2-I")
            #("asimg3.asm", [], "ASIMG3-I")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(*[source] + opts + ["-i", "-o", Files.output])
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        checkImageFilesEq(Files.output, Files.reference)

    for infile, reffiles in [
            ("aslimg.asm", ["ASLIMG-I", "ASLIMG-J", "ASLIMG-K"]),
            ("assimg.asm", ["ASSIMG-I", "ASSIMG-J", "ASSIMG-K", "ASSIMG-L"]),
            ("asreloc.asm", ["ASRELOC-I"])
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(source, "-R", "-i", "-o", Files.output)
        for i, reffile in enumerate(reffiles):
            xdm(Disks.asmimgs, "-e", reffile, "-o", Files.reference)
            checkFilesEq("Image file",
                         Files.outputff[i], Files.reference, fmt="P")

    # some CLI options
    source = os.path.join(Dirs.sources, "ashello.asm")
    xas(source, "--embed", "-R", "-o", Files.output)

    # misc new features
    for infile, reffile in [
            ("asxnew.asm", "ASXNEW-O"),
            ("asmacs.asm", "ASMACS-O")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(source, "-o", Files.output)
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        checkObjCodeEq(Files.output, Files.reference)

    # cleanup
    for i in xrange(4):
        os.remove(Files.outputff[i])
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
