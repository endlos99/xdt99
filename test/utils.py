import sys
import os
import re

from subprocess import call
from config import xdmPy, xhmPy, xvmPy, xasPy, xdaPy, xgaPy, xdgPy, xbasPy


# Utility functions

def chrw(word):
    return chr(word >> 8) + chr(word & 0xFF)


def ordw(word):
    return ord(word[0]) << 8 | ord(word[1])


def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip(">"), 16 if s[:2] == "0x" or s[:1] == ">" else 10)


# Test management functions

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


def xhm(*args, **kargs):
    """invoke HFE Manager"""
    print "HM:", args
    if kargs.get("shell"):
        rc = call(" ".join(xhmPy + list(args)), shell=True)
    else:
        rc = call(xhmPy + list(args),
                  stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xhm99 call returned with failure code " + str(rc))


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
    """invoke assembler"""
    print "AS:", args
    rc = call(xasPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xas99 call returned with failure code " + str(rc))


def xda(*args, **kargs):
    """invoke disassembler"""
    print "DA:", args
    rc = call(xdaPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xda99 call returned with failure code " + str(rc))


def xga(*args, **kargs):
    """invoke GPL assembler"""
    print "GA:", args
    rc = call(xgaPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xga99 call returned with failure code " + str(rc))


def xdg(*args, **kargs):
    """invoke GPL disssembler"""
    print "DG:", args
    rc = call(xdgPy + list(args),
              stdout=kargs.get("stdout"), stderr=kargs.get("stderr"))
    if rc != kargs.get("rc", 0):
        error("OS", "xdg99 call returned with failure code " + str(rc))


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


# Common check functions

def content(fn, mode="rb"):
    """return contents of file"""
    with open(fn, mode) as f:
        data = f.read()
    return data


def content_len(fn):
    """return length of file"""
    return os.path.getsize(fn)


def check_file_exists(fn):
    """check if given file exists"""
    return os.path.isfile(fn)


# Common check functions: xdm99

def check_files_eq(tid, infile, reffile, fmt, mask=None):
    if fmt[0] == "D":
        if "V" in fmt:
            check_text_files_eq(tid, infile, reffile)
        else:
            check_binary_files_eq(tid, infile, reffile, [])
    else:
        check_binary_files_eq(tid, infile, reffile, mask or [])


def check_text_files_eq(tid, infile, reffile):
    """check if file matches reference file"""
    with open(infile, "r") as fin, open(reffile, "r") as fref:
        if fin.readlines() != fref.readlines():
            error(tid, "%s: File contents mismatch" % infile)


def check_text_lines_eq(tid, infile, reffile, fmt):
    """check if text files are equal modulo trailing spaces"""
    reclen = int(re.search("\d+", fmt).group(0))
    with open(infile, "r") as fin, open(reffile, "r") as fref:
        reflines = [line[:-1] + " " * (reclen - len(line) + 1) + "\n"
                    for line in fref.readlines()]
        if fin.readlines() != reflines:
            error(tid, "%s: File contents mismatch" % infile)


def check_binary_files_eq(tid, infile, reffile, mask=()):
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


def check_file_matches(infile, matches):
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


# Common check functions: xas99

def check_obj_code_eq(infile, reffile):
    """check if object code files are equal modulo id tag"""
    with open(infile, "rb") as fin, open(reffile, "rb") as fref:
        indata = fin.read()
        inlines = [indata[i:i + 80] for i in xrange(0, len(indata), 80)]
        refdata = fref.read()
        reflines = [refdata[i:i + 80] for i in xrange(0, len(refdata), 80)]
        if inlines[:-1] != reflines[:-1]:
            error("Object code", "File contents mismatch")


def check_image_files_eq(genfile, reffile):
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


def check_list_files_eq(genfile, reffile, ignore_lino=False):
    """check if list files are equivalent"""
    with open(genfile, "r") as fg, open(reffile, "r") as fr:
        genlist = [(l[:16] + l[19:]).rstrip() for l in fg.readlines()
                   if l[:4] != "****"]
        reflist = [l[2:].rstrip() for l in fr.readlines() if l[:2] == "  "]
    gi, ri = 1, 0  # skip assembler header note
    min_col, max_col = 4 if ignore_lino else 0, 74
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
            gl = gl.replace("; ", "* ")  # unify comments
            # ignore list directives
            if "TITL" in gl[16:] or "PAGE" in gl[16:] or "UNL" in gl[16:] or "LIST" in gl[16:]:
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
        if gl[min_col:max_col] != rl[min_col:max_col]:
            error("List file", "Line mismatch in %d/%d" % (gi, ri))
        gi, ri = gi + 1, ri + 1


# common check functions: xda99/xdg99

def check_bytes(outfile, reffile):
    """check that outfile has not more data than reffile"""
    outbytes, cntbytes = count_bytes(outfile), count_bytes(reffile)
    if outbytes > cntbytes:
        error("BYTEs", "Too many BYTEs/DATAs: %d instead of %d" % (outbytes, cntbytes))


def count_bytes(fn):
    """count bytes declared by directives in source"""
    byte_count = 0
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
        if len(parts) > 2 and parts[1].lower() in ("byte", "data", "stri", "text"):
            # get all args
            args = [x.strip() for x in parts[2].split(",") if x.strip()]
            # know what you count
            if parts[1].lower() == "data":
                byte_count += len(args) * 2
            elif parts[1].lower() == "text":
                byte_count += sum([len(a) / 2 if a[0] == '>' else 1
                                   for a in args])
            elif parts[1].lower() == "stri":
                byte_count += sum([len(a) / 2 if a[0] == '>' else 1
                                   for a in args]) + 1  # len byte
            else:
                byte_count += len(args)
    return byte_count


def check_indent(fn, blocks):
    """check if first lines are indented correctly"""
    with open(fn, "r") as fin:
        source = fin.readlines()
    indents = []
    for line in source:
        if not line:
            continue
        if line[0] == ' ':
            indents.append(re.match(r"\s+(\w)", line).start(1))
        else:
            try:
                indents.append(
                    re.match(r"(?:[\w?!~]+\s+){%d}(\w)" % blocks, line).start(
                        1))
            except AttributeError:
                pass
    if len(indents) < 3:
        error("indent", "Too few indent values: %d" % len(indents))
    return all([i == indents[0] for i in indents[1:]])


def count_mnemonics(fn, offset=0, wanted=None):
    """build dict of all ocurring mnemonics"""
    with open(fn, "r") as fin:
        source = [l[offset:] for l in fin.readlines()]
    mnems = {}
    for line in source:
        parts = re.split(r"\s+", line.rstrip(), maxsplit=2)
        if len(parts) < 2:
            continue
        mnem = parts[1].lower()
        if wanted is not None and wanted != mnem:
            continue
        n = mnems.setdefault(mnem, 0)
        mnems[parts[1].lower()] = n + 1
    return mnems.get(wanted, 0) if wanted is not None else mnems


def check_source(outfile, reffile):
    """compare sources"""
    with open(outfile, "r") as fout, open(reffile, "r") as fref:
        out = fout.readlines()
        ref = fref.readlines()
    j = -1
    for i, oline in enumerate(out):
        # split output instruction (generated source)
        oinstr = re.split(r"\s+", re.sub(";.*$", "", oline.rstrip()).lower(),
                          2)
        if len(oinstr) < 2 or oinstr[1] == "equ":
            continue  # no instruction
        oargs = [a.strip().upper() for a in oinstr[2].split(",")] if len(
            oinstr) > 2 else []
        rline, rinstr, urargs = "", (), ()
        while True:
            j += 1
            rline = re.sub(";.*$", "", ref[j]).rstrip()
            if rline[:1] == '*':
                continue  # ignore comments
            if "IGNORE" in rline:
                break  # don't compare two corresponding lines
            # split reference instruction (original source)
            rinstr = re.split(r"\s+", rline.lower(), 2)
            rargs = [a.strip().upper() for a in rinstr[2].split(",")] if len(
                rinstr) > 2 else []
            # uniform numerical arguments >XXXX, except if they're
            # already >XX (for xdg99)
            urargs = [(">%04X" % xint(a)) if (a[0] == '>' and len(
                a) != 3) or a.isdigit() else a
                      for a in rargs]
            if rline and rinstr[0][-1:] != ":" and rinstr[1] != "equ":
                break
        if "IGNORE" not in rline and (
                oinstr[1] != rinstr[1] or oargs != urargs):
            error("source", "Mismatch in line %d:\n(R) %s\n(O) %s" % (
                i, rline, oline))


def check_origins(fn, origins):
    """check origins in source"""
    with open(fn, "r") as fin:
        source = fin.readlines()
    ocnt = 0
    for line in source:
        m = re.match(r"^(\w+)\s[^;]*; <-(.*)$", line)
        if m:
            addr = int(m.group(1), 16)
            anns = [int(a.strip()[1:], 16) for a in m.group(2).split(",")]
            if addr in origins:
                if origins[addr] == anns:
                    ocnt += 1
                else:
                    error("origin", "Origin mismatch @%04X" % addr)
    if ocnt != len(origins):
        error("origin", "Origin count mismatch: %d/%d" % (ocnt, len(origins)))


def read_stderr(fn, include_warnings=False):
    """read stderr output"""
    errors, lino = {}, "----"
    with open(fn, "r") as f:
        for line in f:
            if "Warning:" in line:
                if include_warnings:
                    warn = re.search(r"<\d>\s+(\d+)\s+-\s+Warning:\s+(.*)", line)
                    if warn:
                        errors[warn.group(1)] = warn.group(2)
                else:
                    continue  # ignore warnings
            err = re.match(r">[ \w.]+<\d>\s+(\d+)", line)
            if err:
                lino = err.group(1)
            else:
                errors[lino] = line[6:].strip()
    return errors


def get_source_markers(source, tag):
    ref_errors = {}
    with open(source, "r") as f:
        for i, line in enumerate(f):
            m = re.search(tag, line)
            if m:
                try:
                    if m.group(1):
                        ref_errors[m.group(1)[1:]] = line
                        continue
                except IndexError:
                    pass
                ref_errors["%04d" % (i + 1)] = line
    return ref_errors


def check_errors(ref, actual):
    """compare two dicts for key equality"""
    for err in ref:
        if err not in actual:
            error("Error messages",
                  "Missing error: " + str(err) + ": " + ref[err])
    for err in actual:
        if err not in ref:
            error("Error messages",
                  "Extraneous error: " + str(err) + ": " + actual[err])


# common check functions xga99

def check_gbc_files_eq(name, genfile, reffile):
    """check if non-zero bytes in binary files are equal"""
    with open(genfile, "rb") as fgen, open(reffile, "rb") as fref:
        genimage = fgen.read()
        refimage = fref.read()[6:]
    if genimage != refimage and genimage != refimage[:-1]:
        error("GPL image", "Image mismatch: " + name)
