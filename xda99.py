#!/usr/bin/env python

# xda99: TMS9900 disassembler
#
# Copyright (c) 2017 Ralph Benzinger <xdt99@endlos.net>
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

VERSION = "1.7.0"


### Utility functions

def ordw(word):
    """word ord"""
    return ord(word[0]) << 8 | ord(word[1])


def chrw(word):
    """word chr"""
    return chr(word >> 8) + chr(word & 0xFF)


def xhex(s):
    """return hex string as integer value"""
    return s and int(s.lstrip(">").lstrip("0x") or "0", 16)


def escape(t):
    """escape non-printable characters"""
    q = t.replace("'", "''")
    return "'" + re.sub(r"[^ -~]",
                        lambda m: "\\%02X" % ord(m.group(0)), q) + "'"


def readbin(n, m="rb"):
    """read lines from file or STDIN"""
    if n == "-":
        return sys.stdin.read()
    else:
        with open(n, m) as f:
            return f.read()


def writelines(n, m, d):
    """write lines to file or STDOUT"""
    if n == "-":
        sys.stdout.write(d)
    else:
        with open(n, m) as f:
            f.write(d)


### Error handling

class XdaError(Exception):
    pass


class XdaLogger:

    leveldebug = 0
    levelinfo = 1
    levelwarn = 2
    levelerror = 3
    
    loglevel = 2

    @staticmethod
    def setlevel(level):
        XdaLogger.loglevel = level

    @staticmethod
    def warn(message):
        if XdaLogger.loglevel <= XdaLogger.levelwarn:
            print "WARNING:", message

    @staticmethod
    def info(message):
        if XdaLogger.loglevel <= XdaLogger.levelinfo:
            print "INFO:", message

    @staticmethod
    def debug(message):
        if XdaLogger.loglevel <= XdaLogger.leveldebug:
            print "DEBUG:", message


### Symbol table

class Symbols:
    """symbol table"""

    def __init__(self, symfiles=None):
        # pre-defined symbols
        self.symbols = {
            0x210C: "VSBW", 0x2110: "VMBW",
            0x2114: "VSBR", 0x2118: "VMBR",
            0x211C: "VWTR", 0x2108: "KSCAN",
            0x2100: "GPLLNK", 0x2104: "XMLLNK",
            0x2120: "DSRLNK", 0x2124: "LOADER",
            0x2022: "UTLTAB", 0x000E: "SCAN",
            0x8300: "PAD", 0x83E0: "GPLWS",
            0x8400: "SOUND",
            0x8800: "VDPRD", 0x8802: "VDPST",
            0x8C00: "VDPWD", 0x8C02: "VDPWA",
            0x9000: "SPCHRD", 0x9400: "SPCHWT",
            0x9800: "GRMRD", 0x9802: "GRMRA",
            0x9C00: "GRMWD", 0x9C02: "GRMWA"
            }
        # additional symbols loaded from file(s)
        if symfiles:
            for sf in symfiles:
                self.load(sf)
        # symbols referenced in program
        self.used = {}

    def load(self, fn):
        """load symbol EQUs from file"""
        with open(fn, "r") as fsym:
            lines = fsym.readlines() + [""]
        for i in xrange(len(lines) - 1):
            longline = lines[i] + lines[i + 1]  # join two lines
            m = re.match(r"^(\w+):?\s*(?:EQU)?\s+(>?[0-9A-F]+)\s",
                         longline.upper())
            if not m:
                continue
            s, a = m.group(1), xhex(m.group(2))
            if self.symbols.get(a) is not None:
                XdaLogger.warn("symbol for %04X already defined, overwritten" % a)
            self.symbols[a] = s

    def resolve(self, value):
        """find symbol name for given value, or return >xx/xxxx value """
        try:
            symbol = self.symbols[value]
        except KeyError:
            return ">%04X" % value
        self.used[symbol] = value  # mark symbol as used for EQU prelude
        return symbol

    def getused(self):
        """return dict of all symbols that have been used"""
        return self.used.iteritems()


### Opcodes

class Opcodes:

    # list of all TMS 9900 opcodes
    opcodes = {
        # 6. arithmetic
        0xA000: ("A", 1),
        0xB000: ("AB", 1),
        0x0740: ("ABS", 6),  # 4 in E/A Manual
        0x0220: ("AI", 8),
        0x0600: ("DEC", 6),
        0x0640: ("DECT", 6),
        0x3C00: ("DIV", 9),
        0x0580: ("INC", 6),
        0x05C0: ("INCT", 6),
        0x3800: ("MPY", 9),
        0x0500: ("NEG", 6),
        0x6000: ("S", 1),
        0x7000: ("SB", 1),
        # 7. jump and branch
        0x0440: ("B", 6),
        0x0680: ("BL", 6),
        0x0400: ("BLWP", 6),
        0x1300: ("JEQ", 2),
        0x1500: ("JGT", 2),
        0x1400: ("JHE", 2),
        0x1B00: ("JH", 2),
        0x1A00: ("JL", 2),
        0x1200: ("JLE", 2),
        0x1100: ("JLT", 2),
        0x1000: ("JMP", 2),
        0x1700: ("JNC", 2),
        0x1600: ("JNE", 2),
        0x1900: ("JNO", 2),
        0x1C00: ("JOP", 2),
        0x1800: ("JOC", 2),
        0x0380: ("RTWP", 7),
        0x0480: ("X", 6),
        0x2C00: ("XOP", 9),
        # 8. compare instructions
        0x8000: ("C", 1),
        0x9000: ("CB", 1),
        0x0280: ("CI", 8),
        0x2000: ("COC", 3),
        0x2400: ("CZC", 3),
        # 9. control and cru instructions
        0x3000: ("LDCR", 4),
        0x1D00: ("SBO", 12),
        0x1E00: ("SBZ", 12),
        0x3400: ("STCR", 4),
        0x1F00: ("TB", 12),
        0x03C0: ("CKOF", 7),
        0x03A0: ("CKON", 7),
        0x0340: ("IDLE", 7),
        0x0360: ("RSET", 7),
        0x03E0: ("LREX", 7),
        # 10. load and move instructions
        0x0200: ("LI", 8),
        0x0300: ("LIMI", 10),
        0x02E0: ("LWPI", 10),
        0xC000: ("MOV", 1),
        0xD000: ("MOVB", 1),
        0x02C0: ("STST", 11),
        0x02A0: ("STWP", 11),
        0x06C0: ("SWPB", 6),
        # 11. logical instructions
        0x0240: ("ANDI", 8),
        0x0260: ("ORI", 8),
        0x2800: ("XOR", 3),
        0x0540: ("INV", 6),
        0x04C0: ("CLR", 6),
        0x0700: ("SETO", 6),
        0xE000: ("SOC", 1),
        0xF000: ("SOCB", 1),
        0x4000: ("SZC", 1),
        0x5000: ("SZCB", 1),
        # 12. shift instructions
        0x0800: ("SRA", 5),
        0x0900: ("SRL", 5),
        0x0A00: ("SLA", 5),
        0x0B00: ("SRC", 5),
        # F18A GPU instructions
        0x0C80: ("CALL", 6),
        0x0C00: ("RET", 7),
        0x0D00: ("PUSH", 6),
        0x0F00: ("POP", 6),
        0x0E00: ("SLC", 5)
        # End of opcodes
    }

    # 13. pseudo instructions    
    pseudos = {  
        0x1000: ("NOP", 2),
        0x045B: ("RT", 6)
    }

    # number of valid MSB bits for each instruction format
    # Example: Format III:  O O O O O O - - / - - - - - - - -
    #          COC s, r  ->  opcodes >2000, >2001, ... >23FF
    opcbitmask = (
        -1, 4, 8, 6, 6, 8, 10, 16, 12, 6,  # regular formats
        16, 12, 12)  # special formats

    # redirect execution
    branches = ("B", "JMP")

    # fork execution
    calls = ("BL", "BLWP",
             "JNE", "JEQ", "JGT", "JLT", "JH", "JHE", "JL", "JLE", "JOC",
             "JNC", "JOP", "JNO")

    # terminate execution
    returns = ("RT", "RTWP")

    def decode(self, prog, idx):
        """get instruction for next words(s)"""
        entry = prog.code[idx]
        assert entry.addr == prog.idx2addr(idx)  # check sanity
        # already disassembled?
        if isinstance(entry, Instruction):
            return entry
        addr, word = entry.addr, entry.word
        # pseudo instruction?
        if word in Opcodes.pseudos:
            mnem, iformat = Opcodes.pseudos[word]
            return Instruction(prog, addr, word, mnem, iformat, [], "")
        mnem = None
        # search for mnemonic: try all bit masks
        for mask, masklen in (
                # (bitmark, number of left-most bit set)
                (0xf000, 4), (0xfc00, 6), (0xff00, 8), (0xffc0, 10),
                (0xfff0, 12), (0xffff, 16)
        ):
            try:
                candidate, iformat = Opcodes.opcodes.get(word & mask)
                # (word & bitmask) matches some opcode, but is the bitmask
                # used here appropriate for the opcode's instruction format?
                if Opcodes.opcbitmask[iformat] == masklen:
                    mnem = candidate
                    break
            except TypeError:
                pass  # try next
        if mnem is None:
            return Literal(addr, word, word, prog.symbols)  # no mnem found
        # decode operands
        try:
            ops = self.decode_iformat(addr, word, prog.code, idx + 1,
                                      iformat, prog.symbols)
        except IndexError as e:
            return entry  # abort decoding
        # build and return instruction
        return Instruction(prog, addr, word, mnem, iformat, ops, "")
    
    def decode_iformat(self, addr, word, code, idx, iformat, symbols):
        """decode operands for given instruction format"""
        # I. two general address instructions
        if iformat == 1:
            td = (word >> 10) & 0x03  # variables ts, s, td, d, etc
            ts = (word >> 4) & 0x03   # correspond to E/A manual
            d = (word >> 6) & 0x0f
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx + i1, td, d, symbols)
            return o1, o2
        # II. jump and bit I/O instructions
        elif iformat == 2:
            disp = -(~word & 0x00ff) - 1 if word & 0x0080 else word & 0x007f
            a = addr + 2 + 2 * disp
            return Operand(None, None, 0, symbols.resolve(a), dest=a),
        # III. logical instructions
        elif iformat == 3:
            d = (word >> 6) & 0x0f
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx + i1, 0, d, symbols)
            return o1, o2
        # IV. CRU multi-bit instructions
        elif iformat == 4:
            c = (word >> 6) & 0x0f
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx, 8, c, symbols)
            return o1, o2
        # V. register shift instructions
        elif iformat == 5:
            c = (word >> 4) & 0x0f
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 8, w, symbols)
            i2, o2 = self.decode_addr(code, idx, 7, c, symbols)
            return o1, o2
        # VI. single address instructions
        elif iformat == 6:
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            return (o1,)
        # VII. control instructions
        elif iformat == 7:
            return ()
        # VIII. immediate instructions
        elif iformat == 8:  # two opers
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 0, w, symbols)
            i2, o2 = self.decode_addr(code, idx, 9, 0, symbols)
            return o1, o2
        elif iformat == 81:  # one opers reg
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 0, w, symbols)
            return (o1,)
        elif iformat == 82:  # one opers addr
            i1, o1 = self.decode_addr(code, idx, 2, 0, symbols)
            return (o1,)
        # IX. extended operations; multiply and divide
        elif iformat == 9:
            d = (word >> 6) & 0x0f
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx + i1, 0, d, symbols)
            return o1, o2
        # special cases
        elif iformat == 10:  # LIMI, LWPI
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 9, 0, symbols)
            return o1,
        elif iformat == 11:  # STST, STWP
            w = word & 0x0f
            return Operand(None, None, 0, "R" + str(w)),
        elif iformat == 12:  # bit operations
            disp = -(~word & 0x00ff) - 1 if word & 0x0080 else word & 0x007f
            return Operand(None, None, 0, str(disp)),
        else:
            raise XdaError("Invalid instruction format " + str(iformat))

    def decode_addr(self, code, idx, t, oper, symbols):
        """decodes address mode of operand"""
        if t == 0:  # workspace register
            return 0, Operand(None, None, 0, "R" + str(oper))
        elif t == 1:  # workspace register indirect
            return 0, Operand(None, None, 0, "*R" + str(oper))
        elif t == 2:  # symbolic or indexed memory
            addr, word = code[idx].addr, code[idx].word
            t = "@" + symbols.resolve(word)
            if oper:
                t += "(R" + str(oper) + ")"
            return 1, Operand(addr, word, 1, t, dest=None if oper else word)
        elif t == 3:  # workspace register indirect auto-incr
            return 0, Operand(None, None, 0, "*R" + str(oper) + "+")
        elif t == 7:  # count
            return 0, Operand(None, None, 0, "%d" % oper)
        elif t == 8:  # register
            return 0, Operand(None, None, 0, "R%d" % oper)
        elif t == 9:  # imm values
            addr, word = code[idx].addr, code[idx].word
            return 1, Operand(addr, word, 1, symbols.resolve(word))
        else:
            raise XdaError("Invalid address format " + str(t))
        
    def jumps(self, prog, instr):
        """return target address of branching instruction"""
        assert instr.mnemonic in Opcodes.branches + Opcodes.calls
        dest = instr.operands[0].dest
        # special case for BLWP:
        if instr.mnemonic == "BLWP" and dest is not None:
            try:
                # BLWP points to WP and PC words
                dest = prog.code[prog.addr2idx(dest + 2)].word  # PC
            except IndexError:
                dest = None
        return dest


class Entry:
    """base class for all entry for a given word position"""
   
    def __init__(self, addr, word, size=1, indicator=' '):
        self.addr = addr  # addr of word
        self.word = word  # value of word 
        self.size = size  # index size of entire instruction
        self.origins = []  # addresses this entry was jumped at from
        self.indicator = indicator  # status indicator

    def list0(self, isprog, mnem="", ops=""):
        """internal pretty printing function"""
        if self.origins:
            torigin = "; <- " + ", ".join([">%04X" % o
                                           for o in sorted(self.origins)])
        else:
            torigin = ""
        if isprog:  # program format, can be re-assembled
            return "L%04X  %-4s %-20s %s" % (self.addr, mnem, ops, torigin)
        else:  # list format
            return "%04X %04X%c  %-4s %-20s %s" % (
                self.addr, self.word, self.indicator, mnem, ops, torigin)

    def list(self, isprog=False):
        """pretty print current entry"""
        return self.list0(isprog)


class Unknown(Entry):
    """unknown value, espc. not disassembled"""

    def __init__(self, addr, word):
        Entry.__init__(self, addr, word, indicator="?")


class Used(Entry):
    """word that is part of an instruction"""

    def __init__(self, addr, word, parent):
        Entry.__init__(self, addr, word, indicator=" ")
        self.parent = parent  # parent instruction


class Instruction(Entry):
    """an instruction"""

    def __init__(self, prog, addr, word, mnemonic, iformat, ops, comment=""):
        Entry.__init__(self, addr, word, 1 + sum([op.size for op in ops]))
        self.prog = prog  # surrounding program
        self.mnemonic = mnemonic  # mnemonic of instruction
        self.iformat = iformat  # instruction format
        self.operands = ops  # list of operands
        self.comment = comment  # optional comment

    def list(self, isprog=False):
        """pretty print current instruction"""
        optexts = [op.text for op in self.operands]
        ops = ", ".join(optexts)
        return Entry.list0(self, isprog, self.mnemonic, ops)
 

class Operand:
    """an instruction operand"""

    def __init__(self, addr, word, size, text, dest=None):
        self.addr = addr  # current address
        self.word = word  # current word
        self.size = size  # operand index size
        self.text = text  # textual representation of operand
        self.dest = dest  # address if direct addressing


class Literal(Entry):
    """TEXT or DATA constants"""
    # NOTE: Literal is not an active entry during disassembly;
    # instead, it's added to the source cum eo.  If this should
    # change, Literal should inherit from Instruction.

    def __init__(self, addr, word, value, symbols):
        if isinstance(value, str):
            assert len(value) % 2 == 0
            Entry.__init__(self, addr, word, len(value) / 2)
            self.mnem = "TEXT"
            self.value = escape(value)
        else:
            Entry.__init__(self, addr, word, 1)
            self.mnem = "DATA"
            self.value = symbols.resolve(value)

    def list(self, isprog=False):
        """return textual representation of literal"""
        return Entry.list0(self, isprog, self.mnem, self.value)


class Program:
    """a binary program"""

    def __init__(self, binary, addr, symbols):
        self.binary = binary  # binary blob
        self.addr = addr  # start addr
        self.symbols = symbols  # symbol table
        self.code = [Unknown(addr + i, ordw(binary[i:i + 2]))  # list of entries
                     for i in xrange(0, len(binary), 2)]
        self.size = len(self.code)  # index size of programm
        self.end = self.addr + len(binary)  # final address of program
        self.equtext = ""  # EQU statements

    def addr2idx(self, addr):
        """converts address to code index"""
        return (addr - self.addr) / 2

    def idx2addr(self, idx):
        """converts code index to addr"""
        return self.addr + idx * 2

    def register(self, idx, instr, force=False):
        """register disassembled instruction in program"""
        assert idx == self.addr2idx(instr.addr)  # consistency
        assert not isinstance(self.code[idx], Instruction)  # no double work
        # is the instruction conflicting with previous instructions?
        if not force:
            for i in xrange(idx, idx + instr.size):
                if not isinstance(self.code[i], Unknown):
                    XdaLogger.warn(
                        "Would overwrite already disassembled index %d" % i)
                    return False
        # persist instruction and mark words of operands as disassembled
        for i in xrange(idx, idx + instr.size):
            # undo instructions of previous disassembly runs
            if isinstance(self.code[i], Instruction):
                self.deregister(i)
            elif isinstance(self.code[i], Used):
                self.deregister(self.code[i].parent)
            self.code[i] = Used(self.code[i].addr, self.code[i].word, idx)
        self.code[idx] = instr  # add current instruction
        return True

    def deregister(self, idx):
        """remove disassembled instruction from code"""
        assert isinstance(self.code[idx], Instruction)
        for i in xrange(self.code[idx].size):
            entry = self.code[idx + i]
            self.code[idx + i] = Unknown(entry.addr, entry.word)

    def list(self, start=None, end=None, isprog=False):
        """pretty print entire program"""
        idx = self.addr2idx(start) if start else 0
        idxto = self.addr2idx(end) if end else self.size
        aorg = " " * (7 if isprog else 12) + "AORG >%04X\n" % self.addr
        listing = [self.code[i].list(isprog=isprog)
                   for i in xrange(idx, idxto)]
        return aorg + self.equtext + "\n".join(listing) + "\n"


class BadSyntax:
    """used for invalid syntax entries"""

    def __init__(self, addr, word):
        self.addr = addr
        self.word = word
        self.size = 1

    def list(self, isprog):
        if isprog:
            return "L%04X  BAD SYNTAX %04X" % (self.addr, self.word)
        else:
            return "%04X %04X!  BAD SYNTAX" % (self.addr, self.word)

    
class Disassembler:
    """disassemble machine code"""

    def __init__(self, excludes):
        self.opcodes = Opcodes()
        self.excludes = excludes
        
    def decode(self, prog, idx, idx_to):
        """decode instructions in range"""
        while 0 <= idx < idx_to:
            instr = self.opcodes.decode(prog, idx)
            success = prog.register(idx, instr)
            assert success == True  # top-down should not have conflicts
            idx += instr.size
    
    def disassemble(self, prog, start=None, end=None):
        """top-down disassembler"""
        idx = prog.addr2idx(start or prog.addr)
        idx_to = prog.addr2idx(end or prog.end)
        self.decode(prog, idx, idx_to)

    def run(self, prog, start, end=None, force=False, origin=None):
        """run disassembler"""
        # check if address is valid
        if not prog.addr <= start < prog.end:
            XdaLogger.warn("Cannot disassemble external context @>%04X" % start)
            return  # cannot disassemble external content        
        idx = prog.addr2idx(start)
        idxto = prog.addr2idx(end or prog.end)
        while 0 <= idx < idxto:
            # excluded range?
            for efrom, eto in self.excludes:
                if efrom <= idx < eto:
                    if eto >= idxto:  # done
                        return
                    idx = eto  # skip to end of excluded range
                    break            
            # disassemble instruction
            if not isinstance(prog.code[idx], Instruction):
                instr = self.opcodes.decode(prog, idx)
                # make entry for instruction
                if not prog.register(idx, instr, force=force):
                    break  # abort on conflict
                new = True
            else:
                # already disassembled
                instr = prog.code[idx]  # Instruction
                new = False
            # mark jump from other address to here, if applicable
            if origin:
                instr.origins.append(origin)
                origin = None
            if not new:
                break  # everything else already done
            # check for control flow changes
            if isinstance(instr, Instruction):
                if instr.mnemonic in Opcodes.branches:
                    # execution is redirected
                    addr = self.opcodes.jumps(prog, instr)
                    if addr is not None:
                        self.run(prog, addr, end,
                                 force=force, origin=prog.idx2addr(idx))
                    break
                elif instr.mnemonic in Opcodes.calls:
                    # execution is forked
                    addr = self.opcodes.jumps(prog, instr)
                    if addr is not None:
                        self.run(prog, addr, end,
                                 force=force, origin=prog.idx2addr(idx))
                elif instr.mnemonic in Opcodes.returns:
                    # execution stops
                    break
            idx += instr.size

    def getstarts(self, prog):
        """returns list of all recognized start addresses"""
        # check for cartridge header
        if prog.binary[0] == "\xaa":
            # cart, no autostart
            menu, starts = ordw(prog.binary[6:8]) - prog.addr, []
            try:
                # find all menu entries
                while menu != 0x0000:
                    starts.append(ordw(prog.binary[menu + 2:menu + 4]))
                    menu = ordw(prog.binary[menu:menu + 2])
            except IndexError:
                XdaLogger.warn("bad cartridge menu structure")
            return starts
        else:
            # unknown binary
            return [prog.addr]  # begin of program

    def findstrings(self, prog, minlen=6, start=None, end=None):
        """convert consecutive unclaimed letters to string literals"""
        idx = prog.addr2idx(start) if start else 0
        idxto = prog.addr2idx(end) if end else prog.size
        # find un-disassembled chunks
        while idx < idxto:
            for i in xrange(idx, idxto):
                try:
                    if not isinstance(prog.code[i], Unknown):
                        break
                except IndexError:
                    break
            # found Unknown chunk (might be empty)
            chunk = prog.binary[idx * 2:i * 2]
            # search for text literal of at least size 6 in Unknown chunk
            m = re.search(r"[A-Za-z0-9 ,.:?!()\-]{%d,}" % minlen, chunk)
            if m:
                # replace Unknowns by Literal
                mstart = m.start(0) if m.start(0) % 2 == 0 else m.start(0) + 1
                mend = m.end(0) if m.end(0) % 2 == 0 else m.end(0) - 1
                # TODO: odd positions would require to issue BYTEs here
                lidx = idx + mstart / 2
                prog.register(lidx, Literal(prog.idx2addr(lidx),
                                            prog.code[lidx].word,
                                            chunk[mstart:mend], prog.symbols))
            idx = i + 1

    def program(self, prog):
        """turns disassembled fragment into assembly source"""
        # turn unknowns into literals
        for idx in xrange(prog.size):
            instr = prog.code[idx]
            if isinstance(instr, Unknown):
                prog.code[idx] = Literal(instr.addr, instr.word, instr.word,
                                         prog.symbols)
        # add symbol EQUs, if needed
        prog.equtext += "".join(["%-8s EQU  >%04X\n" % (s, v)
                                 for s, v in prog.symbols.getused()])


### Command line processing

def main():
    import argparse, zipfile

    args = argparse.ArgumentParser(
        version=VERSION,
        description="TMS9900 disassembler")
    args.add_argument("binary", metavar="<file>",
                      help="machine code file")
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument("-r", "--run", metavar="<addr>", dest="runs", nargs="+",
                      help="run from additional addresses")
    cmd.add_argument("-f", "--from", metavar="<addr>", dest="frm",
                      help="disassemble top-down from address, or 'start'")
    args.add_argument("-a", "--address", metavar="<addr>", dest="addr",
                      help="address of first word")
    args.add_argument("-t", "--to", metavar="<addr>", dest="to",
                      help="disassemble to address (default: end)")
    args.add_argument("-e", "--exclude", metavar="<addr>-<addr>", dest="exclude", nargs="+",
                      help="exclude address ranges")
    args.add_argument("-F", "--force", action="store_true", dest="force",
                      help="force overwriting of previous disassembly")
    args.add_argument("-p", "--program", action="store_true", dest="program",
                      help="disassemble to complete program")
    args.add_argument("-n", "--strings", action="store_true", dest="strings",
                      help="disassemble string literals")
    args.add_argument("-S", "--symbols", dest="symfiles", nargs="+",
                      help="known symbols file(s)")
    args.add_argument("-V", "--verbose", action="store_true", dest="verbose",
                      help="verbose messages")
    args.add_argument("-o", "--output", dest="outfile",
                      help="output filename")
    opts = args.parse_args()

    # setup
    dirname = os.path.dirname(opts.binary) or "."
    basename = os.path.basename(opts.binary)
    barename = os.path.splitext(basename)[0]    
    output = opts.outfile or barename + ".dis"
    
    binary = readbin(opts.binary)
    addr = xhex(opts.addr) if opts.addr is not None else 0x6000
    addrto = xhex(opts.to)

    if opts.verbose:
        XdaLogger.setlevel(1)

    try:
        symbols = Symbols(opts.symfiles)
        prog = Program(binary, addr, symbols=symbols)
        excludes = [[prog.addr2idx(xhex(i)) for i in e.split("-")]
                    for e in (opts.exclude or [])]
        dis = Disassembler(excludes)

        if opts.frm:
            # top-down disassembler: uses specified start address -f
            XdaLogger.info("top-down disassembly")
            addrfrom = (min(dis.getstarts(prog))
                        if opts.frm.lower() == "start" else xhex(opts.frm))
            dis.disassemble(prog, addrfrom, addrto)
        else:
            # run disassembler: uses specified run addresses -r
            XdaLogger.info("run disassembly")
            runs = [xhex(r) for r in (opts.runs or []) if r.lower() != "start"]
            if len(runs) < len(opts.runs):  # means "start" in runs
                runs += dis.getstarts(prog)
            for run in runs:
                dis.run(prog, run, addrto, force=opts.force)
        if opts.strings:
            XdaLogger.info("extracting strings")
            dis.findstrings(prog)
        if opts.program:
            XdaLogger.info("finalizing into complete program")
            dis.program(prog)
    except XdaError as e:
        sys.exit("ERROR: %s: %s." % e)
    except IOError as e:
        sys.exit("ERROR: %s: %s." % (e.filename, e.strerror))   
    try:            
        source = prog.list(isprog=opts.program or False)
        writelines(output, "w", source)
    except IOError as e:
        sys.exit("ERROR: %s: %s." % (e.filename, e.strerror))   
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)    
