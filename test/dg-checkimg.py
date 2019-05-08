#!/usr/bin/env python

import os
import re
import random

from config import Dirs, Files
from utils import xdg, xga, error, check_files_eq, count_bytes, check_bytes


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    # run disassembler
    for srcfile, dopts, aopts in [
            ("gaops.gpl", ["-a", "0", "-r", "6", "17a"], []),
            ("gainst.gpl", ["-a", "0", "-r", "6", "a2", "a3", "aa", "ab", "ac", "b2", "b4"], []),
            ("gabranch.gpl", ["-a", "0", "-f", "5"], []),
            ("gamove.gpl", ["-a", "0", "-f", "6"], []),
            ("gafmt.gpl", ["-a", "0", "-f", "5", "-y", "rag"], ["-y", "rag"]),
            ("gacopy.gpl", ["-a", ">2000", "-r", "2000"], []),
            ("gaexts.gpl", ["-a", "0", "-r", "0x1e"], []),
            ("gapass.gpl", ["-a", "0x6030", "-r", "6030"], [])
            ]:
        source = os.path.join(Dirs.gplsources, srcfile)
        xga(*[source] + aopts + ["-o", Files.reference])
        xdg(*[Files.reference] + dopts + ["-p", "-o", Files.input])
        xga(*[Files.input] + aopts + ["-o", Files.output])
        check_files_eq(srcfile, Files.output, Files.reference, "PROGRAM")
        check_bytes(Files.input, source)
        
    # top-down disassembler
    for srcfile, dopts, aopts in [
            ("gaops.gpl", ["-a", "0", "-f", "6"], []),
            ("gainst.gpl", ["-a", "0", "-f", "6"], []),
            ("gabranch.gpl", ["-a", "0", "-f", "5"], []),
            ("gamove.gpl", ["-a", "0", "-f", "6"], []),
            ("gafmt.gpl", ["-a", "0", "-f", "5", "-y", "rag"], ["-y", "rag"]),
            ("gadirs.gpl", ["-a", "0", "-f", "0"], []),
            ("gacopy.gpl", ["-a", ">2000", "-f", ">2000"], []),
            ("gaexts.gpl", ["-a", "0", "-f", "0x1e"], []),
            ("gapass.gpl", ["-a", "0x6030", "-f", ">6030"], [])
            ]:
        source = os.path.join(Dirs.gplsources, srcfile)
        xga(*[source] + aopts + ["-o", Files.reference])
        xdg(*[Files.reference] + dopts + ["-p", "-o", Files.input])
        xga(*[Files.input] + aopts + ["-o", Files.output])
        check_files_eq(srcfile, Files.output, Files.reference, "PROGRAM")
        if count_bytes(Files.output) > 0:
            error("BYTE", "Too many BYTE directives in result")

    # disassembler run
    for srcfile in ["dgruns.gpl"]:
        source = os.path.join(Dirs.gplsources, srcfile)
        xga(*[source] + ["-o", Files.reference])
        xdg(*[Files.reference] + ["-a", "0", "-r", "0x0", "-p", "-o", Files.input])
        xga(*[Files.input] + ["-o", Files.output])
        check_files_eq(srcfile, Files.output, Files.reference, "PROGRAM")
        check_bytes(Files.input, source)

    # disassemble blob
    binary = os.path.join(Dirs.refs, "blobg.bin")
    #TODO: universal character escape \x..
    #xdg(binary, "-a", "0", "-f", "start", "-p", "-o", Files.input)
    #xga(Files.input, "-o", Files.output)
    #check_files_eq("blobg", Files.output, binary, "PROGRAM")
    #xdg(binary, "-a", "0", "-r", "start", "-p", "-o", Files.input)
    #xga(Files.input, "-o", Files.output)
    #check_files_eq("blobg-run", Files.output, binary, "PROGRAM")

    # disassemble random
    randrange = [n for n in xrange(256) if n != 0x08 and n != 0xfb]
    for r in xrange(16):
        random.seed(r)
        binary = "".join([chr(random.choice(randrange)) for i in xrange(2048)])
        with open(Files.reference, "wb") as fref:
            fref.write(binary)
        xdg(Files.reference, "-a", "1000", "-f", "1000", "-p", "-o", Files.input)
        xga(Files.input, "-o", Files.output)
        check_files_eq("random" + str(r), Files.reference, Files.output, "PROGRAM")

    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
