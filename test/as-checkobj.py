#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, error, checkFilesEq


### Check function

def ordw(word):
    return ord(word[0]) << 8 | ord(word[1])


def checkImageFilesEq(name, genfile, reffile):
    """check if non-zero bytes in binary files are equal"""
    with open(genfile, "rb") as fg, open(reffile, "rb") as fr:
        genimage = fg.read()
        refimage = fr.read()
    if not 0 <= len(genimage) - len(refimage) <= 1:
        print len(genimage), len(refimage)
        error("Object code", "Image length mismatch: " + name)
    if (genimage[:2] != refimage[:2] or
        not (0 <= ordw(genimage[2:4]) - ordw(refimage[2:4]) <= 1) or
        genimage[4:6] != refimage[4:6]):
        error("Object code", "Image header mismatch")
    # TI-generated images may contain arbitrary bytes in BSS segments
    for i in xrange(4, len(refimage)):
        if genimage[i] != "\x00" and genimage[i] != refimage[i]:
            error("Object code", "Image contents mismatch " + name +
                  " @ " + hex(i))


### Main test

def runtest():
    """check cross-generated output against native reference files"""

    # object code
    for infile, opts, reffile in [
            ("asdirs.asm", [], "ASDIRS-O"),
            ("asorgs.asm", [], "ASORGS-O"),
            ("asopcs.asm", [], "ASOPCS-O"),
            ("asexprs.asm", [], "ASEXPRS-O"),
            ("asbss.asm", [], "ASBSS-O"),
            ("asregs.asm", ["-R"], "ASREGS-O"),
            ("ashello.asm", ["-R"], "ASHELLO-O"),
            ("ascopy.asm", [], "ASCOPY-O"),
            ("ascopyn.asm", [], "ASCOPYN-O"),
            ("assize1.asm", [], "ASSIZE1-O"),
            ("assize2.asm", [], "ASSIZE2-O"),
            ("assize3.asm", [], "ASSIZE3-O"),
            ("assize4.asm", [], "ASSIZE4-O"),
            ("astisym.asm", [], "ASTISYM-O"),
            ("asimg1.asm", [], "ASIMG1-O"),
            ("asimg2.asm", [], "ASIMG2-O"),
            ("asimg3.asm", [], "ASIMG3-OX"),
            ("ascart.asm", ["-R"], "ASCART-O")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        xas(*[source] + opts + ["-o", Files.output])
        checkFilesEq("Object code", Files.output, Files.reference, fmt="DF80")
        xas(*[source] + opts + ["--strict", "-o", Files.output])
        checkFilesEq("Object code", Files.output, Files.reference, fmt="DF80")

    # xdt99 extensions
    source = os.path.join(Dirs.sources, "asxext.asm")
    xas(source, "-R", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT0-O", "-o", Files.reference)
    checkFilesEq("Object code", Files.output, Files.reference, fmt="DF80")
    xas(source, "-R", "-D", "sym2", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT1-O", "-o", Files.reference)
    checkFilesEq("Object code", Files.output, Files.reference, fmt="DF80")
    xas(source, "-R", "-D", "sym2=2", "sym3=2", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT2-O", "-o", Files.reference)
    checkFilesEq("Object code", Files.output, Files.reference, fmt="DF80")

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
        checkImageFilesEq(infile, Files.output, Files.reference)

    for infile, reffiles in [
        ("aslimg.asm", ["ASLIMG-I", "ASLIMG-J", "ASLIMG-K"]),
        ("assimg.asm", ["ASSIMG-I", "ASSIMG-J", "ASSIMG-K", "ASSIMG-L"])
        ]:
        source = os.path.join(Dirs.sources, infile)
        xas(source, "-R", "-i", "-o", Files.output)
        for i, reffile in enumerate(reffiles):
            xdm(Disks.asmimgs, "-e", reffile, "-o", Files.reference)
            checkFilesEq("Image file",
                         Files.outputff[i], Files.reference, fmt="P")

    # cleanup
    for i in xrange(4):
        os.remove(Files.outputff[i])
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
