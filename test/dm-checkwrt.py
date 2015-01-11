#!/usr/bin/env python

import os
import shutil
import random

from config import Dirs, Disks, Files
from utils import xdm, checkFilesEq


### Utility functions

def createTextline(length):
    """create line of random text with checksum"""
    vs = [random.randint(0, 79) for _ in range(length - 1)]
    cc = (- sum(vs)) % 80
    return "".join(chr(v + 48) for v in vs + [cc])


def createBlob(size):
    """create random binary data with checksum"""
    vs = [random.randint(0, 255) for _ in range(size - 1)]
    cc = (- sum(vs)) % 256
    return "".join(chr(v) for v in vs + [cc])


def createTextFile(count, length, fixed, partial):
    """create text file with random records"""
    name = "D%c%03dX%03d%s" % ("F" if fixed else "V", length, count,
                               "P" if partial else "")
    path = os.path.join(Dirs.tmp, name.lower())
    lines = [
        createTextline(random.randint(0, length) if partial else length)
        for _ in xrange(count)
        ]
    data = "\n".join(lines) + "\n"
    fmt = ("DIS/FIX" if fixed else "DIS/VAR") + str(length)
    with open(path, "w") as f:  # "w" mangles \n into \r\n
        f.write(data)
    return name, path, fmt


def createBinaryFile(size):
    """create binary file with random binary data"""
    name = "PROG%05d" % size
    path = os.path.join(Dirs.tmp, name.lower())
    data = createBlob(size)
    with open(path, "wb") as f:
        f.write(data)
    return name, path, "PROGRAM"


### Main test

def runtest():
    """check reading and writing of random data"""
    
    # setup
    shutil.copyfile(Disks.blank, Disks.work)
    shutil.copyfile(Disks.blank, Disks.tifiles)
    shutil.copyfile(Disks.blank, Disks.recsgen)

    # create files
    files = []
    for count, length in [
            (1, 2), (300, 2), (60, 10), (10, 63), (10, 64), (10, 126),
            (1, 127), (10, 127), (10, 128), (10, 129), (1, 254), (5, 254),
            (1, 255), (5, 255)
            ]:
        files.append(createTextFile(count, length, False, False))
        files.append(createTextFile(count, length, True, False))
    for count, length in [(20, 127), (15, 254), (15, 255)]:
        files.append(createTextFile(count, length, False, True))
        files.append(createTextFile(count, length, True, True))
    for size in [1, 2, 254, 255, 511, 513, 2560]:
        files.append(createBinaryFile(size))

    bigFiles = []
    for count, length in [(200, 127), (100, 254), (100, 255)]:
        bigFiles.append(createTextFile(count, length, False, True))
        bigFiles.append(createTextFile(count, length, True, True))
    for size in [25600]:
        bigFiles.append(createBinaryFile(size))

    # add files one by one and check
    for name, path, fmt in files:
        xdm(Disks.work, "-a", path, "-f", fmt)
        xdm(Disks.work, "-e", name, "-o", Files.output)
        checkFilesEq("Write records", Files.output, path, fmt)

    # remove files one by one and check
    for name, path, fmt in files:
        xdm(Disks.work, "-e", name, "-o", Files.output)
        checkFilesEq("Write records", Files.output, path, fmt)
        xdm(Disks.work, "-d", name)

    # add all files
    for name, path, fmt in files:
        xdm(Disks.work, "-a", path, "-f", fmt)

    # extract in and convert to/from TIFile format
    for name, path, fmt in files:
        xdm(Disks.work, "-e", name, "-o", Files.reference)
        xdm(Disks.work, "-e", name, "-t", "-o", Files.tifile)
        xdm(Files.tifile, "-F", "-o", Files.output)
        checkFilesEq("Write records", Files.output, Files.reference, fmt)
        xdm(Files.reference, "-T", "-o", Files.output, "-f", fmt, "-n", name)
        checkFilesEq("Write records", Files.output, Files.tifile,
                     "PROGRAM", [(0x1e, 0x26)])

    # add and remove TIFs
    for name, path, fmt in files:
        xdm(Disks.work, "-e", name, "-t", "-o", Files.tifile)
        xdm(Disks.tifiles, "-t", "-a", Files.tifile)
    checkFilesEq("Write records", Disks.tifiles, Disks.work, "P")

    # add and remove big files
    for name, path, fmt in bigFiles:
        xdm(Disks.work, "-a", path, "-f", fmt)
        xdm(Disks.work, "-e", name, "-o", Files.output)
        checkFilesEq("Write records", Files.output, path, fmt)
        xdm(Disks.work, "-d", name)

    # create well-defined TI disk
    for name, path, fmt in files:
        xdm(Disks.recsgen, "-a", path, "-f", fmt)

    # remove temporary files
    for name, path, fmt in files + bigFiles:
        os.remove(path)
    os.remove(Files.output)
    os.remove(Files.tifile)
    os.remove(Files.reference)
    os.remove(Disks.work)
    os.remove(Disks.tifiles)


if __name__ == "__main__":
    runtest()
