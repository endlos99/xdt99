#!/usr/bin/env python

import os
import random
import glob

from config import Dirs, Files
from utils import xda, xas, error, checkFilesEq


### Check function

def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip(">"), 16 if s[:2] == "0x" or s[:1] == ">" else 10)


def checkData(fn):
    """count DATAs in source"""
    datas = 0
    with open(fn, "r") as fin:
        source = fin.readlines()
    for line in source:
        cs = line.split()
        if (len(cs) >= 2 and cs[1].lower() == "data" or
                len(cs) >= 1 and cs[0].lower() == "data"):
            datas += 1
    return datas
    
    
def checkEq(value1, value2, msg):
    if value1 != value2:
        error(msg, "Count mismatch: expected %d, but got %d" % (
            value2, value1))


### Main test

def runtest():
    """check cross-generated output against native reference files"""

    # disassembler: run
    for srcfile, aopts, addr, start in [
            #("asopcs.asm", ["-R"], "0000", "0000"]), only for -d
            ("asexprs.asm", [], "0000", "0154"),
            ("asregs.asm", ["-R"], "0000", "0000"),
            ("ascart.asm", ["-R"], "0000", "000c"),
            ("darun.asm", ["-R"], "0000", "0002")
            ]:
        source = os.path.join(Dirs.sources, srcfile)
        asref = Files.reference + "_" + addr
        asout = Files.output + "_" + addr
        xas(*[source, "-b"] + aopts + ["-o", Files.reference])
        xda(asref, "-a", addr, "-r", start, "-p", "-o", Files.input)
        xas(*[Files.input, "-b", "-R", "-o", Files.output])
        checkFilesEq(srcfile, asout, asref, "PROGRAM")

    # disassembler: top-down
    for srcfile, aopts, addr, start in [
            ("asopcs.asm", ["-R"], "0000", "0000"),
            ("asexprs.asm", [], "0000", "0154"),
            ("asregs.asm", ["-R"], "0000", "0000"),
            ("ascart.asm", ["-R"], "0000", "000c"),
            ("darun.asm", ["-R"], "0000", "0002")
            ]:
        source = os.path.join(Dirs.sources, srcfile)
        asref = Files.reference + "_" + addr
        asout = Files.output + "_" + addr
        xas(*[source, "-b"] + aopts + ["-o", Files.reference])
        xda(asref, "-a", addr, "-f", start, "-p", "-o", Files.input)
        xas(*[Files.input, "-b", "-R", "-o", Files.output])
        checkFilesEq(srcfile, asout, asref, "PROGRAM")

    # running disassembler
    source = os.path.join(Dirs.sources, "darun.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference + "_0000", "-a", "0", "-r", "2", "-p",
        "-o", Files.output)
    checkEq(checkData(Files.output), checkData(source), "run")

    source = os.path.join(Dirs.sources, "daexec.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    xda(Files.reference + "_1000", "-a", "1000", "-r", "103c", "1008", "-p",
        "-o", Files.output)
    checkEq(checkData(Files.output), checkData(source), "run")    

    # disassemble cart BINs
    for binfile, start in (
            ("blobm.bin", "6012"),
            ("blobh.bin", "start")):
        binary = os.path.join(Dirs.refs, binfile)
        xda(binary, "-a", "6000", "-r", start, "-p", "-o", Files.input)
        xas(Files.input, "-b", "-R", "-o", Files.output)
        checkFilesEq(binary, Files.output + "_6000", binary, "PROGRAM")

        xda(binary, "-a", "6000", "-f", start, "-p", "-o", Files.input)
        xas(Files.input, "-b", "-R", "-o", Files.output)
        checkFilesEq(binary, Files.output + "_6000", binary, "PROGRAM")

    # disassemble random
    for r in xrange(16):
        random.seed(r)
        binary = "".join([chr(random.randrange(256)) for i in xrange(2048)])
        with open(Files.reference, "wb") as fref:
            fref.write(binary)
        xda(Files.reference, "-a", "1000", "-f", "1000", "-p",
            "-o", Files.input)
        xas(Files.input, "-b", "-R", "-o", Files.output)
        checkFilesEq("random" + str(r), Files.reference,
                     Files.output + "_1000", "PROGRAM")
        
    # Cleanup
    os.remove(Files.input)
    for f in glob.glob(Files.output + "*"):
        os.remove(f)
    for f in glob.glob(Files.reference + "*"):
        os.remove(f)


if __name__ == "__main__":
    runtest()
    print "OK"
