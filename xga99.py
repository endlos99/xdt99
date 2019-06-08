#!/usr/bin/env python

# xga99: A GPL cross-assembler
#
# Copyright (c) 2015-2019 Ralph Benzinger <xdt99@endlos.net>
#
# This program is part of the TI 99 Cross-Development Tools (xdt99).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import sys
import math
import re
import os.path

VERSION = "2.0.0"


# Utility functions

def ordw(word):
    """word ord"""
    return ord(word[0]) << 8 | ord(word[1])


def chrw(word):
    """word chr"""
    return chr(word >> 8) + chr(word & 0xff)


def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip(">"), 16 if s[:2] == "0x" or s[:1] == ">" else 10)


def trunc(i, m):
    """round integer down to multiple of m"""
    return i - i % m


def readlines(n, m="r"):
    """read lines from file or STDIN"""
    if n == "-":
        return sys.stdin.readlines()
    else:
        with open(n, m) as f:
            return f.readlines()


def writedata(n, d, m="wb"):
    """write data to file or STDOUT"""
    if n == "-":
        sys.stdout.write(d)
    else:
        with open(n, m) as f:
            f.write(d)


def outname(basename, extension, output=None, addition=None, count=1):
    if basename == "-":
        return "-"
    if count == 1:
        return output or basename + extension
    if output is not None:
        basename, extension = os.path.splitext(output)
    return basename + "_" + addition + extension


# Error handling

class AsmError(Exception):
    pass


# Symbol table

class Address:
    """absolute GROM address"""

    def __init__(self, addr, local=False):
        if local:
            self.addr = addr & 0x1fff  # address within GROM, e.g., BR/BS
            self.size = 1
        else:
            self.addr = addr  # global 16-bit address, e.g., B
            self.size = 2
        self.local = local

    def hex(self):
        return "%04X" % self.addr

    def __eq__(self, other):
        return (isinstance(other, Address) and
                self.addr == other.addr and
                self.local == other.local)

    def __ne__(self, other):
        return not self == other


class Local:
    """local label reference"""

    def __init__(self, name, distance):
        self.name = name
        self.distance = distance


class Operand:
    """general source or destination address or imm value"""

    def __init__(self, addr, vram=False, grom=False, vreg=False,
                 imm=0, indirect=False, index=None):
        self.addr = addr
        self.vram = vram
        self.grom = grom  # implies not indirect
        self.vreg = vreg
        self.immediate = imm
        self.indirect = indirect
        self.index = index
        self.bytes = self.generate()
        assert not any([isinstance(b, Address) for b in self.bytes])
        self.size = len(self.bytes)

    def generate(self):
        if self.immediate == 1 or self.vreg:
            return [self.addr & 0xff]
        elif self.immediate == 2:
            return [self.addr >> 8, self.addr & 0xff]
        cpuram = (not self.vram and not self.grom) or self.indirect
        addr = (self.addr - 0x8300 if cpuram else self.addr) % 0x10000
        mask = (0b1000 |
                (0b0100 if self.index is not None else 0) |
                (0b0010 if self.vram else 0) |
                (0b0001 if self.indirect else 0)) << 4
        # form MOVE
        if self.grom and not self.indirect:
            bs = [addr >> 8, addr & 0xff]
        # form I
        elif cpuram and 0x00 <= addr <= 0x7f and (
                not (self.indirect or self.index)):
            bs = [addr]
        # form II/III
        # NOTE: could II-V include address mode G*?
        elif addr < 0x0f00:
            bs = [mask | addr >> 8, addr & 0xff]
        # form IV/V
        else:
            bs = [mask | 0b1111, addr >> 8, addr & 0xff]
        if self.index:
            bs.append(self.index & 0xff)
        return bs

    def __eq__(self, other):
        return (isinstance(other, Operand) and
                self.addr == other.addr and self.vram == other.vram and
                self.grom == other.grom and self.vreg == other.vreg and
                self.immediate == other.immediate and
                self.indirect == other.indirect and
                self.index == other.index)

    def __ne__(self, other):
        return not self == other


class Symbols:
    """symbol table and line counter"""

    def __init__(self, add_defs=()):
        self.symbols = {}
        self.predefs = {
            # CPU RAM
            "MAXMEM": 0x8370,
            "DATSTK": 0x8372,
            "SUBSTK": 0x8373,
            "KEYBRD": 0x8374,
            "KEY": 0x8375,
            "JOYY": 0x8376,
            "JOYX": 0x8377,
            "RANDOM": 0x8378,
            "TIMER": 0x8379,
            "MOTION": 0x837a,
            "VDPSTT": 0x837b,
            "STATUS": 0x837c,
            "CB": 0x837d,
            "YPT": 0x837e,
            "XPT": 0x837f,
            # floating point arithmetic
            "FAC": 0x834a,
            "ARG": 0x835c,
            "SGN": 0x8375,
            "EXP": 0x8376,
            "VSPTR": 0x836e,
            "FPERAD": 0x836c,
            # RAG assembler
            "ERCODE": 0x8354,
            "VPAB": 0x8356,
            "VSTACK": 0x836e
            }
        for defs in add_defs:
            parts = defs.upper().split("=")
            value = Parser.symconst(parts[1]) if len(parts) > 1 else 1
            self.symbols[parts[0]] = value
        self.reset_LC()
        self.locations = []  # list of (lidx, name), must not be deleted between passes

    def reset_LC(self):
        self.LC = 0
        self.updated = False

    def add_symbol(self, name, value, pass_no):
        """add symbol to symbol table or update existing symbol"""
        prev_value = self.symbols.get(name)
        if pass_no == 0:
            if not re.match(r"[^\W\d]\w*$", name) and "$" not in name:
                raise AsmError("Invalid symbol name: " + name)
            if prev_value is not None:
                raise AsmError("Multiple symbols: " + name)
            self.symbols[name] = value
        elif value != prev_value:
            self.symbols[name] = value
            self.updated = True
        return name

    def add_label(self, lidx, label, pass_no):
        """add label, in every pass to update its LC"""
        name = self.add_symbol(label, Address(self.LC), pass_no)
        if (lidx, name) not in self.locations:
            self.locations.append((lidx, name))

    def add_local_label(self, lidx, label, pass_no):
        """add local label, in every pass to update its LC"""
        self.add_label(lidx, label + "$" + str(lidx), pass_no)

    def get_symbol(self, name, pass_no=99, check=False, needed=False, not_found=0):
        if pass_no == 0 and not needed:
            return not_found
        value = self.symbols.get(name)
        if value is None:
            value = self.predefs.get(name)
            if check and value is None:
                raise AsmError("Unknown symbol: " + name)
        return value

    def get_local(self, name, lpos, distance, pass_no):
        if pass_no == 0:
            return 0
        targets = [(l, n) for (l, n) in self.locations
                   if n[:len(name) + 1] == name + "$"]
        try:
            i, lidx = next((j, l) for j, (l, n) in enumerate(targets) if l >= lpos)
            if distance > 0 and lidx > lpos:
                distance -= 1  # i points to +! unless lidx == lpos
        except StopIteration:
            i = len(targets)  # beyond last label
        try:
            _, fullname = targets[i + distance]
        except IndexError:
            return None
        return self.get_symbol(fullname, pass_no=pass_no)

    def is_symbol(self, name):
        return name in self.symbols


class Objcode:
    """generate object code"""

    def __init__(self, symbols, grom, aorg):
        self.symbols = symbols
        self.base_grom = grom
        self.base_aorg = aorg
        self.code = []
        self.entry = None
        self.reset_gen()

    def reset_gen(self):
        """prepare new assembly pass"""
        self.segments = []
        self.symbols.reset_LC()
        self.segment(self.base_grom, self.base_aorg, init=True)

    def segment(self, grom, base, init=False):
        """create new code segment"""
        if not init and self.code:
            self.segments.append(
                (self.grom, self.base, self.symbols.LC, self.code))
        self.grom = grom
        self.base = base
        self.symbols.LC = self.grom + self.base
        self.code = []

    def process_label(self, lidx, label, pass_no):
        if not label:
            return
        if label[0] == "!":
            self.symbols.add_local_label(lidx, label[1:], pass_no)
        else:
            self.symbols.add_label(lidx, label, pass_no)

    def emit(self, *args):
        """generate byte code"""
        self.code.append((self.symbols.LC, args))
        self.symbols.LC += sum(
            [a.size if isinstance(a, Operand) else
             a.size if isinstance(a, Address) else
             0 if a is None else 1
             for a in args])

    def list(self, lino, line=None, eos=False, text1=None, text2=None):
        """create list file entry"""
        if lino == 0:
            # change of source
            l = Line(lino, line, eos)
            l.text1 = l.text2 = "****"
            self.code.append((0, l))
        elif lino > 0:
            # regular statement
            self.code.append((self.symbols.LC, Line(lino, line, eos)))
        else:
            # followup lines to statement
            last_line = self.code[-1][1]
            assert isinstance(last_line, Line)
            last_line.text1, last_line.text2 = text1, text2

    def wrapup(self):
        """wrap-up code generation"""
        self.segments.append(
            (self.grom, self.base, self.symbols.LC, self.code))

    def generate_dump(self):
        """generate raw dump of internal data structures (debug)"""
        self.wrapup()
        dump, i = "", 0
        for grom, base, final_LC, code in self.segments:
            dump += "%sGROM >%04X AORG >%04X:" % (
                "\n" if dump and dump[-1] != "\n" else "", grom, base)
            for LC, bs in code:
                if isinstance(bs, Line):
                    continue
                dump += "\n%04X:  " % LC
                for b in bs:
                    if isinstance(b, Address):
                        dump += "(%04X)  " % b.addr
                    elif isinstance(b, Operand):
                        for bb in b.bytes:
                            dump += "%02X  " % bb
                    else:
                        dump += "%02X  " % b
                    i += 1
        dump += "\n"
        for i, s in enumerate(self.symbols.symbols):
            v = self.symbols.get_symbol(s)
            dump += "%-8s>%04X %c" % (
                s, v.addr if isinstance(v, Address) else v,
                "\n" if i % 5 == 4 else " ")
        return dump if dump[-1] == "\n" else dump + "\n"

    def generate_byte_code(self):
        """generate GPL byte code"""
        self.wrapup()
        mems = {}
        # put bytes into memory
        for grom, base, final_LC, code in self.segments:
            mem = mems.setdefault(grom, {})
            for LC, bs in code:
                if isinstance(bs, Line):
                    continue
                addr = LC
                for b in bs:
                    if isinstance(b, Address):
                        if b.local:
                            mem[addr - 1] |= (b.addr >> 8) & 0x1f
                            mem[addr] = b.addr & 0xff
                        else:
                            mem[addr] = b.addr >> 8
                            mem[addr + 1] = b.addr & 0xff
                        addr += b.size
                    elif isinstance(b, Operand):
                        for i, bb in enumerate(b.bytes):
                            assert 0 <= bb < 256
                            mem[addr + i] = bb
                        addr += b.size
                    else:
                        assert 0 <= b < 256
                        mem[addr] = b
                        addr += 1
        # build individual GROMs
        groms = []
        for grom in mems:
            mem = mems[grom]
            addrs = mem.keys()
            if addrs:  # could be empty if only lines are before GROM dir
                sfirst, slast = min(addrs), max(addrs) + 1
                bs = "".join([chr(mem[addr] & 0xff) if addr in mem else "\x00"
                              for addr in xrange(sfirst, slast)])
                groms.append((grom, sfirst, bs))
        return groms

    def generate_header(self, grom, base, name):
        """generate GPL header"""
        offset = base - grom
        if offset < 0x16:
            raise AsmError("No space for GROM header")
        entry = self.entry or self.symbols.get_symbol("START") or base
        gpl_header = "\xaa\x01\x00\x00\x00\x00%s" % chrw(grom + 0x10) + "\x00" * 8
        menu_name = name[:offset - 0x15]
        info = "\x00\x00%s%c%s" % (
            chrw(entry.addr if isinstance(entry, Address) else entry),
            len(menu_name), menu_name)
        return gpl_header + info

    def generate_image(self, name):
        """generate memory image for GROM"""
        groms = self.generate_byte_code()
        if len(groms) > 1:
            raise AsmError("Multiple GROMs currently not supported")
        grom, base, image = groms[0]
        header = self.generate_header(grom, base, name)
        padding = "\x00" * (base - grom - len(header))
        return header + padding + image

    def generate_cart(self, name):
        """generate RPK file for use as MESS rom cartridge"""
        image = self.generate_image(name)
        layout = """<?xml version="1.0" encoding="utf-8"?>
                    <romset version="1.0">
                        <resources>
                            <rom id="gromimage" file="%s.bin"/>
                        </resources>
                        <configuration>
                            <pcb type="standard">
                                <socket id="grom_socket" uses="gromimage"/>
                            </pcb>
                        </configuration>
                    </romset>""" % name
        metainf = """<?xml version="1.0"?>
                     <meta-inf>
                         <name>%s</name>
                     </meta-inf>""" % name
        return image, layout, metainf

    def generate_text(self, byte_code, mode):
        """convert binary data into text representation"""
        text = ""
        for grom, sfirst, mem in byte_code:
            mem += "\x00"  # safety pad for word size
            if 'r' in mode:
                word = lambda i: ordw(mem[i + 1:((i - 1) if i > 0 else None):-1])  # byte-swapped
            else:
                word = lambda i: ordw(mem[i:i + 2])

            fmt = "%s%04x" if '4' in mode else "%s%02x"
            tf = lambda x: x  # use value as-is

            if 'a' in mode:  # assembly
                hex_prefix = ">"
                data_prefix = ("       byte " if '2' in mode else
                               "       data ")
                suffix = "\n"
                text += ";      grom >%04x\n" % grom
            elif 'b' in mode:  # BASIC
                hex_prefix = ""
                data_prefix = "DATA "
                suffix = "\n"
                fmt = "%s%d"
                tf = lambda x: x - 0x10000 if x > 32767 else x  # hex to dec
            elif 'c' in mode:  # C
                hex_prefix = "0x"
                data_prefix = "  "
                suffix = ",\n"
            else:
                raise AsmError("Bad text format: " + mode)

            if '4' in mode:  # words
                ws = [fmt % (hex_prefix, tf(word(i)))
                      for i in xrange(0, len(mem), 2)]
                lines = [data_prefix + ", ".join(ws[i:i + 4]) + suffix
                         for i in xrange(0, len(ws), 4)]
            else:  # bytes (default)
                bs = [fmt % (hex_prefix, ord(mem[i]))
                      for i in xrange(0, len(mem))]
                lines = [data_prefix + ", ".join(bs[i:i + 8]) + suffix
                         for i in xrange(0, len(bs), 8)]
            text += "".join(lines)
        return text

    def generate_list(self, gensymbols):
        """generate listing file"""
        listing = []
        for grom, base, final_LC, code in self.segments:
            words, slino, sline, skip = [], None, None, False
            # code:  Line()             <-
            #        (LC, [byte, ...])  <-  belongs together
            #        (LC, [byte, ...])  <-
            #        Line()
            #        ...
            for LC, bs in code:
                if isinstance(bs, Line):
                    if slino is not None:
                        a0, w0 = words[0] if words else ("    ", "  ")
                        listing.append("%4s %-2s %-5s %s" % (
                            slino, a0, w0, sline))
                        for addri, wordi, in words[1:]:
                            listing.append("     %-2s %-5s" % (addri, wordi))
                            if bs.end_of_source:
                                break
                    slino = "%04d" % bs.lino if bs.lino else "****"
                    sline = bs.line
                    if not (bs.text1 is None and bs.text2 is None):
                        warg = ("    " if bs.text2 is None else
                                bs.text2 if isinstance(bs.text2, str) else
                                bs.text2.hex() if isinstance(bs.text2, Address) else
                                "%04X" % bs.text2)
                        words = [("%04X" % LC if bs.text1 is None else bs.text1, warg[0:2]),
                                 (0, warg[2:4])]
                        skip = True
                    else:
                        words = []
                        skip = False
                elif skip:
                    pass
                else:
                    o = 0
                    for b in bs:
                        if isinstance(b, Address):
                            if b.size == 1:
                                # back-patch previous line with high byte of current address
                                patched_byte = int(words[-1][1], 16) | int(b.hex()[0:2], 16)
                                words[-1] = (words[-1][0], "%02x" % patched_byte)
                                words.append(("%04X" % (LC + o), b.hex()[2:4]))  # regular line
                            else:
                                words.append(("%04X" % (LC + o), b.hex()[0:2]))
                                words.append(("%04X" % (LC + o + 1), b.hex()[2:4]))
                            o += b.size
                        elif isinstance(b, Operand):
                            for x in b.bytes:
                                words.append(("%04X" % (LC + o), "%02X" % x))
                                o += 1
                        else:
                            words.append(("%04X" % (LC + o), "%02X" % b))
                            o += 1
        symbols = self.generate_symbols() if gensymbols else ""
        return ("XGA99 CROSS-ASSEMBLER   VERSION " + VERSION + "\n" +
                "\n".join(listing) + "\n\n" + symbols + "\n")

    def generate_symbols(self, equ=False):
        """generate symbols"""
        symbols = self.symbols.symbols
        symlist = []
        for symbol in sorted(symbols):
            if symbol[0] == '$' or symbol[0] == "_":
                continue  # skip local and internal symbols
            addr = symbols.get(symbol)
            addr_value = addr.addr if isinstance(addr, Address) else addr
            symlist.append((symbol, addr_value))
        fmt = "{}:\n       equ  >{:04X}" if equ else "    {:.<20} >{:04X}"
        return "\n".join([fmt.format(*symbol) for symbol in symlist])


class Word:
    """auxiliary class for word arithmetic"""

    def __init__(self, value, pass_no=None):
        self.value = value % 0x10000
        self.pass_no = pass_no

    def sign(self):
        return -1 if self.value & 0x8000 else +1

    def abs(self):
        return -self.value % 0x10000 if self.value & 0x8000 else self.value

    def add(self, arg):
        self.value = (self.value + arg.value) % 0x10000

    def sub(self, arg):
        self.value = (self.value - arg.value) % 0x10000

    def mul(self, op, arg):
        if op in "/%" and arg.value == 0:
            if self.pass_no == 0:
                return 0  # temporary value
            else:
                raise AsmError("Division by zero")
        sign = arg.sign() if op == "%" else self.sign() * arg.sign()
        val = (self.abs() * arg.abs() if op == "*" else
               self.abs() / arg.abs() if op == "/" else
               self.abs() % arg.abs() if op == "%" else None)
        self.value = (val if sign > 0 else -val) % 0x10000

    def bit(self, op, arg):
        val = (self.value & arg.value if op == "&" else
               self.value | arg.value if op == "|" else
               self.value ^ arg.value if op == "^" else None)
        self.value = val % 0x10000


class Line:
    """source code line"""

    def __init__(self, lino, line, end_of_source=False):
        self.lino = lino
        self.line = line
        self.end_of_source = end_of_source
        self.text1 = self.text2 = None


# Directives

class Directives:
    @staticmethod
    def EQU(parser, code, label, ops):
        value = parser.expression(ops[0])
        code.symbols.add_symbol(label, value, parser.pass_no)

    @staticmethod
    def DATA(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        code.emit(*[Address(parser.expression(op)) for op in ops])

    @staticmethod
    def BYTE(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        code.emit(*[parser.expression(op) & 0xff for op in ops])

    @staticmethod
    def TEXT(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        for op in ops:
            text = parser.text(op)
            code.emit(*[ord(c) for c in text])

    @staticmethod
    def STRI(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        text = "".join([parser.text(op) for op in ops])
        code.emit(len(text), *[ord(c) for c in text])

    @staticmethod
    def FLOAT(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        for op in ops:
            bytes_ = parser.radix100(op)
            code.emit(*bytes_)

    @staticmethod
    def BSS(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        size = parser.expression(ops[0])
        code.emit(*[0x00 for _ in range(size)])

    @staticmethod
    def GROM(parser, code, label, ops):
        value = parser.value(ops[0])
        grom = (value << 13) if value < 8 else value & 0xe000
        code.segment(grom, 0x0000)
        code.process_label(parser.lidx, label, parser.pass_no)

    @staticmethod
    def AORG(parser, code, label, ops):
        base = parser.value(ops[0])
        if not 0 <= base < 0x2000:
            raise AsmError("AORG offset %04X out of range" % base)
        code.segment(code.grom, base)
        code.process_label(parser.lidx, label, parser.pass_no)

    @staticmethod
    def TITLE(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        text = parser.text(ops[0])
        code.symbols.title = text[:12]

    @staticmethod
    def FMT(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        parser.fmt_mode = True
        code.emit(0x08)

    @staticmethod
    def FOR(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        parser.for_loops.append(Address(code.symbols.LC + 1))
        count = parser.expression(ops[0])
        code.emit(0xC0 + count - 1)

    @staticmethod
    def FEND(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        if parser.for_loops:
            addr = parser.for_loops.pop()
            if ops:
                addr = Address(parser.label(ops[0]))
            code.emit(0xFB, addr)
        elif parser.fmt_mode:
            code.emit(0xFB)
            parser.fmt_mode = False
        else:
            raise AsmError("Syntax error: unexpected FEND")

    @staticmethod
    def COPY(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        filename = parser.filename(ops[0])
        parser.open(filename=filename)

    @staticmethod
    def BCOPY(parser, code, label, ops):
        """extension: include binary file as BYTE stream"""
        code.process_label(parser.lidx, label, parser.pass_no)
        filename = parser.filename(ops[0])
        path = parser.find(filename)  # might throw exception
        with open(path, "rb") as f:
            bs = [ord(x) for x in f.read()]
            code.emit(*bs)

    @staticmethod
    def END(parser, code, label, ops):
        code.process_label(parser.lidx, label, parser.pass_no)
        if ops:
            code.entry = code.symbols.get_symbol(ops[0], pass_no=parser.pass_no, check=True)
        parser.stop()

    ignores = [
        "", "PAGE", "LIST", "UNL", "LISTM", "UNLM"
        ]

    @staticmethod
    def process(parser, code, label, mnemonic, operands):
        """process directives"""
        if mnemonic in Directives.ignores:
            code.process_label(parser.lidx, label, parser.pass_no)
            return True
        try:
            fn = getattr(Directives, mnemonic)
        except AttributeError:
            return False
        try:
            fn(parser, code, label, operands)
        except (IndexError, ValueError):
            raise AsmError("Syntax error")
        return True


# Opcodes

class Opcodes:
    op_imm = lambda parser, x: (parser.expression(x[0]),)
    op_imm_gs = lambda parser, x: (parser.expression(x[0]),
                                   parser.gaddress(x[1], is_gs=True))
    op_opt = lambda d: lambda parser, x: (parser.expression(x[0]) if x else d,)
    op_gd = lambda parser, x: (parser.gaddress(x[0], is_gs=False),)
    op_gs_gd = lambda parser, x: (parser.gaddress(x[0], is_gs=True),
                                  parser.gaddress(x[1], is_gs=False))
    op_gs_dgd = lambda parser, x: (parser.gaddress(x[0], is_gs=True, is_d=True),
                                   parser.gaddress(x[1], is_gs=False))
    op_lab = lambda parser, x: (parser.label(x[0]),)
    op_move = lambda parser, x: parser.move(x)

    opcodes = {
        # 4.1 compare and test instructions
        "H": (0x09, 5, None),
        "GT": (0x0a, 5, None),
        "CARRY": (0x0c, 5, None),
        "OVF": (0x0d, 5, None),
        "CEQ": (0xd4, 1, op_gs_gd),
        "DCEQ": (0xd5, 1, op_gs_dgd),
        "CH": (0xc4, 1, op_gs_gd),
        "DCH": (0xc5, 1, op_gs_dgd),
        "CHE": (0xc8, 1, op_gs_gd),
        "DCHE": (0xc9, 1, op_gs_dgd),
        "CGT": (0xcc, 1, op_gs_gd),
        "DCGT": (0xcd, 1, op_gs_dgd),
        "CGE": (0xd0, 1, op_gs_gd),
        "DCGE": (0xd1, 1, op_gs_dgd),
        "CLOG": (0xd8, 1, op_gs_gd),
        "DCLOG": (0xd9, 1, op_gs_dgd),
        "CZ": (0x8e, 6, op_gd),
        "DCZ": (0x8f, 6, op_gd),
        # 4.2 program control instructions
        "BS": (0x60, 4, op_lab),
        "BR": (0x40, 4, op_lab),
        "B": (0x05, 3, op_lab),
        "CASE": (0x8a, 6, op_gd),
        "DCASE": (0x8b, 6, op_gd),
        "CALL": (0x06, 3, op_lab),
        "FETCH": (0x88, 6, op_gd),
        "RTN": (0x00, 5, None),
        "RTNC": (0x01, 5, None),
        # 4.4 arithmetic and logical instructions
        "ADD": (0xa0, 1, op_gs_gd),
        "DADD": (0xa1, 1, op_gs_dgd),
        "SUB": (0xa4, 1, op_gs_gd),
        "DSUB": (0xa5, 1, op_gs_dgd),
        "MUL": (0xa8, 1, op_gs_gd),
        "DMUL": (0xa9, 1, op_gs_dgd),
        "DIV": (0xac, 1, op_gs_gd),
        "DDIV": (0xad, 1, op_gs_dgd),
        "INC": (0x90, 6, op_gd),
        "DINC": (0x91, 6, op_gd),
        "INCT": (0x94, 6, op_gd),
        "DINCT": (0x95, 6, op_gd),
        "DEC": (0x92, 6, op_gd),
        "DDEC": (0x93, 6, op_gd),
        "DECT": (0x96, 6, op_gd),
        "DDECT": (0x97, 6, op_gd),
        "ABS": (0x80, 6, op_gd),
        "DABS": (0x81, 6, op_gd),
        "NEG": (0x82, 6, op_gd),
        "DNEG": (0x83, 6, op_gd),
        "INV": (0x84, 6, op_gd),
        "DINV": (0x85, 6, op_gd),
        "AND": (0xb0, 1, op_gs_gd),
        "DAND": (0xb1, 1, op_gs_dgd),
        "OR": (0xb4, 1, op_gs_gd),
        "DOR": (0xb5, 1, op_gs_dgd),
        "XOR": (0xb8, 1, op_gs_gd),
        "DXOR": (0xb9, 1, op_gs_dgd),
        "CLR": (0x86, 6, op_gd),
        "DCLR": (0x87, 6, op_gd),
        "ST": (0xbc, 1, op_gs_gd),
        "DST": (0xbd, 1, op_gs_dgd),
        "EX": (0xc0, 1, op_gs_gd),
        "DEX": (0xc1, 1, op_gs_dgd),
        "PUSH": (0x8c, 6, op_gd),
        "MOVE": (0x20, 9, op_move),
        "SLL": (0xe0, 1, op_gs_gd),  # opGdGs in TI Guide ff.
        "DSLL": (0xe1, 1, op_gs_dgd),
        "SRA": (0xdc, 1, op_gs_gd),
        "DSRA": (0xdd, 1, op_gs_dgd),
        "SRL": (0xe4, 1, op_gs_gd),
        "DSRL": (0xe5, 1, op_gs_dgd),
        "SRC": (0xe8, 1, op_gs_gd),
        "DSRC": (0xe9, 1, op_gs_dgd),
        # 4.5 graphics and miscellaneous instructions
        "COINC": (0xed, 1, op_gs_dgd),
        "BACK": (0x04, 2, op_imm),
        "ALL": (0x07, 2, op_imm),
        "RAND": (0x02, 2, op_opt(255)),
        "SCAN": (0x03, 5, None),
        "XML": (0x0f, 2, op_imm),
        "EXIT": (0x0b, 5, None),
        "I/O": (0xf6, 8, op_imm_gs),  # opGsImm
        # BASIC
        "PARSE": (0x0e, 2, op_imm),
        "CONT": (0x10, 5, None),
        "EXEC": (0x11, 5, None),
        "RTNB": (0x12, 5, None),
        # undocumented
        "SWGR": (0xf8, 1, op_gs_gd),
        "DSWGR": (0xf9, 1, op_gs_dgd),
        "RTGR": (0x13, 5, None)
        # end of opcodes
    }

    pseudos = {
        # 4.3 bit manipulation and pseudo instruction
        "RB": ("AND", ["2**($1)^>FFFF", "$2"]),
        "SB": ("OR", ["2**($1)", "$2"]),
        "TBR": ("CLOG", ["2**($1)", "$2"]),
        "HOME": ("DCLR", ["@YPT"]),
        "POP": ("ST", ["*STATUS", "$1"])
    }

    op_text = lambda parser, x: parser.fmttext(x)
    op_char = lambda parser, x: (parser.fmtcount(x[0]),
                                 parser.expression(x[1]))
    op_hstr = lambda parser, x: (parser.fmtcount(x[0], max_count=27),
                                 parser.gaddress(x[1], is_gs=True, plain_only=True))
    op_incr = lambda parser, x: (parser.fmtcount(x[0]),)
    op_value = lambda parser, x: (1, parser.expression(x[0]))
    op_bias = lambda parser, x: parser.fmtbias(x)

    fmt_codes = {
        "HTEXT": (0x00, op_text),
        "VTEXT": (0x20, op_text),
        "HCHAR": (0x40, op_char),
        "VCHAR": (0x60, op_char),
        "COL+": (0x80, op_incr),
        "ROW+": (0xa0, op_incr),
        "HSTR": (0xe0, op_hstr),
        # "FOR": (0xc0, op_value),  # -> directive
        # "FEND": (0xfb, None),  # -> directive
        "BIAS": (0xfc, op_bias),
        "ROW": (0xfe, op_value),
        "COL": (0xff, op_value)
    }

    @staticmethod
    def process(parser, code, label, mnemonic, operands):
        """get assembly code for mnemonic"""
        code.process_label(parser.lidx, label, parser.pass_no)
        if mnemonic in Opcodes.pseudos:
            mnemonic, opers = Opcodes.pseudos[mnemonic]
            operands = [re.sub(r"\$(\d+)",
                               lambda m: operands[int(m.group(1)) - 1], o)
                        for o in opers]
        if parser.fmt_mode:
            try:
                opcode, parse = Opcodes.fmt_codes[mnemonic]
                args = parse(parser, operands) if parse else []
            except (KeyError, ValueError, IndexError):
                raise AsmError("Syntax error in FMT mode")
            Opcodes.generate(code, opcode, 7, args)
        else:
            try:
                opcode, fmt, parse = Opcodes.opcodes[mnemonic]
                args = parse(parser, operands) if parse else []
            except (KeyError, ValueError, IndexError):
                raise AsmError("Syntax error")
            Opcodes.generate(code, opcode, fmt, args)

    @staticmethod
    def generate(code, opcode, fmt, args):
        """generate byte code"""
        # format #
        if fmt == 1:
            assert isinstance(args[0], Operand)
            s = 1 if args[0].immediate else 0
            code.emit(opcode | s << 1, args[1], args[0])
        elif fmt == 2:
            code.emit(opcode, args[0])
        elif fmt == 3:
            code.emit(opcode, Address(args[0]))
        elif fmt == 4:
            code.emit(opcode, Address(args[0], local=True))
        elif fmt == 5:
            code.emit(opcode)
        elif fmt == 6:
            code.emit(opcode, args[0])
        elif fmt == 7:
            oo = args[0] - 1 if len(args) > 0 else 0
            code.emit(opcode | oo, *args[1:])
        elif fmt == 8:
            code.emit(opcode, args[1], args[0] & 0xff)
        elif fmt == 9:
            oo, ln, gd, gs = args
            code.emit(opcode | oo, ln, gd, gs)
        else:
            raise AsmError("Unsupported opcode format " + str(fmt))


# Parsing

class SyntaxVariant:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Syntax:
    """various syntax conventions"""

    @staticmethod
    def get(style):
        try:
            return getattr(Syntax, style)
        except AttributeError:
            raise AsmError("Unknown syntax style " + style)

    xdt99 = SyntaxVariant(
        ga=r"(?:(@|\*|V@|V\*|G@)|(#|R@))([^(]+)(?:\(@?([^)]+)\))?$",
        gprefix="G@",
        moveops=r"([^,]+),\s*([^,]+),\s*([^,]+)$",
        tdelim="'",
        # regex replacements applied to escaped mnemonic and op fields
        repls=[
            (r"^HMOVE\b", "HSTR"),  # renamed HMOVE -> HSTR
            (r"^ORG\b", "AORG"),  # TI
            (r"^TITL\b", "TITLE"),  # RYTE DATA
            (r"^HTEX\b", "HTEXT"),
            (r"^VTEX\b", "VTEXT"),
            (r"^HCHA\b", "HCHAR"),
            (r"^VCHA\b", "VCHAR"),
            (r"^SCRO\b", "BIAS"),
            (r"&([01]+)", r":\1"),
            (r"^IDT\b", "TITLE"),  # RAG
            (r"^IO\b", "I/O"),
            (r"^IROW\b", "ROW+"),
            (r"^ICOL\b", "COL+")
            ]
        )

    mizapf = SyntaxVariant(
        ga=r"(?:([@*]|VDP[@*]|GR[OA]M@)|(VREG))([^(]+)(?:\(@?([^)]+)\))?$",
        gprefix="GROM@",
        moveops=r"(.+)\s+BYTES\s+FROM\s+(.+)\s+TO\s+(.+)$",
        tdelim='"',
        repls=[
            (r"^PRINTH\s+(.+)\sTIMES\s+(.+)\b", r"HCHAR \1,\2"),
            (r"^PRINTV\s+(.+)\sTIMES\s+(.+)\b", r"VCHAR \1,\2"),
            (r"^FOR\s+(.+)\sTIMES\s+DO\b", r"FOR \1"),
            (r"^PRINTH\b", "HTEXT"),
            (r"^PRINTV\b", "VTEXT"),
            (r"^DOWN\b", "ROW+"),
            (r"^RIGHT\b", "COL+"),
            (r"^END\b", "FEND"),
            (r"^HMOVE\b", "HSTR"),
            (r"^XGPL\b", "BYTE")
            ]
        )


class Preprocessor:
    """xdt99-specific preprocessor extensions"""

    def __init__(self, parser):
        self.parser = parser
        self.parse = True
        self.parse_branches = []
        self.parse_macro = None
        self.macros = {}

    def args(self, ops):
        lhs = self.parser.expression(ops[0], needed=True)
        rhs = self.parser.expression(ops[1], needed=True) if len(ops) > 1 else 0
        return lhs, rhs

    def DEFM(self, code, ops):
        if len(ops) != 1:
            raise AsmError("Invalid syntax")
        self.parse_macro = ops[0]
        if self.parse_macro in self.macros:
            raise AsmError("Duplicate macro name")
        self.macros[self.parse_macro] = []

    def ENDM(self, code, ops):
        raise AsmError("Found .ENDM without .DEFM")

    def IFDEF(self, code, ops):
        self.parse_branches.append(self.parse)
        self.parse = code.symbols.is_symbol(ops[0]) if self.parse else None

    def IFNDEF(self, code, ops):
        self.parse_branches.append(self.parse)
        self.parse = not code.symbols.is_symbol(ops[0]) if self.parse else None

    def IFEQ(self, code, ops):
        self.parse_branches.append(self.parse)
        self.parse = cmp(*self.args(ops)) == 0 if self.parse else None

    def IFNE(self, code, ops):
        self.parse_branches.append(self.parse)
        self.parse = cmp(*self.args(ops)) != 0 if self.parse else None

    def IFGT(self, code, ops):
        self.parse_branches.append(self.parse)
        self.parse = cmp(*self.args(ops)) > 0 if self.parse else None

    def IFGE(self, code, ops):
        self.parse_branches.append(self.parse)
        self.parse = cmp(*self.args(ops)) >= 0 if self.parse else None

    def ELSE(self, code, ops):
        self.parse = not self.parse if self.parse is not None else None

    def ENDIF(self, code, ops):
        self.parse = self.parse_branches.pop()

    def ERROR(self, code, ops):
        if self.parse:
            raise AsmError("Error state")

    def inst_macro_args(self, text):
        try:
            return re.sub(r"\$(\d+)",
                          lambda m: self.parser.macro_args[int(m.group(1)) - 1],
                          text)
        except (ValueError, IndexError):
            return text

    def instline(self, line):
        # temporary kludge, breaks comments
        parts = re.split(r"('(?:[^']|'')*'|\"[^\"]*\")", line)
        parts[::2] = [self.inst_macro_args(p) for p in parts[::2]]
        return "".join(parts)

    def process(self, code, label, mnemonic, operands, line):
        """process preprocessor directive"""
        if self.parse_macro:
            if mnemonic == ".ENDM":
                self.parse_macro = None
            elif mnemonic == ".DEFM":
                raise AsmError("Cannot define macro within macro")
            else:
                self.macros[self.parse_macro].append(line)
            return False, None, None
        if self.parse and operands and '$' in line:
            operands = [self.inst_macro_args(op) for op in operands]
            line = self.instline(line)
        if mnemonic and mnemonic[0] == '.':
            code.process_label(self.parser.lidx, label, 0)
            name = mnemonic[1:]
            if name in self.macros:
                if self.parse:
                    self.parser.open(macro=name, ops=operands)
            else:
                try:
                    fn = getattr(Preprocessor, name)
                except AttributeError:
                    raise AsmError("Invalid preprocessor directive")
                try:
                    fn(self, code, operands)
                except (IndexError, ValueError):
                    raise AsmError("Syntax error")
            return False, None, None
        else:
            return self.parse, operands, line


class Parser:
    """scanner and parser class"""

    def __init__(self, symbols, syntax, include_path=None, warnings=True):
        self.prep = Preprocessor(self)
        self.symbols = symbols
        self.syntax = Syntax.get(syntax)
        self.text_literals = []
        self.fn = None
        self.path = None
        self.source = None
        self.macro_args = []
        self.lino = -1
        self.suspended_files = []
        self.include_path = include_path or ["."]
        self.pass_no = 0
        self.lidx = 0
        self.fmt_mode = False
        self.for_loops = []
        self.warnings = []
        self.warnings_enabled = warnings

    def reset(self, code):
        """reset state for new assembly pass"""
        self.fmt_mode = False
        self.for_loops = []
        code.reset_gen()

    def warn(self, message):
        # warn in pass 2 to avoid duplicates and to prevent false expr values 0
        if self.warnings_enabled and self.pass_no > 0 and message not in self.warnings:
            self.warnings.append(message)

    def open(self, filename=None, macro=None, ops=None):
        """open new source file or macro buffer"""
        if len(self.suspended_files) > 100:
            raise AsmError("Too many nested files or macros")
        if self.source is not None:
            self.suspended_files.append((self.fn, self.path, self.source, self.macro_args, self.lino))
        if filename:
            newfile = "-" if filename == "-" else self.find(filename)
            if newfile is None:
                raise AsmError("Could not find file " + filename)
            self.path, fn = os.path.split(newfile)
            self.fn = "> " + fn
            try:
                self.source = readlines(newfile, "r")
            except IOError as e:
                raise AsmError(e)
        else:
            # set self.fn here to indicate macro instantiation in list file
            self.source = self.prep.macros[macro]
            self.macro_args = ops or []
        self.lino = 0

    def resume(self):
        """close current source file and resume previous one"""
        try:
            self.fn, self.path, self.source, self.macro_args, self.lino = self.suspended_files.pop()
            return True
        except IndexError:
            self.fn, self.path, self.source, self.macro_args, self.lino = None, None, None, None, -1
            return False

    def stop(self):
        """stop reading source"""
        while self.resume():
            pass

    def find(self, filename):
        """locate file that matches native filename or TI filename"""
        include_path = [self.path] + self.include_path if self.path else self.include_path
        ti_name = re.match(r"DSK\d?\.(.*)", filename)
        if ti_name:
            native_name = ti_name.group(1)
            extensions = ["", ".g99", ".G99", ".gpl", ".GPL", ".g", ".G"]
        else:
            native_name = filename
            extensions = [""]
        for i in include_path:
            for e in extensions:
                include_file = os.path.join(i, native_name + e)
                if os.path.isfile(include_file):
                    return include_file
                include_file = os.path.join(i, native_name.lower() + e)
                if os.path.isfile(include_file):
                    return include_file
        raise AsmError("File not found")

    def read(self):
        """get next logical line from source files"""
        while self.source is not None:
            try:
                line = self.source[self.lino]
                self.lino += 1
                return self.lino, line.rstrip(), self.fn
            except IndexError:
                self.resume()
        return None, None, None

    def line(self, line):
        """parse single source line"""
        if not line or line[0] == "*":
            return None, None, None, None, False
        parts = self.escape(line).split(";")
        fields = re.split(r"\s+", parts[0], maxsplit=1)
        label = fields[0]
        instruction = fields[1] if len(fields) > 1 else ""
        # convert to native syntax
        for pat, repl in self.syntax.repls:
            instruction = re.sub(pat, repl, instruction)
        # analyze instruction
        fields = re.split(r"\s+", instruction, maxsplit=1)
        mnemonic = fields[0]
        optext = fields[1] if len(fields) > 1 else ""
        # arguments
        opfields = re.split(r" {2,}|\t", optext, maxsplit=1)
        operands = ([op.strip() for op in opfields[0].split(",")]
                    if opfields[0] else [])
        comment = " ".join(opfields[1:]) + ";".join(parts[1:])
        return label, mnemonic, operands, comment, True

    def escape(self, text):
        """remove and save text literals from line"""
        parts = re.split(r"('(?:[^']|'')*'|\"[^\"]*\")", text)  # not-lit, lit, not-lit, lit, ...
        literals = [s[1:-1].replace(self.syntax.tdelim * 2, self.syntax.tdelim)
                    for s in parts[1::2]]  # unquote text delimiters
        parts[1::2] = ["%c%s%c" % (self.syntax.tdelim, len(self.text_literals) + i, self.syntax.tdelim)
                       for i in xrange(len(literals))]
        self.text_literals.extend(literals)
        return "".join(parts).upper()

    def parse(self, code):
        """parse source code and generate object code"""
        source, errors = [], []
        # prepare source (pass 0)
        self.pass_no = 0
        self.lidx = 0
        prev_label = None
        # pass 0
        while True:
            # get next source line
            lino, line, filename = self.read()
            if lino is None:
                break
            try:
                # break line into fields
                label, mnemonic, operands, comment, stmt = self.line(line)
                keep, operands, line = self.prep.process(code, label, mnemonic, operands, line)
                if not keep:
                    continue
                source.append((lino, label, mnemonic, operands, line, filename, stmt))
                if not stmt:
                    continue
                self.lidx += 1
                # process continuation label
                if prev_label:
                    if label:
                        raise AsmError("Invalid continuation for label")
                    label, prev_label = prev_label, None
                elif label[-1:] == ":" and not mnemonic:
                    prev_label = label
                    continue
                if label[-1:] == ":":
                    label = label[:-1]
                # process directives only
                Directives.process(self, code, label, mnemonic, operands) or \
                    Opcodes.process(self, code, label, mnemonic, operands)
            except AsmError as e:
                errors.append("%s <1> %04d - %s\n***** %s\n" % (
                    filename, lino, line, e.message))
        if self.prep.parse_branches:
            errors.append("***** Error: Missing .endif\n")
        if self.prep.parse_macro:
            errors.append("***** Error: Missing .endm\n")
        if errors:
            return errors
        # code generation (passes 1+)
        while True:
            self.pass_no += 1
            if self.pass_no > 32:
                errors.append("Too many assembly passes, aborting. :-(\n")
                break
            self.reset(code)
            self.lidx = 0
            errors = []
            for lino, label, mnemonic, operands, line, filename, stmt in source:
                code.list(lino, line=line)
                if not stmt:
                    continue
                self.lidx += 1
                # process continuation label
                if prev_label:
                    if label:
                        raise AsmError("Invalid continuation for label")
                    label, prev_label = prev_label, None
                elif label[-1:] == ":" and not mnemonic:
                    prev_label = label
                    continue
                if label[-1:] == ":":
                    label = label[:-1]
                # process directives and opcodes
                try:
                    Directives.process(self, code, label, mnemonic, operands) or \
                        Opcodes.process(self, code, label, mnemonic, operands)
                except AsmError as e:
                    errors.append("%s <%d> %04d - %s\n***** %s\n" % (
                        filename, self.pass_no, lino, line, e.message))
                for msg in self.warnings:
                    sys.stderr.write("%s <2> %04d - Warning: %s\n" % (filename, lino, msg))
                self.warnings = []  # warnings per line
            if self.fmt_mode:
                self.warn("Source ends with open FMT block")
            if errors and self.pass_no > 1 or not self.symbols.updated:
                break
        return errors

    def value(self, op):
        """parse well-defined value"""
        e = self.expression(op)
        return e.addr if isinstance(e, Address) else e

    def label(self, op):
        """parse label"""
        s = op[len(self.syntax.gprefix):] if op.startswith(self.syntax.gprefix) else op
        addr = self.expression(s)
        return addr.addr if isinstance(addr, Address) else addr

    def move(self, ops):
        """parse MOVE instruction"""
        m = re.match(self.syntax.moveops, ",".join(ops))
        if not m:
            raise AsmError("Syntax error")
        parts = m.groups()
        ln = self.gaddress(parts[0].strip(), is_gs=True, is_d=True)
        gs = self.gaddress(parts[1].strip(), is_gs=True, is_d=True, is_move=True)
        gd = self.gaddress(parts[2].strip(), is_gs=False, is_d=True, is_move=True)
        rbit = 0b10000 if not gd.grom else 0
        vbit = 0b01000 if gd.vreg or (gd.grom and gd.index) else 0
        cbit = 0b00100 if not gs.grom or gs.indirect else 0
        ibit = 0b00010 if gs.grom and (gs.index or gs.indirect) else 0
        nbit = 0b00001 if ln.immediate else 0
        oo = rbit | vbit | cbit | ibit | nbit
        return oo, ln, gd, gs

    def fmtcount(self, op, max_count=32):
        """parse FMT count"""
        count = self.expression(op)
        if self.pass_no > 0 and count > max_count:
            raise AsmError("Count cannot exceed %d here" % max_count)
        return count

    def fmttext(self, ops):
        """parse FMT text"""
        ts = [self.text(op) for op in ops]
        if any([len(t) > 32 for t in ts]):
            raise AsmError("Text length cannot exceed 32 characters")
        vs = [ord(c) for t in ts for c in t]
        return [len(vs)] + vs

    def fmtbias(self, ops):
        """parse FMT BIAS"""
        bias = self.gaddress(ops[0], is_gs=True)
        if bias.immediate:
            return 1, bias.addr & 0xff
        else:
            return 2, bias

    def gaddress(self, op, is_gs, is_d=False, is_move=False, plain_only=False):
        """parse general source or destination address operand"""
        m = re.match(self.syntax.ga, op)
        if m:
            addr = m.group(1) or "C"
            vram = addr[0] == "V"
            grom = addr[0] == "G"
            vreg = m.group(2) is not None
            indirect = addr[-1] == "*"
            value = self.expression(m.group(3))
            index = self.expression(m.group(4)) if m.group(4) else None
            if index is not None and 0x00 <= index <= 0xff:
                index += 0x8300
            elif self.pass_no > 0 and index is not None and not 0x8300 <= index <= 0x83ff:
                raise AsmError("Index out of range: >%04X" % index)
            if vreg and not (is_move and not is_gs):
                raise AsmError("Invalid VDP register outside MOVE")
            if self.pass_no > 0 and vreg and not 0 <= value <= 7:
                raise AsmError("VDP register out of range: %d" % value)
            if grom and not is_move:
                raise AsmError("Invalid GROM address outside MOVE")
            if plain_only and (grom or vram or vreg or indirect or index):
                raise AsmError("Invalid address format, only '@>xxxx' allowed here")
            return Operand(value, vram=vram, grom=grom, vreg=vreg, indirect=indirect, index=index)
        if is_gs:
            # immediate value as address
            if is_move:
                self.warn("Treating '%s' as ROM address, did you intend a GROM address?" % op)
            value = self.expression(op)
            return Operand(value, imm=2 if is_d else 1)
        raise AsmError("Invalid G%c address operand: %s" % ("s" if is_gs else "d", op))

    def expression(self, expr, needed=False):
        """parse complex arithmetical expression"""
        value = Word(0, pass_no=self.pass_no)
        terms = ["+"] + [tok.strip() for tok in
                         re.split(r"([-+/%~&|^()]|\*\*?)", expr)]
        i, stack = 0, []
        while i < len(terms):
            op, term, negate, corr = terms[i], terms[i + 1], False, 0
            i += 2
            if op == ")":
                v = value.value
                value, op, negate, corr = stack.pop()
            else:
                # unary operators
                while not term and i < len(terms) and terms[i] in "+-~(":
                    term = terms[i + 1]
                    if terms[i] == "-":
                        negate = not negate
                    elif terms[i] == "~":
                        negate, corr = not negate, corr + (1 if negate else -1)
                    elif terms[i] == "(":
                        stack.append((value, op, negate, corr))
                        op, term, negate, corr = "+", terms[i + 1], False, 0
                        value = Word(0)
                    i += 2
                term_val = self.term(term, needed)
                if isinstance(term_val, Local):
                    dist = -term_val.distance if negate else term_val.distance
                    term_val = self.symbols.get_local(term_val.name, self.lidx, dist, self.pass_no)
                    negate = False
                if term_val is None:
                    raise AsmError("Invalid expression: " + term)
                v = term_val.addr if isinstance(term_val, Address) else term_val
            w = Word((-v if negate else v) + corr)
            if op == "+":
                value.add(w)
            elif op == "-":
                value.sub(w)
            elif op in "*/%":
                value.mul(op, w)
            elif op in "&|^":
                value.bit(op, w)
            elif op == "**":
                base, exp = Word(1), w.value
                for j in xrange(exp):
                    base.mul("*", value)
                value = base
            else:
                raise AsmError("Invalid operator: " + op)
        return value.value

    def term(self, op, needed=False):
        """parse term"""
        if op[0] == ">":
            return int(op[1:], 16)
        elif op[0] == ":":
            return int(op[1:], 2)
        elif op.isdigit():
            return int(op)
        elif op == "$":
            return Address(self.symbols.LC)
        elif op[0] == "!":
            m = re.match("(!+)(.*)", op)
            return Local(m.group(2), len(m.group(1)))
        elif op[0] == op[-1] == self.syntax.tdelim:
            c = self.text_literals[int(op[1:-1])]
            if len(c) == 1:
                return ord(c[0])
            elif len(c) == 2:
                return ord(c[0]) << 8 | ord(c[1])
            elif len(c) == 0:
                return 0
            else:
                raise AsmError("Invalid text literal: " + c)
        else:
            v = self.symbols.get_symbol(op, pass_no=self.pass_no, check=True, needed=needed)
            return v

    def text(self, op):
        """parse quoted text literal or byte string"""
        try:
            if op[0] == ">":
                op0 = op + "0"
                return "".join([chr(int(op0[i:i + 2], 16))
                                for i in xrange(1, len(op), 2)])
            elif op[0] == op[-1] == self.syntax.tdelim:
                return self.text_literals[int(op[1:-1])]
        except (IndexError, ValueError):
            pass
        raise AsmError("Invalid text literal: " + op)

    def radix100(self, op):
        """parse floating-point number and convert to radix-100 format"""
        sign, digits = (-1, op[1:]) if op[0] == '-' else (+1, op)  # sign
        # find hundreds
        try:
            int_part, frac_part = digits.strip("0").split('.')  # with decimal point
        except ValueError:
            int_part, frac_part = digits.lstrip("0"), ""  # no decimal point
        if not int_part:
            if not frac_part:
                return [0] * 8  # op is zero
            while frac_part[:2] == "00":  # only faction
                frac_part = frac_part[2:]
        elif len(int_part) % 2 == 1:
            int_part = "0" + int_part
        # build mantissa
        mantissa = int_part + frac_part + "00000000000000"
        hundreds = [int(mantissa[i:i + 2]) for i in xrange(0, 14, 2)]
        # get exponent
        try:
            exponent = int(math.floor(math.log(float(digits), 100)))  # digits != 0
        except ValueError:
            raise AsmError("Bad format for floating point number: " + op)
        # invert first word if negative
        bytes_ = [exponent + 0x40] + hundreds
        if sign < 0:
            bytes_[1] = 0x100 - bytes_[1]  # cannot yield 0x100 for bytes_[1], since always != 0
            bytes_[0] = ~bytes_[0] & 0xff
        # return radix-100 format
        return bytes_

    def filename(self, op):
        """parse double-quoted filename"""
        if len(op) < 3:
            raise AsmError("Invalid filename: " + op)
        if op[0] == op[-1] == self.syntax.tdelim:
            return self.text_literals[int(op[1:-1])]
        return op[1:-1]

    @staticmethod
    def symconst(op):
        """parse symbol constant (-D option)"""
        try:
            return int(op[1:], 16) if op[0] == ">" else int(op)
        except ValueError:
            return op


# Main assembler

class Assembler:
    """main driver class"""

    def __init__(self, syntax, grom, aorg, target="", include_path=None, defs=(), warnings=True):
        self.syntax = syntax
        self.grom = grom
        self.aorg = aorg
        self.include_path = include_path
        self.defs = ["_xga99_" + target] + list(defs)
        self.warnings = warnings

    def assemble(self, srcname):
        symbols = Symbols(add_defs=self.defs)
        code = Objcode(symbols, self.grom, self.aorg)
        parser = Parser(symbols,
                        syntax=self.syntax,
                        include_path=self.include_path,
                        warnings=self.warnings)
        parser.open(srcname)
        errors = parser.parse(code)
        return code, errors


# Command line processing

def main():
    import argparse, zipfile

    args = argparse.ArgumentParser(
        description="GPL cross-assembler, v" + VERSION)
    args.add_argument("source", metavar="<source>",
                      help="GPL source code")
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument("-i", "--image", action="store_true", dest="image",
                     help="create GROM image with GPL header data")
    cmd.add_argument("-c", "--cart", action="store_true", dest="cart",
                     help="create MESS cartridge image")
    cmd.add_argument("-t", "--text", dest="text", nargs="?", metavar="<format>",
                     help="create text file with binary values")
    cmd.add_argument("--dump", action="store_true", dest="dump",
                     help=argparse.SUPPRESS)  # debugging
    args.add_argument("-n", "--name", dest="name", metavar="<name>",
                      help="set program name")
    args.add_argument("-G", "--grom", dest="grom", metavar="<GROM>",
                      help="set GROM base address")
    args.add_argument("-A", "--aorg", dest="aorg", metavar="<origin>",
                      help="set AORG origin in GROM for byte code")
    args.add_argument("-y", "--syntax", dest="syntax", metavar="<style>",
                      help="set syntax style (xdt99, rag, mizapf)")
    args.add_argument("-I", "--include", dest="inclpath", metavar="<paths>",
                      help="list of include search paths")
    args.add_argument("-D", "--define-symbol", nargs="+", dest="defs",
                      metavar="<sym=val>",
                      help="add symbol to symbol table")
    args.add_argument("-L", "--list", dest="list", metavar="<file>",
                      help="generate list file")
    args.add_argument("-S", "--symbol-table", action="store_true", dest="symtab",
                      help="add symbol table to list file")
    args.add_argument("-E", "--symbol-file", dest="equs", metavar="<file>",
                      help="put symbols in EQU file")
    args.add_argument("-w", action="store_true", dest="nowarn",
                      help="hide warnings")
    args.add_argument("-o", "--output", dest="output", metavar="<file>",
                      help="set output file name")
    opts = args.parse_args()

    # setup
    dirname = os.path.dirname(opts.source) or "."
    basename = os.path.basename(opts.source)
    barename = os.path.splitext(basename)[0]
    # output = opts.output or (
    #     barename + ".rpk" if opts.cart else
    #     barename + ".bin" if opts.image else
    #     barename + ".dat" if opts.text else
    #     barename + ".gbc"
    #     )
    name = opts.name or barename[:16].upper()
    grom = (xint(opts.grom) if opts.grom is not None else
            0x6000 if opts.cart else 0x0000)
    aorg = (xint(opts.aorg) if opts.aorg is not None else
            0x0030 if opts.cart else 0x0000)
    inclpath = [dirname] + (opts.inclpath.split(",") if opts.inclpath else [])

    # assembly
    target = ("image" if opts.image else
              "cart" if opts.cart else
              "gbc")
    asm = Assembler(target=target,
                    syntax=opts.syntax or "xdt99",
                    grom=grom,
                    aorg=aorg,
                    include_path=inclpath,
                    defs=opts.defs or (),
                    warnings=not opts.nowarn)
    try:
        # assemble
        code, errors = asm.assemble(basename)

        # output
        if errors:
            sys.stderr.write("".join(errors))
        elif opts.dump:
            sys.stdout.write(code.generate_dump())
        elif opts.cart:
            data, layout, metainf = code.generate_cart(name)
            try:
                with zipfile.ZipFile(outname(barename, ".zip", output=opts.output), "w") as archive:
                    archive.writestr(name + ".bin", data)
                    archive.writestr("layout.xml", layout)
                    archive.writestr("meta-inf.xml", metainf)
            except IOError as e:
                sys.exit("File error: %s: %s." % (e.filename, e.strerror))
        else:
            if opts.image:
                result = ((None, code.generate_image(name)),)
                extension = ".img"
                mode = "wb"
            elif opts.text:
                byte_code = code.generate_byte_code()
                result = ((None, code.generate_text(byte_code, opts.text.lower())),)
                extension = ".dat"
                mode = "w"
            else:
                byte_code = code.generate_byte_code()
                result = [("%04x" % grom, bytes_) for (grom, base, bytes_) in byte_code]
                extension = ".gbc"
                mode = "wb"
            count = len(result)
            for addr, data in result:
                writedata(outname(barename, extension, output=opts.output, addition=addr, count=count),
                          data,
                          mode)
        if opts.list:
            listing = code.generate_list(opts.symtab)
            writedata(opts.list, listing, "w")
        if opts.equs:
            writedata(opts.equs, code.generate_symbols(equ=True))
    except IOError as e:
        sys.exit("File error: %s: %s." % (e.filename, e.strerror))
    except AsmError as e:
        sys.exit("Error: %s" % e)

    # return status
    return 1 if errors else 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
