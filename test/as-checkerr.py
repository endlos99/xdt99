#!/usr/bin/env python

import os
import re

from config import Dirs, Disks, Files
from utils import xas, xdm, error


def readstderr(fn):
    """read stderr output"""
    errors, lino = {}, "----"
    with open(fn, "r") as f:
        for line in f:
            err = re.match("<\d>\s+(\d+)", line)
            if err:
                lino = err.group(1)
            else:
                errors[lino] = line[6:].strip()
    return errors


def compare(ref, actual):
    """compare two dicts for key equality"""
    for err in ref:
        if err not in actual:
            error("Error messages",
                  "Missing error: " + str(err) + ": " + ref[err])
    for err in actual:
        if err not in ref:
            error("Error messages",
                  "Extraneous error: " + str(err) + ": " + actual[err])


def runtest():
    """check error messages against native assembler listing"""

    # cross-assembler error messages
    source = os.path.join(Dirs.sources, "aserrs.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-s", "-o", Files.output, stderr=ferr, rc=1)
    xaserrors = readstderr(Files.error)
    
    # TI assembler error messages
    tierrors = {}
    xdm(Disks.asmsrcs, "-e", "ASERRS-L", "-o", Files.reference)
    with open(Files.reference, "r") as f:
        for line in f:
            err = re.match("\*{5}\s+([A-Z ]*) - (\d+)", line)
            if err:
                lino, errmsg = err.group(2), err.group(1)
                tierrors[lino] = errmsg

    # compare
    compare(tierrors, xaserrors)

    # xdt99-specific errors
    source = os.path.join(Dirs.sources, "asxerrs.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-R", "-o", Files.output, stderr=ferr, rc=1)
    xaserrors = readstderr(Files.error)
    referrors = {}
    with open(source, "r") as f:
        for i, line in enumerate(f):
            if line.find(";ERROR") != -1:
                referrors["%04d" % (i + 1)] = line

    compare(referrors, xaserrors)
                
    # cleanup
    os.remove(Files.error)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
