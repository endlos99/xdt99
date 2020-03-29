#!/usr/bin/env python

# xda99: TMS9900 disassembler
#
# Copyright (c) 2017-2020 Ralph Benzinger <xdt99@endlos.net>
#
# This program is part of the TI 99 Cross-Development Tools (xdt99).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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


VERSION = '3.0.0'


# Utility functions

def ordw(word):
    """word ord"""
    return (word[0] << 8) | word[1]


def chrw(word):
    """word chr"""
    return bytes((word >> 8, word & 0xff))


def xhex(text):
    """return hex string as integer value"""
    try:
        return text if text is None else int(re.sub(r'^>|^0x', '', text), 16)
    except ValueError:
        raise XdaError('Invalid hex value: ' + text)


def escape(bytes_):
    """escape non-printable characters"""
    bytes_ = bytes_.replace(b"'", b"''")
    return "'" + ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_) + "'"


def readbin(name, mode='rb'):
    """read lines from file or STDIN"""
    if name == '-':
        if 'b' in mode:
            return sys.stdin.buffer.read()
        else:
            return sys.stdin.read()
    else:
        with open(name, mode) as f:
            return f.read()


def writelines(name, data, mode='rb'):
    """write lines to file or STDOUT"""
    if name == '-':
        if 'b' in mode:
            sys.stdout.buffer.write(data)
        else:
            sys.stdout.write(data)
    else:
        with open(name, mode) as f:
            f.write(data)


# Error handling

class XdaError(Exception):
    pass


class XdaLogger(object):

    level_debug = 0
    level_info = 1
    level_warn = 2
    level_error = 3

    log_level = 2

    @staticmethod
    def setlevel(level):
        XdaLogger.log_level = level

    @staticmethod
    def warn(message):
        if XdaLogger.log_level <= XdaLogger.level_warn:
            print('Warning:', message)

    @staticmethod
    def info(message):
        if XdaLogger.log_level <= XdaLogger.level_info:
            print('Info:', message)

    @staticmethod
    def debug(message):
        if XdaLogger.log_level <= XdaLogger.level_debug:
            print('Debug:', message)


# Symbol table

class Symbols(object):
    """symbol table"""

    def __init__(self, symfiles=None):
        # pre-defined symbols
        self.symbols = {
            0x210c: 'VSBW', 0x2110: 'VMBW',
            0x2114: 'VSBR', 0x2118: 'VMBR',
            0x211c: 'VWTR', 0x2108: 'KSCAN',
            0x2100: 'GPLLNK', 0x2104: 'XMLLNK',
            0x2120: 'DSRLNK', 0x2124: 'LOADER',
            0x2022: 'UTLTAB', 0x000e: 'SCAN',
            0x8300: 'PAD', 0x83e0: 'GPLWS',
            0x8400: 'SOUND',
            0x8800: 'VDPRD', 0x8802: 'VDPST',
            0x8c00: 'VDPWD', 0x8c02: 'VDPWA',
            0x9000: 'SPCHRD', 0x9400: 'SPCHWT',
            0x9800: 'GRMRD', 0x9802: 'GRMRA',
            0x9c00: 'GRMWD', 0x9c02: 'GRMWA'
            }
        # additional symbols loaded from file(s)
        if symfiles:
            for sf in symfiles:
                self.load(sf)
        # symbols referenced in program
        self.used = {}

    def load(self, fn):
        """load symbol EQUs from file"""
        with open(fn, 'r') as fsym:
            lines = fsym.readlines() + ['']
        for i in range(len(lines) - 1):
            longline = lines[i] + lines[i + 1]  # join two lines to resolve continuation labels
            m = re.match(r'^(\w+):?\s*(?:EQU)?\s+(>?[0-9A-F]+)\s', longline.upper())
            if not m:
                continue
            symbol, addr = m.group(1), xhex(m.group(2))
            if self.symbols.get(addr) is not None:
                XdaLogger.warn(f'Symbol for >{addr:04X} already defined, overwritten')
            self.symbols[addr] = symbol

    def resolve(self, value):
        """find symbol name for given value, or return >xx/xxxx value """
        try:
            symbol = self.symbols[value]
        except KeyError:
            return f'>{value:04X}'
        self.used[symbol] = value  # mark symbol as used for EQU prelude
        return symbol

    def get_used(self):
        """return dict of all symbols that have been used"""
        return self.used.items()


# Opcodes

class Opcodes(object):

    # listing of all TMS 9900 opcodes
    opcodes = {
        # 6. arithmetic
        0xa000: ('A', 1),
        0xb000: ('AB', 1),
        0x0740: ('ABS', 6),  # 4 in E/A Manual
        0x0220: ('AI', 8),
        0x0600: ('DEC', 6),
        0x0640: ('DECT', 6),
        0x3c00: ('DIV', 9),
        0x0580: ('INC', 6),
        0x05c0: ('INCT', 6),
        0x3800: ('MPY', 9),
        0x0500: ('NEG', 6),
        0x6000: ('S', 1),
        0x7000: ('SB', 1),
        # 7. jump and branch
        0x0440: ('B', 6),
        0x0680: ('BL', 6),
        0x0400: ('BLWP', 6),
        0x1300: ('JEQ', 2),
        0x1500: ('JGT', 2),
        0x1400: ('JHE', 2),
        0x1b00: ('JH', 2),
        0x1a00: ('JL', 2),
        0x1200: ('JLE', 2),
        0x1100: ('JLT', 2),
        0x1000: ('JMP', 2),
        0x1700: ('JNC', 2),
        0x1600: ('JNE', 2),
        0x1900: ('JNO', 2),
        0x1c00: ('JOP', 2),
        0x1800: ('JOC', 2),
        0x0380: ('RTWP', 7),
        0x0480: ('X', 6),
        0x2c00: ('XOP', 9),
        # 8. compare instructions
        0x8000: ('C', 1),
        0x9000: ('CB', 1),
        0x0280: ('CI', 8),
        0x2000: ('COC', 3),
        0x2400: ('CZC', 3),
        # 9. control and cru instructions
        0x3000: ('LDCR', 4),
        0x1d00: ('SBO', 12),
        0x1e00: ('SBZ', 12),
        0x3400: ('STCR', 4),
        0x1f00: ('TB', 12),
        0x03c0: ('CKOF', 7),
        0x03a0: ('CKON', 7),
        0x0340: ('IDLE', 7),
        0x0360: ('RSET', 7),
        0x03e0: ('LREX', 7),
        # 10. load and move instructions
        0x0200: ('LI', 8),
        0x0300: ('LIMI', 10),
        0x02e0: ('LWPI', 10),
        0xc000: ('MOV', 1),
        0xd000: ('MOVB', 1),
        0x02c0: ('STST', 11),
        0x02a0: ('STWP', 11),
        0x06c0: ('SWPB', 6),
        # 11. logical instructions
        0x0240: ('ANDI', 8),
        0x0260: ('ORI', 8),
        0x2800: ('XOR', 3),
        0x0540: ('INV', 6),
        0x04c0: ('CLR', 6),
        0x0700: ('SETO', 6),
        0xe000: ('SOC', 1),
        0xf000: ('SOCB', 1),
        0x4000: ('SZC', 1),
        0x5000: ('SZCB', 1),
        # 12. shift instructions
        0x0800: ('SRA', 5),
        0x0900: ('SRL', 5),
        0x0a00: ('SLA', 5),
        0x0b00: ('SRC', 5),
        # End of opcodes
    }

    opcodes_9995 = {
        0x01c0: ('MPYS', 6),
        0x0180: ('DIVS', 6),
        0x0080: ('LST', 8),
        0x0090: ('LWP', 8)
    }

    opcodes_f18a = {
        # F18A GPU instructions
        0x0c80: ('CALL', 6),
        0x0c00: ('RET', 7),
        0x0d00: ('PUSH', 6),
        0x0f00: ('POP', 6),
        0x0e00: ('SLC', 5)
    }

    # 13. pseudo instructions
    pseudos = {
        0x1000: ('NOP', 2),
        0x045b: ('RT', 6)
    }

    # number of valid MSB bits for each instruction format
    # Example: Format III:  O O O O O O - - / - - - - - - - -
    #                       \---------------/
    #           8 bits needed to identify opcode for format III
    opcbitmask = (
        -1, 4, 8, 6, 6, 8, 10, 16, 12, 6,  # regular formats
        16, 12, 12)  # special formats

    # opcodes that redirect execution
    branches = ('B', 'JMP')

    # opcodes that fork execution
    calls = ('BL', 'BLWP',
             'JNE', 'JEQ', 'JGT', 'JLT', 'JH', 'JHE', 'JL', 'JLE', 'JOC',
             'JNC', 'JOP', 'JNO')

    # opcodes that terminate execution
    returns = ('RT', 'RTWP')

    def __init__(self, no_r, tms9995=False, f18a=False):
        self.regstr = '' if no_r else 'R'
        self.tms9995 = tms9995
        self.f18a = f18a

    def get(self, code):
        """return Opcode entry for code word"""
        entry = Opcodes.opcodes.get(code)
        if entry is None and self.tms9995:
            entry = Opcodes.opcodes_9995.get(code)
        if entry is None and self.f18a:
            entry = Opcodes.opcodes_f18a.get(code)
        return entry

    def decode(self, program, idx, tms9995=False, f18a=False):
        """get instruction for next words(s)"""
        entry = program.code[idx]
        assert entry.addr == program.idx2addr(idx)  # check sanity
        # already disassembled?
        if isinstance(entry, Instruction):
            return entry
        addr, word = entry.addr, entry.word
        # pseudo instruction?
        if word in Opcodes.pseudos:
            mnemonic, instr_format = Opcodes.pseudos[word]
            return Instruction(program, addr, word, mnemonic, instr_format, [], '')
        mnemonic = None
        # search for mnemonic: try all bit masks
        for mask, mask_len in (
                # (bitmask, number of left-most bit set)
                (0xf000, 4), (0xfc00, 6), (0xff00, 8), (0xffc0, 10), (0xfff0, 12), (0xffff, 16)
        ):
            try:
                candidate, instr_format = Opcodes.opcodes.get(word & mask)
                # (word & bitmask) might match the prefix of some other opcode, so we need
                # to check if the opcode bit length matches the current mask bit length
                if Opcodes.opcbitmask[instr_format] == mask_len:
                    mnemonic = candidate
                    break
            except TypeError:
                pass  # try next
        if mnemonic is None:
            return Literal(addr, word, word, program.symbols)  # no mnemonic found, keep as data
        # decode operands
        try:
            ops = self.decode_instr_format(addr, word, program.code, idx + 1, instr_format, program.symbols)
        except IndexError as e:
            return entry  # abort decoding
        # build and return instruction
        return Instruction(program, addr, word, mnemonic, instr_format, ops, '')

    def decode_instr_format(self, addr, word, code, idx, instr_format, symbols):
        """decode operands for given instruction format"""
        # I. two general address instructions
        if instr_format == 1:
            td = (word >> 10) & 0x03  # variables ts, s, td, d, etc
            ts = (word >> 4) & 0x03   # correspond to E/A manual
            d = (word >> 6) & 0x0f
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx + i1, td, d, symbols)
            return o1, o2
        # II. jump and bit I/O instructions
        elif instr_format == 2:
            disp = -(~word & 0x00ff) - 1 if word & 0x0080 else word & 0x007f
            a = addr + 2 + 2 * disp
            return Operand(None, None, 0, symbols.resolve(a), dest=a),
        # III. logical instructions
        elif instr_format == 3:
            d = (word >> 6) & 0x0f
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx + i1, 0, d, symbols)
            return o1, o2
        # IV. CRU multi-bit instructions
        elif instr_format == 4:
            c = (word >> 6) & 0x0f
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx, 8, c, symbols)
            return o1, o2
        # V. register shift instructions
        elif instr_format == 5:
            c = (word >> 4) & 0x0f
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 8, w, symbols)
            i2, o2 = self.decode_addr(code, idx, 7, c, symbols)
            return o1, o2
        # VI. single address instructions
        elif instr_format == 6:
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            return o1,
        # VII. control instructions
        elif instr_format == 7:
            return ()
        # VIII. immediate instructions
        elif instr_format == 8:  # two opers
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 0, w, symbols)
            i2, o2 = self.decode_addr(code, idx, 9, 0, symbols)
            return o1, o2
        elif instr_format == 81:  # one opers reg
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 0, w, symbols)
            return (o1,)
        elif instr_format == 82:  # one opers addr
            i1, o1 = self.decode_addr(code, idx, 2, 0, symbols)
            return (o1,)
        # IX. extended operations; multiply and divide
        elif instr_format == 9:
            d = (word >> 6) & 0x0f
            ts = (word >> 4) & 0x03
            s = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, ts, s, symbols)
            i2, o2 = self.decode_addr(code, idx + i1, 0, d, symbols)
            return o1, o2
        # special cases
        elif instr_format == 10:  # LIMI, LWPI
            w = word & 0x0f
            i1, o1 = self.decode_addr(code, idx, 9, 0, symbols)
            return o1,
        elif instr_format == 11:  # STST, STWP
            w = word & 0x0f
            return Operand(None, None, 0, self.regstr + str(w)),
        elif instr_format == 12:  # bit operations
            disp = -(~word & 0x00ff) - 1 if word & 0x0080 else word & 0x007f
            return Operand(None, None, 0, str(disp)),
        else:
            raise XdaError('Invalid instruction format ' + str(instr_format))

    def decode_addr(self, code, idx, t, operand, symbols):
        """decodes address mode of operand"""
        if t == 0:  # workspace register
            return 0, Operand(None, None, 0, self.regstr + str(operand))
        elif t == 1:  # workspace register indirect
            return 0, Operand(None, None, 0, '*' + self.regstr + str(operand))
        elif t == 2:  # symbolic or indexed memory
            addr, word = code[idx].addr, code[idx].word
            t = '@' + symbols.resolve(word)
            if operand:
                t += '(' + self.regstr + str(operand) + ')'
            return 1, Operand(addr, word, 1, t, dest=None if operand else word)
        elif t == 3:  # workspace register indirect auto-incr
            return 0, Operand(None, None, 0, '*' + self.regstr + str(operand) + '+')
        elif t == 7:  # count
            return 0, Operand(None, None, 0, str(operand))
        elif t == 8:  # register
            return 0, Operand(None, None, 0, self.regstr + str(operand))
        elif t == 9:  # imm values
            addr, word = code[idx].addr, code[idx].word
            return 1, Operand(addr, word, 1, symbols.resolve(word))
        else:
            raise XdaError('Invalid address format ' + str(t))

    def jump_target(self, prog, instr):
        """return target address of branching instruction"""
        assert instr.mnemonic in Opcodes.branches + Opcodes.calls
        dest = instr.operands[0].dest
        # special case for BLWP:
        if instr.mnemonic == 'BLWP' and dest is not None:
            try:
                # BLWP points to WP and PC words
                dest = prog.code[prog.addr2idx(dest + 2)].word  # PC
            except IndexError:
                dest = None
        return dest


class Entry(object):
    """base class for all entries for a given word position"""

    def __init__(self, addr, word, size=1, indicator=' '):
        self.addr = addr  # addr of word
        self.word = word  # value of word
        self.size = size  # index size of entire instruction
        self.origins = []  # addresses this entry was jumped at from
        self.indicator = indicator  # status indicator

    def _list(self, as_prog, strict, mnemonic='', ops=''):
        """internal pretty printing function"""
        if self.origins:
            origin = '; <- ' + ', '.join(f'>{o:04X}' for o in sorted(self.origins))
        else:
            origin = ''
        prog_fmt = 'L{:04X}  {:4s} {:20s} {:s}'
        list_fmt = '{:04X} {:04X}{:s}  {:4s} {:20s} {:s}'
        if not strict:
            prog_fmt = prog_fmt.lower()
            list_fmt = list_fmt.lower()
            mnemonic = mnemonic.lower()
            origin = origin.lower()
            ops = ','.join(op if "'" in op else op.lower() for op in ops.split(','))  # keeps spacing
        if as_prog:  # program format, can be re-assembled
            return prog_fmt.format(self.addr, mnemonic, ops, origin)
        else:  # listing format
            return list_fmt.format(self.addr, self.word, self.indicator, mnemonic, ops, origin)

    def list(self, as_prog=False, strict=False, concise=False):
        """pretty print current entry"""
        return self._list(as_prog, strict)


class Unknown(Entry):
    """unknown, not disassembled value"""

    def __init__(self, addr, word):
        Entry.__init__(self, addr, word, indicator='?')

    def list(self, as_prog=False, strict=False, concise=False):
        return None if concise else self._list(as_prog, strict)


class Used(Entry):
    """word that is part of an instruction"""

    def __init__(self, addr, word, parent):
        Entry.__init__(self, addr, word, indicator=' ')
        self.parent = parent  # parent instruction


class Instruction(Entry):
    """an instruction"""

    def __init__(self, prog, addr, word, mnemonic, instr_format, ops, comment=''):
        Entry.__init__(self, addr, word, 1 + sum(op.size for op in ops))
        self.prog = prog  # surrounding program
        self.mnemonic = mnemonic  # mnemonic of instruction
        self.instr_format = instr_format  # instruction format
        self.operands = ops  # listing of operands
        self.comment = comment  # optional comment

    def list(self, as_prog=False, strict=False, concise=False):
        """pretty print current instruction"""
        ops_text = [op.text for op in self.operands]
        ops = (',' if strict else ', ').join(ops_text)
        return Entry._list(self, as_prog, strict, self.mnemonic, ops)


class Operand(object):
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
        if isinstance(value, bytes):
            assert len(value) % 2 == 0
            Entry.__init__(self, addr, word, len(value) // 2)
            self.mnemonic = 'TEXT'
            self.value = escape(value)
        else:
            Entry.__init__(self, addr, word, 1)
            self.mnemonic = 'DATA'
            self.value = symbols.resolve(value)

    def list(self, as_prog=False, strict=False, concise=False):
        """return textual representation of literal"""
        return Entry._list(self, as_prog, strict, self.mnemonic, self.value)


class Program(object):
    """a binary program"""

    def __init__(self, binary, addr, symbols):
        self.binary = binary  # binary blob
        self.addr = addr  # start addr
        self.symbols = symbols  # symbol table
        self.code = [Unknown(addr + i, ordw(binary[i:i + 2]))  # listing of entries
                     for i in range(0, len(binary), 2)]
        self.size = len(self.code)  # index size of programm
        self.end = self.addr + len(binary)  # final address of program
        self.equ_text = ''  # EQU statements

    def addr2idx(self, addr):
        """converts address to code index"""
        return (addr - self.addr) // 2

    def idx2addr(self, idx):
        """converts code index to addr"""
        return self.addr + idx * 2

    def addr_range(self, text):
        """convert address range in index range"""
        try:
            start, stop = text.split('-')
        except ValueError:
            raise XdaError('Bad range specifier: ' + text)
        return self.addr2idx(xhex(start)), self.addr2idx(xhex(stop))

    def register(self, idx, instr, force=False):
        """register disassembled instruction in program"""
        assert idx == self.addr2idx(instr.addr)  # consistency
        assert not isinstance(self.code[idx], Instruction)  # no double work
        # is the instruction conflicting with previous instructions?
        if not force:
            for i in range(idx, idx + instr.size):
                if not isinstance(self.code[i], Unknown):
                    XdaLogger.warn('Would overwrite already disassembled index ' + str(i))
                    return False
        # persist instruction and mark words of operands as disassembled
        for i in range(idx, idx + instr.size):
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
        for i in range(self.code[idx].size):
            entry = self.code[idx + i]
            self.code[idx + i] = Unknown(entry.addr, entry.word)

    def list(self, start=None, end=None, strict=False, concise=False, as_prog=False):
        """pretty print entire program"""
        start_idx = self.addr2idx(start) if start else 0
        end_idx = self.addr2idx(end) if end else self.size
        aorg = (' ' * (7 if as_prog else 12) +
                ('AORG >{:04X}\n' if strict else 'aorg >{:04x}\n').format(self.addr))
        equ_text = self.equ_text if strict else self.equ_text.lower()
        listing = [self.code[i].list(as_prog=as_prog, strict=strict, concise=concise)
                   for i in range(start_idx, end_idx)]
        if concise and not as_prog:  # no unknown parts in programs
            listing = self.condense(listing)
        return aorg + equ_text + '\n'.join(listing) + '\n'

    def condense(self, listing):
        i = 0
        while i < len(listing):
            if listing[i] is None:
                del listing[i]
            elif i > 0 and int(listing[i][:4], 16) - int(listing[i - 1][:4], 16) > 2:
                listing.insert(i, '....')
                i += 2
            else:
                i += 1
        return listing


class BadSyntax(object):
    """used for invalid syntax entries"""

    def __init__(self, addr, word):
        self.addr = addr
        self.word = word
        self.size = 1

    def list(self, as_prog=False, strict=False, concise=False):
        if as_prog:
            error = 'L{:04X}  BAD SYNTAX {:04X}'.format(self.addr, self.word)
        else:
            error = '{:04X} {:04X}!  BAD SYNTAX'.format(self.addr, self.word)
        return error if strict else error.lower()


class Disassembler(object):
    """disassemble machine code"""

    def __init__(self, excludes, no_r=False, tms9995=False, f18a=False):
        self.opcodes = Opcodes(no_r, tms9995=tms9995, f18a=f18a)
        self.excludes = excludes

    def is_excluded(self, addr):
        """is addr in any excluded range?"""
        for excl_from, excl_to in self.excludes:
            if excl_from <= addr < excl_to:
                return excl_from, excl_to
        return None

    def decode(self, program, idx, idx_to):
        """decode instructions in range"""
        while 0 <= idx < idx_to:
            excluded_range = self.is_excluded(idx)
            if excluded_range is not None:
                _, next_addr = excluded_range
                idx = next_addr + next_addr % 2  # round up to next even
            instr = self.opcodes.decode(program, idx)
            success = program.register(idx, instr)
            assert success  # top-down should not have conflicts
            idx += instr.size

    def disassemble(self, program, start=None, end=None):
        """top-down disassembler"""
        idx = program.addr2idx(start or program.addr)
        idx_to = program.addr2idx(end or program.end)
        self.decode(program, idx, idx_to)

    def run(self, program, start, end=None, force=False, origin=None):
        """run disassembler"""
        # check if address is valid
        if not program.addr <= start < program.end:
            XdaLogger.warn(f'Cannot disassemble external context @>{start:04X}')
            return  # cannot disassemble external content
        start_idx = program.addr2idx(start)
        end_idx = program.addr2idx(end or program.end)
        while 0 <= start_idx < end_idx:
            # excluded range?
            for excl_from, excl_to in self.excludes:
                if excl_from <= start_idx < excl_to:
                    if excl_to >= end_idx:  # done
                        return
                    start_idx = excl_to  # skip to end of excluded range
                    break
            # disassemble instruction
            if not isinstance(program.code[start_idx], Instruction):
                instr = self.opcodes.decode(program, start_idx)
                # make entry for instruction
                if not program.register(start_idx, instr, force=force):
                    break  # abort on conflict
                new = True
            else:
                # already disassembled
                instr = program.code[start_idx]  # Instruction
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
                    addr = self.opcodes.jump_target(program, instr)
                    if addr is not None:
                        self.run(program, addr, end, force=force, origin=program.idx2addr(start_idx))
                    break
                elif instr.mnemonic in Opcodes.calls:
                    # execution is forked
                    addr = self.opcodes.jump_target(program, instr)
                    if addr is not None:
                        self.run(program, addr, end, force=force, origin=program.idx2addr(start_idx))
                elif instr.mnemonic in Opcodes.returns:
                    # execution stops
                    break
            start_idx += instr.size

    def get_starts(self, program):
        """returns listing of all recognized start addresses"""
        # check for cartridge header
        if program.binary[0] == 0xaa:
            # cart, no autostart
            menu, starts = ordw(program.binary[6:8]) - program.addr, []
            try:
                # find all menu entries
                while menu != 0x0000:
                    starts.append(ordw(program.binary[menu + 2:menu + 4]))
                    menu = ordw(program.binary[menu:menu + 2])
            except IndexError:
                XdaLogger.warn('Bad cartridge menu structure')
            return starts
        else:
            # unknown binary
            return [program.addr]  # begin of program

    def find_strings(self, program, min_len=6, start=None, end=None):
        """convert consecutive unclaimed letters to string literals"""
        start_idx = program.addr2idx(start) if start else 0
        end_idx = program.addr2idx(end) if end else program.size
        # find un-disassembled chunks
        while start_idx < end_idx:
            for i in range(start_idx, end_idx):
                try:
                    if not isinstance(program.code[i], Unknown):
                        break
                except IndexError:
                    break
            # found Unknown chunk (might be empty)
            chunk = program.binary[start_idx * 2:i * 2]
            # search for text literal of at least size 6 in Unknown chunk
            m = re.search(rb'[A-Za-z0-9 ,.:?!()\-]{%d,}' % min_len, chunk)
            if m:
                # replace Unknowns by Literal
                m_start = m.start(0) if m.start(0) % 2 == 0 else m.start(0) + 1
                m_end = m.end(0) if m.end(0) % 2 == 0 else m.end(0) - 1
                # TODO: odd positions would require to issue BYTEs here
                lidx = start_idx + m_start // 2
                program.register(lidx, Literal(program.idx2addr(lidx),
                                               program.code[lidx].word,
                                            chunk[m_start:m_end], program.symbols))
            start_idx = i + 1

    def make_program(self, program):
        """turns disassembled fragment into assembly source"""
        # turn unknowns into literals
        for idx in range(program.size):
            instr = program.code[idx]
            if isinstance(instr, Unknown):
                program.code[idx] = Literal(instr.addr, instr.word, instr.word, program.symbols)
        # add symbol EQUs, if needed
        program.equ_text += ''.join('{:8s} EQU  >{:04X}\n'.format(s, v) for s, v in program.symbols.get_used())


# Command line processing

def main():
    import argparse

    args = argparse.ArgumentParser(
        description='TMS9900 disassembler, v' + VERSION,
        epilog="All addresses are hex values and may by prefixed optionally by '>' or '0x'.")
    args.add_argument('binary', metavar='<file>',
                      help='machine code file')
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument('-r', '--run', metavar='<addr>', dest='runs', nargs='+',
                      help='run from additional addresses')
    cmd.add_argument('-f', '--from', metavar='<addr>', dest='frm',
                      help="disassemble top-down from address, or 'start'")
    args.add_argument('-a', '--address', metavar='<addr>', dest='addr',
                      help='address of first word')
    args.add_argument('-t', '--to', metavar='<addr>', dest='to',
                      help='disassemble to address (default: end)')
    args.add_argument('-e', '--exclude', metavar='<addr>-<addr>', dest='exclude', nargs='+',
                      help='exclude address ranges')
    args.add_argument('-k', '--skip', metavar='<bytes>', dest='skip',
                      help='skip bytes at beginning of file')
    args.add_argument('-F', '--force', action='store_true', dest='force',
                      help='force overwriting of previous disassembly')
    args.add_argument('-5', '--9995', action='store_true', dest='dis_9995',
                      help='disassembly TMS9995 opcodes')
    args.add_argument('-18', '--f18a', action='store_true', dest='dis_f18a',
                      help='disassembly F18A opcodes')
    args.add_argument('-p', '--program', action='store_true', dest='program',
                      help='disassemble to complete program')
    args.add_argument('-c', '--concise', action='store_true', dest='concise',
                      help='show only disassembled parts')
    args.add_argument('-n', '--strings', action='store_true', dest='strings',
                      help='disassemble string literals')
    args.add_argument('-R', '--no-r', action='store_true', dest='nor',
                      help='do not prepend registers with 'R'')
    args.add_argument('-s', '--strict', action='store_true', dest='strict',
                      help='use strict legacy syntax')
    args.add_argument('-S', '--symbols', metavar='<file>', dest='symfiles', nargs='+',
                      help='known symbols file(s)')
    args.add_argument('-V', '--verbose', action='store_true', dest='verbose',
                      help='verbose messages')
    args.add_argument('-o', '--output', metavar='<file>', dest='outfile',
                      help='output filename')
    opts = args.parse_args()

    # setup
    basename = os.path.basename(opts.binary)
    barename = os.path.splitext(basename)[0]
    output = opts.outfile or barename + '.dis'

    if opts.verbose:
        XdaLogger.setlevel(XdaLogger.level_info)

    try:
        binary = readbin(opts.binary)[xhex(opts.skip) or 0:]
        addr = xhex(opts.addr) if opts.addr is not None else 0x6000
        addr_to = xhex(opts.to)

        symbols = Symbols(opts.symfiles)
        program = Program(binary, addr, symbols=symbols)
        excludes = [program.addr_range(e) for e in (opts.exclude or ())]
        disasm = Disassembler(excludes, no_r=opts.nor, tms9995=opts.dis_9995, f18a=opts.dis_f18a)

        if opts.frm:
            # top-down disassembler: uses specified start address -f
            XdaLogger.info('top-down disassembly')
            addr_from = min(disasm.get_starts(program)) if opts.frm.lower() == 'start' else xhex(opts.frm)
            disasm.disassemble(program, addr_from, addr_to)
        else:
            # run disassembler: uses specified run addresses -r
            XdaLogger.info('run disassembly')
            runs = [xhex(r) for r in (opts.runs or []) if r.lower() != 'start']
            auto_run = any(r.lower() == 'start' for r in (opts.runs or []))
            if auto_run:
                runs += disasm.get_starts(program)
            for run in runs:
                disasm.run(program, run, addr_to, force=opts.force)
        if opts.strings:
            XdaLogger.info('extracting strings')
            disasm.find_strings(program)
        if opts.program:
            XdaLogger.info('finalizing into complete program')
            disasm.make_program(program)
    except XdaError as e:
        sys.exit(f'Error: {str(e):s}.')
    except IOError as e:
        sys.exit(f'{e.filename:s}: {e.strerror:s}.')
    try:
        source = program.list(as_prog=opts.program or False, strict=opts.strict, concise=opts.concise)
        writelines(output, source, 'w')
    except OSError as e:
        sys.exit(f'{e.filename:s}: {e.strerror:s}.')
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
