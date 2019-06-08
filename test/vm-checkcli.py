#!/usr/bin/env python

import os
import shutil

from config import Dirs, Disks, Files
from utils import xvm, xdm, error, check_files_eq


# Check functions

def check_file_len(infile, minlines=-1, maxlines=99999):
    """check if file has certain length"""
    try:
        with open(infile, "r") as f:
            line_count = len(f.readlines())
    except IOError:
        line_count = 0
    if not minlines <= line_count <= maxlines:
        error("CLI",
              "%s: Line count mismatch: found %d lines, expected %d to %d" % (
                  infile, line_count, minlines, maxlines))


# Main test

def runtest():
    """check command line interface"""

    # setup
    with open(Disks.volumes, "wb") as v:
        for i in xrange(4 * 1600):
            v.write("\x00" * 256)  # Disk.bytes_per_sector
    shutil.copyfile(Disks.recsgen, Disks.work)

    # volume operations
    xvm(Disks.volumes, "2", "-w", Disks.recsgen, "--keep-size")
    xvm(Disks.volumes, "1,3-4", "-w", Disks.recsdis, "--keep-size")

    with open(Files.error, "w") as fout:
        xvm(Disks.volumes, "1-5", stdout=fout)
        xvm(Disks.volumes, "4", "-i", stdout=fout)
        xvm(Disks.volumes, "5", "-i", stderr=fout, rc=1)

    xvm(Disks.volumes, "2", "-r", Files.output)
    check_files_eq("xvm", Files.output, Disks.recsgen, "P")
    xvm(Disks.volumes, "1", "-r", Files.output)
    check_files_eq("xvm", Files.output, Disks.recsdis, "P")
    xvm(Disks.volumes, "4", "-r", Files.output)
    check_files_eq("xvm", Files.output, Disks.recsdis, "P")
    xvm(Disks.volumes, "4", "-r", Files.output, "--keep-size")
    check_files_eq("xvm", Files.output, Disks.recsdis, "P",
                   mask=[(360 * 256, 1600 * 256)])

    # file operations
    xvm(Disks.volumes, "2", "-e", "DF254X015P", "-o", Files.output)
    xdm(Disks.recsgen, "-e", "DF254X015P", "-o", Files.reference)
    check_files_eq("xvm", Files.output, Files.reference, "P")

    xvm(Disks.volumes, "1", "-w", Disks.work, "--keep-size")
    ref = os.path.join(Dirs.refs, "sector1")
    xdm(Disks.work, "-a", ref, "-f", "DF80")
    xvm(Disks.volumes, "1", "-a", ref, "-f", "DF80")
    xvm(Disks.volumes, "1", "-r", Files.output)
    check_files_eq("xvm", Files.output, Disks.work, "P")

    xvm(Disks.volumes, "3", "-w", Disks.work)
    xvm(Disks.volumes, "3", "-a", ref, "-f", "DF80", "-n", "REFFILE")
    xvm(Disks.volumes, "3", "-r", Files.output)
    xdm(Files.output, "-e", "REFFILE", "-q", "-o", Files.reference)

    ref = os.path.join(Dirs.refs, "glob")
    xvm(Disks.volumes, "1", "-a", ref + "?", "-n", "GLOBA1", shell=True)
    xvm(Disks.volumes, "1", "-e", "GLOBA1", "-o", Files.output)
    xvm(Disks.volumes, "1", "-e", "GLOBA2", "-o", Files.output)
    with open(Files.error, "w") as ferr:
        xvm(Disks.volumes, "1", "-e", "GLOBA3", "-o", Files.output,
            stderr=ferr, rc=1)
    xvm(Disks.volumes, "1", "-d", "GLOB*", "-o", Files.output)
    xvm(Disks.volumes, "1", "-a", ref + "*", "-n", "GLOBB1", shell=True)
    xvm(Disks.volumes, "1", "-e", "GLOBB1", "-o", Files.output)
    xvm(Disks.volumes, "1", "-e", "GLOBB2", "-o", Files.output)
    xvm(Disks.volumes, "1", "-e", "GLOBB3", "-o", Files.output)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Files.error)
    os.remove(Disks.work)
    os.remove(Disks.volumes)


if __name__ == "__main__":
    runtest()
    print "OK"
