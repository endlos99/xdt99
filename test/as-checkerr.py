#!/usr/bin/env python

import os
import re

from config import Dirs, Disks, Files
from utils import xas, xdm, error


def runtest():
    """check error messages against native assembler listing"""

    # cross-assembler error messages
    aserrors = {}
    source = os.path.join(Dirs.sources, "aserrs.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-o", Files.output, stderr=ferr, rc=1)
    with open(Files.error, "r") as f:
        for line in f:
            err = re.match("<\d>\s+(\d+)", line)
            if err:
                lino = err.group(1)
            else:
                aserrors[lino] = line[6:].strip()

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
    for err in tierrors:
        if err not in aserrors:
            error("Error messages",
                  "Missing error: " + str(err) + ": " + tierrors[err])
    for err in aserrors:
        if err not in tierrors:
            error("Error messages",
                  "Extraneous error: " + str(err) + ": " + aserrors[err])

    # cleanup
    os.remove(Files.output)
    os.remove(Files.error)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
