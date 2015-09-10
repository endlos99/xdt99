#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import xas, xdm, error


### Check function

def ordw(word):
    return ord(word[0]) << 8 | ord(word[1])


### Main test

def runtest():
    """check command line interface"""

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


if __name__ == "__main__":
    runtest()
    print "OK"
