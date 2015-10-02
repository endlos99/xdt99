#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, checkObjCodeEq, error


### Check functions

def checkConcatEq(infiles, reffile):
    data = ""
    for fn in infiles:
        with open(fn, "rb") as f:
            data += f.read()
    with open(reffile, "rb") as f:
        ref = f.read()
    if data != ref:
        error("Files", "Incorrect binary data")


def checkNoFiles(files):
    for fn in files:
        if os.path.isfile(fn):
            error("Files", "Extraneous file " + fn)


### Main test

def runtest():
    """check xdt99 extensions"""

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

    # SAVE directive
    source = os.path.join(Dirs.sources, "asxsave.asm")
    xas(source, "-b", "--base", "0xb000", "-o", Files.output)
    save1s = [Files.output + "_" + ext
              for ext in ["b000", "b020", "b030"]]
    checkConcatEq(save1s, os.path.join(Dirs.refs, "save1"))
    checkNoFiles([Files.output + "_b080"])

    # bank switching
    source = os.path.join(Dirs.sources, "asxbank1.asm")
    xas(source, "-b", "-o", Files.output)
    save2s = [Files.output + "_" + ext
              for ext in ["0000", "0010", "6000_b0", "6000_b1", "6100_b0",
                          "6200_b1", "6200_b2"]]
    checkConcatEq(save2s, os.path.join(Dirs.refs, "save2"))
    checkNoFiles([Files.output + "_" + ext
                  for ext in ["0000_b0", "6000", "6100_b1", "6200_b0"]])

    source = os.path.join(Dirs.sources, "asxbank2.asm")
    xas(source, "-b", "-o", Files.output)
    save3s = [Files.output + "_" + ext
              for ext in ["c000", "c000_b0", "c000_b1", "d000_b0", "e000_b1"]]
    checkConcatEq(save3s, os.path.join(Dirs.refs, "save3"))
    checkNoFiles([Files.output + "_" + ext
                  for ext in ["d000", "d000_b1", "e000", "e000_b0"]])

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    for fn in save1s + save2s + save3s:
        os.remove(fn)


if __name__ == "__main__":
    runtest()
    print "OK"
