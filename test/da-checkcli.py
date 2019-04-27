#!/usr/bin/env python

import os
import re
import glob

from config import Dirs, Files
from utils import xda, xas, error, check_indent, count_mnemonics, check_source, check_origins


# Check function

def check_strings(outfile, reffile):
    with open(outfile, "r") as fout, open(reffile, "r") as fref:
        out = [line for line in fout.readlines() if "text" in line.lower()]
        ref = [line for line in fref.readlines() if "text" in line.lower()]
        if len(out) != len(ref):
            error("text", "TEXT count mismatch: %d/%d" % (len(out), len(ref)))
        tout = [re.split(r"\s+", line)[2].lower() for line in out]
        tref = [re.split(r"\s+", line)[2].lower() for line in ref]
        if tout != tref:
            error("text", "TEXT mismatch")


def check_range(outfile, fidx, tidx):
    """check if only given range was disassembled"""
    with open(outfile, "r") as fout:
        src = fout.readlines()[1:]  # skip AORG
    for i in xrange(1, len(src)):
        if fidx <= i < tidx and src[i][9] != ' ':
            error("start", "Missing disassembly at %d" % i)
        if not fidx <= i < tidx and src[i][9] != '?':
            error("start", "Bad disassembly at %d" % i)

    
def count_datas(fn):
    """count DATAs in source"""
    with open(fn, "r") as fin:
        source = fin.readlines()
    count = 0
    for line in source:        
        parts = re.split(r"\s+", line, maxsplit=2)
        if len(parts) > 2 and parts[1].lower() == "data":
            count += 1
    return count


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    # source and symbol EQU file
    source = os.path.join(Dirs.sources, "dasource.asm")
    xas(source, "-b", "-R", "-o", Files.reference, "-E", Files.input)
    xda(Files.reference, "-a", "6000", "-f", "6016", "-p", "-S", Files.input, "-o", Files.output)
    check_source(Files.output, source)

    # symbols w/o EQUs
    source = os.path.join(Dirs.sources, "dasym.asm")
    syms = os.path.join(Dirs.sources, "dasym.txt")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference, "-a", "2000", "-f", "2000", "-p", "-S", syms, "-o", Files.output)
    check_source(Files.output, source)

    # from/to
    source = os.path.join(Dirs.sources, "dastart.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference, "-a", "6000", "-f", "601c",
        "-o", Files.output)
    check_range(Files.output, 14, 999)
    xda(Files.reference, "-a", "6000", "-r", "6006", "-o", Files.output)
    check_range(Files.output, 3, 999)
    xda(Files.reference, "-a", "6000", "-f", "600c", "-t", "6010", "-o", Files.output)
    check_range(Files.output, 6, 8)
    xda(Files.reference, "-a", "6000", "-r", "6004", "-t", "6014", "-o", Files.output)
    check_range(Files.output, 2, 10)
    
    # exclude
    source = os.path.join(Dirs.sources, "daexclude.asm")
    xas(source, "-b", "-o", Files.reference)
    xda(Files.reference, "-a", "0", "-r", "0x0", "-e", "0-2", "8-12", "-p", "-o", Files.output)
    datas = count_datas(Files.output)
    if datas != 6:
        error("exclude", "DATA count mismatch: %d/6" % datas)

    # "start"
    source = os.path.join(Dirs.sources, "dastart.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference, "-a", "6000", "-f", "start", "-o", Files.output)
    m1 = sum(count_mnemonics(Files.output, offset=9).values())
    if m1 != 4:
        error("start", "mnemonic count mismatch: %d/4" % m1)
    xda(Files.reference, "-a", "6000", "-r", "start", "-o", Files.output)
    m2 = sum(count_mnemonics(Files.output, offset=9).values())
    if m2 != 4:
        error("start", "mnemonic count mismatch: %d/4" % m2)

    # origins
    source = os.path.join(Dirs.sources, "dajumps.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference, "-a", "0", "-r", "0", "-o", Files.output)
    check_origins(Files.output, {
        0xa: [0x2a],
        0x20: [0x12],
        0x2e: [0xe, 0x24, 0x30]})

    # strings (won't really work with "-f", unless the order is changed
    source = os.path.join(Dirs.sources, "datext.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference, "-a", "7000", "-r", "7000", "-p", "-n",
        "-o", Files.output)
    check_strings(Files.output, source)
    
    # force
    source = os.path.join(Dirs.sources, "daforce.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference, "-a", "a000", "-r", "a000", "-o", Files.output)
    movs = count_mnemonics(Files.output, offset=9, wanted="mov")
    if movs != 2:
        error("force", "MOV mnemonics count mismatch: %d/2" % movs)
    xda(Files.reference, "-a", "a000", "-r", "a000", "-F", "-o", Files.output)
    movs = count_mnemonics(Files.output, offset=9, wanted="mov")
    if movs != 0:
        error("force", "MOV mnemonics count mismatch: %d/0" % movs)

    # layout
    source = os.path.join(Dirs.sources, "dastart.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference, "-a", "6000", "-f", "start", "-o", Files.output)
    check_indent(Files.output, 2)
    xda(Files.reference, "-a", "6000", "-f", "start", "-p", "-o", Files.output)
    check_indent(Files.output, 1)

    # Cleanup
    os.remove(Files.input)
    for f in glob.glob(Files.output + "*"):
        os.remove(f)
    for f in glob.glob(Files.reference + "*"):
        os.remove(f)


if __name__ == "__main__":
    runtest()
    print "OK"
