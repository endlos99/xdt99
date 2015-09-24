#!/usr/bin/env python

import os
import re

from config import Disks, Files, Dirs
from utils import xdm, xbas, error, checkFilesEq


### Check functions

def checkListingEq(infile, reffile):
    """check if TI BASIC listings are equal"""
    reflist, prevlino = [], 0
    with open(reffile, "r") as f:
        for l in f:
            if not l.strip():
                continue
            m = re.match("(\d+)\s+", l)
            currlino = int(m.group(1)) if m else -1
            if 0 <= currlino - prevlino < 3:
                reflist.append(l)
                prevlino = currlino
            else:
                # continuation of previous source line
                reflist[-1] = reflist[-1][:-1] + l
    with open(infile, "r") as f:
        for i, l in enumerate(f):
            if l.rstrip() != reflist[i].rstrip():
                error("Listing", "Source mismatch on line %d:\nexpected: %sactual: %s" % (
                    i + 1, reflist[i], l))


def genListing(infile, outfile):
    lino = 1
    with open(infile, "r") as fin, open(outfile, "w") as fout:
        for l in fin:
            if l.strip():
                fout.write("%d %s" % (lino, l))
                lino += 1


### Main test

def runtest():
    """compare xbas99 generation to TI references"""

    for fn in [
            "KEYWORDS", "STATMNTS", "NUMBERS", "COMMENTS", "LOWRCASE",
            "GIBBRISH"
            ]:
        # compare generated xbas99 listing with TI BASIC reference
        xdm(Disks.basic1, "-e", fn, "-o", Files.input)
        xdm(Disks.basic1, "-e", fn + "-L", "-o", Files.reference)
        xbas(Files.input, "-d", "-o", Files.output)
        checkListingEq(Files.output, Files.reference)

        # ditto with MERGE format
        xdm(Disks.basic1, "-e", fn + "-M", "-o", Files.input)
        xbas(Files.input, "-d", "--merge", "-o", Files.output)
        if os.name != "nt":
            checkListingEq(Files.output, Files.reference)

        # compare generated xbas99 basic program with TI BASIC reference
        xdm(Disks.basic1, "-e", fn + "-L", "-o", Files.input)
        xdm(Disks.basic1, "-e", fn, "-o", Files.reference)
        xbas(Files.input, "-c", "-j", "3", "-o", Files.output)
        checkFilesEq("Tokenization", Files.output, Files.reference, "P")

        # ditto with non-canonically formatted original source
        rawlist = os.path.join(Dirs.basic, fn.lower() + ".txt")
        genListing(rawlist, Files.input)
        xbas(Files.input, "-c", "-o", Files.output)
        checkFilesEq("Tokenization", Files.output, Files.reference, "P")

    # check using randomized listings
    for i in xrange(8):
        fn = "RAND%02d" % i
        xdm(Disks.basic2, "-e", fn, "-o", Files.input)
        xdm(Disks.basic2, "-e", fn + "-L", "-o", Files.reference)

        # compare generated xbas99 listing with TI BASIC reference
        xbas(Files.input, "-d", "-o", Files.output)
        checkListingEq(Files.output, Files.reference)

        # compare generated xbas99 basic program with TI BASIC reference
        xbas(Files.reference, "-c", "-j", "3", "-o", Files.output)
        checkFilesEq("Tokenization", Files.output, Files.input, "P")

    # check long format
    path = os.path.join(Dirs.basic, "sample-l.bin")
    xbas(path, "-d", "-o", Files.output)
    path = os.path.join(Dirs.basic, "sample-n.bin")
    xbas(path, "-d", "-o", Files.reference)
    checkFilesEq("Long Format", Files.output, Files.reference, "P")

    # check listing protection
    xdm(Disks.basic1, "-e", "STATMNTS-L", "-o", Files.input)
    xbas(Files.input, "-c", "-j", "3", "--protect", "-o", Files.output)
    xbas(Files.input, "-c", "-j", "3", "-o", Files.reference)
    checkFilesEq("Protection", Files.output, Files.reference, "P",
                 mask=[(0, 2)])

    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
