#!/usr/bin/env python

#UPD

import os
import shutil
import re

from config import Dirs, Disks, Files, Masks
from utils import xdm, error, checkFilesEq


### Check functions

def checkFileLen(infile, minlines=-1, maxlines=99999):
    """check if text file has certain length"""

    try:
        with open(infile, "r") as f:
            linecnt = len(f.readlines())
    except IOError:
        linecnt = 0
    if not minlines <= linecnt <= maxlines:
        error("CLI",
              "%s: Line count mismatch: found %d lines, expected %d to %d" % (
                  infile, linecnt, minlines, maxlines))

def checkFileSize(infile, size):
    """check if file has certain size"""
    statinfo = os.stat(infile)
    if statinfo.st_size != size:
        error("CLI",
              "%s: File size mismatch: found %d bytes, expected %d" % (
                  infile, statinfo.st_size, size))

def checkFileMatches(infile, matches):
    """check if text file contents match regular expressions"""
    try:
        with open(infile, "r") as f:
            contents = f.readlines()
    except IOError:
        error("CLI", "%s: File not found" % infile)
    for line, pattern in matches:
        try:
            if not re.search(pattern, contents[line]):
                error("CLI", "%s: Line %d does not match" % (infile, line))
        except IndexError:
            error("CLI", "%s: Line %d missing" % (infile, line))


### Main test

def runtest():
    """check command line interface"""

    # setup
    shutil.copyfile(Disks.recsgen, Disks.work)

    # disk image operations
    with open(Files.output, "w") as f1, open(Files.reference, "w") as f2:
        xdm(Disks.work, "-i", stdout=f2)
        xdm(Disks.work, "-q", stdout=f1)
    checkFilesEq("CLI", Files.output, Files.reference, "DIS/VAR255")

    xdm(Disks.work, "-e", "PROG00255", "DV064X010", "DF002X001")
    xdm(Disks.work, "-e", "PROG00255", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "prog00255", "PROGRAM")
    xdm(Disks.work, "-e", "DV064X010", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "dv064x010", "DIS/VAR64")
    xdm(Disks.work, "-e", "DF002X001", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "df002x001", "DIS/FIX 2")

    with open(Files.output, "w") as f1:
        xdm(Disks.work, "-p", "DV064X010", stdout=f1)
    checkFilesEq("CLI", Files.output, "dv064x010", "DIS/VAR 64")

    with open(Files.error, "w") as ferr:
        xdm(Disks.work, "-e", "INVALID", stderr=ferr, rc=1)

    xdm(Disks.work, "-s", "0x01", "-o", Files.output)
    checkFilesEq("CLI", Files.output,
                 os.path.join(Dirs.refs, "sector1"), "DIS/VAR255")

    # add, rename, remove files
    shutil.copyfile(Disks.blank, Disks.work)
    xdm(Disks.work, "-a", "prog00255", "dv064x010", "df002x001")
    xdm(Disks.work, "-e", "PROG00255", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "prog00255", "PROGRAM")
    xdm(Disks.work, "-e", "DV064X010", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "dv064x010", "PROGRAM")  #!

    shutil.copyfile(Disks.work, Disks.tifiles)
    xdm(Disks.work, "-e", "PROG00255", "-o", Files.reference)
    xdm(Disks.work, "-r", "PROG00255:OTHERNAME")
    xdm(Disks.work, "-e", "OTHERNAME", "-o", Files.output)
    checkFilesEq("CLI", Files.output, Files.reference, "P")
    xdm(Disks.work, "-r", "OTHERNAME:PROG00255")
    checkFilesEq("CLI", Disks.work, Disks.tifiles, "P")

    xdm(Disks.work, "-d", "PROG00255", "DV064X010", "DF002X001")
    with open(Files.output, "w") as f1, open(Files.reference, "w") as f2:
        xdm(Disks.work, "-i", stdout=f1)
        xdm(Disks.blank, "-i", stdout=f2)
    checkFilesEq("CLI", Files.output, Files.reference, "DIS/VAR255")

    shutil.copyfile(Disks.recsgen, Disks.work)
    xdm(Disks.work, "-e", "DF127*")
    if (not os.path.isfile("df127x001") or not os.path.isfile("df127x010") or
        not os.path.isfile("df127x020p")):
        error("CLI", "DF127*: Missing files")

    xdm(Disks.work, "-d", "PROG*", "D?010X060")
    with open(Files.error, "w") as ferr:
        xdm(Disks.work, "-e", "PROG00255", stderr=ferr, rc=1)
        xdm(Disks.work, "-e", "DV010X060", stderr=ferr, rc=1)
        xdm(Disks.work, "-e", "DF010X060", stderr=ferr, rc=1)
        
    # initialize disk
    xdm(Disks.work, "--initialize", "360", "-n", "SSSD")
    checkFileSize(Disks.work, 360 * 256)
    checkFilesEq("CLI", Disks.work, Disks.blank, "P")
    os.remove(Disks.work)
    xdm(Disks.work, "--initialize", "SSSD", "-n", "SSSD")
    checkFileSize(Disks.work, 360 * 256)
    checkFilesEq("CLI", Disks.work, Disks.blank, "P")
    xdm(Disks.work, "--initialize", "800", "-n", "INIT")
    with open(Files.output, "w") as f:
        xdm(Disks.work, "-i", stdout=f)
    checkFileMatches(Files.output, [(0, "\s2\s+used\s+798\s+free\s")])
    os.remove(Disks.work)
    xdm(Disks.work, "--initialize", "CF", "-n", "INIT")
    with open(Files.output, "w") as f:
        xdm(Disks.work, "-i", stdout=f)
    checkFileMatches(Files.output, [(0, "\s2\s+used\s+1598\s+free\s")])
    with open(Files.error, "w") as ferr:
        xdm(Disks.work, "--initialize", "1", stderr=ferr, rc=1)
        xdm(Disks.work, "--initialize", "1601", stderr=ferr, rc=1)
        xdm(Disks.work, "--initialize", "FOO", stderr=ferr, rc=1)

    # resize disk
    shutil.copyfile(Disks.recsgen, Disks.work)
    for s in ["800", "248", "1600"]:
        xdm(Disks.work, "-Z", s, "-q")
        for f in ["PROG02560", "DF129X010", "DV127X010", "DV255X015P"]:
            xdm(Disks.work, "-e", f, "-q", "-o", Files.output)
            xdm(Disks.recsgen, "-e", f, "-o", Files.reference)
            checkFilesEq("CLI", Files.output, Files.reference, "PROGRAM")
    with open(Files.error, "w") as ferr:
        xdm(Disks.work, "-Z", "240", stderr=ferr, rc=1)
        xdm(Disks.work, "-Z", "1608", stderr=ferr, rc=1)

    # repair disks
    shutil.copyfile(Disks.bad, Disks.work)
    with open(Files.output, "w") as f1, open(Files.reference, "w") as f2:
        xdm(Disks.work, "-c", stderr=f1, rc=1)
        xdm(Disks.work, "-R", stderr=f2)
    checkFileLen(Files.output, minlines=2)
    with open(Files.output, "w") as f1:
        xdm(Disks.work, "-c", stderr=f1)
    checkFileLen(Files.output, maxlines=0)

    # TIFile operations
    shutil.copyfile(Disks.recsgen, Disks.work)
    xdm(Disks.work, "-e", "PROG00255", "DV064X010", "-t")
    xdm(Disks.work, "-e", "PROG00255", "-t", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "prog00255.tfi", "PROGRAM")
    xdm(Disks.work, "-e", "DV064X010", "-t", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "dv064x010.tfi", "PROGRAM")

    with open(Files.output, "w") as f:
        xdm("dv064x010.tfi", "-I", stdout=f)

    xdm(Disks.work, "-e", "PROG00255")
    xdm("prog00255", "-T", "-o", Files.output)
    checkFilesEq("CLI TIFiles", Files.output, "prog00255.tfi",
                 "PROGRAM", Masks.TIFile)

    xdm("dv064x010.tfi", "-F")
    xdm("dv064x010.tfi", "-F", "-o", Files.output)
    checkFilesEq("CLI TIFiles", Files.output, "dv064x010", "PROGRAM")
    xdm(Disks.work, "-e", "DV064X010", "-o", Files.reference)
    checkFilesEq("CLI TIFiles", "dv064x010", Files.reference, "DIS/VAR 64")

    xdm("dv064x010", "-T", "-o", Files.output,
        "-n", "DV064X010", "-f", "DIS/VAR 64")
    checkFilesEq("CLI TIFiles", Files.output, "dv064x010.tfi",
                 "PROGRAM", Masks.TIFile)
    os.remove("dv064x010.tfi")
    xdm("dv064x010", "-T", "-n", "DV064X010", "-f", "DIS/VAR 64")
    checkFilesEq("CLI TIFiles", "dv064x010.tfi", Files.output,
                 "PROGRAM", Masks.TIFile)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Files.error)
    os.remove("prog00255")
    os.remove("prog00255.tfi")
    os.remove("dv064x010")
    os.remove("dv064x010.tfi")
    os.remove("df002x001")
    os.remove("df127x001")
    os.remove("df127x010")
    os.remove("df127x020p")
    os.remove(Disks.work)
    os.remove(Disks.tifiles)


if __name__ == "__main__":
    runtest()
