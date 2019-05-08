#!/usr/bin/env python

import os
import re

from config import Dirs, Disks, Files
from utils import xas, xdm, error, read_stderr, get_source_markers, check_errors


# Main test

def runtest():
    """check error messages against native assembler listing"""

    # cross-assembler error messages
    source = os.path.join(Dirs.sources, "aserrs.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-s", "-o", Files.output, stderr=ferr, rc=1)
    xas_errors = read_stderr(Files.error)

    # TI assembler error messages
    ti_errors = {}
    xdm(Disks.asmsrcs, "-e", "ASERRS-L", "-o", Files.reference)
    with open(Files.reference, "r") as f:
        for line in f:
            err = re.match(r"\*{5}\s+([A-Z ]*) - (\d+)", line)
            if err:
                lino, err_msg = err.group(2), err.group(1)
                ti_errors[lino] = err_msg

    # compare
    check_errors(ti_errors, xas_errors)

    # xdt99-specific errors
    source = os.path.join(Dirs.sources, "asxerrs.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-R", "-o", Files.output, stderr=ferr, rc=1)
    xas_errors = read_stderr(Files.error)
    ref_errors = get_source_markers(source, r";ERROR(:....)?")
    check_errors(ref_errors, xas_errors)

    # xdt99-specific errors (image generation)
    source = os.path.join(Dirs.sources, "asxerrsb.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-R", "-b", "-o", Files.output, stderr=ferr, rc=1)
    xas_errors = read_stderr(Files.error)
    ref_errors = get_source_markers(source, tag=r";ERROR(:....)?")
    check_errors(ref_errors, xas_errors)

    # files not found
    source = os.path.join(Dirs.sources, "ascopyi.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-o", Files.output, stderr=ferr, rc=1)

    # warnings
    source = os.path.join(Dirs.sources, "aswarn.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=0)  # no error
    act_errors = read_stderr(Files.error, include_warnings=True)
    exp_errors = get_source_markers(source, tag=r";WARN")
    check_errors(exp_errors, act_errors)

    source = os.path.join(Dirs.sources, "asuusym.asm")  # undefined symbols
    with open(Files.error, "w") as ferr:
        xas(source, "-R", "-o", Files.output, stderr=ferr, rc=0)  # no error
    with open(Files.error, "r") as fin:
        output = fin.read()
    if output.strip()[-14:] != "U1 U2 U3 U4 U5":
        error("stdout", "Bad list of unreferenced symbols")

    with open(Files.error, "w") as ferr:
        xas(source, "-R", "-w", "-o", Files.output, stderr=ferr, rc=0)  # no error
    with open(Files.error, "r") as fin:
        output = fin.read()
    if output.strip():
        error("stdout", "Unwanted  list of unreferenced symbols")

    # STDOUT
    source = os.path.join(Dirs.sources, "asstdout.asm")
    with open(Files.error, "w") as fout:
        xas(source, "-b", "-R", "-o", Files.output, stdout=fout, rc=0)  # no error
    with open(Files.error, "r") as fin:
        output = fin.read()
    if output.strip() != "hello 42 world!":
        error("stdout", "Invalid STDOUT output: " + output)

    # cleanup
    os.remove(Files.error)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print "OK"
