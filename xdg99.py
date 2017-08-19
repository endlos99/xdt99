#!/usr/bin/env python

# xgd99: A GPL disassembler
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
    return chr(word >> 8) + chr(word & 0xff)


def xhex(s):
    """return string with optional > or 0x as hexadecimal value"""
    return s and int(s.lstrip(">").lstrip("0x") or "0", 16)


def escape(t):
    """escape non-printable characters"""
    q = t.replace("'", "''")
    return "'" + re.sub(r"[^ -~]", lambda m: "\\%02X" % ord(m.group(0)), q) + "'"


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

class Invalid(Exception):
    """invalid disassembly"""
    pass


class XdgError(Exception):
    """abort disassembly"""
    pass


class XdgLogger:
    """issue message"""
    
    leveldebug = 0
    levelinfo = 1
    levelwarn = 2
    levelerror = 3
    
    loglevel = 3

    @staticmethod
    def setlevel(level):
        """change current log level"""
        XdgLogger.loglevel = level

    @staticmethod
    def error(message):
        """issue error message"""
        if XdgLogger.loglevel <= XdgLogger.levelerror:
            print "ERROR:", message

    @staticmethod
    def warn(message):
        """issue warning"""
        if XdgLogger.loglevel <= XdgLogger.levelwarn:
            print "WARNING:", message

    @staticmethod
    def info(message):
        """issue informational message"""
        if XdgLogger.loglevel <= XdgLogger.levelinfo:
            print "INFO:", message

    @staticmethod
    def debug(message):
        """issue debugging message"""
        if XdgLogger.loglevel <= XdgLogger.leveldebug:
            print "DEBUG:", message


### Language Syntax

class SyntaxVariant:
    """helper class"""
    
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Syntax:
    """different syntax conventions"""

    @staticmethod
    def get(style):
        try:
            return getattr(Syntax, style)
        except AttributeError:
            raise XdgError("Unknown syntax style " + style)

    xdt99 = SyntaxVariant(  # default
        grom = "G",
        vdp = "V",
        reg = "#",
        tdelim = "'",
        repls = {}
        )

    rag = SyntaxVariant(  # RAG
        grom = "G",
        vdp = "V",
        reg = "#",
        tdelim = "'",
        repls = {
            "TITLE": ("TITL", None),
            "I/O":   ("IO", None),
            "ROW+":  ("IROW", None),
            "COL+":  ("ICOL", None),
            "HTEXT": ("HTEX", None),
            "VTEXT": ("VTEX", None),
            "HCHAR": ("HCHA", None),
            "HMOVE": ("HSTR", None),
            "VCHAR": ("VCHA", None),
            "BIAS":  ("SCRO", None)
            }
        )

    ryte = SyntaxVariant(  # RYTE DATA
        grom="G",
        vdp="V",
        reg="#",
        move="%d, %s, %s",
        moves="%d,%s,%s",
        tdelim="'",
        repls={
            "TITLE": ("TITL", None),
            "HTEXT": ("HTEX", None),
            "VTEXT": ("VTEX", None),
            "HCHAR": ("HCHA", None),
            "HMOVE": ("HSTR", None),
            "VCHAR": ("VCHA", None),
            "BIAS":  ("SCRO", None)
            }
        )

    mizapf = SyntaxVariant(  # TIMT
        grom = "GROM",
        vdp = "VDP",
        reg = "VREG",
        tdelim = '"',
        repls={
            "MOVE": ("MOVE", "{0} BYTES FROM {1} TO {2}"),
            "HCHAR": ("PRINTH", "%s TIMES %s"),
            "VCHAR": ("PRINTV", "%s TIMES %s"),
            "FOR": ("FOR", "%s TIMES DO"),
            "HTEXT": ("PRINTH", None),
            "VTEXT": ("PRINTV", None),
            "ROW+": ("DOWN", None),
            "COL+": ("RIGHT", None),
            "FEND": ("END", None)
            }
        )


### Symbol table
 
class Symbols:
    """symbol table"""

    def __init__(self, symfiles=None):
        # pre-defined symbols
        self.symbols = {
            # CPU RAM
            0x8370: "MAXMEM", 0x8372: "DATSTK", 0x8373: "SUBSTK",
            0x8374: "KEYBRD", 0x8375: "KEY", 0x8376: "JOYY",
            0x8377: "JOYX", 0x8378: "RANDOM", 0x8379: "TIMER",
            0x837A: "MOTION", 0x837B: "VDPSTT", 0x837C: "STATUS",
            0x837D: "CB", 0x837E: "YPT", 0x837F: "XPT",
            # RAG assembler
            0x8354: "ERCODE", 0x8356: "VPAB", 0x836E: "VSTACK"
            }
        # additional symbols loaded from file(s)
        if symfiles:
            for sf in symfiles:
                self.load(sf)
        # symbols referenced in program
        self.used = {}

    def load(self, fn):
        """load symbol table from file"""
        with open(fn, "r") as fsym:
            lines = fsym.readlines() + [""]
        for i in xrange(len(lines) - 1):
            longline = lines[i] + lines[i + 1]  # join two lines
            m = re.match(r"^(\w+):?\s*\n?\s+EQU\s+(>?[0-9A-F]+)(?:\s|$)",
                         longline.upper())
            if not m:
                continue
            # found label s, EQU, and value v
            s, v = m.group(1), xhex(m.group(2))
            if self.symbols.get(v) is not None:
                XdgLogger.warn("symbol for %04X already defined, overwritten" % v)
            self.symbols[v] = s

    def resolve(self, value, d=True):
        """find symbol name for given value, or return >xx/xxxx value """
        try:
            symbol = self.symbols[value]
        except KeyError:
            return ">%04X" % value if d else ">%02X" % (value & 0xff)
        self.used[symbol] = value  # mark symbol as used for EQU prelude
        return symbol
        
    def getused(self):
        """return dict of all symbols that have been used"""
        return self.used.iteritems()


### Opcodes

class Opcodes:

    # list of all GPL opcodes
    opcode_list = (
        # opcode, mnemonic, iformat, infmt, togglefmt
        # 4.1 compare and test instructions
        (0x09, "H", 5, False, 0),
        (0x0A, "GT", 5, False, 0),
        (0x0C, "CARRY", 5, False, 0),
        (0x0D, "OVF", 5, False, 0),
        (0xD4, "CEQ", 1, False, 0),
        (0xD5, "DCEQ", 1, False, 0),
        (0xC4, "CH", 1, False, 0),
        (0xC5, "DCH", 1, False, 0),
        (0xC8, "CHE", 1, False, 0),
        (0xC9, "DCHE", 1, False, 0),
        (0xCC, "CGT", 1, False, 0),
        (0xCD, "DCGT", 1, False, 0),
        (0xD0, "CGE", 1, False, 0),
        (0xD1, "DCGE", 1, False, 0),
        (0xD8, "CLOG", 1, False, 0),
        (0xD9, "DCLOG", 1, False, 0),
        (0x8E, "CZ", 6, False, 0),
        (0x8F, "DCZ", 6, False, 0),
        # 4.2 program control instructions
        (0x60, "BS", 4, False, 0),
        (0x40, "BR", 4, False, 0),
        (0x05, "B", 3, False, 0),
        (0x8A, "CASE", 6, False, 0),
        (0x8B, "DCASE", 6, False, 0),
        (0x06, "CALL", 3, False, 0),
        (0x88, "FETCH", 6, False, 0),
        (0x00, "RTN", 5, False, 0),
        (0x01, "RTNC", 5, False, 0),
        # 4.4 arithmetic and logical instructions
        (0xA0, "ADD", 1, False, 0),
        (0xA1, "DADD", 1, False, 0),
        (0xA4, "SUB", 1, False, 0),
        (0xA5, "DSUB", 1, False, 0),
        (0xA8, "MUL", 1, False, 0),
        (0xA9, "DMUL", 1, False, 0),
        (0xAC, "DIV", 1, False, 0),
        (0xAD, "DDIV", 1, False, 0),
        (0x90, "INC", 6, False, 0),
        (0x91, "DINC", 6, False, 0),
        (0x94, "INCT", 6, False, 0),
        (0x95, "DINCT", 6, False, 0),
        (0x92, "DEC", 6, False, 0),
        (0x93, "DDEC", 6, False, 0),
        (0x96, "DECT", 6, False, 0),
        (0x97, "DDECT", 6, False, 0),
        (0x80, "ABS", 6, False, 0),
        (0x81, "DABS", 6, False, 0),
        (0x82, "NEG", 6, False, 0),
        (0x83, "DNEG", 6, False, 0),
        (0x84, "INV", 6, False, 0),
        (0x85, "DINV", 6, False, 0),
        (0xB0, "AND", 1, False, 0),
        (0xB1, "DAND", 1, False, 0),
        (0xB4, "OR", 1, False, 0),
        (0xB5, "DOR", 1, False, 0),
        (0xB8, "XOR", 1, False, 0),
        (0xB9, "DXOR", 1, False, 0),
        (0x86, "CLR", 6, False, 0),
        (0x87, "DCLR", 6, False, 0),
        (0xBC, "ST", 1, False, 0),
        (0xBD, "DST", 1, False, 0),
        (0xC0, "EX", 1, False, 0),
        (0xC1, "DEX", 1, False, 0),
        (0x8C, "PUSH", 6, False, 0),
        (0x20, "MOVE", 9, False, 0),
        (0xE0, "SLL", 1, False, 0),
        (0xE1, "DSLL", 1, False, 0),
        (0xDC, "SRA", 1, False, 0),
        (0xDD, "DSRA", 1, False, 0),
        (0xE4, "SRL", 1, False, 0),
        (0xE5, "DSRL", 1, False, 0),
        (0xE8, "SRC", 1, False, 0),
        (0xE9, "DSRC", 1, False, 0),
        # 4.5 graphics and miscellaneous instructions
        (0xED, "COINC", 1, False, 0),
        (0x04, "BACK", 2, False, 0),
        (0x07, "ALL", 2, False, 0),
        (0x08, "FMT", 10, False, +1),  # format
        (0x02, "RAND", 2, False, 0),
        (0x03, "SCAN", 5, False, 0),
        (0x0F, "XML", 2, False, 0),
        (0x0B, "EXIT", 5, False, 0),
        (0xF6, "I/O", 8, False, 0),
        # BASIC
        (0x0E, "PARSE", 2, False, 0),
        (0x10, "CONT", 5, False, 0),
        (0x11, "EXEC", 5, False, 0),
        (0x12, "RTNB", 5, False, 0),
        # undocumented
        (0xF8, "SWGR", 1, False, 0),
        (0xF9, "DSWGR", 1, False, 0),
        (0x13, "RTGR", 5, False, 0),
        # format (+ 0x100)
        (0x00, "HTEXT", 13, True, 0),
        (0x20, "VTEXT", 13, True, 0),
        (0x40, "HCHAR", 14, True, 0),
        (0x60, "VCHAR", 14, True, 0),
        (0x80, "COL+", 16, True, 0),
        (0xA0, "ROW+", 16, True, 0),
        (0xE0, "HMOVE", 15, True, 0),
        (0xC0, "FOR", 16, True, +1),
        (0xFB, "FEND", 17, True, -1),
        (0xFC, "BIAS", 11, True, 0),  # immediate value
        (0xFD, "BIAS", 12, True, 0),  # address
        (0xFE, "ROW", 11, True, 0),
        (0xFF, "COL", 11, True, 0)
    )

    # mask and shift of additionally used opcode bits for every format
    # Example:  Format I: 1 X X X X X S D,  Opcode >D4 = CEQ
    #           Bit S alters the opcode, so >D6 is also CEQ
    #           --> need to add both >D4 and >D6 to opcode table.
    opcbitmask = ((-1, -1), (1, 1), (0, 0), (0, 0), (5, 0), (0, 0),  # normal
                  (0, 0), (0, 0), (0, 0), (5, 0),
                  (0, 0), (0, 0), (1, 0), (5, 0), (5, 0), (5, 0), (5, 0), (0, 0))  # FMT
    
    # redirect execution
    branches = ("B", "CASE", "DCASE")

    # fork execution
    calls = ("BS", "BR", "CALL")  # EXEC calls BASIC

    # terminate execution
    returns = ("RTN", "RTNC", "RTNB", "EXIT")

    class Move:
        """move parameters"""

        def __init__(self, byte, gs):
            r, v, c, i = byte & 0x10, byte & 0x08, byte & 0x04, byte & 0x02
            if gs:
                # source
                self.grom = i or not c
                self.vreg = False
                self.idxd = i and not c
                self.indr = i and c
            else:
                # destination
                self.grom = not r
                self.vreg = v and r
                self.idxd = v and not r
                self.indr = False
                     
    def __init__(self, syntax):
        """complete list to contain all 2*256 opcodes"""
        self.syntax = syntax
        self.opcodes = {}
        for opc, mnem, iformat, in_fmt, toggle_fmt in self.opcode_list:
            # get unspecified bits in opcode byte
            mask, shift = Opcodes.opcbitmask[iformat]
            opc += 0x100 if in_fmt else 0  # FMT opcodes >100->1FF
            # fill all possible values for given mnemonic
            for i in xrange(1 << mask):
                self.opcodes[opc + (i << shift)] = (mnem, iformat, in_fmt, toggle_fmt)
        
    def decode(self, prog, idx, fmtlvl):
        """disassemble instruction in next bytes(s)"""
        entry = prog.code[idx]
        assert entry.addr == prog.idx2addr(idx)  # check sanity
        # already disassembled?
        if isinstance(entry, Instruction):
            return entry, entry.fmtlvl
        # find mnemonic for opcode
        addr, byte = entry.addr, entry.byte
        try:
            mnem, iformat, in_fmt, toggle_fmt = self.opcodes.get(
                byte + 0x100 if fmtlvl else byte)
        except TypeError:
            if fmtlvl:
                # unknown FMT instruction yields error
                return BadSyntax(addr, byte), 0
            else:
                # unknown instruction yields BYTE directive
                return Literal(addr, byte, byte), fmtlvl
        # check if isntruction is in right domain (FMT or not)
        if in_fmt != bool(fmtlvl):
            return  BadSyntax(addr, byte), fmtlvl
        # decode operands based on instruction format (iformat)
        try:
            ops = self.decode_iformat(addr, byte, prog.code, idx + 1,
                                      prog.symbols, iformat, fmtlvl)
        except IndexError as e:
            # last instruction stepped beyond last index of program
            XdgLogger.warn("incomplete program")
            return Literal(addr, byte, byte), fmtlvl
        except Invalid as e:
            # disassembly was incorrect
            XdgLogger.warn("invalid disassembly: " + str(e))
            return Literal(addr, byte, byte), fmtlvl
        # update domain
        fmtlvl += toggle_fmt
        # return disassembled instruction
        return Instruction(prog, addr, byte, mnem, iformat, ops, fmtlvl,
                           self.syntax, ""), fmtlvl

    def decode_iformat(self, addr, byte, code, idx, symbols, iformat, fmtlvl):
        """decode operands for given instruction format"""
        if iformat == 1:  # two general addresses
            s = byte & 0x02
            d = byte & 0x01
            i1, o1 = self.decode_addr(code, idx, symbols)
            i2, o2 = (self.decode_imm(code, idx + i1, symbols, d) if s else
                      self.decode_addr(code, idx + i1, symbols))
            return o2, o1
        elif iformat == 2:  # one immediate value
            i1, o1 = self.decode_imm(code, idx, symbols)
            return o1,
        elif iformat == 3:  # B instruction
            i1, o1 = self.decode_imm(code, idx, symbols, d=True)
            return o1,
        elif iformat == 4:  # BR, BS instructions
            g = addr & 0xe000  # current GROM
            a = g + ((byte & 0x1f) << 8) + code[idx].byte
            s = symbols.resolve(a)
            return Operand(code[idx].addr, code[idx].byte, 1, s, dest=a),  # no G@
        elif iformat == 5:  # no operands
            return ()
        elif iformat == 6:  # one address
            i1, o1 = self.decode_addr(code, idx, symbols)
            return o1,
        elif iformat == 7:  # FMT
            return ()
        elif iformat == 8:  # address and immediate
            i1, o1 = self.decode_addr(code, idx, symbols)
            i2, o2 = self.decode_imm(code, idx + i1, symbols)
            return o2, o1  # reversed order
        elif iformat == 9:  # MOVE
            mgs = Opcodes.Move(byte, gs=True)
            mgd = Opcodes.Move(byte, gs=False)
            n = byte & 0x01
            i1, o1 = (self.decode_imm(code, idx, symbols, d=True) if n else  # len
                      self.decode_addr(code, idx, symbols))
            i2, o2 = self.decode_addr(code, idx + i1, symbols, move=mgd)  # gd
            i3, o3 = self.decode_addr(code, idx + i1 + i2, symbols, move=mgs)  # gs
            return o1, o3, o2
        elif iformat == 10:  # FMT
            return ()
        elif iformat == 11:  # ROW/COL
            i1, o1 = self.decode_imm(code, idx, symbols)
            return o1,
        elif iformat == 12:  # BIAS
            if byte & 0x01:
                # address
                i1, o1 = self.decode_addr(code, idx, symbols)
            else:
                # immediate
                i1, o1 = self.decode_imm(code, idx, symbols)
            return o1,
        elif iformat == 13:  # HTEXT, VTEXT
            v = (byte & 0x1f) + 1
            return Operand(code[idx].addr, code[idx].byte, v,
                           escape("".join([chr(code[i].byte)
                                           for i in xrange(idx, idx + v)]))),
        elif iformat == 14:  # HCHAR, VCHAR
            v = (byte & 0x1f) + 1
            i1, o1 = 0, Operand(addr, v, 0, ">%02X" % v)
            i2, o2 = self.decode_imm(code, idx, symbols)
            return o1, o2
        elif iformat == 15:  # HMOVE
            v = (byte & 0x1f) + 1
            i1, o1 = 0, Operand(addr, v, 0, ">%02X" % v)
            i2, o2 = self.decode_addr(code, idx, symbols)
            return o1, o2
        elif iformat == 16:  # ROW+/COL+
            v = (byte & 0x1f) + 1
            return Operand(addr, byte, 0, ">%02X" % v),
        elif iformat == 17:
            if fmtlvl > 1:
                # FOR ... FEND
                return Operand(addr, 0, 2, ""),  # skip address of for
            else:
                # FMT ... FEND
                return ()
        else:
            raise XdgError("Unsupported instruction format " + str(iformat))

    def decode_addr(self, code, idx, symbols, move=None):
        """decode general address in operand"""
        addr, byte = code[idx].addr, code[idx].byte
        # is MOVE instruction?
        if move:
            # VDP register
            if move.vreg:
                if not 0 <= byte <= 7:
                    raise Invalid("VDP register too large")        
                return 1, Operand(addr, byte, 1, self.syntax.reg + str(byte))
            # GROM address variants are encodded by MOVE flags
            if move.grom:
                d = (byte << 8) + code[idx + 1].byte
                s = symbols.resolve(d)
                if move.indr:
                    # G* is an invention of Ryta Data
                    raise Invalid("G* is not a valid address mode")
                if move.idxd:
                    # indexed G@x(@y)
                    t = symbols.resolve(0x8300 + code[idx + 2].byte, d=False)
                    return 3, Operand(addr, byte, 3,
                                      "%s@%s(@%s)" % (self.syntax.grom, s, t))
                # regular GROM address
                return 2, Operand(addr, byte, 2,
                                  "%s@%s" % (self.syntax.grom, s))
        # not MOVE
        if not (byte & 0x80):
            # direct addressing >8300->837F
            d = 0x8300 + byte
            s = symbols.resolve(d)
            return 1, Operand(addr, byte, 1, "@" + s, dest=d)
        is_idx = byte & 0x40  # indexed
        is_vdp = byte & 0x20  # VDP RAM (V)
        is_idr = byte & 0x10  # indirect (*)
        v = self.syntax.vdp if is_vdp else ""
        g = self.syntax.grom if move and move.grom else ""
        offset = 0x8300 if not is_vdp or is_idr else 0
        a = byte & 0x0f
        # direct addressing
        if a == 0x0f:
            # 3 bytes
            d, l = (code[idx + 1].byte << 8) + code[idx + 2].byte, 3
            if not 0xeff <= d <= 0xffff:
                raise Invalid("address encoding should use 2 bytes instead of 3 bytes")
        else:
            # 2 bytes
            d, l = (a << 8) + code[idx + 1].byte, 2
            if ((not is_vdp and not is_idr and not is_idx and not 0x80 <= d) or
                    (not d <= 0xeff)):
                raise Invalid("address encoding should use 1 byte instead of 2 bytes")
        s = symbols.resolve((d + offset) & 0xffff)
        t = (v + g + ("*" if is_idr else "@") + s)
        # indexed addressing
        if is_idx:
            v = code[idx + l].byte
            s = symbols.resolve(0x8300 + v)
            t += "(@" + (s if s[0] != '>' else ">%02X" % v) + ")"  # TODO: hack
            l += 1
        return l, Operand(addr, byte, l, t)

    def decode_imm(self, code, idx, symbols, d=False):
        """decode immediate value in operand"""
        v = (code[idx].byte << 8) + code[idx + 1].byte if d else code[idx].byte
        t = symbols.resolve(v) if d else ">%02X" % v
        s = 2 if d else 1
        return s, Operand(code[idx].addr, code[idx].byte, s, t, dest=v)

    def jumps(self, prog, instr):
        """return target address of branching and calling instructions"""
        assert instr.mnemonic in Opcodes.branches + Opcodes.calls
        if instr.mnemonic in ("CASE", "DCASE"):
            # find all BR instructions following (D)CASE statement
            idx = prog.addr2idx(instr.addr + 1 + instr.operands[0].size)
            fmtlvl = 0
            for i in xrange(0, 512, 2):
                br, fmtlvl = self.decode(prog, idx + i, fmtlvl)
                if isinstance(br, Instruction) and br.mnemonic == "BR":
                    if not prog.register(idx + i, br):
                        break  # could not register BR instruction
                else:
                    break  # reached end of BR instructions
            return [prog.code[j].operands[0].dest
                    for j in xrange(idx, idx + i, 2)]
        else:
            # return saved dest= addresses
            return [op.dest for op in instr.operands if op.dest is not None]


class Entry:
    """base class for all entries for that may fill a byte position"""
    
    def __init__(self, addr, byte, size=1, indicator=' '):
        self.addr = addr  # addr of byte
        self.byte = byte  # value of byte
        self.size = size  # index size of entire instruction
        self.origins = []  # addresses this entry was jumped at from
        self.indicator = indicator  # status indicator

    def list0(self, isprog, mnem="", ops=""):
        """pretty print current entry"""
        if self.origins:
            torigin = "; <- " + ", ".join([">%04X" % o
                                           for o in sorted(self.origins)])
        else:
            torigin = ""
        if isprog:  # program format, can be re-assembled
            return "L%04X  %-5s %-20s %s" % (self.addr, mnem, ops, torigin)
        else:  # list format
            return "%04X %02X%c  %-5s %-20s %s" % (
                self.addr, self.byte, self.indicator, mnem, ops, torigin)

    def list(self, isprog=False):
        """pretty print current entry"""
        return self.list0(isprog)


class Unknown(Entry):
    """unknown entry that has not been disassembled"""

    def __init__(self, addr, byte):
        Entry.__init__(self, addr, byte, indicator="?")


class Used(Entry):
    """entry that is part of an instruction"""

    def __init__(self, addr, byte, parent):
        Entry.__init__(self, addr, byte, indicator=" ")
        self.parent = parent  # index of instruction


class Literal(Entry):
    """TEXT or BYTE constants"""
    # NOTE: Literal is not an active entry during disassembly;
    # instead, it's added to the source cum eo.  If this should
    # change, Literal should inherit from Instruction.

    def __init__(self, addr, byte, value):
        if isinstance(value, str):
            Entry.__init__(self, addr, byte, len(value))
            self.mnem = "TEXT"
            self.value = escape(value)
        else:
            Entry.__init__(self, addr, byte, 1)
            self.mnem = "BYTE"
            self.value = ">%02X" % value  # bytes are not resolved

    def list(self, isprog=False):
        """return textual representation of literal"""
        return Entry.list0(self, isprog, self.mnem, self.value)


class Instruction(Entry):
    """an instruction"""

    def __init__(self, prog, addr, byte, mnemonic, iformat, ops, fmtlvl,
                 syntax, comment=""):
        Entry.__init__(self, addr, byte, 1 + sum([op.size for op in ops]))
        self.prog = prog  # surrounding program (list of entries)
        self.mnemonic = mnemonic  # mnemonic of instruction
        self.iformat = iformat  # instruction format
        self.operands = ops  # list of operands
        self.comment = comment  # optional comment
        self.fmtlvl = fmtlvl  # current FMT level (0=normal, 1+=FMT mode)
        self.syntax = syntax  # syntax variant used

    def list(self, isprog=False):
        """pretty print current instruction"""
        optexts = [op.text for op in self.operands]
        try:
            # adjust for requested syntax variant
            mnem, opfmt = self.syntax.repls[self.mnemonic]
            ops = opfmt.format(*optexts) if opfmt else ", ".join(optexts)
        except KeyError:
            # keep original
            mnem = self.mnemonic
            ops = ", ".join(optexts)
        return Entry.list0(self, isprog, mnem, ops)
 

class Operand:
    """an instruction operand"""

    def __init__(self, addr, byte, size, text, dest=None):
        self.addr = addr  # current address
        self.byte = byte  # current byte
        self.size = size  # operand index size
        self.text = text  # textual representation of operand
        self.dest = dest  # direct addressing


class Program:
    """the program to disassemble"""

    def __init__(self, binary, addr, symbols):
        self.binary = binary  # binary blob
        self.addr = addr  # initial address of binary
        self.symbols = symbols  # symbol table
        self.code = [Unknown(addr + i, ord(binary[i]))  # list of entries
                     for i in xrange(len(binary))]
        self.size = len(self.code)  # index size of program
        self.end = self.addr + self.size  # final address of program
        self.equtext = ""

    def addr2idx(self, addr):
        """converts address to program index"""
        return addr - self.addr

    def idx2addr(self, idx):
        """converts program index to address"""
        return self.addr + idx

    def register(self, idx, instr, force=False):
        """register disassembled instruction in program"""
        assert idx == self.addr2idx(instr.addr)  # consistency
        assert not isinstance(self.code[idx], Instruction)  # no double work
        # are some of the operands already taken by other instructions?
        if not force:
            for i in xrange(idx, idx + instr.size):
                if not isinstance(self.code[i], Unknown):
                    XdgLogger.warn(
                        "Would overwrite already disassembled index %d" % i)
                    return False
        # persist instruction and mark bytes of operands as disassembled
        for i in xrange(idx + 1, idx + instr.size):
            # undo previous disassembly runs
            if isinstance(self.code[i], Instruction):
                self.deregister(i)
            elif isinstance(self.code[i], Used):
                self.deregister(self.code[i].parent)
            self.code[i] = Used(self.code[i].addr, self.code[i].byte, idx)
        self.code[idx] = instr  # add current instruction
        return True

    def deregister(self, idx):
        """remove disassembled instruction from code"""
        assert isinstance(self.code[idx], Instruction)
        for i in xrange(self.code[idx].size):
            entry = self.code[idx + i]
            self.code[idx + i] = Unknown(entry.addr, entry.byte)
        
    def list(self, start=None, end=None, isprog=False):
        """pretty print entire program"""
        idx = self.addr2idx(start) if start else 0
        idxto = self.addr2idx(end) if end else self.size
        indent = " " * (7 if isprog else 10)
        orgs = (indent + "GROM >%04X\n" % (self.addr & 0xe000) +
                indent + "AORG >%04X\n" % (self.addr & 0x1fff))
        listing = [self.code[i].list(isprog=isprog)
                   for i in xrange(idx, idxto)]
        return orgs + self.equtext + "\n".join(listing) + "\n"


class BadSyntax:
    """used for invalid syntax entries"""

    def __init__(self, addr, byte):
        self.addr = addr
        self.byte = byte
        self.size = 1

    def list(self, isprog):
        if isprog:
            return "L%04X  BAD SYNTAX %02X" % (self.addr, self.byte)
        else:
            return "%04X %02X!  BAD SYNTAX" % (self.addr, self.byte)


class Disassembler:
    """disassemble machine code"""

    def __init__(self, syntax, excludes):
        self.opcodes = Opcodes(syntax)  # prepare opcodes
        self.excludes = excludes
        
    def decode(self, prog, idx, idxto, fmtlvl):
        """decode range of instructions"""
        while 0 <= idx < idxto:
            instr, fmtlvl = self.opcodes.decode(prog, idx, fmtlvl)
            success = prog.register(idx, instr)
            assert success == True  # top-down should not have conflicts
            idx += instr.size
    
    def disassemble(self, prog, start=None, end=None):
        """top-down disassembler"""
        idx = prog.addr2idx(start or prog.addr)
        idxto = prog.addr2idx(end or prog.end)
        self.decode(prog, idx, idxto, 0)

    def run(self, prog, start, end=None, force=False, origin=None):
        """run disassembler"""
        # check if address is valid
        if not prog.addr <= start < prog.end:
            XdgLogger.warn("Cannot disassemble external context @>%04X" % start)
            return  # cannot disassemble external content
        idx = prog.addr2idx(start)
        idxto = prog.addr2idx(end or prog.end)
        fmtlvl = 0  # start in standard mode
        # disassemble loop
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
                instr, fmtlvl = self.opcodes.decode(prog, idx, fmtlvl)
                # make entry for instruction
                if not prog.register(idx, instr, force=force):
                    break  # abort on conflict
                new = True
            else:
                # already disassembled
                instr = prog.code[idx]  # Instruction
                fmtlvl = instr.fmtlvl
                new = False
            # mark jump from other address to here, if applicable
            if origin:
                instr.origins.append(origin)
                origin = None
            if not new:
                break  # everything else already done
            # check for flow control changes
            if isinstance(instr, Instruction):
                if instr.mnemonic in Opcodes.branches:
                    # execution is redirected
                    for addr in self.opcodes.jumps(prog, instr):
                        self.run(prog, addr, end,
                                 force=force, origin=prog.idx2addr(idx))
                    break
                elif instr.mnemonic in Opcodes.calls:
                    # execution is forked
                    for addr in self.opcodes.jumps(prog, instr):
                        self.run(prog, addr, end,
                                 force=force, origin=prog.idx2addr(idx))
                elif instr.mnemonic in Opcodes.returns:
                    # execution stops
                    break
            idx += instr.size

    def getstarts(self, prog):
        """returns start addresses for given program"""
        # check for cart header
        if prog.binary[0] == "\xaa" and prog.addr == 0x6000:
            # autostart?
            if ord(prog.binary[1]) >= 0x80:
                XdgLogger.info("auto-starting cart")
                idx = 0x10 if prog.binary[16] != "\x00" else 0x13
                # do not start disassembly at >6010/>6013, as the run
                # disassembler would also follow >6011/>6014, which is
                # incorrect here
                self.decode(prog, idx, idx + 1, 0)  # decode BR
                return [prog.code[idx].operands[0].dest]  # follow manually
            # regular cart, return menu entry start addresses
            menu, starts = ordw(prog.binary[6:8]) - prog.addr, []
            try:
                while menu != 0x0000:
                    starts.append(ordw(prog.binary[menu + 2:menu + 4]))
                    menu = ordw(prog.binary[menu:menu + 2])
            except:
                XdgLogger.warn("bad cartridge menu structure")
            return starts
        else:
            # unknown binary
            return [prog.addr]  # begin of program

    def findstrings(self, prog, minlen=6, start=None, end=None):
        """convert consecutive unclaimed letters to string literals"""
        idx = prog.addr2idx(start) if start else 0
        idxto = prog.addr2idx(end) if end else prog.size
        # find un-disassembled chunks
        while 0 <= idx < idxto:
            for i in xrange(idx, idxto):
                try:
                    if not isinstance(prog.code[i], Unknown):
                        break
                except IndexError:
                    break
            # found Unknown chunk (might be empty)
            chunk = prog.binary[idx:i]
            # search for text literal of at least size 6 in Unknown chunk
            m = re.search(r"[A-Za-z0-9 ,.:?!()\-]{%d,}" % minlen, chunk)
            if m:
                # replace Unknowns by Literal
                pidx = idx + m.start(0)
                prog.register(pidx, Literal(prog.idx2addr(pidx),
                                            prog.code[pidx],
                                            chunk[m.start(0):m.end(0)]))
            idx = i + 1

    def program(self, prog):
        """turns disassembled fragment into assembly source"""
        # make Unknowns into Literals
        for idx in xrange(prog.size):
            instr = prog.code[idx]
            if isinstance(instr, Unknown):
                prog.register(idx, Literal(instr.addr, instr.byte, instr.byte))
        # add symbol EQUs, if needed
        prog.equtext += "".join(["%-8s EQU  >%04X\n" % (s, v)
                                 for s, v in prog.symbols.getused()])

    def toggle(self, prog, addr):
        """disassemle/undo at given index (unused)"""
        idx = prog.addr2idx(addr)
        if isinstance(prog.code[idx], Unknown):
            start = prog.idx2addr(idx)
            self.run(prog, start, start + 1)
        else:
            for i in prog.code[idx].size:
                prog.register(idx + i, Unknown(prog.code[idx + i].addr,
                                               prog.code[idx + i].byte))


### Command line processing

def main():
    import argparse

    args = argparse.ArgumentParser(
        version=VERSION,
        description="GPL disassembler",
        epilog="All addresses are hex values and may by prefixed optionally by '>' or '0x'.")
    args.add_argument("source", metavar="<source>",
                      help="GPL binary code")
    cmd = args.add_mutually_exclusive_group(required=True)
    cmd.add_argument("-r", "--run", metavar="<addr>", dest="runs", nargs="+",
                      help="disassemble running from addresses, or 'start'")
    cmd.add_argument("-f", "--from", metavar="<addr>", dest="frm",
                      help="disassemble top-down from address or 'start'")
    args.add_argument("-a", "--address", metavar="<addr>", dest="addr",
                      help="GROM address of first byte")
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
    args.add_argument("-s", "--syntax", dest="syntax",
                      help="syntax variant to use")
    args.add_argument("-S", "--symbols", dest="symfiles", nargs="+",
                      help="known symbols files")
    args.add_argument("-V", "--verbose", action="store_true", dest="verbose",
                      help="verbose messages")
    args.add_argument("-o", "--output", dest="outfile",
                      help="output filename")
    opts = args.parse_args()

    # setup
    dirname = os.path.dirname(opts.source) or "."
    basename = os.path.basename(opts.source)
    barename = os.path.splitext(basename)[0]
    output = opts.outfile or barename + ".dis"
    
    binary = readbin(opts.source)
    addr = xhex(opts.addr) if opts.addr is not None else 0x6000
    addrto = xhex(opts.to)

    if opts.verbose:
        XdgLogger.setlevel(1)

    try:
        symbols = Symbols(symfiles=opts.symfiles)
        prog = Program(binary, addr, symbols=symbols)
        syntax = Syntax.get(opts.syntax or "xdt99")
        excludes = [[prog.addr2idx(xhex(i)) for i in e.split("-")]
                    for e in (opts.exclude or [])]
        dis = Disassembler(syntax, excludes)

        if opts.frm:
            # top-down disassembler: uses specified start address -f
            XdgLogger.info("top-down disassembly")
            addrfrom = min(dis.getstarts(prog)) if opts.frm.lower() == "start" else xhex(opts.frm)
            dis.disassemble(prog, addrfrom, addrto)
        else:
            # run disassembler: uses specified run addresses -r
            XdgLogger.info("run trace disassembly")
            runs = [xhex(r) for r in (opts.runs or []) if r.lower() != "start"]
            if len(runs) < len(opts.runs):  # means "start" in runs
                runs += dis.getstarts(prog)
            for run in runs:
                dis.run(prog, run, addrto, force=opts.force)
        if opts.strings:
            XdgLogger.info("extractign strings")            
            dis.findstrings(prog)
        if opts.program:
            XdgLogger.info("finalizing into complete program")
            dis.program(prog)
    except XdgError as e:
        XdgLogger.error("ERROR: %s" % e)
    except IOError as e:
        sys.exit("%s: %s." % (e.filename, e.strerror))
    try:
        source = prog.list(isprog=opts.program or False)
        writelines(output, "w", source)
    except IOError as e:
        sys.exit("%s: %s." % (e.filename, e.strerror))
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)    
