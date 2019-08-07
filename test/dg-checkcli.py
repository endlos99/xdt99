#!/usr/bin/env python

import os
import re

from config import Dirs, Files
from utils import (xdg, xga, error, check_indent, count_mnemonics, check_source, check_origins,
                   count_bytes, check_ellipsis)


# Check function

def check_syntax(fn, syntax_name):
    """check if source has no foreign syntax elements"""
    syntax = {
        "rag": ("TITLE", "I/O", "ROW+", "COL+", "HTEXT", "VTEXT", "HCHAR", "HMOVE", "VCHAR", "BIAS"),
        "ryte": ("TITLE", "HTEXT", "VTEXT", "HCHAR", "HMOVE", "VCHAR", "BIAS"),
        "mizapf": ("HCHAR", "VCHAR", "HTEXT", "VTEXT", "ROW+", "COL+", "END")
        }[syntax_name]
    mnemonics = count_mnemonics(fn)
    for m in mnemonics:
        if m == "move" or m == "for":  # same mnemonic, but different args
            continue
        if m in syntax:
            error("syntax", "invalid menmonic " + m)

            
def check_move(fn, syntax_name):
    """ check syntax variant for MOVE instruction"""
    move_stmt = ("grom>0000aorg>0000" +
                 "move>1234bytesfromgrom@>6800tovdp*>8302" +
                 "move@>8300(@>03)bytesfromgrom@>8304(@>01)tovreg0"
                 if syntax_name == "mizapf" else
                 "grom>0000aorg>0000" +
                 "move>1234,g@>6800,v*>8302" +
                 "move@>8300(@>03),g@>8304(@>01),#0")
    with open(fn, "r") as f:
        data = "".join([l[9:] for l in f.readlines()])
    ref = re.sub(r"\s+", "", data)  # eliminate white space
    if ref != move_stmt:
        error("MOVE syntax", "MOVE syntax mismatch")


# Main test

def runtest():
    """check disassembly"""

    # source with sym file
    source = os.path.join(Dirs.gplsources, "dgsource.gpl")
    xga(source, "-o", Files.reference, "-E", Files.input)
    xdg(Files.reference, "-a", "2000", "-f", ">2000", "-p", "-S", Files.input, "-o", Files.output)
    check_source(Files.output, source)

    # from/to
    source = os.path.join(Dirs.gplsources, "dgexclude.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "0", "-f", "0x3", "-t", "0xa", "-p",
        "-o", Files.output)
    byte_count = count_bytes(Files.output)
    if byte_count != 13:
        error("from/to", "BYTE count mismatch: %d" % byte_count)
    
    # exclude
    source = os.path.join(Dirs.gplsources, "dgexclude.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "0", "-r", "0x0", "-e", "2-4", "10-14", "-p",
        "-o", Files.output)
    byte_count = count_bytes(Files.output)
    if byte_count != 6:
        error("exclude", "BYTE count mismatch: %d" % byte_count)

    # syntax
    source = os.path.join(Dirs.gplsources, "dgsyntax.gpl")
    xga(source, "-o", Files.reference)
    for syntax in "rag", "ryte", "mizapf":
        xdg(Files.reference, "-a", "0", "-f", "0", "-y", syntax,
            "-o", Files.output)
        check_syntax(Files.output, syntax)

    # syntax MOVE
    source = os.path.join(Dirs.gplsources, "dgsynmove.gpl")
    xga(*[source] + ["-o", Files.reference])
    for syntax in "xdt99", "rag", "ryte", "mizapf":
        xdg(Files.reference, "-a", "0", "-f", "0", "-y", syntax, "-o", Files.output)
        check_move(Files.output, syntax)

    # "start"
    source = os.path.join(Dirs.gplsources, "dgstart.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "6000", "-f", "start", "-o", Files.output)
    memn_count_1 = sum(count_mnemonics(Files.output, offset=9).values())
    if memn_count_1 != 6:
        error("start", "mnemonic count mismatch: %d/6" % memn_count_1)
    xdg(Files.reference, "-a", "6000", "-r", "start", "-o", Files.output)
    mnem_count_2 = sum(count_mnemonics(Files.output, offset=9).values())
    if mnem_count_2 != 6:
        error("start", "mnemonic count mismatch: %d/6" % mnem_count_2)

    # origins
    source = os.path.join(Dirs.gplsources, "dgjumps.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "0", "-r", "0", "-o", Files.output)
    check_origins(Files.output, {
        0x0: [0x12, 0x25],
        0x1a: [0xd, 0x20],
        0x28: [0x8, 0x22]})

    # strings
    source = os.path.join(Dirs.gplsources, "dgtext.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "8000", "-r", "8000", "-n", "-p", "-o", Files.output)
    mnems = count_mnemonics(Files.output)
    if mnems.get("byte") != 8:
        error("strings", "BYTE count mismatch: %d" % bytes)
    if mnems.get("text") != 2:
        error("strings", "TEXT count mismatch: %d" % bytes)
        
    # force
    source = os.path.join(Dirs.gplsources, "dgforce.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "a000", "-r", "a000", "-o", Files.output)
    n = sum(count_mnemonics(Files.output, offset=9).values())
    if n != 7:
        error("force", "Mnemonics count mismatch: %d != 7" % n)
    xdg(Files.reference, "-a", "a000", "-r", "a000", "-F", "-o", Files.output)
    nf = sum(count_mnemonics(Files.output, offset=9).values())
    if nf != 8:
        error("force", "Mnemonics count mismatch: %d != 8" % nf)

    # skip -k
    source = os.path.join(Dirs.gplsources, "dgsource.gpl")
    xga(source, "-o", Files.output, "-E", Files.input)
    with open(Files.output, "rb") as fin, open(Files.reference, "wb") as fout:
        data = fin.read()
        fout.write(b"\x99" * 0x999)
        fout.write(data)
    xdg(Files.reference, "-a", "2000", "-f", ">2000", "-k", "999", "-p", "-S", Files.input, "-o", Files.output)
    check_source(Files.output, source)

    # strict -s
    source = os.path.join(Dirs.gplsources, "dgsource.gpl")
    xga(source, "-o", Files.reference, "-E", Files.input)
    xdg(Files.reference, "-a", "2000", "-f", ">2000", "-p", "-S", Files.input, "-o", Files.output)
    with open(Files.output, "r") as fin:
        for line in fin.readlines():
            line = re.sub(r"'[^']*'", "", line)  # escape literal
            if line != line.lower():
                error("strict", "Source file not entirely lower case: %s" % line)

    xdg(Files.reference, "-a", "2000", "-f", ">2000", "-p", "-s", "-S", Files.input, "-o", Files.output)
    with open(Files.output, "r") as fin:
        for line in fin.readlines():
            if line != line.upper():
                error("strict", "Source file not entirely upper case: %s" % line)

    # concise -c
    source = os.path.join(Dirs.gplsources, "dgconcis.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "4000", "-r", "4000", "-s", "-c", "-o", Files.output)
    check_ellipsis(Files.output, skip=2)
    # no condensed output when disassembling as program (-p)

    # layout
    source = os.path.join(Dirs.gplsources, "dgstart.gpl")
    xga(source, "-o", Files.reference)
    xdg(Files.reference, "-a", "6000", "-f", "start", "-o", Files.output)
    check_indent(Files.output, 2)
    xdg(Files.reference, "-a", "6000", "-f", "start", "-p", "-o", Files.output)
    check_indent(Files.output, 1)
        
    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print("OK")
