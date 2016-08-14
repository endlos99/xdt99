import sys
import re

from subprocess import call
from config import xdmPy, xvmPy, xasPy, xgaPy, xbasPy


### Utility functions

def chrw(word):
    return chr(word >> 8) + chr(word & 0xFF)


def ordw(word):
    return ord(word[0]) << 8 | ord(word[1])


### Test management functions

def xdm(*args, **kargs):
    """invoke Disk Manager"""
    print "DM:", args
    if kargs.get("shell"):
        rc = call(" ".join(xdmPy + list(args)), shell=True)
    else:
        rc = call(xdmPy + list(args), stdin=kargs.get("stdin"),
                  stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xdm99 call returned with failure code " + str(rc))


def xvm(*args, **kargs):
    """invoke Volume Manager"""
    print "VM:", args
    if kargs.get("shell"):
        rc = call(" ".join(xvmPy + list(args)), shell=True)
    else:
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


def xbas(*args, **kargs):
    """invoke TI BASIC tool"""
    print "BAS:", args
    rc = call(xbasPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xbas99 call returned with failure code " + str(rc))


def error(tid, msg):
    """report test error"""
    sys.exit("ERROR: " + tid + ": " + msg)


### Common check functions: xdm99

def checkFilesEq(tid, infile, reffile, fmt, mask=None):
    if fmt[0] == "D":
        if "V" in fmt:
            checkTextFilesEq(tid, infile, reffile)
        else:
            #checkTextLinesEq(tid, infile, reffile, fmt)
            checkBinaryFilesEq(tid, infile, reffile, [])
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


def checkFileMatches(infile, matches):
    """check if text file contents match regular expressions"""
    try:
        with open(infile, "r") as f:
            contents = f.readlines()
    except IOError:
        error("CLI", "%s: File not found" % infile)
    for line, pattern in matches:
        try:
            if not re.search(pattern, contents[line]):
                error("CLI",
                      "%s: Line %d does not match" % (infile, line))
        except IndexError:
            error("CLI", "%s: Line %d missing" % (infile, line))


### Common check functions: xas99

def checkObjCodeEq(infile, reffile):
    """check if object code files are equal modulo id tag"""
    with open(infile, "rb") as fin, open(reffile, "rb") as fref:
        indata = fin.read()
        inlines = [indata[i:i + 80] for i in xrange(0, len(indata), 80)]
        refdata = fref.read()
        reflines = [refdata[i:i + 80] for i in xrange(0, len(refdata), 80)]
        if inlines[:-1] != reflines[:-1]:
            error("Object code", "File contents mismatch")


def checkImageFilesEq(genfile, reffile):
    """check if non-zero bytes in binary files are equal"""
    with open(genfile, "rb") as fg, open(reffile, "rb") as fr:
        genimage = fg.read()
        refimage = fr.read()
    if not 0 <= len(genimage) - len(refimage) <= 1:
        print len(genimage), len(refimage)
        error("Object code", "Image length mismatch")
    if (genimage[:2] != refimage[:2] or
        not (0 <= ordw(genimage[2:4]) - ordw(refimage[2:4]) <= 1) or
        genimage[4:6] != refimage[4:6]):
        error("Object code", "Image header mismatch")
    # TI-generated images may contain arbitrary bytes in BSS segments
    for i in xrange(4, len(refimage)):
        if genimage[i] != "\x00" and genimage[i] != refimage[i]:
            error("Image file", "Image contents mismatch @ " + hex(i))


def checkListFilesEq(genfile, reffile, ignoreLino=False):
    """check if list files are equivalent"""
    with open(genfile, "rb") as fg, open(reffile, "rb") as fr:
        genlist = [(l[:16] + l[19:]).rstrip() for l in fg.readlines()
                   if l[:4] != "****"]
        reflist = [l[2:].rstrip() for l in fr.readlines() if l[:2] == "  "]
    gi, ri = 1, 0
    mincol, maxcol = 4 if ignoreLino else 0, 74
    while gi < len(genlist):
        gl, rl = genlist[gi], reflist[ri]
        # ignore deliberate changes
        try:
            if gl[10] in ".X":
                rl = rl[:10] + gl[10:15] + rl[15:]  # no data
            if gl[14] == "r":
                rl = rl[:14] + "r" + rl[15:]
            if "ORG" in rl[16:] or "BES" in rl[16:]:
                rl = rl[:5] + gl[5:9] + rl[9:]  # no address
            # ignore list directives
            if ("TITL" in gl[16:] or "PAGE" in gl[16:] or "UNL" in gl[16:] or
                    "LIST" in gl[16:]):
                gi += 1
                continue
            # ignore BYTE sections
            if "BYTE" in gl[16:] and "BYTE" in rl[16:]:
                gi += 1
                while not genlist[gi][16:].rstrip():
                    gi += 1
                ri += 1
                while not reflist[ri][16:].rstrip():
                    ri += 1
                continue
        except IndexError:
            pass
        if gl[mincol:maxcol] != rl[mincol:maxcol]:
            error("List file", "Line mismatch in %d/%d" % (gi, ri))
        gi, ri = gi + 1, ri + 1
