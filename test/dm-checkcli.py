#!/usr/bin/env python

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

    xdm(Disks.work, "-S", "0x01", "-o", Files.output)
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
    xdm(Disks.work, "-e", "DF127*", "PROG00001", "PROG00002")
    if (not os.path.isfile("df127x001") or not os.path.isfile("df127x010") or
        not os.path.isfile("df127x020p")):
        error("CLI", "DF127*: Missing files")

    xdm(Disks.work, "-d", "PROG*", "D?010X060")
    with open(Files.error, "w") as ferr:
        xdm(Disks.work, "-e", "PROG00255", stderr=ferr, rc=1)
        xdm(Disks.work, "-e", "DV010X060", stderr=ferr, rc=1)
        xdm(Disks.work, "-e", "DF010X060", stderr=ferr, rc=1)

    # multi-file naming
    xdm(Disks.work, "-n", "MULTI", "-a", "prog00001", "prog00255", "prog00002")
    xdm(Disks.work, "-e", "MULTI", "-o", Files.output)
    checkFilesEq("CLI", "prog00001", Files.output, "P")
    xdm(Disks.work, "-e", "MULTJ", "-o", Files.output)
    checkFilesEq("CLI", "prog00255", Files.output, "P")
    xdm(Disks.work, "-e", "MULTK", "-o", Files.output)
    checkFilesEq("CLI", "prog00002", Files.output, "P")

    xdm("-T", "prog00001", "prog00255", "prog00002", "-n", "MULTFI")
    xdm(Disks.work, "-t", "-a", "prog00001.tfi", "prog00255.tfi",
        "prog00002.tfi")
    xdm(Disks.work, "-e", "MULTFI", "-o", Files.output)
    checkFilesEq("CLI", "prog00001", Files.output, "P")
    xdm(Disks.work, "-e", "MULTFJ", "-o", Files.output)
    checkFilesEq("CLI", "prog00255", Files.output, "P")
    xdm(Disks.work, "-e", "MULTFK", "-o", Files.output)
    checkFilesEq("CLI", "prog00002", Files.output, "P")

    xdm("-T", "prog00255", "prog00002", "-9", "-n", "MULV9T")
    xdm(Disks.work, "-9", "-a", "prog00255.v9t9", "prog00002.v9t9")
    xdm(Disks.work, "-e", "MULV9T", "-o", Files.output)
    checkFilesEq("CLI", "prog00255", Files.output, "P")
    xdm(Disks.work, "-e", "MULV9U", "-o", Files.output)
    checkFilesEq("CLI", "prog00002", Files.output, "P")

    ref = os.path.join(Dirs.refs, "glob")
    xdm(Disks.work, "-a", ref + "?", "-n", "GLOBA1", shell=True)
    xdm(Disks.work, "-e", "GLOBA1", "-o", Files.output)
    xdm(Disks.work, "-e", "GLOBA2", "-o", Files.output)
    with open(Files.error, "w") as ferr:
        xdm(Disks.work, "-e", "GLOBA3", "-o", Files.output, stderr=ferr, rc=1)
    xdm(Disks.work, "-d", "GLOB*", "-o", Files.output)
    xdm(Disks.work, "-a", ref + "*", "-n", "GLOBB1", shell=True)
    xdm(Disks.work, "-e", "GLOBB1", "-o", Files.output)
    xdm(Disks.work, "-e", "GLOBB2", "-o", Files.output)
    xdm(Disks.work, "-e", "GLOBB3", "-o", Files.output)

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
    f = os.path.join(Dirs.refs, "vardis")
    for n in ["AA", "BB"]:
        xdm(Disks.work, "--initialize", "SSSD", "-a", f, "-n", n)
        with open(Files.output, "w") as fout:
            xdm(Disks.work, "-i", stdout=fout)
        checkFileMatches(Files.output, [(0, n + "\s+"), (2, n + "\s+")])

    # set geometry
    xdm(Disks.work, "--initialize", "1600", "-n", "GEO")
    for g, p in [("1S1D", "1S/1D\s+40 TpS"), ("99T8D7S", "7S/8D\s+99 TpS"),
                 ("22TDD", "7S/2D\s+22 TpS"), ("DSSD", "2S/1D\s+22 TpS"),
                 ("1T", "2S/1D\s+1 TpS"), ("3D 10T 9S", "9S/3D\s+10 TpS"),
                 ("SD DS", "2S/1D\s+10 TpS"), ("SS", "1S/1D\s+10 TpS")]:
        xdm(Disks.work, "--set-geometry", g)
        with open(Files.output, "w") as fout:
            xdm(Disks.work, "-i", "-q", stdout=fout)
        checkFileMatches(Files.output, [(0, p)])

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
        xdm(Disks.work, "-C", stderr=f1, rc=1)
        xdm(Disks.work, "-R", stderr=f2)
    checkFileLen(Files.output, minlines=2)
    with open(Files.output, "w") as f1:
        xdm(Disks.work, "-C", stderr=f1)
    checkFileLen(Files.output, maxlines=0)

    # FIAD operations
    shutil.copyfile(Disks.recsgen, Disks.work)
    xdm(Disks.work, "-e", "PROG00255", "DV064X010", "-t")
    xdm(Disks.work, "-e", "PROG00255", "-t", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "prog00255.tfi", "PROGRAM")
    xdm(Disks.work, "-e", "DV064X010", "-t", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "dv064x010.tfi", "PROGRAM")

    with open(Files.output, "w") as f:
        xdm("-I", "prog00255.tfi", "dv064x010.tfi", stdout=f)

    xdm(Disks.work, "-e", "PROG00255", "DV064X010", "-9")
    xdm(Disks.work, "-e", "PROG00255", "-9", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "prog00255.v9t9", "PROGRAM")
    xdm(Disks.work, "-e", "DV064X010", "-9", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "dv064x010.v9t9", "PROGRAM")

    with open(Files.output, "w") as f:
        xdm("-I", "prog00255.v9t9", "dv064x010.v9t9", stdout=f)

    xdm(Disks.work, "-e", "PROG00255")
    xdm("-T", "prog00255", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "prog00255.tfi", "PROGRAM", Masks.TIFile)
    xdm("-T", "prog00255", "-9", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "prog00255.v9t9", "PROGRAM", Masks.v9t9)

    xdm(Disks.work, "-e", "DV064X010", "-o", Files.reference)
    xdm("-F", "dv064x010.tfi")
    checkFilesEq("CLI", "dv064x010", Files.reference, "DIS/VAR 64")
    xdm("-F", "dv064x010.tfi", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "dv064x010", "PROGRAM")

    xdm("-F", "dv064x010.v9t9", "-9")
    checkFilesEq("CLI", "dv064x010", Files.reference, "DIS/VAR 64")
    xdm("-F", "dv064x010.v9t9", "-o", Files.output)
    checkFilesEq("CLI", Files.output, "dv064x010", "PROGRAM")

    xdm("-T", "dv064x010", "-o", Files.output,
        "-n", "DV064X010", "-f", "DIS/VAR 64")
    checkFilesEq("CLI", Files.output, "dv064x010.tfi", "PROGRAM", Masks.TIFile)
    os.remove("dv064x010.tfi")
    xdm("-T", "dv064x010", "-n", "DV064X010", "-f", "DIS/VAR 64")
    checkFilesEq("CLI", "dv064x010.tfi", Files.output, "PROGRAM", Masks.TIFile)

    xdm("-T", "dv064x010", "-9", "-o", Files.output,
        "-n", "DV064X010", "-f", "DIS/VAR 64")
    checkFilesEq("CLI", Files.output, "dv064x010.v9t9", "PROGRAM", Masks.v9t9)
    os.remove("dv064x010.v9t9")
    xdm("-T", "dv064x010", "-9", "-n", "DV064X010", "-f", "DIS/VAR 64")
    checkFilesEq("CLI", "dv064x010.v9t9", Files.output, "PROGRAM", Masks.v9t9)

    # usage errors
    with open(Files.error, "w") as ferr:
        xdm("-a", Files.output, stderr=ferr, rc=1)
        xdm("-T", "prog00001", "prog00002", "-o", Files.output,
            stderr=ferr, rc=1)
        xdm("-T", "prog00001", "prog00002", "-9", "-o", Files.output,
            stderr=ferr, rc=1)
        xdm("-F", "-o", Files.output, stderr=ferr, rc=2)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Files.error)
    os.remove(Disks.work)
    os.remove(Disks.tifiles)
    for fn in [
        "prog00001", "prog00002", "prog00255", "dv064x010",
        "df002x001", "df127x001", "df127x010", "df127x020p",
        "prog00001.tfi", "prog00002.tfi", "prog00255.tfi", "dv064x010.tfi",
        "prog00002.v9t9", "prog00255.v9t9", "dv064x010.v9t9"
        ]:
        os.remove(fn)


if __name__ == "__main__":
    runtest()
