#!/usr/bin/env python

import os
import re

from config import Dirs, Files
from utils import (xdg, xga, error, checkIndent, countMnemonics, checkSource,
                   checkOrigins)


### Check function

def checkBytes(outfile, reffile):
    """check that outfile has not more data than reffile"""
    outbytes, cntbytes = countBytes(outfile), countBytes(reffile)
    if outbytes > cntbytes:
        error("BYTEs", "Too many BYTEs/DATAs: %d instead of %d" % (
            outbytes, cntbytes))


def countBytes(fn):
    """count bytes declared by directives in source"""
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
            elif parts[1].lower() == "text":
                bytecnt += sum([len(a) / 2 if a[0] == '>' else 1
                                for a in args])
            elif parts[1].lower() == "stri":
                bytecnt += sum([len(a) / 2 if a[0] == '>' else 1
                                for a in args]) + 1  # len byte
            else:
                bytecnt += len(args)
    return bytecnt
    

def checkSyntax(fn, syntaxname):
    """check if source has no foreign syntax elements"""
    syntax = {
        "rag": ("TITLE", "I/O", "ROW+", "COL+", "HTEXT", "VTEXT", "HCHAR",
                "HMOVE", "VCHAR", "BIAS"),
        "ryte": ("TITLE", "HTEXT", "VTEXT", "HCHAR", "HMOVE", "VCHAR", "BIAS"),
        "mizapf": ("HCHAR", "VCHAR", "HTEXT", "VTEXT", "ROW+", "COL+", "END")
        }[syntaxname]
    mnems = countMnemonics(fn)
    for m in mnems:
        if m == "move" or m == "for":  # same mnem, but different args
            continue
        if m in syntax:
            error("syntax", "invalid menmonic " + m)

            
def checkMove(fn, syntaxname):
    """ check syntax variant for MOVE instruction"""
    movestmt = ("GROM>0000AORG>0000" +
                "MOVE>1234BYTESFROMGROM@>6800TOVDP*>8302" +
                "MOVE@>8300(@>03)BYTESFROMGROM@>8304(@>01)TOVREG0"
                if syntaxname == "mizapf" else
                "GROM>0000AORG>0000" +
                "MOVE>1234,G@>6800,V*>8302" +
                "MOVE@>8300(@>03),G@>8304(@>01),#0")
    with open(fn, "r") as f:
        data = "".join([l[9:] for l in f.readlines()])
    ref = re.sub(r"\s+", "", data)  # eliminate white space
    if ref != movestmt:
        error("MOVE syntax", "MOVE syntax mismatch")


### Main test

def runtest():
    """check disassembly"""

    # source with sym file
    source = os.path.join(Dirs.gplsources, "dgsource.gpl")
    xga(source, "-o", Files.reference, "-E", Files.input)
    xdg(Files.reference, "-a", "2000", "-f", ">2000", "-p", "-S", Files.input,
        "-o", Files.output)
    checkSource(Files.output, source)

    # from/to
    source = os.path.join(Dirs.gplsources, "dgexclude.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "0", "-f", "0x3", "-t", "0xa", "-p",
        "-o", Files.output)
    bytecnt = countBytes(Files.output)
    if bytecnt != 13:
        error("from/to", "BYTE count mismatch: %d" % bytecnt)
    
    # exclude
    source = os.path.join(Dirs.gplsources, "dgexclude.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "0", "-r", "0x0", "-e", "2-4", "10-14", "-p",
        "-o", Files.output)
    bytecnt = countBytes(Files.output)
    if bytecnt != 6:
        error("exclude", "BYTE count mismatch: %d" % bytecnt)

    # syntax
    source = os.path.join(Dirs.gplsources, "dgsyntax.gpl")
    xga(source, "-o", Files.reference)
    for syntax in "rag", "ryte", "mizapf":
        xdg(Files.reference, "-a", "0", "-f", "0", "-s", syntax,
            "-o", Files.output)
        checkSyntax(Files.output, syntax)

    # syntax MOVE
    source = os.path.join(Dirs.gplsources, "dgsynmove.gpl")
    xga(*[source] + ["-o", Files.reference])
    for syntax in "xdt99", "rag", "ryte", "mizapf":
        xdg(Files.reference, "-a", "0", "-f", "0", "-s", syntax,
            "-o", Files.output)
        checkMove(Files.output, syntax)

    # "start"
    source = os.path.join(Dirs.gplsources, "dgstart.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "6000", "-f", "start", "-o", Files.output)
    m1 = sum(countMnemonics(Files.output, offset=9).values())
    if m1 != 6:
        error("start", "mnemonic count mismatch: %d/6" % m1)
    xdg(Files.reference, "-a", "6000", "-r", "start", "-o", Files.output)
    m2 = sum(countMnemonics(Files.output, offset=9).values())
    if m2 != 6:
        error("start", "mnemonic count mismatch: %d/6" % m2)

    # origins
    source = os.path.join(Dirs.gplsources, "dgjumps.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "0", "-r", "0", "-o", Files.output)
    checkOrigins(Files.output, {
        0x0: [0x12, 0x25],
        0x1a: [0xd, 0x20],
        0x28: [0x8, 0x22]})

    # strings
    source = os.path.join(Dirs.gplsources, "dgtext.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "8000", "-r", "8000", "-n", "-p",
        "-o", Files.output)
    mnems = countMnemonics(Files.output)
    if mnems.get("byte") != 8:
        error("strings", "BYTE count mismatch: %d" % bytes)
    if mnems.get("text") != 2:
        error("strings", "TEXT count mismatch: %d" % bytes)
        
    # force
    source = os.path.join(Dirs.gplsources, "dgforce.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "a000", "-r", "a000", "-o", Files.output)
    n = sum(countMnemonics(Files.output, offset=9).values())
    if n != 7:
        error("force", "Mnemonics count mismatch: %d != 7" % n)
    xdg(Files.reference, "-a", "a000", "-r", "a000", "-F", "-o", Files.output)
    nf = sum(countMnemonics(Files.output, offset=9).values())
    if nf != 8:
        error("force", "Mnemonics count mismatch: %d != 8" % nf)

    # layout
    source = os.path.join(Dirs.gplsources, "dgstart.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "6000", "-f", "start", "-o", Files.output)
    checkIndent(Files.output, 2)
    xdg(Files.reference, "-a", "6000", "-f", "start", "-p", "-o", Files.output)
    checkIndent(Files.output, 1)
        
    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
