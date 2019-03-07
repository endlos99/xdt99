#!/usr/bin/env python

import os
import re

from config import Dirs, Disks, Files
from utils import (xas, xdm, error, content, contentlen,
                   checkObjCodeEq, checkImageFilesEq, checkListFilesEq)


def ordw(word):
    return ord(word[0]) << 8 | ord(word[1])


def remove(files):
    for fn in files:
        if os.path.exists(fn):
            os.remove(fn)


### Check functions

def checkExists(files):
    for fn in files:
        try:
            with open(fn, "rb") as f:
                x = f.read()[0]
        except (IOError, IndexError):
            error("Files", "File missing or empty: " + fn)


def checkBinTextEqual(outfile, reffile):
    with open(outfile, "r") as fout, open(reffile, "rb") as fref:
        txt = " ".join(fout.readlines())
        bin = fref.read()
    if len(bin) % 2 == 1:
        bin += "\x00"
    bytes = [ord(x) for x in bin]
    dirs = [int(m, 16) for m in re.findall(">([0-9A-Fa-f]{2})", txt)][1:]
    if bytes != dirs:                                              # skip AORG
        error("DATA", "DATA/word mismatch")


def checkInstructions(outfile, instr):
    with open(outfile, "r") as fout:
        txt = fout.readlines()
    condensed = [line.replace(" ", "").strip() for line in txt if line.strip()]
    for i, line in enumerate(condensed):
        if (not ((instr[i][0] == 'b' and (line[:4] == instr[i])) or
                 line == instr[i])):
            error("text", "Malformed text file")


def checkSymbols(outfile, symbols):
    """check if all symbol/value pairs are in symfile"""
    with open(outfile, "r") as fout:
        source = fout.readlines()
    equs = {}
    for i in xrange(0, len(source), 2):
        sym = source[i].split(':')[0]
        val = source[i + 1].upper().split("EQU", 1)[1].strip().split()[0]
        equs[sym] = val
    for sym, val in symbols:
        if equs.get(sym) != val:
            error("symbols", "Symbol mismatch for %s=%s/%s" % (
                sym, val, equs.get(sym)))


### Main test

def runtest():
    """check command line interface"""

    # input and output files
    source = os.path.join(Dirs.sources, "ashello.asm")
    with open(Files.output, "wb") as f:
        xas(source, "-R", "-o", "-", stdout=f)
    xdm(Disks.asmsrcs, "-e", "ASHELLO-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)

    with open(Files.output, "wb") as f:
        xas(source, "-R", "-i", "-o", "-", stdout=f)
    xdm(Disks.asmsrcs, "-e", "ASHELLO-I", "-o", Files.reference)
    checkImageFilesEq(Files.output, Files.reference)

    with open(Files.output, "w") as f:
        xas(source, "-R", "-o", Files.output, "-L", "-", stdout=f)
    xdm(Disks.asmsrcs, "-e", "ASHELLO-L", "-o", Files.reference)
    checkListFilesEq(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, "nonexisting")
    with open(Files.error, "w") as ferr:
        xas(source, "-i", "-R", "-o", Files.output, stderr=ferr, rc=1)
    with open(Files.error, "r") as ferr:
        errs = ferr.readlines()
    if len(errs) != 1 or errs[0][:10] != "File error":
        error("File errors", "Incorrect file error message")

    # include path
    source = os.path.join(Dirs.sources, "ascopyi.asm")
    incls = os.path.join(Dirs.sources, "test") + "," + \
        os.path.join(Dirs.sources, "test", "test")
    xas(source, "-i", "-I", incls, "-o", Files.output)
    with open(Files.output, "rb") as f:
        data = f.read()
    if len(data[6:]) != 20:
        error("Include paths", "Incorrect image length")

    # command-line definitions
    source = os.path.join(Dirs.sources, "asdef.asm")
    xas(source, "-b", "-D", "s1=1", "s3=3", "s2=4", "-o", Files.output)
    assert content(Files.output) == "\x01\x03"
    xas(source, "-b", "-D", "s1=2,s2=2,s3=3", "-o", Files.output)
    assert content(Files.output) == "\x02\x03"

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

    # various parameter combinations
    source = os.path.join(Dirs.sources, "asxbank1.asm")
    remove([Files.reference])
    xas(source, "-b", "-o", Files.output, "-L", Files.reference)
    checkExists([Files.reference])

    # text data output
    source = os.path.join(Dirs.sources, "ascart.asm")
    xas(source, "-b", "-R", "-f", "-o", Files.reference)
    xas(source, "-t", "a2", "-R", "-f", "-o", Files.output)
    checkBinTextEqual(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, "asmtext.asm")
    xas(source, "-t", "a2", "-R", "-o", Files.output)
    checkInstructions(Files.output,
                      [";aorg>1000", "byte", ";aorg>2000", "byte"])

    # symbols
    source = os.path.join(Dirs.sources, "assyms.asm")
    xas(source, "-b", "-R", "-o", Files.reference, "-E", Files.output)
    checkSymbols(Files.output,
                 (("START", ">0000"), ("S1", ">0001"), ("S2", ">0018"),
                  ("VDPWA", ">8C02")))

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Files.error)


if __name__ == "__main__":
    runtest()
    print "OK"
