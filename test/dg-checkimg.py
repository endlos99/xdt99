#!/usr/bin/env python

import os
import re
import random

from config import Dirs, Files
from utils import xdg, xga, error, checkFilesEq


### Check function

def checkBytes(outfile, reffile):
    """check that outfile has not more data than reffile"""
    outbytes, cntbytes = countBytes(outfile), countBytes(reffile)
    if (outbytes > cntbytes):
        error("BYTEs", "Too many BYTEs/DATAs: %d instead of %d" % (
            outbytes, cntbytes))


def countBytes(fn):
    """count BYTEs/DATAs in source"""
    bytecnt = 0
    with open(fn, "r") as fin:
        source = fin.readlines()
    for line in source:
        # get rid of quoted single quotes ''
        line = re.sub(r"'(?:[^']|'')*'",
                      lambda x: ",".join(["z"] *
                                         (len(x.group(0)) - 2 -
                                          x.group(0)[1:-1].count("''"))),
                      line)
        # get instruction parts
        parts = re.split(r"\s+", line, maxsplit=2)
        if len(parts) > 2 and parts[1].lower() in (
                "byte", "data", "stri", "text"):
            # get all args
            args = [x.strip() for x in parts[2].split(",") if x.strip()]
            # know what you count
            if parts[1].lower() == "data":
                bytecnt += len(args) * 2
            elif  parts[1].lower() == "text":
                bytecnt += sum([len(a) / 2 if a[0] == '>' else 1
                                for a in args])
            elif parts[1].lower() == "stri":
                bytecnt += sum([len(a) / 2 if a[0] == '>' else 1
                                for a in args]) + 1  # len byte
            else:
                bytecnt += len(args)
    return bytecnt

    
### Main test

def runtest():
    """check cross-generated output against native reference files"""

    # run disassembler
    for srcfile, dopts, aopts in [
            ("gaops.gpl", ["-a", "0", "-r", "6", "17a"], []),
            ("gainst.gpl", ["-a", "0", "-r", "6", "a2", "a3", "aa", "ab", "ac", "b2", "b4"], []),
            ("gabranch.gpl", ["-a", "0", "-f", "5"], []),
            ("gamove.gpl", ["-a", "0", "-f", "6"], []),
            ("gafmt.gpl", ["-a", "0", "-f", "5", "-s", "rag"], ["-s", "rag"]),
            ("gacopy.gpl", ["-a", ">2000", "-r", "2000"], []),
            ("gaexts.gpl", ["-a", "0", "-r", "0x1e"], []),
            ("gapass.gpl", ["-a", "0x6030", "-r", "6030"], [])
            ]:
        source = os.path.join(Dirs.gplsources, srcfile)
        xga(*[source] + aopts + ["-o", Files.reference])
        xdg(*[Files.reference] + dopts + ["-p", "-o", Files.input])
        xga(*[Files.input] + aopts + ["-o", Files.output])
        checkFilesEq(srcfile, Files.output, Files.reference, "PROGRAM")
        checkBytes(Files.input, source)
        
    # top-down disassembler
    for srcfile, dopts, aopts in [
            ("gaops.gpl", ["-a", "0", "-f", "6"], []),
            ("gainst.gpl", ["-a", "0", "-f", "6"], []),
            ("gabranch.gpl", ["-a", "0", "-f", "5"], []),
            ("gamove.gpl", ["-a", "0", "-f", "6"], []),
            ("gafmt.gpl", ["-a", "0", "-f", "5", "-s", "rag"], ["-s", "rag"]),
            ("gadirs.gpl", ["-a", "0", "-f", "0"], []),
            ("gacopy.gpl", ["-a", ">2000", "-f", ">2000"], []),
            ("gaexts.gpl", ["-a", "0", "-f", "0x1e"], []),
            ("gapass.gpl", ["-a", "0x6030", "-f", ">6030"], [])
            ]:
        source = os.path.join(Dirs.gplsources, srcfile)
        xga(*[source] + aopts + ["-o", Files.reference])
        xdg(*[Files.reference] + dopts + ["-p", "-o", Files.input])
        xga(*[Files.input] + aopts + ["-o", Files.output])
        checkFilesEq(srcfile, Files.output, Files.reference, "PROGRAM")
        if countBytes(Files.output) > 0:
            error("BYTE", "Too many BYTE directives in result")

    # disassembler run
    for srcfile in ["dgruns.gpl"]:
        source = os.path.join(Dirs.gplsources, srcfile)
        xga(*[source] + ["-o", Files.reference])
        xdg(*[Files.reference] + ["-a", "0", "-r", "0x0", "-p", "-o", Files.input])
        xga(*[Files.input] + ["-o", Files.output])
        checkFilesEq(srcfile, Files.output, Files.reference, "PROGRAM")
        checkBytes(Files.input, source)

    # disassemble blob
    binary = os.path.join(Dirs.refs, "blobg.bin")
    #TODO: universal character escape \x..
    #xdg(binary, "-a", "0", "-f", "start", "-p", "-o", Files.input)
    #xga(Files.input, "-o", Files.output)
    #checkFilesEq("blobg", Files.output, binary, "PROGRAM")
    #xdg(binary, "-a", "0", "-r", "start", "-p", "-o", Files.input)
    #xga(Files.input, "-o", Files.output)
    #checkFilesEq("blobg-run", Files.output, binary, "PROGRAM")

    # disassemble random
    randrange = [n for n in xrange(256) if n != 0x08 and n != 0xfb]
    for r in xrange(16):
        random.seed(r)
        binary = "".join([chr(random.choice(randrange)) for i in xrange(2048)])
        with open(Files.reference, "wb") as fref:
            fref.write(binary)
        xdg(Files.reference, "-a", "1000", "-f", "1000", "-p", "-o", Files.input)
        xga(Files.input, "-o", Files.output)
        checkFilesEq("random" + str(r), Files.reference, Files.output, "PROGRAM")

    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
