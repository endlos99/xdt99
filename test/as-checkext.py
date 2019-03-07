#!/usr/bin/env python

import os
import re

from config import Dirs, Disks, Files
from utils import xas, xdm, checkFileExists, checkObjCodeEq, readstderr,  compareErrors, error


def referrrors(source):
    referrors = {}
    with open(source, "r") as f:
        for i, line in enumerate(f):
            m = re.search(r";ERROR(:....)?", line)
            if m:
                if m.group(1):
                    referrors[m.group(1)[1:]] = line
                else:
                    referrors["%04d" % (i + 1)] = line
    return referrors


### Check functions

def checkConcatEq(infiles, reffile):
    data = ""
    for fn in infiles:
        with open(fn, "rb") as f:
            data += f.read()
    with open(reffile, "rb") as f:
        ref = f.read()
    if data != ref:
        error("Files", "Incorrect binary data")


def checkNoFiles(files):
    for fn in files:
        if os.path.isfile(fn):
            error("Files", "Extraneous file " + fn)


def checkFileSizes(files):
    for fn, fs in files:
        size = None
        with open(fn, "rb") as f:
            size = len(f.read())
        if fs != size:
            error("Files", "Incorrect file size " + fn + ": " + str(size))


def checkNumericalEqual(output, ref):
    idx = 0
    with open(output, "r") as fout, open(ref, "rb") as fref:
        data = fref.read()
        for l in fout:
            line = l.strip()
            if not line or line[0] == '*' or line[0] == ';':
                continue
            if line[:4].lower() != "byte":
                error("Files", "Bad format: " + l)
            toks = [x.strip() for x in line[4:].split(",")]
            vals = [int(x[1:], 16) if x[0] == ">" else int(x)
                    for x in toks]
            for v in vals:
                if chr(v) != data[idx]:
                    error("Files", "Unexpected data: %d/%d at %d" %
                          (v, ord(data[idx]), idx))
                idx += 1


### Main test

def runtest():
    """check xdt99 extensions"""

    # xdt99 extensions
    source = os.path.join(Dirs.sources, "asxext.asm")
    xas(source, "-R", "-f", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT0-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2", "-f", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT1-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2=2", "sym3=2", "-f", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT2-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2=2,sym3=2", "-f", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT2-O", "-o", Files.reference)
    checkObjCodeEq(Files.output, Files.reference)

    # some CLI options
    source = os.path.join(Dirs.sources, "ashello.asm")
    xas(source, "--embed", "-R", "-o", Files.output)

    # misc new features
    for infile, reffile in [
            ("asxnew.asm", "ASXNEW-O"),
            ("asmacs.asm", "ASMACS-O")
            ]:
        source = os.path.join(Dirs.sources, infile)
        xas(source, "-o", Files.output)
        xdm(Disks.asmsrcs, "-e", reffile, "-o", Files.reference)
        checkObjCodeEq(Files.output, Files.reference)

    # SAVE directive
    source = os.path.join(Dirs.sources, "asxsave.asm")
    xas(source, "-b", "--base", "0xb000", "-o", Files.output)
    save1s = [Files.output + "_" + ext
              for ext in ["b000", "b020", "b030"]]
    checkConcatEq(save1s, os.path.join(Dirs.refs, "save1"))
    checkNoFiles([Files.output + "_b080"])

    # bank switching: obsolete AORG addr, bank
    source = os.path.join(Dirs.sources, "asxbank1.asm")
    xas(source, "-b", "-o", Files.output)
    save2s =[Files.output + "_" + ext
              for ext in ["0000", "6000_b0", "6000_b1", "6100_b0", "6200_b1",
                          "6200_b2"]]
    checkConcatEq(save2s, os.path.join(Dirs.refs, "save2"))
    checkNoFiles([Files.output + "_0000_b0", Files.output + "_6100_b1"])

    source = os.path.join(Dirs.sources, "asxbank2.asm")
    xas(source, "-b", "-o", Files.output)
    save3s = [Files.output + "_" + ext
              for ext in ["c000_b0", "c000_b1", "d000_b0", "e000_b1"]]
    checkConcatEq(save3s, os.path.join(Dirs.refs, "save3"))
    checkNoFiles([Files.output + "_" + ext
                  for ext in ["c000", "d000", "d000_b1", "e000", "e000_b0"]])

    source = os.path.join(Dirs.sources, "asxsegm.asm")
    xas(source, "-b", "-o", Files.output)
    checkFileSizes([(Files.output + "_" + ext, size)
                    for ext, size in [("0000", 20), ("b000_b1", 14),
                                      ("b010_b1", 2), ("b012_b2", 6)]])

    # BANK directive
    source = os.path.join(Dirs.sources, "asdbank.asm")
    xas(source, "-b", "-R", "-o", Files.output)
    save4s = [Files.output + ext for ext in ["_6000_b0", "_6000_b1"]]
    checkConcatEq(save4s, os.path.join(Dirs.refs, "asdbank"))

    # cross-bank access
    source = os.path.join(Dirs.sources, "asxbank.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=0)  # no error

    source = os.path.join(Dirs.sources, "asnxbank.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=1)  # with errors

    # sections shared across banks
    source = os.path.join(Dirs.sources, "asshbank.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=1)  # with errors
    act_errors = readstderr(Files.error)
    exp_errors = referrrors(source)
    compareErrors(exp_errors, act_errors)

    source = os.path.join(Dirs.sources, "asshbankx.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=0)  # no error

    # data output (-t)
    source = os.path.join(Dirs.sources, "ashexdat.asm")
    xas(source, "-t", "a2", "-R", "-o", Files.output)
    xas(source, "-b", "-R", "-o", Files.reference)
    checkNumericalEqual(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, "asxtext.asm")
    xas(source, "-t", "a2", "-o", Files.output + "1")
    xas(source, "-t", "c4", "-o", Files.output + "2")
    xas(source, "-t", "b", "-o", Files.output + "3")
    xas(source, "-t", "a4", "-o", Files.output + "4")
    xas(source, "-t", "c", "-o", Files.output + "5")
    save5s = [Files.output + ext
              for ext in ["1", "2", "3", "4", "5"]]
    checkConcatEq(save5s, os.path.join(Dirs.refs, "asxtext"))

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    for fn in set(save1s + save2s + save3s + save4s + save5s):
        os.remove(fn)


if __name__ == "__main__":
    runtest()
    print "OK"
