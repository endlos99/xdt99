import sys
import os
import re

from subprocess import call
from config import xdm_py, xhm_py, xvm_py, xas_py, xda_py, xga_py, xdg_py, xbas_py, Dirs


# Utility functions

def r(filename):
    return os.path.join(Dirs.refs, filename)


def t(filename):
    return os.path.join(Dirs.tmp, filename)


def ordw(word):
    """word ord"""
    return (word[0] << 8) | word[1]


def chrw(word):
    """word chr"""
    return bytes((word >> 8, word & 0xff))


def chrws(*words):
    """word chr"""
    bs = []
    for word in words:
        bs.extend((word >> 8, word & 0xff))
    return bytes(bs)


def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip('>'), 16 if s[:2] == '0x' or s[:1] == '>' else 10)


def sinc(s, i):
    """return string increased by i"""
    return s[:-1] + chr(ord(s[-1]) + i)


# Test management functions

def xdm(*args, **kargs):
    """invoke Disk Manager"""
    print('DM:', args)
    if kargs.get('shell'):
        rc = call(' '.join(xdm_py + list(args)), shell=True)
    else:
        rc = call(xdm_py + list(args), stdin=kargs.get('stdin'),
                  stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xdm99 call returned with failure code ' + str(rc))


def xhm(*args, **kargs):
    """invoke HFE Manager"""
    print('HM:', args)
    if kargs.get('shell'):
        rc = call(' '.join(xhm_py + list(args)), shell=True)
    else:
        rc = call(xhm_py + list(args),
                  stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xhm99 call returned with failure code ' + str(rc))


def xvm(*args, **kargs):
    """invoke Volume Manager"""
    print('VM:', args)
    if kargs.get('shell'):
        rc = call(' '.join(xvm_py + list(args)), shell=True)
    else:
        rc = call(xvm_py + list(args),
                  stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xvm99 call returned with failure code ' + str(rc))


def xas(*args, **kargs):
    """invoke assembler"""
    print('AS:', args)
    rc = call(xas_py + list(args),
              stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xas99 call returned with failure code ' + str(rc))


def xda(*args, **kargs):
    """invoke disassembler"""
    print('DA:', args)
    rc = call(xda_py + list(args),
              stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xda99 call returned with failure code ' + str(rc))


def xga(*args, **kargs):
    """invoke GPL assembler"""
    print('GA:', args)
    rc = call(xga_py + list(args),
              stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xga99 call returned with failure code ' + str(rc))


def xdg(*args, **kargs):
    """invoke GPL disssembler"""
    print('DG:', args)
    rc = call(xdg_py + list(args),
              stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xdg99 call returned with failure code ' + str(rc))


def xbas(*args, **kargs):
    """invoke TI BASIC tool"""
    print('BAS:', args)
    rc = call(xbas_py + list(args),
              stdout=kargs.get('stdout'), stderr=kargs.get('stderr'))
    if rc != kargs.get('rc', 0):
        error('OS', 'xbas99 call returned with failure code ' + str(rc))


def error(tid, msg):
    """report test error"""
    sys.exit('ERROR: ' + tid + ': ' + msg)


def clear_env(var):
    """clear specific config from environment"""
    try:
        del os.environ[var]
    except KeyError:
        pass


def delfile(*filenames):
    """delete files or directories, if exist"""
    for filename in filenames:
        if os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            for filename_ in os.listdir(filename):
                os.remove(os.path.join(filename, filename_))


# Common check functions

def content(fn, mode='rb'):
    """return contents of file"""
    with open(fn, mode) as f:
        data = f.read()
    return data


def content_lines(fn, skip=0):
    """return lines of file"""
    with open(fn, 'r') as f:
        lines = f.readlines()
    return ' '.join(lines[skip:])


def content_cat(fn):
    """return lines of file"""
    with open(fn, 'r') as f:
        lines = ' '.join(line[:-1] for line in f)
    return lines


def content_line_array(fn):
    """return lines of file"""
    with open(fn, 'r') as f:
        lines = f.readlines()
    return lines


def content_len(fn):
    """return length of file"""
    try:
        return os.path.getsize(fn)
    except FileNotFoundError:
        return -1


def check_file_exists(fn):
    """check if given file exists"""
    return os.path.isfile(fn)


def check_file_empty(fn):
    """return if file is empty"""
    return os.path.getsize(fn) == 0


def concat(flist, out):
    """concatenate file contents"""
    with open(out, 'wb') as fout:
        for fn in flist:
            with open(fn, 'rb') as fin:
                data = fin.read()
                fout.write(data)


# Common check functions: xdm99

def check_files_eq(tid, infile, reffile, fmt, mask=None):
    if fmt[0] == 'D':
        if 'V' in fmt:
            check_text_files_eq(tid, infile, reffile)
        else:
            check_binary_files_eq(tid, infile, reffile, [])
    else:
        check_binary_files_eq(tid, infile, reffile, mask or [])


def check_text_files_eq(tid, infile, reffile, skip=0):
    """check if file matches reference file"""
    with open(infile, 'r') as fin, open(reffile, 'r') as fref:
        if fin.readlines()[skip:] != fref.readlines()[skip:]:
            error(tid, '%s: File contents mismatch' % infile)


def check_text_lines_eq(tid, infile, reffile, fmt):
    """check if text files are equal modulo trailing spaces"""
    reclen = int(re.search('\d+', fmt).group(0))
    with open(infile, 'r') as fin, open(reffile, 'r') as fref:
        reflines = [line[:-1] + ' ' * (reclen - len(line) + 1) + '\n'
                    for line in fref.readlines()]
        if fin.readlines() != reflines:
            error(tid, '%s: File contents mismatch' % infile)


def check_binary_files_eq(tid, infile, reffile, mask=()):
    """check if binary files are equal modulo mask"""
    with open(infile, 'rb') as fin, open(reffile, 'rb') as fref:
        indata = fin.read()
        refdata = fref.read()
        cutlen = 0
        for i, j in mask:
            assert cutlen <= i <= j
            indata = indata[:i - cutlen] + indata[j - cutlen:]
            refdata = refdata[:i - cutlen] + refdata[j - cutlen:]
            cutlen += j - i
        if indata != refdata:
            error(tid, '%s: File contents mismatch' % infile)


def check_bin_text_eq(tid, infile, reffile):
    """check if DISPLAY files with binary parts are equal"""
    with open(infile, 'rb') as fin, open(reffile, 'rb') as fref:
        indata = fin.read()
        refdata = fref.read()
    if indata == refdata:
        return
    # replace line separators by 0xff
    indata_norm = indata.replace(b'\x0d\x0a', b'\xff').replace(b'\x0a', b'\xff').replace(b'\x0d', b'\xff')
    refdata_norm = refdata.replace(b'\x0d\x0a', b'\xff').replace(b'\x0a', b'\xff').replace(b'\x0d', b'\xff')
    if indata_norm != refdata_norm:
        error(tid, 'Normalized file contents mismatch')


def check_file_matches(infile, matches):
    """check if text file contents match regular expressions"""
    try:
        with open(infile, 'r') as f:
            contents = f.readlines()
    except IOError:
        error('CLI', '%s: File not found' % infile)
    for line, pattern in matches:
        try:
            if not re.search(pattern, contents[line]):
                error('CLI',
                      '%s: Line %d does not match' % (infile, line))
        except IndexError:
            error('CLI', '%s: Line %d missing' % (infile, line))


# Common check functions: xas99

def _tags(objcode, compressed, filter=None):
    taglen = 3 if compressed else 5
    refdefs = []
    if compressed:  # ignore :id line
        objcode = b''.join([objcode[i:i + 80].rstrip() for i in range(0, len(objcode) - 80, 80)])  # ignore :id line
    else:  # ignore line numbers and :id line
        objcode = b''.join([objcode[i:i + 76].rstrip() for i in range(0, len(objcode) - 80, 80)])
    yield objcode[:taglen]  # rec count
    objcode = objcode[taglen + 8:].lstrip()  # skip to first tag
    while objcode:
        if objcode[:1] in b'3456':  # those might not be in the same order for xas99
            refdefs.append(objcode[:taglen + 6])  # include name
            objcode = objcode[taglen + 6:]
        elif objcode[:1] == b'7' and refdefs:  # ignore checksum in refdefs
            objcode = objcode[taglen:].lstrip()
        elif objcode[:1] == b'F':
            objcode = objcode[1:]  # just skip end of record marker
        else:
            if filter is None or objcode[0] in filter:
                yield objcode[:taglen]
            objcode = objcode[taglen:]
    for tag in sorted(refdefs):
        yield tag


def check_obj_code_eq(infile, reffile, compressed=False, tagfilter=None):
    """check if object code files are equal modulo id tag"""
    with open(infile, 'rb') as fin, open(reffile, 'rb') as fref:
        indata = fin.read()
        refdata = fref.read()
        for i, (intag, reftag) in enumerate(zip(_tags(indata, compressed, tagfilter),
                                                _tags(refdata, compressed, tagfilter))):
            if intag != reftag:
                error('Object code', 'Mismatch for tag no. {:d}: {}/{}'.format(i, str(intag), str(reftag)))


def check_image_files_eq(genfile, reffile, ignore=()):
    """check if non-zero bytes in binary files are equal"""
    with open(genfile, 'rb') as fg, open(reffile, 'rb') as fr:
        genimage = fg.read()
        refimage = fr.read()
    for imin, imax in ignore:  # must be in decreasing order!
        genimage = genimage[:imin] + genimage[imax:]
        refimage = refimage[:imin] + refimage[imax:]
    if not 0 <= len(genimage) - len(refimage) <= 1:
        error('Image', 'Image length mismatch')
    if (genimage[:2] != refimage[:2] or
            not (0 <= ordw(genimage[2:4]) - ordw(refimage[2:4]) <= 1) or
            genimage[4:6] != refimage[4:6]):
        error('Image', 'Image header mismatch')
    # TI-generated images may contain arbitrary bytes in BSS segments
    for i in range(4, len(refimage)):
        if genimage[i] and genimage[i] != refimage[i]:
            error('Image', 'Image contents mismatch @ ' + hex(i))


def check_image_set_eq(gendata, refdata):
    """check if genfile is outfile, module padding at outfile"""
    if any(data[:2] != b'\xff\xff' for data in gendata[:-1]):
        error('image', 'Bad continuation marker')
    if gendata[-1][:2] != b'\x00\x00':
        error('image', 'Missing >0000 end marker')
    sortedgendata = sorted(gendata, key=lambda d: ordw(d[4:6]))
    sortedrefdata = sorted(refdata, key=lambda d: ordw(d[4:6]))
    if len(sortedgendata) != len(sortedrefdata):
        error('image', 'Image file count mismatch')
    for genimage, refimage in zip(sortedgendata, sortedrefdata):
        padlen = len(refimage) - len(genimage)
        if not 0 <= padlen <= 1:
            error('Image', 'Image length mismatch')
        if not (ordw(refimage[2:4]) - ordw(genimage[2:4]) == padlen) or genimage[4:6] != refimage[4:6]:
            error('Image', 'Image header mismatch')
        # TI-generated images may contain arbitrary bytes in BSS segments
        for i in range(4, len(refimage) - padlen):
            if genimage[i] and genimage[i] != refimage[i]:
                error('Image', 'Image contents mismatch @ ' + hex(i))


def check_list_files_eq(genfile, reffile, ignore_lino=False):
    """check if listing files are equivalent
       ignores symbol listing at end of reffile by checking upto end of genfile
    """
    with open(genfile, 'r') as fg, open(reffile, 'r') as fr:
        genlist = [(l[:16] + l[19:]).rstrip() for l in fg.readlines()
                   if l.strip() and l[5:9] != '****' and l[19] != '<']
        reflist = [l[2:].rstrip() for l in fr.readlines() if l[:2] == '  ']
    gi, ri = 1, 0  # skip assembler header note
    min_col, max_col = 4 if ignore_lino else 0, 74
    while gi < len(genlist):
        gl, rl = genlist[gi], reflist[ri]
        # ignore deliberate changes
        try:
            if gl[10] in '.X':
                rl = rl[:10] + gl[10:15] + rl[15:]  # no data
            if gl[14] == 'r' and rl[14] == "'":  # reloc
                rl = rl[:14] + 'r' + rl[15:]
            if gl[14] == 'e':  # reloc or external (REF)
                rl = rl[:10] + '0000e' + rl[15:]  # remove REF chain
            if 'ORG' in rl[16:] or 'BES' in rl[16:]:
                rl = rl[:5] + gl[5:9] + rl[9:]  # no address
            gl = gl.replace(';', '*')  # unify comments
            # ignore listing directives
            if 'TITL' in gl[16:] or 'PAGE' in gl[16:] or 'UNL' in gl[16:] or 'LIST' in gl[16:]:
                gi += 1
                continue
            # ignore BYTE sections
            if gl[16:] == rl[16:] and ('BYTE' in gl[16:] or 'TEXT' in gl[16:]):
                gi, ri = gi + 1, ri + 1
                while genlist[gi][:4] == '    ':
                    gi += 1
                while reflist[ri][:4] == '    ':
                    ri += 1
                continue
        except IndexError:
            pass
        if gl[min_col:max_col] != rl[min_col:max_col]:
            error('List file', f'Line mismatch in {gi}/{ri}:\n{gl}\n{rl}')
        gi, ri = gi + 1, ri + 1


def check_list_against_binary(listfile, binfile):
    with open(listfile, 'r') as fl, open(binfile, 'rb') as fb:
        lines = fl.readlines()
        blob = fb.read()

    mem = {}
    for line in lines:
        try:
            addr = int(line[5:9].strip(), 16)
        except ValueError:
            continue

        word = line[10:14].strip()
        try:
            value = int(word, 16)
        except ValueError:
            if word == 'XXXX':
                value = 0
            else:
                continue

        if len(word) == 2:
            mem[addr] = value
        elif len(word) == 4:
            mem[addr] = value >> 8
            mem[addr + 1] = value & 0xff

    lc = min(mem)
    for b in blob:
        listb = mem.get(lc, 0)
        if listb != b:
            error('bin list', f'Unexpected byte @>{lc:04X}: >{listb:02X}, expected >{b:02X}')
        lc += 1


def check_dat_file_eq(datfile, binfile):
    """check that textual representation matches binary file"""
    with open(datfile, 'r') as fd, open(binfile, 'rb') as fb:
        dat = ''.join(fd.readlines()[1:])
        bin = fb.read()
    values = [xint(x) for x in re.findall(r'>\w{2}', dat)]
    if bytes(values) != bin:
        error('dat', 'Values and binary file mismatch')


# common check functions: xda99/xdg99

def check_bytes(outfile, reffile):
    """check that outfile has not more data than reffile"""
    outbytes, cntbytes = count_bytes(outfile), count_bytes(reffile)
    if outbytes > cntbytes:
        error('BYTEs', 'Too many BYTEs/DATAs: %d instead of %d' % (outbytes, cntbytes))


def count_bytes(fn):
    """count bytes declared by directives in source"""
    byte_count = 0
    with open(fn, 'r') as fin:
        source = fin.readlines()
    for line in source:
        # get rid of quoted single quotes ''
        line = re.sub(r"'(?:[^']|'')*'",
                      lambda x: ','.join(['z'] * (len(x.group(0)) - 2 - x.group(0)[1:-1].count("''"))),
                      line)
        # get instruction parts
        parts = re.split(r'\s+', line, maxsplit=2)
        if len(parts) > 2 and parts[1].lower() in ('byte', 'data', 'stri', 'text'):
            # get all args
            args = [x.strip() for x in parts[2].split(',') if x.strip()]
            # know what you count
            if parts[1].lower() == 'data':
                byte_count += len(args) * 2
            elif parts[1].lower() == 'text':
                byte_count += sum([len(a) // 2 if a[0] == '>' else 1
                                   for a in args])
            elif parts[1].lower() == 'stri':
                byte_count += sum([len(a) // 2 if a[0] == '>' else 1
                                   for a in args]) + 1  # len byte
            else:
                byte_count += len(args)
    return byte_count


def check_indent(fn, blocks):
    """check if first lines are indented correctly"""
    with open(fn, 'r') as fin:
        source = fin.readlines()
    indents = []
    for line in source:
        if not line:
            continue
        if line[0] == ' ':
            indents.append(re.match(r'\s+(\w)', line).start(1))
        else:
            try:
                indents.append(
                    re.match(r'(?:[\w?!~]+\s+){%d}(\w)' % blocks, line).start(
                        1))
            except AttributeError:
                pass
    if len(indents) < 3:
        error('indent', 'Too few indent values: %d' % len(indents))
    return all([i == indents[0] for i in indents[1:]])


def count_mnemonics(fn, offset=0, wanted=None):
    """build dict of all occurring mnemonics"""
    with open(fn, 'r') as fin:
        source = [l[offset:] for l in fin.readlines()]
    mnems = {}
    for line in source:
        parts = re.split(r'\s+', line.rstrip(), maxsplit=2)
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
    with open(outfile, 'r') as fout, open(reffile, 'r') as fref:
        out = fout.readlines()
        ref = fref.readlines()
    j = -1
    for i, oline in enumerate(out):
        # split output instruction (generated source)
        oinstr = re.split(r'\s+', re.sub(';.*$', '', oline.rstrip()).lower(),
                          2)
        if len(oinstr) < 2 or oinstr[1] == 'equ':
            continue  # no instruction
        oargs = [a.strip().upper() for a in oinstr[2].split(',')] if len(
            oinstr) > 2 else []
        rline, rinstr, urargs = '', (), ()
        while True:
            j += 1
            rline = re.sub(';.*$', '', ref[j]).rstrip()
            if rline[:1] == '*':
                continue  # ignore comments
            if 'IGNORE' in rline:
                break  # don't compare two corresponding lines
            # split reference instruction (original source)
            rinstr = re.split(r'\s+', rline.lower(), 2)
            rargs = [a.strip().upper() for a in rinstr[2].split(',')] if len(
                rinstr) > 2 else []
            # uniform numerical arguments >XXXX, except if they're
            # already >XX (for xdg99)
            urargs = [('>%04X' % xint(a)) if (a[0] == '>' and len(
                a) != 3) or a.isdigit() else a
                      for a in rargs]
            if rline and rinstr[0][-1:] != ':' and rinstr[1] != 'equ':
                break
        if 'IGNORE' not in rline and (
                oinstr[1] != rinstr[1] or oargs != urargs):
            error('source', 'Mismatch in line %d:\n(R) %s\n(O) %s' % (
                i, rline, oline))


def check_origins(fn, origins):
    """check origins in source"""
    with open(fn, 'r') as fin:
        source = fin.readlines()
    ocnt = 0
    for line in source:
        m = re.match(r'^(\w+)\s[^;]*; <-(.*)$', line)
        if m:
            addr = int(m.group(1), 16)
            anns = [int(a.strip()[1:], 16) for a in m.group(2).split(',')]
            if addr in origins:
                if origins[addr] == anns:
                    ocnt += 1
                else:
                    error('origin', 'Origin mismatch @%04X' % addr)
    if ocnt != len(origins):
        error('origin', 'Origin count mismatch: %d/%d' % (ocnt, len(origins)))


def read_stderr(fn, include_warnings=False):
    """read stderr output"""
    errors = []
    with open(fn, 'r') as f:
        lines = f.readlines()[1:]  # ignore ": xas99, version ..."
    for err, line in zip(lines[::2], lines[1::2]):
        if 'Warning' in line:
            if include_warnings:
                warn = re.search(r'<.>\s+(\d+|\*+)\s+-', err)
                if warn:
                    errors.append(warn.group(1))
            else:
                continue  # ignore warnings
        else:
            err = re.search(r'<.>\s+(\d+)', err)
            if err:
                errors.append(err.group(1))
    return errors


def get_source_markers(source, tag):
    ref_errors = []
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            m = re.search(tag, line)
            if m:
                try:
                    if m.group(1):
                        ref_errors.append(m.group(1)[1:])
                        continue
                except IndexError:
                    pass
                ref_errors.append(f'{i + 1:04d}')
    return ref_errors


def check_errors(ref, actual):
    """compare two dicts for key equality"""
    for err in ref:
        if err not in actual:
            error('Error messages', 'Missing error of line ' + err)
    for err in actual:
        if err[0] == '*':
            continue
        if err not in ref:
            error('Error messages', 'Extraneous error in line ' + err)


def check_ellipsis(fn, skip=0):
    with open(fn, 'r') as fin:
        addrs = [None if line[0] == '.' else int(line[:4], 16) for line in fin.readlines()[skip:]]

    for i, a in enumerate(addrs):
        if a is None:
            continue
        try:
            if addrs[i + 1] is None:
                if addrs[i + 2] - a <= 2:
                    error('concise', "Badly placed '....' within address segment")
            else:
                if addrs[i + 1] - a > 2:
                    error('concise', "Missing '....' between two address segments")
        except IndexError:
            pass


# common check functions xga99

def check_gbc_files_eq(name, genfile, reffile, offset=0):
    """check if non-zero bytes in binary files are equal"""
    with open(genfile, 'rb') as fgen, open(reffile, 'rb') as fref:
        genimage = fgen.read()
        refimage = fref.read()[6:]
    if genimage[offset:] != refimage and genimage[offset:] != refimage[:-1]:
        error('GPL image', 'Image mismatch: ' + name)
    if genimage[:offset] != bytes(offset):
        error('GPL image', 'Non-zero offset prefix')
