import sys
import re

from subprocess import call
from config import xdmPy, xvmPy, xasPy, xgaPy


### Utility functions

def chrw(word):
    """word chr"""
    return chr(word >> 8) + chr(word & 0xFF)


### Test management functions

def xdm(*args, **kargs):
    """invoke Disk Manager"""
    print "DM:", args
    rc = call(xdmPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xdm99 call returned with failure code " + str(rc))


def xvm(*args, **kargs):
    """invoke Volume Manager"""
    print "VM:", args
    rc = call(xvmPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xvm99 call returned with failure code " + str(rc))


def xas(*args, **kargs):
    """invoke Assembler"""
    print "AS:", args
    rc = call(xasPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xas99 call returned with failure code " + str(rc))


def xga(*args, **kargs):
    """invoke Assembler"""
    print "GA:", args
    rc = call(xgaPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xga99 call returned with failure code " + str(rc))


def error(tid, msg):
    """report test error"""
    sys.exit("ERROR: " + tid + ": " + msg)


### Common check functions

def checkFilesEq(tid, infile, reffile, fmt, mask=None):
    if fmt[0] == "D":
        if "V" in fmt:
            checkTextFilesEq(tid, infile, reffile)
        else:
            checkTextLinesEq(tid, infile, reffile, fmt)
    else:
        checkBinaryFilesEq(tid, infile, reffile, mask or [])


def checkTextFilesEq(tid, infile, reffile):
    """check if file matches reference file"""
    with open(infile, "r") as fin, open(reffile, "r") as fref:
        if fin.readlines() != fref.readlines():
            error(tid, "%s: File contents mismatch" % infile)


def checkTextLinesEq(tid, infile, reffile, fmt):
    """check if text files are equal modulo trailing spaces"""
    reclen = int(re.search("\d+", fmt).group(0))
    with open(infile, "r") as fin, open(reffile, "r") as fref:
        reflines = [line[:-1] + " " * (reclen - len(line) + 1) + "\n"
                    for line in fref.readlines()]
        if fin.readlines() != reflines:
            error(tid, "%s: File contents mismatch" % infile)


def checkBinaryFilesEq(tid, infile, reffile, mask):
    """check if binary files are equal modulo mask"""
    with open(infile, "rb") as fin, open(reffile, "rb") as fref:
        indata = fin.read()
        refdata = fref.read()
        cutlen = 0
        for i, j in mask:
            assert cutlen <= i <= j
            indata = indata[:i - cutlen] + indata[j - cutlen:]
            refdata = refdata[:i - cutlen] + refdata[j - cutlen:]
            cutlen += j - i
        if indata != refdata:
            error(tid, "%s: File contents mismatch" % infile)
