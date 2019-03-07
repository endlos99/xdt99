#!/usr/bin/env python

import os
import re

from config import Dirs, Disks, Files
from utils import xas, xdm, readstderr,  compareErrors


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
            err = re.match(r"\*{5}\s+([A-Z ]*) - (\d+)", line)
            if err:
                lino, errmsg = err.group(2), err.group(1)
                tierrors[lino] = errmsg

    # compare
    compareErrors(tierrors, xaserrors)

    # xdt99-specific errors
    source = os.path.join(Dirs.sources, "asxerrs.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-R", "-o", Files.output, stderr=ferr, rc=1)
    xaserrors = readstderr(Files.error)
    referrors = {}
    with open(source, "r") as f:
        for i, line in enumerate(f):
            m = re.search(r";ERROR(:....)?", line)
            if m:
                if m.group(1):
                    referrors[m.group(1)[1:]] = line
                else:
                    referrors["%04d" % (i + 1)] = line

    compareErrors(referrors, xaserrors)

    # xdt99-specific errors (image generation)
    source = os.path.join(Dirs.sources, "asxerrsb.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-R", "-b", "-o", Files.output, stderr=ferr, rc=1)
    xaserrors = readstderr(Files.error)
    referrors = {}
    with open(source, "r") as f:
        for i, line in enumerate(f):
            m = re.search(r";ERROR(:....)?", line)
            if m:
                if m.group(1):
                    referrors[m.group(1)[1:]] = line
                else:
                    referrors["%04d" % (i + 1)] = line

    compareErrors(referrors, xaserrors)

    # files not found
    source = os.path.join(Dirs.sources, "ascopyi.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-o", Files.output, stderr=ferr, rc=1)

    # cleanup
    os.remove(Files.error)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
