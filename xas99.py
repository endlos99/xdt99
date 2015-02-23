#!/usr/bin/env python

# xas99: A TMS9900 cross-assembler
#
# Copyright (c) 2015 Ralph Benzinger <xdt99@endlos.net>
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
import re
import os.path

VERSION = "1.2.0"


### Utility functions

def ordw(word):
    """word ord"""
    return ord(word[0]) << 8 | ord(word[1])


def chrw(word):
    """word chr"""
    return chr(word >> 8) + chr(word & 0xFF)


### Error handling

class AsmError(Exception):
    pass


### Symbol table

class Address:
    """absolute or relocatable address"""

    def __init__(self, addr, relocatable=False):
        self.addr = addr
        self.relocatable = relocatable


class Reference:
    """external reference"""

    def __init__(self, name):
        self.name = name


class Block:
    """reserved block of bytes"""

    def __init__(self, size):
        self.size = size


class Symbols:
    """symbol table and line counter"""

    def __init__(self, addRegisters=False, addDefs=None):
        self.symbols = {
            "R" + str(i): i for i in xrange(16)
            } if addRegisters else {}
        self.exts = {
            "VSBW": 0x210C, "VMBW": 0x2110,
            "VSBR": 0x2114, "VMBR": 0x2118,
            "VWTR": 0x211C, "KSCAN": 0x2108,
            "GPLLNK": 0x2100, "XMLLNK": 0x2104,
            "DSRLNK": 0x2120, "LOADER": 0x2124,
            "UTLTAB": 0x2022, "SCAN": 0x000E,
            "PAD": 0x8300, "GPLWS": 0x83E0,
            "SOUND": 0x8400,
            "VDPRD": 0x8800, "VDPSTA": 0x8802,
            "VDPWD": 0x8C00,
            "SPCHRD": 0x9000, "SPCHWT": 0x9400,
            "GRMRD": 0x9800, "GRMRA": 0x9802,
            "GRMWD": 0x9C00, "GRMWA": 0x9C02
            }
        for d in addDefs or []:
            parts = d.upper().split("=")
            val = Parser.symconst(parts[1]) if len(parts) > 1 else 1
            self.symbols[parts[0]] = val
        self.refdefs = []
        self.xops = {}
        self.idt = "        "
        self.resetLC()

    def resetLC(self):
        self.LC = 0
        self.relocLC = True

    def addSymbol(self, name, value):
        if name in self.symbols:
            raise AsmError("Multiple symbols: " + name)
        self.symbols[name] = value

    def addLabel(self, label):
        self.addSymbol(label, Address(self.LC, self.relocLC))

    def addDef(self, name):
        if name in self.refdefs:
            raise AsmError("Multiple symbols")
        self.refdefs.append(name)

    def addRef(self, name):
        if name in self.refdefs:
            return
        self.refdefs.append(name)
        self.addSymbol(name, Reference(name))

    def addXop(self, name, mode):
        self.xops[name] = mode

    def getSymbol(self, name):
        return self.symbols.get(name)


### Code generation

class Objdummy:
    """dummy code generation for keeping track of line counter"""

    def __init__(self, symbols):
        self.symbols = symbols
        self.savedLC = {True: 0x0000, False: 0x0000}
        self.segment(0x0000, relocatable=True, init=True)

    def segment(self, base, relocatable=False, dummy=False, init=False):
        if not init:
            self.savedLC[self.symbols.relocLC] = self.symbols.LC
        self.symbols.relocLC = relocatable
        self.symbols.LC = self.savedLC[relocatable] if base is None else base

    def even(self):
        if self.symbols.LC % 2 == 1:
            self.symbols.LC += 1

    def byte(self, byte):
        self.symbols.LC += 1

    def word(self, word):
        self.even()
        self.symbols.LC += 2

    def block(self, size):
        self.symbols.LC += size

    def emit(self, opcode, saddr=None, daddr=None):
        self.even()
        self.symbols.LC += 2 + (
            2 if saddr is not None else 0) + (
            2 if daddr is not None else 0)

    def processLabel(self, label):
        if label:
            self.symbols.addLabel(label)


class Objcode:
    """generate object code"""

    def __init__(self, symbols):
        self.symbols = symbols
        self.entry = None
        self.segments = []
        self.savedLC = { True: 0x0000, False: 0x0000 }
        self.segment(0x0000, relocatable=True, init=True)
        self.done = False

    def processLabel(self, label):
        pass

    def segment(self, base, relocatable=False, dummy=False, init=False):
        if not init:
            self.savedLC[self.symbols.relocLC] = self.symbols.LC
            self.segments.append((self.base, self.symbols.LC,
                                  self.symbols.relocLC, self.dummy,
                                  self.code))
        self.base = self.savedLC[relocatable] if base is None else base
        self.symbols.relocLC = relocatable
        self.symbols.LC = self.base
        self.dummy = dummy
        self.code = []

    def even(self):
        if self.symbols.LC % 2 == 1:
            self.symbols.LC += 1

    def byte(self, byte):
        byte %= 0x100
        if self.symbols.LC % 2 == 0:
            self.code.append((self.symbols.LC, byte << 8))
        else:
            prevLC, prevWord = self.code[-1] if self.code else (0, None)
            if self.symbols.LC == prevLC + 1 and isinstance(prevWord, int):
                self.code[-1] = (self.symbols.LC - 1, prevWord | byte)
            else:
                self.code.append((self.symbols.LC - 1, byte))
        self.symbols.LC += 1

    def word(self, word):
        self.even()
        self.code.append((self.symbols.LC, word))
        self.symbols.LC += 2

    def block(self, size):
        self.code.append((self.symbols.LC, Block(size)))
        self.symbols.LC += size

    def emit(self, opcode, saddr=None, daddr=None):
        self.word(opcode)
        if saddr is not None:
            self.word(saddr)
        if daddr is not None:
            self.word(daddr)

    def genDump(self):
        """generate raw dump of internal data structures (debug)"""
        self.prepare()
        dump = ""
        for (base, finalLC, reloc, dummy, code) in self.segments:
            dump += "%s%cORG @ >%04X:\n" % (
                "\n" if dump and dump[-1] != "\n" else "",
                "R" if reloc else "D" if dummy else "A",
                base)
            for i, (LC, w) in enumerate(code):
                if i % 8 == 0:
                    dump += "%04X:  " % LC
                if isinstance(w, Address):
                    dump += "%04X%c " % (w.addr, "r" if w.relocatable else "a")
                elif isinstance(w, Reference):
                    dump += "%-6s" % (w.name[:6])
                elif isinstance(w, Block):
                    dump += "%04X# " % w.size
                else:
                    dump += "%04X  " % w
                if i % 8 == 7:
                    dump += "\n"
        return dump if dump[-1] == "\n" else dump + "\n"

    def genObjCode(self):
        """generate object code (E/A option 3)"""
        self.prepare()
        tags = Records()
        relocLCs = [finalLC for base, finalLC, reloc, dummy, code
                    in self.segments if reloc]
        relocSize = relocLCs[-1] if relocLCs else 0
        tags.add("0%04X%-8s" % (relocSize, self.symbols.idt))
        # add code and data words section
        refs = {}
        for base, finalLC, reloc, dummy, code in self.segments:
            if dummy:
                continue
            tags.addLC()
            for LC, w in code:
                if isinstance(w, Address):
                    tags.add("%c%04X" % (
                        "C" if w.relocatable else "B", w.addr), LC, reloc)
                elif isinstance(w, Reference):
                    prevLC, prevReloc = refs.get(w.name, (0, False))
                    tags.add("%c%04X" % ("C" if prevReloc else "B", prevLC),
                             LC, reloc)
                    refs[w.name] = (LC, reloc)
                elif isinstance(w, Block):
                    tags.add("%c%04X" % ("A" if reloc else "9", LC))
                    tags.addLC()
                else:
                    tags.add("B%04X" % w, LC, reloc)
        tags.flush()
        # program entry
        if self.entry:
            tags.add("%c%04X" % ("2" if self.entry.relocatable else "1",
                                 self.entry.addr))
            tags.flush()
        # add def and ref symbols section
        for s in self.symbols.refdefs:
            symbol = self.symbols.getSymbol(s)
            if isinstance(symbol, Reference):
                prevLC, prevReloc = refs.get(s, (0, False))
                tags.add("%c%04X%-6s" % (
                    "3" if prevReloc else "4", prevLC, s[:6]))
            elif symbol:
                reloc = isinstance(symbol, Address) and symbol.relocatable
                addr = symbol.addr if isinstance(symbol, Address) else symbol
                tags.add("%c%04X%-6s" % ("5" if reloc else "6", addr, s[:6]))
        # closing section
        tags.flush()
        tags.append(":       99/4 AS")
        return tags.dump()

    def genImage(self, baseAddr=0xA000):
        """generate memory image (E/A option 5)"""
        self.prepare()
        sload = self.symbols.getSymbol("SLOAD") or Address(baseAddr)
        loadAddr = sload.addr + baseAddr if sload.relocatable else sload.addr
        mem = {}
        for base, finalLC, reloc, dummy, code in self.segments:
            if dummy:
                continue
            for LC, w in code:
                addr = LC + baseAddr if reloc else LC
                if isinstance(w, Address):
                    mem[addr] = w.addr + baseAddr if w.relocatable else w.addr
                elif isinstance(w, Reference):
                    if w.name not in self.symbols.exts:
                        raise AsmError("Unknown reference: " + w.name)
                    mem[addr] = self.symbols.exts.get(w.name, 0x0000)
                elif isinstance(w, Block):
                    a, s = (addr, (w.size + 1) / 2) if addr % 2 == 0 else \
                           (addr + 1, w.size / 2)
                    for i in xrange(s / 2):
                        mem[a + i] = 0x0000
                else:
                    mem[addr] = w
        addrs = mem.keys()
        sfirst = self.symbols.getSymbol("SFIRST") or Address(min(addrs))
        minAddr = sfirst.addr + baseAddr if sfirst.relocatable else sfirst.addr
        slast = self.symbols.getSymbol("SLAST") or Address(max(addrs) + 2)
        maxAddr = slast.addr + baseAddr if slast.relocatable else slast.addr
        size = maxAddr - minAddr + 6
        words = "".join([chrw(mem[addr]) if addr in mem else "\x00\x00"
                         for addr in xrange(minAddr, maxAddr, 2)])
        if size % 2 == 1:
            words = words[:-1]
        return "\x00\x00" + chrw(size) + chrw(loadAddr) + words

    def genCart(self, name):
        """generate RPK file for use as MESS rom cartridge"""
        self.prepare()
        send = self.entry or Address(0x6030)
        entry = send.addr + 0x6030 if send.relocatable else send.addr
        gpl = "\xaa\x01\x00\x00\x00\x00\x60\x10" + "\x00" * 8
        proginfo = "\x00\x00%s%c%s" % (chrw(entry), len(name), name)
        pad = "\x00" * (27 - len(name))
        code = self.genImage(0x6030)[6:]
        layout = """<?xml version="1.0" encoding="utf-8"?>
                    <romset version="1.0">
                        <resources>
                            <rom id="romimage" file="%s.bin"/>
                        </resources>
                        <configuration>
                            <pcb type="standard">
                                <socket id="rom_socket" uses="romimage"/>
                            </pcb>
                        </configuration>
                    </romset>""" % name
        metainf = """<?xml version="1.0"?>
                     <meta-inf>
                         <name>%s</name>
                     </meta-inf>""" % name
        return gpl + proginfo + pad + code, layout, metainf

    def prepare(self):
        """wrap-up code generation"""
        if not self.done:
            self.segment(None, relocatable=False, dummy=False)
            self.done = True


class Records:
    """object code tag and record handling"""

    def __init__(self):
        self.records = []
        self.record = ""
        self.needsLC = True

    def add(self, tag, LC=None, reloc=False):
        """add tag to records"""
        addLC = self.needsLC and LC is not None
        tagPenalty = (5 if tag[0] in "9A" else 0) + (5 if addLC else 0)
        if len(self.record) + len(tag) + tagPenalty > 64:
            self.flush()
            addLC = LC is not None
        tagLC = ("%c%04X" % ("A" if reloc else "9", LC)) if addLC else ""
        self.record += tagLC + tag
        self.needsLC = False

    def addLC(self):
        """add LC tag for next object code tag"""
        self.needsLC = True

    def append(self, record):
        """add predefined record"""
        self.records.append(record)

    def flush(self):
        """close current record and add checksum"""
        checksum = reduce(lambda s, c: s + ord(c), self.record, ord("7"))
        self.records.append(self.record +
                            "7%04XF" % (~checksum + 1 & 0xFFFF) +
                            " " * (69 - len(self.record)))
        self.record = ""
        self.addLC()

    def dump(self):
        """dump records as DIS/FIX80"""
        lines = ["%-75s %04d\n" % (line, i + 1)
                 for i, line in enumerate(self.records)]
        return "".join(lines)


class Word:
    """auxiliary class for word arithmetic"""

    def __init__(self, value):
        self.value = value % 0x10000

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


### Directives

class Directives:
    @staticmethod
    def DEF(parser, code, label, ops):
        if parser.passno != 1:
            return
        code.processLabel(label)
        for op in ops:
            code.symbols.addDef(op[:6] if parser.strictMode else op)

    @staticmethod
    def REF(parser, code, label, ops):
        if parser.passno != 1:
            return
        for op in ops:
            code.symbols.addRef(op[:6] if parser.strictMode else op)

    @staticmethod
    def EQU(parser, code, label, ops):
        if parser.passno != 1:
            return
        value = parser.expression(ops[0], wellDefined=True)
        code.symbols.addSymbol(label, value)

    @staticmethod
    def DATA(parser, code, label, ops):
        code.even()
        code.processLabel(label)
        for op in ops:
            w = parser.expression(op)
            code.word(w)

    @staticmethod
    def BYTE(parser, code, label, ops):
        code.processLabel(label)
        for op in ops:
            b = parser.expression(op)
            code.byte(b)

    @staticmethod
    def TEXT(parser, code, label, ops):
        code.processLabel(label)
        for op in ops:
            text = parser.text(op)
            for c in text:
                code.byte(ord(c))

    @staticmethod
    def BSS(parser, code, label, ops):
        code.processLabel(label)
        size = parser.value(ops[0])
        code.block(size)

    @staticmethod
    def BES(parser, code, label, ops):
        size = parser.value(ops[0])
        code.block(size)
        code.processLabel(label)

    @staticmethod
    def EVEN(parser, code, label, ops):
        code.even()
        code.processLabel(label)  # differs from E/A manual!

    @staticmethod
    def AORG(parser, code, label, ops):
        base = parser.value(ops[0]) if ops else None
        code.segment(base, relocatable=False)
        code.processLabel(label)

    @staticmethod
    def RORG(parser, code, label, ops):
        base = parser.value(ops[0]) if ops else None
        code.segment(base, relocatable=True)
        code.processLabel(label)

    @staticmethod
    def DORG(parser, code, label, ops):
        base = parser.value(ops[0]) if ops else None
        code.segment(base, dummy=True)
        code.processLabel(label)

    @staticmethod
    def COPY(parser, code, label, ops):
        code.processLabel(label)
        filename = parser.filename(ops[0])
        parser.open(filename)

    @staticmethod
    def END(parser, code, label, ops):
        code.processLabel(label)
        if ops:
            code.entry = code.symbols.getSymbol(
                ops[0][:6] if parser.strictMode else ops[0])
        parser.stop()

    @staticmethod
    def IDT(parser, code, label, ops):
        if parser.passno != 1:
            return
        code.processLabel(label)
        text = parser.text(ops[0]) if ops else "        "
        code.symbols.idt = text[:8]

    @staticmethod
    def DXOP(parser, code, label, ops):
        if parser.passno != 1:
            return
        if len(ops) != 2:
            raise AsmError("Invalid arguments")
        code.processLabel(label)
        mode = parser.expression(ops[1], wellDefined=True)
        code.symbols.addXop(ops[0], str(mode))

    ignores = [
        "",
        "PSEG", "PEND", "CSEG", "CEND", "DSEG", "DEND",
        "UNL", "LIST", "PAGE", "TITL", "LOAD", "SREF"
        ]

    @staticmethod
    def process(parser, code, label, mnemonic, operands):
        if mnemonic in Directives.ignores:
            code.processLabel(label)
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


class Preprocessor:
    """xdt99-specific preprocessor extensions"""

    def __init__(self, parser):
        self.parser = parser
        self.parse = True
        self.parseBranches = []

    def args(self, ops):
        lhs = self.parser.expression(
            ops[0], wellDefined=True, relaxed=True)
        rhs = self.parser.expression(
            ops[1], wellDefined=True, relaxed=True) if len(ops) > 1 else 0
        return lhs, rhs

    def IFDEF(self, code, label, ops):
        self.parseBranches.append(self.parse)
        self.parse = (code.symbols.getSymbol(ops[0]) is not None if self.parse
                      else None)

    def IFNDEF(self, code, label, ops):
        self.parseBranches.append(self.parse)
        self.parse = (code.symbols.getSymbol(ops[0]) is None if self.parse
                      else None)

    def IFEQ(self, code, label, ops):
        self.parseBranches.append(self.parse)
        self.parse = cmp(*self.args(ops)) == 0 if self.parse else None

    def IFNE(self, code, label, ops):
        self.parseBranches.append(self.parse)
        self.parse = cmp(*self.args(ops)) != 0 if self.parse else None

    def IFGT(self, code, label, ops):
        self.parseBranches.append(self.parse)
        self.parse = cmp(*self.args(ops)) > 0 if self.parse else None

    def IFGE(self, code, label, ops):
        self.parseBranches.append(self.parse)
        self.parse = cmp(*self.args(ops)) >= 0 if self.parse else None

    def ELSE(self, code, label, ops):
        self.parse = not self.parse if self.parse is not None else None

    def ENDIF(self, code, label, ops):
        self.parse = self.parseBranches.pop()

    def process(self, code, label, mnemonic, operands):
        if mnemonic[:1] != '.':
            return self.parse
        try:
            fn = getattr(Preprocessor, mnemonic[1:])
        except AttributeError:
            raise AsmError("Invalid preprocessor directive")
        try:
            fn(self, code, label, operands)
        except (IndexError, ValueError):
            raise AsmError("Syntax error")
        return False


### Opcodes

class Opcodes:
    opGa = lambda parser, x: parser.address(x)  # [0x0000 .. 0xFFFF]
    opWa = lambda parser, x: parser.register(x)  # [0 .. 15]
    opIop = lambda parser, x: parser.expression(x)  # [0x0000 .. 0xFFFF]
    opCru = lambda parser, x: parser.expression(x)  # [-128 .. 127]
    opDisp = lambda parser, x: parser.relative(x)  # [-128 .. 127]
    opCnt = lambda parser, x: parser.expression(x)  # [0 .. 15]
    opScnt = lambda parser, x: parser.expression(x)  # [0 .. 15]
    opXop = lambda parser, x: parser.expression(x)  # [1 .. 2]

    opcodes = {
        # 6. arithmetic
        "A": (0xA000, 1, opGa, opGa),
        "AB": (0xB000, 1, opGa, opGa),
        "ABS": (0x0740, 6, opGa, None),  # listed as 4 in E/A Manual
        "AI": (0x0220, 8, opWa, opIop),
        "DEC": (0x0600, 6, opGa, None),
        "DECT": (0x0640, 6, opGa, None),
        "DIV": (0x3C00, 9, opGa, opWa),
        "INC": (0x0580, 6, opGa, None),
        "INCT": (0x05C0, 6, opGa, None),
        "MPY": (0x3800, 9, opGa, opWa),
        "NEG": (0x0500, 6, opGa, None),
        "S": (0x6000, 1, opGa, opGa),
        "SB": (0x7000, 1, opGa, opGa),
        # 7. jump and branch
        "B": (0x0440, 6, opGa, None),
        "BL": (0x0680, 6, opGa, None),
        "BLWP": (0x0400, 6, opGa, None),
        "JEQ": (0x1300, 2, opDisp, None),
        "JGT": (0x1500, 2, opDisp, None),
        "JHE": (0x1400, 2, opDisp, None),
        "JH": (0x1B00, 2, opDisp, None),
        "JL": (0x1A00, 2, opDisp, None),
        "JLE": (0x1200, 2, opDisp, None),
        "JLT": (0x1100, 2, opDisp, None),
        "JMP": (0x1000, 2, opDisp, None),
        "JNC": (0x1700, 2, opDisp, None),
        "JNE": (0x1600, 2, opDisp, None),
        "JNO": (0x1900, 2, opDisp, None),
        "JOP": (0x1C00, 2, opDisp, None),
        "JOC": (0x1800, 2, opDisp, None),
        "RTWP": (0x0380, 7, None, None),
        "X": (0x0480, 6, opGa, None),
        "XOP": (0x2C00, 9, opGa, opXop),
        # 8. compare instructions
        "C": (0x8000, 1, opGa, opGa),
        "CB": (0x9000, 1, opGa, opGa),
        "CI": (0x0280, 8, opWa, opIop),
        "COC": (0x2000, 3, opGa, opWa),
        "CZC": (0x2400, 3, opGa, opWa),
        # 9. control and cru instructions
        "LDCR": (0x3000, 4, opGa, opCnt),
        "SBO": (0x1D00, 2, opCru, None),
        "SBZ": (0x1E00, 2, opCru, None),
        "STCR": (0x3400, 4, opGa, opCnt),
        "TB": (0x1F00, 2, opCru, None),
        "CKOF": (0x03C0, 7, None, None),
        "CKON": (0x03A0, 7, None, None),
        "IDLE": (0x0340, 7, None, None),
        "RSET": (0x0360, 7, None, None),
        "LREX": (0x03E0, 7, None, None),
        # 10. load and move instructions
        "LI": (0x0200, 8, opWa, opIop),
        "LIMI": (0x0300, 81, opIop, None),
        "LWPI": (0x02E0, 81, opIop, None),
        "MOV": (0xC000, 1, opGa, opGa),
        "MOVB": (0xD000, 1, opGa, opGa),
        "STST": (0x02C0, 8, opWa, None),
        "STWP": (0x02A0, 8, opWa, None),
        "SWPB": (0x06C0, 6, opGa, None),
        # 11. logical instructions
        "ANDI": (0x0240, 8, opWa, opIop),
        "ORI": (0x0260, 8, opWa, opIop),
        "XOR": (0x2800, 3, opGa, opWa),
        "INV": (0x0540, 6, opGa, None),
        "CLR": (0x04C0, 6, opGa, None),
        "SETO": (0x0700, 6, opGa, None),
        "SOC": (0xE000, 1, opGa, opGa),
        "SOCB": (0xF000, 1, opGa, opGa),
        "SZC": (0x4000, 1, opGa, opGa),
        "SZCB": (0x5000, 1, opGa, opGa),
        # 12. shift instructions
        "SRA": (0x0800, 5, opWa, opScnt),
        "SRL": (0x0900, 5, opWa, opScnt),
        "SLA": (0x0A00, 5, opWa, opScnt),
        "SRC": (0x0B00, 5, opWa, opScnt)
        # end of opcodes
    }

    pseudos = {
        # 13. pseudo instructions
        "NOP": ("JMP", ["$+2"]),
        "RT": ("B", ["*11"])
    }

    @staticmethod
    def process(parser, code, label, mnemonic, operands):
        """get assembly code for mnemonic"""
        code.even()
        code.processLabel(label)
        if mnemonic in Opcodes.pseudos:
            mnemonic, operands = Opcodes.pseudos[mnemonic]
        elif mnemonic in parser.symbols.xops:
            mode = parser.symbols.xops[mnemonic]
            mnemonic, operands = "XOP", [operands[0], mode]
        if mnemonic in Opcodes.opcodes:
            try:
                opcode, fmt, parse1, parse2 = Opcodes.opcodes[mnemonic]
                arg1 = parse1(parser, operands[0]) if parse1 else None
                arg2 = parse2(parser, operands[1]) if parse2 else None
                Opcodes.generate(code, opcode, fmt, arg1, arg2)
            except (IndexError, ValueError):
                raise AsmError("Syntax error")
        else:
            raise AsmError("Invalid mnemonic: " + mnemonic)

    @staticmethod
    def generate(code, opcode, fmt, arg1, arg2):
        """generate byte code"""
        # I. two general address instructions
        if fmt == 1:
            ts, s, sa = arg1
            td, d, da = arg2
            b = opcode | td << 10 | d << 6 | ts << 4 | s
            code.emit(b, sa, da)
        # II. jump and bit I/O instructions
        elif fmt == 2:
            b = opcode | arg1 & 0xFF
            code.emit(b)
        # III. logical instructions
        elif fmt == 3:
            ts, s, sa = arg1
            d = arg2
            b = opcode | d << 6 | ts << 4 | s
            code.emit(b, sa)
        # IV. CRU multi-bit instructions
        elif fmt == 4:
            ts, s, sa = arg1
            c = arg2
            b = opcode | c << 6 | ts << 4 | s
            code.emit(b, sa)
        # V. register shift instructions
        elif fmt == 5:
            w = arg1
            c = arg2
            b = opcode | c << 4 | w
            code.emit(b)
        # VI. single address instructions
        elif fmt == 6:
            ts, s, sa = arg1
            b = opcode | ts << 4 | s
            code.emit(b, sa)
        # VII. control instructions
        elif fmt == 7:
            b = opcode
            code.emit(b)
        # VIII. immediate instructions
        elif fmt == 8:
            b = opcode | arg1
            code.emit(b, arg2)
        elif fmt == 81:
            b = opcode
            code.emit(b, arg1)
        # IX. extended operations; multiply and divide
        elif fmt == 9:
            ts, s, sa = arg1
            r = arg2
            b = opcode | r << 6 | ts << 4 | s
            code.emit(b, sa)
        else:
            raise AsmError("Invalid opcode format " + str(fmt))


### Parsing

class Parser:
    """scanner and parser class"""

    def __init__(self, symbols, includePath=None, strictMode=False):
        self.prep = Preprocessor(self)
        self.symbols = symbols
        self.textlits = []
        self.path, self.file, self.lino = None, None, -1
        self.suspendedFiles = []
        self.includePath = includePath or ["."]
        self.strictMode = strictMode
        self.parseBranches = [True]
        self.passno = 0

    def open(self, filename):
        """open new source file"""
        newfile = self.find(filename)
        if not newfile:
            raise IOError(1, "File not found", filename)
        if self.file:
            self.suspendedFiles.append((self.path, self.file, self.lino))
        self.path = os.path.dirname(newfile)
        self.file = open(newfile, mode="r")
        self.lino = 0

    def resume(self):
        """close current source file and resume previous one"""
        try:
            self.path, self.file, self.lino = self.suspendedFiles.pop()
            return True
        except IndexError:
            self.path, self.file, self.lino = None, None, -1
            return False

    def stop(self):
        """stop reading source"""
        while self.resume():
            pass

    def find(self, filename):
        """locate file that matches native filename or TI filename"""
        includePath = ([self.path] + self.includePath if self.path else
                       self.includePath)
        tiname = re.match("DSK\d?\.(.*)", filename)
        if tiname:
            nativeName = tiname.group(1)
            extensions = ["", ".asm", ".ASM", ".s", ".S"]
        else:
            nativeName = filename
            extensions = [""]
        for i in includePath:
            for e in extensions:
                includefile = os.path.join(i, nativeName + e)
                if os.path.isfile(includefile):
                    return includefile
                includefile = os.path.join(i, nativeName.lower() + e)
                if os.path.isfile(includefile):
                    return includefile
        return None

    def read(self):
        """get next logical line from source files"""
        while self.file:
            line = self.file.readline()
            if not line:
                self.resume()
            else:
                self.lino += 1
                if line.strip() and line[0] != "*":
                    return self.lino, line.rstrip()
        return -1, None

    def parse(self, dummy, code):
        """parse source code and generate object code"""
        source, errors = [], []
        # first pass: scan symbols
        self.passno = 1
        self.symbols.resetLC()
        while True:
            lino, line = self.read()
            if line is None:
                break
            label, mnemonic, operands, comment = self.line(line)
            #print "<1>", lino, "-", label, mnemonic, operands
            try:
                if not self.prep.process(dummy, label, mnemonic, operands):
                    continue
                Directives.process(self, dummy, label, mnemonic, operands) or \
                    Opcodes.process(self, dummy, label, mnemonic, operands)
            except AsmError as e:
                errors.append("<1> %04d - %s\n***** %s\n" % (
                    lino, line, e.message))
            source.append((lino, label, mnemonic, operands, line))
        # second pass: generate code
        self.passno = 2
        self.symbols.resetLC()
        for lino, label, mnemonic, operands, line in source:
            #print "<2>", lino, "-", label, mnemonic, operands
            try:
                Directives.process(self, code, label, mnemonic, operands) or \
                    Opcodes.process(self, code, label, mnemonic, operands)
            except AsmError as e:
                errors.append("<2> %04d - %s\n***** %s\n" % (
                    lino, line, e.message))
        return errors

    def line(self, line):
        """parse single source line"""
        if self.strictMode:
            # blanks separate fields
            fields = re.split("\s+", self.escape(line), maxsplit=3)
            label, mnemonic, optext, comment = fields + [""] * (4 - len(fields))
            label = label[:6]
            operands = re.split(",", optext) if optext else []
        else:
            # comment field separated by two blanks
            parts = self.escape(line).split(";")
            fields = re.split("\s+", parts[0], maxsplit=2)
            label, mnemonic, optext = fields + [""] * (3 - len(fields))
            opfields = re.split(" {2,}|\t", optext, maxsplit=1)
            operands = ([op.strip() for op in opfields[0].split(",")]
                        if opfields[0] else [])
            comment = " ".join(opfields[1:]) + ";".join(parts[1:])
        return label, mnemonic, operands, comment

    def escape(self, text):
        """remove and save text literals from line"""
        parts = re.split("('(?:[^']|'')*')", text)
        lits = [s[1:-1].replace("''", "'") for s in parts[1::2]]
        parts[1::2] = ["'%s'" % (len(self.textlits) + i)
                       for i in xrange(len(lits))]
        self.textlits.extend(lits)
        return "".join(parts).upper()

    def address(self, op):
        """parse general address into t-field, register, address value"""
        if op[0] == "@":
            i = op.find("(")
            if i >= 0 and op[-1] == ")":
                return (0b10, self.register(op[i + 1:-1]),
                        self.expression(op[1:i]))
            else:
                return 0b10, 0, self.expression(op[1:])
        elif op[0] == "*":
            if op[-1] == "+":
                return 0b11, self.register(op[1:-1]), None
            else:
                return 0b01, self.register(op[1:]), None
        else:
            return 0b00, self.register(op), None

    def relative(self, op):
        """parse relative address (LC displacement)"""
        if self.passno == 1:
            return 0
        addr = self.expression(op)
        if (isinstance(addr, Address) and
                addr.relocatable != self.symbols.relocLC):
            raise AsmError("Invalid relocatable address")
        disp = ((addr.addr if isinstance(addr, Address) else addr) -
                self.symbols.LC) / 2 - 1
        if disp < -128 or disp > 127:
            raise AsmError("Out of range: " + op + " +/- " + hex(disp))
        return disp

    def expression(self, expr,
                   wellDefined=False, absolute=False, relaxed=False):
        """parse complex arithmetical expression"""
        if self.passno == 1 and not wellDefined:
            return 0
        value, reloccount = Word(0), 0
        terms = ["+"] + [tok.strip() for tok in
                         re.split(r"([-+*/])" if self.strictMode else
                                  r"([-+/%~&|^()]|\*\*?)", expr)]
        i, stack = 0, []
        while i < len(terms):
            op, term, negate, corr = terms[i], terms[i + 1], False, 0
            i += 2
            if op == ")":
                v, reloc = value.value, reloccount
                value, reloccount, op, negate, corr = stack.pop()
            else:
                # unary operators
                while not term and i < len(terms) and terms[i] in "+-~(":
                    term = terms[i + 1]
                    if terms[i] == "-":
                        negate = not negate
                    elif terms[i] == "~":
                        negate, corr = not negate, corr + (1 if negate else -1)
                    elif terms[i] == "(":
                        stack.append((value, reloccount, op, negate, corr))
                        op, term, negate, corr = "+", terms[i + 1], False, 0
                        value, reloccount = Word(0), 0
                    i += 2
                termval = self.term(term, wellDefined, relaxed)
                if termval is None:
                    raise AsmError("Invalid expression: " + term)
                elif isinstance(termval, Reference):
                    if len(terms) != 2 or wellDefined:
                        raise AsmError("Invalid reference: " + expr)
                    return termval
                elif isinstance(termval, Address):
                    v, reloc = termval.addr, 1 if termval.relocatable else 0
                else:
                    v, reloc = termval, 0
            w = Word((-v if negate else v) + corr)
            if op == "+":
                value.add(w)
                reloccount += reloc if not negate else -reloc
            elif op == "-":
                value.sub(w)
                reloccount -= reloc if not negate else -reloc
            elif op in "*/%":
                value.mul(op, w)
                if reloccount > 0:
                    raise AsmError("Invalid address: " + expr)
            elif op in "&|^":
                value.bit(op, w)
                if reloccount > 0:
                    raise AsmError("Invalid address: " + expr)
            elif op == "**":
                base, exp = Word(1), w.value
                for j in xrange(exp):
                    base.mul("*", value)
                value = base
            else:
                raise AsmError("Invalid operator: " + op)
        if not 0 <= reloccount <= (0 if absolute else 1):
            raise AsmError("Invalid address: " + expr)
        return Address(value.value, True) if reloccount else value.value

    def term(self, op, wellDefined=False, relaxed=False):
        """parse constant or symbol"""
        if op[0] == ">":
            return int(op[1:], 16)
        elif op == "$":
            return Address(self.symbols.LC, self.symbols.relocLC)
        elif op.isdigit():
            return int(op)
        elif op[0] == op[-1] == "'":
            c = self.textlits[int(op[1:-1])]
            if len(c) == 1:
                return ord(c[0])
            elif len(c) == 2:
                return ord(c[0]) << 8 | ord(c[1])
            elif len(c) == 0:
                return 0
            else:
                raise AsmError("Invalid text literal: " + c)
        else:
            v = self.symbols.getSymbol(op[:6] if self.strictMode else op)
            if v is None and (self.passno > 1 or wellDefined):
                if relaxed:
                    return 0
                else:
                    raise AsmError("Unknown symbol: " + op)
            return v

    def value(self, op):
        """parse well-defined value"""
        e = self.expression(op, wellDefined=True)
        return e.addr if isinstance(e, Address) else e

    def register(self, op):
        """parse register"""
        if self.passno == 1:
            return 0
        op = op.strip()
        if op[0] == ">":
            r = int(op[1:], 16)
        elif op.isdigit():
            r = int(op)
        else:
            r = self.symbols.getSymbol(op[:6] if self.strictMode else op)
            if r is None:
                raise AsmError("Unknown symbol: " + op)
        if not 0 <= r <= 15:
            raise AsmError("Invalid register: " + op)
        return r

    def text(self, op):
        """parse single-quoted text literal"""
        s, negate = (op[1:], True) if op[0] == "-" else (op, False)
        if not (len(s) >= 2 and s[0] == s[-1] == "'"):
            raise AsmError("Invalid text literal: " + op)
        s = self.textlits[int(s[1:-1])] or '\x00'  # '' equals '\x00'
        return s[:-1] + chr(-ord(s[-1]) % 0x100) if negate else s

    def filename(self, op):
        """parse double-quoted filename"""
        if not (len(op) >= 3 and op[0] == op[-1] == '"'):
            raise AsmError("Invalid filename: " + op)
        return op[1:-1]

    @staticmethod
    def symconst(op):
        """parse symbol constant (-D option)"""
        try:
            return int(op[1:], 16) if op[0] == ">" else int(op)
        except ValueError:
            return op


### Main assembler

class Assembler:
    """main driver class"""

    def __init__(self, addRegisters=False, strictMode=False,
                 includePath=None, defs=None):
        self.addRegisters = addRegisters
        self.strictMode = strictMode
        self.includePath = includePath
        self.defs = defs

    def assemble(self, srcname):
        symbols = Symbols(addRegisters=self.addRegisters, addDefs=self.defs)
        dummy = Objdummy(symbols)
        code = Objcode(symbols)
        parser = Parser(symbols, includePath=self.includePath,
                        strictMode=self.strictMode)
        parser.open(srcname)
        errors = parser.parse(dummy, code)
        return code, errors


### Command line processing

def main():
    import argparse, zipfile

    args = argparse.ArgumentParser(
        version=VERSION,
        description="TMS 9900 cross-assembler")
    args.add_argument("source", metavar="<source>",
                      help="assembly source code")
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument("-i", "--image", action="store_true", dest="image",
                     help="create program image")
    cmd.add_argument("-c", "--cart", action="store_true", dest="cart",
                     help="create MESS cart image")
    cmd.add_argument("--dump", action="store_true", dest="dump",
                     help=argparse.SUPPRESS)  # debugging
    args.add_argument("-s", "--strict", action="store_true", dest="strict",
                      help="disable xas99 extension to TI Assembler")
    args.add_argument("-n", "--name", dest="name", metavar="<name>",
                      help="set program name for cartridge")
    args.add_argument("-R", "--register-symbols", action="store_true", dest="optr",
                      help="add register symbols (TI Assembler option R)")
    args.add_argument("-C", "--compress", action="store_true", dest="optc",
                      help="compress object code (TI Assembler option C) (ignored)")
    args.add_argument("-L", "--listing", dest="optl", metavar="<file>",
                      help="generate listing (TI Assembler option L) (ignored)")
    args.add_argument("-S", "--symbol-table", action="store_true", dest="optl",
                      help="add symbol table to listing (TI Assembler option S) (ignored)")
    args.add_argument("-D", "--define-symbol", nargs="+", dest="defs",
                      metavar="<sym=val>",
                      help="add symbol to symbol table")
    args.add_argument("-o", "--output", dest="output", metavar="<file>",
                      help="set output file name")
    opts = args.parse_args()

    # setup
    dirname = os.path.dirname(opts.source) or "."
    basename = os.path.basename(opts.source)
    barename = os.path.splitext(basename)[0]
    output = opts.output or (
        barename + ".img" if opts.image else
        barename + ".rpk" if opts.cart else
        barename + ".obj"
        )
    name = opts.name or barename[:10].upper()

    # assembly
    asm = Assembler(addRegisters=opts.optr,
                    strictMode=opts.strict,
                    includePath=[dirname],
                    defs=opts.defs or [])
    try:
        code, errors = asm.assemble(basename)
    except IOError as e:
        sys.exit("File error: %s: %s." % (e.filename, e.strerror))

    # output
    if errors:
        sys.stderr.write("".join(errors))
    elif opts.dump:
        sys.stdout.write(code.genDump())
    elif opts.cart:
        data, layout, metainf = code.genCart(name)
        try:
            with zipfile.ZipFile(output, "w") as archive:
                archive.writestr(name + ".bin", data)
                archive.writestr("layout.xml", layout)
                archive.writestr("meta-inf.xml", metainf)
        except IOError as e:
            sys.exit("File error: %s: %s." % (e.filename, e.strerror))
    else:
        data = code.genImage() if opts.image else code.genObjCode()
        try:
            with open(output, "wb") as fout:
                fout.write(data)
        except IOError as e:
            sys.exit("File error: %s: %s." % (e.filename, e.strerror))

    # return status
    return 1 if errors else 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
