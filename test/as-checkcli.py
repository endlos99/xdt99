#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, error, checkObjCodeEq, checkImageFilesEq, \
                  checkListFilesEq


### Check function

def ordw(word):
    return ord(word[0]) << 8 | ord(word[1])


### Main test

def runtest():
    """check command line interface"""

    # input and output files
    source = os.path.join(Dirs.sources, "ashello.asm")
    with open(Files.output, "wb") as f:
        xas(source, "-R", "-o", "-", stdout=f)
    xdm(Disks.asmsrcs, "-e", "ASHELLO-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)

    with open(Files.output, "wb") as f:
        xas(source, "-R", "-i", "-o", "-", stdout=f)
    xdm(Disks.asmsrcs, "-e", "ASHELLO-I", "-o", Files.reference)
    checkImageFilesEq(Files.output, Files.reference)

    with open(Files.output, "w") as f:
        xas(source, "-R", "-o", Files.output, "-L", "-", stdout=f)
    xdm(Disks.asmsrcs, "-e", "ASHELLO-L", "-o", Files.reference)
    checkListFilesEq(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, "nonexisting")
    with open(Files.error, "w") as ferr:
        xas(source, "-i", "-R", "-o", Files.output, stderr=ferr, rc=1)
    with open(Files.error, "r") as ferr:
        errs = ferr.readlines()
    if len(errs) != 1 or errs[0][:10] != "File error":
        error("File errors", "Incorrect file error message")

    # include path
    source = os.path.join(Dirs.sources, "ascopyi.asm")
    incls = os.path.join(Dirs.sources, "test") + "," + \
        os.path.join(Dirs.sources, "test", "test")
    xas(source, "-i", "-I", incls, "-o", Files.output)
    with open(Files.output, "rb") as f:
        data = f.read()
    if len(data[6:]) != 20:
        error("Include paths", "Incorrect image length")

    # jumpstart disk
    source = os.path.join(Dirs.sources, "ashello.asm")
    xas(source, "-R", "--jumpstart", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASHELLO-I", "-o", Files.reference)
    with open(Files.output, "rb") as fout, open(Files.reference, "rb") as fref:
        disk = fout.read()
        prog = fref.read()
    if len(disk) != 360 * 256:
        error("Jumpstart", "Incorrect disk size: %d" % len(disk))
    if disk[0:10] != "xas99-JS\xc2\xb9" or disk[56:256] != "\xff" * 200:
        error("Jumpstart", "Invalid sector 0 data")
    plen = ordw(prog[2:4]) - 6
    if disk[512:512 + plen] != prog[6:6 + plen]:
        error("Jumpstart", "Invalid program data")

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Files.error)


if __name__ == "__main__":
    runtest()
    print "OK"
