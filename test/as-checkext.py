#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import (xas, xdm, check_obj_code_eq, check_binary_files_eq, read_stderr, check_errors,
                   get_source_markers, error)


# Check functions

def check_concat_eq(infiles, reffile):
    data = ""
    for fn in infiles:
        with open(fn, "rb") as f:
            data += f.read()
    with open(reffile, "rb") as f:
        ref = f.read()
    if data != ref:
        error("Files", "Incorrect binary data")


def check_no_files(files):
    for fn in files:
        if os.path.isfile(fn):
            error("Files", "Extraneous file " + fn)


def check_file_sizes(files):
    for fn, fs in files:
        size = None
        with open(fn, "rb") as f:
            size = len(f.read())
        if fs != size:
            error("Files", "Incorrect file size " + fn + ": " + str(size))


def check_numeric_eq(output, ref):
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


# Main test

def runtest():
    """check xdt99 extensions"""

    # xdt99 extensions
    source = os.path.join(Dirs.sources, "asxext.asm")
    xas(source, "-R", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT0-O", "-o", Files.reference)
    check_obj_code_eq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT1-O", "-o", Files.reference)
    check_obj_code_eq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2=2", "sym3=2", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT2-O", "-o", Files.reference)
    check_obj_code_eq(Files.output, Files.reference)
    xas(source, "-R", "-D", "sym2=2,sym3=2", "-o", Files.output)
    xdm(Disks.asmsrcs, "-e", "ASXEXT2-O", "-o", Files.reference)
    check_obj_code_eq(Files.output, Files.reference)

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
        check_obj_code_eq(Files.output, Files.reference)

    # SAVE directive
    source = os.path.join(Dirs.sources, "asxsave.asm")
    xas(source, "-b", "--base", "0xb000", "-o", Files.output)
    save1s = [Files.output + "_" + ext
              for ext in ["b000", "b020", "b030"]]
    check_concat_eq(save1s, os.path.join(Dirs.refs, "save1"))
    check_no_files([Files.output + "_b080"])

    # bank switching: obsolete AORG addr, bank
    source = os.path.join(Dirs.sources, "asxbank1.asm")
    xas(source, "-b", "-o", Files.output)
    save2s =[Files.output + "_" + ext
              for ext in ["0000", "6000_b0", "6000_b1", "6100_b0", "6200_b1",
                          "6200_b2"]]
    check_concat_eq(save2s, os.path.join(Dirs.refs, "save2"))
    check_no_files([Files.output + "_0000_b0", Files.output + "_6100_b1"])

    source = os.path.join(Dirs.sources, "asxbank2.asm")
    xas(source, "-b", "-o", Files.output)
    save3s = [Files.output + "_" + ext
              for ext in ["c000_b0", "c000_b1", "d000_b0", "e000_b1"]]
    check_concat_eq(save3s, os.path.join(Dirs.refs, "save3"))
    check_no_files([Files.output + "_" + ext
                    for ext in ["c000", "d000", "d000_b1", "e000", "e000_b0"]])

    source = os.path.join(Dirs.sources, "asxsegm.asm")
    xas(source, "-b", "-o", Files.output)
    check_file_sizes([(Files.output + "_" + ext, size)
                      for ext, size in [("0000", 20), ("b000_b1", 14),
                                      ("b010_b1", 2), ("b012_b2", 6)]])

    # BANK directive
    source = os.path.join(Dirs.sources, "asdbank.asm")
    xas(source, "-b", "-R", "-o", Files.output)
    save4s = [Files.output + ext for ext in ["_6000_b0", "_6000_b1"]]
    check_concat_eq(save4s, os.path.join(Dirs.refs, "asdbank"))

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
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, r";ERROR(:....)?")
    check_errors(exp_errors, act_errors)

    source = os.path.join(Dirs.sources, "asshbankx.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=0)  # no error

    # data output (-t)
    source = os.path.join(Dirs.sources, "ashexdat.asm")
    xas(source, "-t", "a2", "-R", "-o", Files.output)
    xas(source, "-b", "-R", "-o", Files.reference)
    check_numeric_eq(Files.output, Files.reference)

    source = os.path.join(Dirs.sources, "asxtext.asm")
    xas(source, "-t", "a2", "-o", Files.output + "1")
    xas(source, "-t", "c4", "-o", Files.output + "2")
    xas(source, "-t", "b", "-o", Files.output + "3")
    xas(source, "-t", "a4", "-o", Files.output + "4")
    xas(source, "-t", "c", "-o", Files.output + "5")
    save5s = [Files.output + ext
              for ext in ["1", "2", "3", "4", "5"]]
    check_concat_eq(save5s, os.path.join(Dirs.refs, "asxtext"))

    # auto-generated constants (b#, w#)
    source = os.path.join(Dirs.sources, "asautogen.asm")
    xas(source, "-b", "-R", "-o", Files.output)
    source = os.path.join(Dirs.sources, "asautoman.asm")
    xas(source, "-b", "-R", "-o", Files.reference)
    check_binary_files_eq("autogen", Files.output, Files.reference)

    source = os.path.join(Dirs.sources, "asautorel.asm")
    xas(source, "-b", "-R", "-o", Files.output)  # address is now >00xx instead of >a0xx
    with open(Files.reference, "rb+") as f:
        data = f.read()
        data = data.replace("\xa0", "\x00")
        f.seek(0)
        f.write(data)
    check_binary_files_eq("autogen", Files.output, Files.reference)

    # register LSB access (l#)
    source = os.path.join(Dirs.sources, "asxrlb.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=0)
    ref = os.path.join(Dirs.sources, "asxrlbn.asm")
    xas(ref, "-b", "-R", "-o", Files.reference)
    check_binary_files_eq("rlb", Files.output, Files.reference)

    act_errors = read_stderr(Files.error, include_warnings=True)
    exp_errors = get_source_markers(source, tag=r";WARN")
    check_errors(exp_errors, act_errors)

    # size modifier (s#)
    source = os.path.join(Dirs.sources, "assmod.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=0)
    ref = os.path.join(Dirs.sources, "assmodn.asm")
    xas(ref, "-b", "-R", "-o", Files.reference)
    check_binary_files_eq("s#", Files.output, Files.reference)
    with open(Files.error, "r") as ferr:
        if "TEXT4" not in ferr.read():
            error("s#", "Missing warning about TEXT4")

    source = os.path.join(Dirs.sources, "assmode.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-b", "-R", "-o", Files.output, stderr=ferr, rc=1)
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, tag=r";ERROR")
    check_errors(exp_errors, act_errors)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    for fn in set(save1s + save2s + save3s + save4s + save5s):
        os.remove(fn)


if __name__ == "__main__":
    runtest()
    print "OK"
