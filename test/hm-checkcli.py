#!/usr/bin/env python

import os
import shutil
import re
import gzip

from config import Dirs, Disks, Files
from utils import xhm, xdm, error, checkFilesEq


### Check functions

def checkFileContains(infile, pattern):
    """check if text file contains at least one RE match"""
    try:
        with open(infile, "r") as fin:
            for line in fin:
                if re.search(pattern, line):
                    return
    except IOError:
        pass
    error("HFE", "%s: no match found" % infile)


### Main test

def runtest():
    """check command line interface"""

    # conversion HFE <-> disk pseudo-disks
    for n in ["rsssd", "rdssd", "rssdd", "rdsdd",
              "rsssd80t", "rdssd80t", "tiit80t"]:
        refdsk = os.path.join(Dirs.hfe, n + ".dsk")
        refhfe = os.path.join(Dirs.hfe, n + "_dsk.hfe.gz")
        with gzip.open(refhfe, "rb") as fin, open(Files.reference, "wb") as fout:
            fout.write(fin.read())
        xhm("-T", refdsk, "-o", Files.input)
        checkFilesEq("HFE", Files.input, Files.reference, "PROGRAM")
        xhm("-F", Files.input, "-o", Files.output)
        checkFilesEq("HFE", Files.output, refdsk, "PROGRAM")

    # xdm99 delegation
    with gzip.open(Disks.hfe, "rb") as fin, open(Disks.work, "wb") as fout:
        fout.write(fin.read())
    with open(Files.output, "w") as fout:
        xhm(Disks.work, stdout=fout)
    checkFileContains(Files.output, "HFEDISK.*1S/1D.*40")
    checkFileContains(Files.output, "HFEFILE")

    # image manipulation
    ref = os.path.join(Dirs.refs, "ti-text")
    xhm(Disks.work, "-a", ref, "-n", "TESTFILE", "-f", "DV60")
    xhm(Disks.work, "-e", "TESTFILE", "-o", Files.output)
    xhm("-o", Files.output, Disks.work, "-e", "TESTFILE")
    checkFilesEq("HFE", Files.output, ref, "PRORGAM")
    with open(Files.output, "wb") as fout:
        xhm(Disks.work, "-p", "TESTFILE", stdout=fout)
    checkFilesEq("HFE", Files.output, ref, "PRORGAM")

    ref = os.path.join(Dirs.refs, "V10R.tfi")
    shutil.copyfile(ref, Files.reference)    
    xhm(Disks.work, "-a", Files.reference, "-t")
    xhm(Disks.work, "-e", "V10R", "-o", Files.output)
    xhm("-o", Files.output, Disks.work, "-e", "V10R")
    ref = os.path.join(Dirs.refs, "v10r.txt")
    checkFilesEq("HFE", Files.output, ref, "PRORGAM")

    # image resize
    with open(Files.output, "w") as fout:
        xhm("--hfe-info", Disks.work, stdout=fout)
    checkFileContains(Files.output, "Tracks: 40")
    checkFileContains(Files.output, "Sides: 1")
    checkFileContains(Files.output, "Encoding: 2")  # SD
    xhm(Disks.work, "-Z", "dsdd")
    with open(Files.output, "w") as fout:
        xhm("--hfe-info", Disks.work, stdout=fout)
    checkFileContains(Files.output, "Tracks: 40")
    checkFileContains(Files.output, "Sides: 2")
    checkFileContains(Files.output, "Encoding: 0")  # DD

    # image creation
    xhm(Disks.work, "-X", "dssd80t", "-a", ref, "-n", "WALDO")
    with open(Files.output, "w") as fout:
        xhm(Disks.work, "-i", stdout=fout)
    checkFileContains(Files.output, "2S/1D\s+80")
    checkFileContains(Files.output, "WALDO.*PROGRAM")
    with open(Files.output, "w") as fout:
        xhm("--hfe-info", Disks.work, stdout=fout)
    checkFileContains(Files.output, "Tracks: 80")
    checkFileContains(Files.output, "Sides: 2")
    checkFileContains(Files.output, "Encoding: 2")  # SD

    # messy stuff
    xdm(Disks.work, "-X", "sssd")
    xdm(Disks.work, "--set-geometry", "dssd")  # image too short now!
    xhm("-T", Disks.work, "-o", Files.input)
    with open(Files.output, "w") as fout:
        xhm("--hfe-info", Files.input, stdout=fout)
    checkFileContains(Files.output, "Tracks: 40")
    checkFileContains(Files.output, "Sides: 2")  # DS
    checkFileContains(Files.output, "Encoding: 2")  # SD
    with open(Files.error, "w") as ferr:  # quelch error msg
        xhm(Files.input, stderr=ferr, rc=1)  # invalid track count

    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Files.error)
    os.remove(Disks.work)


if __name__ == "__main__":
    runtest()
