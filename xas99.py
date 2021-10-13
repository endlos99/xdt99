#!/usr/bin/env python3

# xas99: A TMS9900 cross-assembler
#
# Copyright (c) 2015-2021 Ralph Benzinger <r@0x01.de>
#
# This program is part of the TI 99 Cross-Development Tools (xdt99).
#
# xdt99 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import platform
import re
import math
import os.path
from functools import reduce


VERSION = '3.1.1'


# Utilities

class Util:
    """utility static methods"""

    @staticmethod
    def even(n):
        """round value down to even value"""
        return n - n % 2

    @staticmethod
    def ordw(word):
        """word ord"""
        return (word[0] << 8) | word[1]

    @staticmethod
    def chrw(word):
        """word chr"""
        return bytes((word >> 8, word & 0xff))

    @staticmethod
    def cmp(x, y):
        return (x > y) - (x < y)

    @staticmethod
    def xint(s):
        """return hex or decimal value"""
        return 0 if s is None else int(s.lstrip('>'), 16 if s[:2] == '0x' or s[:1] == '>' else 10)

    @staticmethod
    def sinc(s, i):
        """string sequence increment"""
        return None if s is None else s[:-1] + chr(ord(s[-1]) + i)

    @staticmethod
    def val(n):
        """dereference address"""
        return n.addr if isinstance(n, Address) else n

    @staticmethod
    def writedata(filename, data, mode='wb'):
        """write data to file or STDOUT"""
        if filename == '-':
            if 'b' in mode:
                sys.stdout.buffer.write(data)
            else:
                sys.stdout.write(data)
        else:
            with open(filename, mode) as f:
                f.write(data)

    @staticmethod
    def readdata(filename, data=None, encoding=None):
        """read data from file or STDIN (or return supplied data)"""
        if encoding is None:
            if filename == '-':
                return data or sys.stdin.buffer.read()
            else:
                with open(filename, 'rb') as f:
                    data = f.read()
                    return data
        else:
            try:
                if filename == '-':
                    return data or sys.stdin.read().encode(encoding)
                else:
                    with open(filename, 'r') as f:
                        data = f.read()
                    return data.encode(encoding)
            except UnicodeDecodeError:
                sys.exit('Bad encoding: ' + encoding)

    @staticmethod
    def readlines(filename, mode='r'):
        """read lines from file or STDIN"""
        if filename == '-':
            return sys.stdin.readlines()
        else:
            with open(filename, mode) as f:
                return f.readlines()

    @staticmethod
    def outname(basename, ext, tag='', redef=None, altname=None):
        """return output filename"""
        if redef is None:
            return basename + tag + ext
        else:
            return '-' if redef == '-' else (altname or redef) + tag

    @staticmethod
    def name_suffix(base=None, bank=None, use_base=False, bank_count=0):
        return (('' if not use_base else f'_{base:04x}') +
                ('' if bank is None or bank_count <= 1 else f'_b{bank}'))

    @staticmethod
    def max_bins_per_bank(binaries):
        """return max binaries per bank and None (None needed for bank-less programs)"""
        banks = [b for b, *_ in binaries]
        bank_count = max((b + 1 for b in banks if b is not None and b != Symbols.BANK_ALL), default=0)
        counts = {i: 0 for i in (None, *range(bank_count))}
        for b in banks:
            if b == Symbols.BANK_ALL:
                for i in range(bank_count):
                    counts[i] += 1
            else:
                counts[b] += 1
        return max(counts.values(), default=0)


# Exception Class

class AsmError(Exception):
    pass


# Misc. Objects

class Address(object):
    """absolute or relocatable address"""

    def __init__(self, addr, bank=None, reloc=False, unit_id=0):
        self.addr = addr
        self.bank = bank
        self.reloc = reloc
        self.unit_id = unit_id  # -1 for predefined and command-line defined symbols

    def hex(self):
        return '{:04X}{:s}'.format(self.addr, 'r' if self.reloc else ' ')

    def __eq__(self, other):
        """required for externally defined symbols in Symbols"""
        return (isinstance(other, Address) and
                self.addr == other.addr and self.bank == other.bank and self.reloc == other.reloc and
                self.unit_id == other.unit_id)


class Local(object):
    """local label reference"""

    def __init__(self, name, distance):
        self.name = name
        self.distance = distance


class AutoConstant(Address):

    def __init__(self, value, size='W', bank=None, symbols=None):
        super().__init__(None, unit_id=symbols.unit_id)
        self.value = value
        self.size = size
        self.bank = bank
        self.name = self.get_name(size, value, bank)
        self.addr = None
        self.symbols = symbols  # for finding address of auto-constant later

    @staticmethod
    def get_name(size, value, bank):
        return '_%auto' + size + str(value) + 'b' + str(bank)

    def resolve_addr(self):
        self.addr = self.symbols.get_symbol(self.name)
        return self.addr


class Reference(object):
    """external reference"""

    def __init__(self, name):
        self.name = name


class Value(object):
    """wraps value of auto-constants"""

    def __init__(self, value):
        self.value = value


class Block(object):
    """reserved block of bytes"""

    def __init__(self, size):
        self.size = size


class Word(object):
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
        sign = arg.sign() if op == '%' else self.sign() * arg.sign()
        val = self.abs() * arg.abs()
        self.value = (val if sign > 0 else -val) % 0x10000

    def div(self, op, arg):
        if arg.value == 0:
            raise AsmError('Division by zero')
        sign = arg.sign() if op == '%' else self.sign() * arg.sign()
        val = (self.abs() // arg.abs() if op == '/' else
               self.abs() % arg.abs() if op == '%' else None)
        self.value = (val if sign > 0 else -val) % 0x10000

    def bit(self, op, arg):
        val = (self.value & arg.value if op == '&' else
               self.value | arg.value if op == '|' else
               self.value ^ arg.value if op == '^' else None)
        self.value = val % 0x10000


# Opcodes and Directives

class Timing(object):

    WAITSTATES = 4

    def __init__(self, cycles, mem_accesses, read=False, byte=False, x2=False):
        """capture the basic timing information for instruction execution,
           under the assumption that
          - registers reside in scratchpad RAM, and
          - instructions reside in waitstate RAM.
        """
        self.cycles = cycles
        self.mem_accesses = mem_accesses
        self.addl_cycles = (0, 4, 8, 6) if byte else (0, 4, 8, 8)  # value for each addressing mode
        self.addl_mem = ((0, 2, 4, 2) if x2 else
                         (0, 1, 2, 1) if read else
                         (0, 2, 3, 2))

    def time0(self):
        """compute number of cycles for execution (no args)"""
        return self.cycles + self.WAITSTATES * self.mem_accesses

    def time1(self, tx, xa):
        """compute number of cycles for execution (one arg)"""
        # NOTE: represents tables A/B: [0, 1, 1/2, 2], but compensates
        #       for register read with zero wait state
        c = self.cycles + self.addl_cycles[tx]
        m = self.mem_accesses + self.addl_mem[tx]
        return c + self.WAITSTATES * m

    def time2(self, ts, sa, td, da):
        """compute number of cycles for execution (one arg)"""
        c = self.cycles + self.addl_cycles[ts] + self.addl_cycles[td]
        m = self.mem_accesses + [0, 1, 2, 1][ts] + [0, 2, 3, 2][td]
        return c + self.WAITSTATES * m


class Opcodes(object):
    op_ga = lambda parser, x: parser.address(x)  # [0x0000 .. 0xFFFF]
    op_wa = lambda parser, x: parser.register(x)  # [0 .. 15]
    op_imm = lambda parser, x: parser.expression(x, iop=True)  # [0x0000 .. 0xFFFF]
    op_cru = lambda parser, x: parser.expression(x, iop=True)  # [-128 .. 127]
    op_disp = lambda parser, x: parser.relative(x)  # [-254 .. 256]
    op_cnt = lambda parser, x: parser.expression(x, iop=True)  # [0 .. 15]
    op_scnt = lambda parser, x: parser.expression(x, iop=True, allow_r0=True)  # [0 .. 15]
    op_xop = lambda parser, x: parser.expression(x, iop=True)  # [1 .. 2]

    opcodes_9900 = {
        # 6. arithmetic
        'A': (0xa000, 1, op_ga, op_ga, Timing(14, 1)),
        'AB': (0xb000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        'ABS': (0x0740, 6, op_ga, None, Timing(14, 1)),  # 4 in E/A Manual
        'AI': (0x0220, 8, op_wa, op_imm, Timing(14, 2)),
        'DEC': (0x0600, 6, op_ga, None, Timing(10, 1)),
        'DECT': (0x0640, 6, op_ga, None, Timing(10, 1)),
        'DIV': (0x3c00, 9, op_ga, op_wa, Timing(124, 1, read=True)),
        'INC': (0x0580, 6, op_ga, None, Timing(10, 1)),
        'INCT': (0x05c0, 6, op_ga, None, Timing(10, 1)),
        'MPY': (0x3800, 9, op_ga, op_wa, Timing(52, 1, read=True)),
        'NEG': (0x0500, 6, op_ga, None, Timing(12, 1)),
        'S': (0x6000, 1, op_ga, op_ga, Timing(14, 1)),
        'SB': (0x7000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        # 7. jump and branch
        'B': (0x0440, 6, op_ga, None, Timing(8, 1, read=True)),
        'BL': (0x0680, 6, op_ga, None, Timing(12, 1, read=True)),
        'BLWP': (0x0400, 6, op_ga, None, Timing(26, 1, read=True, x2=True)),
        'JEQ': (0x1300, 2, op_disp, None, Timing(10, 1)),
        'JGT': (0x1500, 2, op_disp, None, Timing(10, 1)),
        'JHE': (0x1400, 2, op_disp, None, Timing(10, 1)),
        'JH': (0x1b00, 2, op_disp, None, Timing(10, 1)),
        'JL': (0x1a00, 2, op_disp, None, Timing(10, 1)),
        'JLE': (0x1200, 2, op_disp, None, Timing(10, 1)),
        'JLT': (0x1100, 2, op_disp, None, Timing(10, 1)),
        'JMP': (0x1000, 2, op_disp, None, Timing(10, 1)),
        'JNC': (0x1700, 2, op_disp, None, Timing(10, 1)),
        'JNE': (0x1600, 2, op_disp, None, Timing(10, 1)),
        'JNO': (0x1900, 2, op_disp, None, Timing(10, 1)),
        'JOP': (0x1c00, 2, op_disp, None, Timing(10, 1)),
        'JOC': (0x1800, 2, op_disp, None, Timing(10, 1)),
        'RTWP': (0x0380, 7, None, None, Timing(14, 1)),
        'X': (0x0480, 6, op_ga, None, Timing(8, 1, read=True)),  # approx.
        'XOP': (0x2c00, 9, op_ga, op_xop, Timing(36, 2)),
        # 8. compare instructions
        'C': (0x8000, 1, op_ga, op_ga, Timing(14, 1, read=True)),
        'CB': (0x9000, 1, op_ga, op_ga, Timing(14, 1, read=True, byte=True)),
        'CI': (0x0280, 8, op_wa, op_imm, Timing(14, 2)),
        'COC': (0x2000, 3, op_ga, op_wa, Timing(14, 1)),
        'CZC': (0x2400, 3, op_ga, op_wa, Timing(14, 1)),
        # 9. control and cru instructions
        'LDCR': (0x3000, 4, op_ga, op_cnt, Timing(52, 1)),
        'SBO': (0x1d00, 2, op_cru, None, Timing(12, 2)),
        'SBZ': (0x1e00, 2, op_cru, None, Timing(12, 2)),
        'STCR': (0x3400, 4, op_ga, op_cnt, Timing(60, 1)),
        'TB': (0x1f00, 2, op_cru, None, Timing(12, 2)),
        'CKOF': (0x03c0, 7, None, None, Timing(12, 1)),
        'CKON': (0x03a0, 7, None, None, Timing(12, 1)),
        'IDLE': (0x0340, 7, None, None, Timing(12, 1)),
        'RSET': (0x0360, 7, None, None, Timing(12, 1)),
        'LREX': (0x03e0, 7, None, None, Timing(12, 1)),
        # 10. load and move instructions
        'LI': (0x0200, 8, op_wa, op_imm, Timing(12, 2)),
        'LIMI': (0x0300, 81, op_imm, None, Timing(16, 2)),
        'LWPI': (0x02e0, 81, op_imm, None, Timing(10, 2)),
        'MOV': (0xc000, 1, op_ga, op_ga, Timing(14, 1)),
        'MOVB': (0xd000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        'STST': (0x02c0, 8, op_wa, None, Timing(8, 1)),
        'STWP': (0x02a0, 8, op_wa, None, Timing(8, 1)),
        'SWPB': (0x06c0, 6, op_ga, None, Timing(10, 1)),
        # 11. logical instructions
        'ANDI': (0x0240, 8, op_wa, op_imm, Timing(14, 2)),
        'ORI': (0x0260, 8, op_wa, op_imm, Timing(14, 2)),
        'XOR': (0x2800, 3, op_ga, op_wa, Timing(14, 1, read=True)),
        'INV': (0x0540, 6, op_ga, None, Timing(10, 1)),
        'CLR': (0x04c0, 6, op_ga, None, Timing(10, 1)),
        'SETO': (0x0700, 6, op_ga, None, Timing(10, 1)),
        'SOC': (0xe000, 1, op_ga, op_ga, Timing(14, 1)),
        'SOCB': (0xf000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        'SZC': (0x4000, 1, op_ga, op_ga, Timing(14, 1)),
        'SZCB': (0x5000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        # 12. shift instructions
        'SRA': (0x0800, 5, op_wa, op_scnt, Timing(52, 1)),
        'SRL': (0x0900, 5, op_wa, op_scnt, Timing(52, 1)),
        'SLA': (0x0a00, 5, op_wa, op_scnt, Timing(52, 1)),
        'SRC': (0x0b00, 5, op_wa, op_scnt, Timing(52, 1))
        # end of opcodes
    }

    opcodes_f18a = {
        # F18A GPU instructions
        'CALL': (0x0c80, 6, op_ga, None, Timing(0, 0)),
        'RET': (0x0c00, 7, None, None, Timing(0, 0)),
        'PUSH': (0x0d00, 6, op_ga, None, Timing(0, 0)),
        'POP': (0x0f00, 6, op_ga, None, Timing(0, 0)),
        'SLC': (0x0e00, 5, op_wa, op_scnt, Timing(0, 0))
    }

    opcodes_9995 = {
        # 9995 instructions
        'MPYS': (0x01c0, 6, op_ga, None, Timing(0, 0)),  # Note that 9900 timing and 9995 timing
        'DIVS': (0x0180, 6, op_ga, None, Timing(0, 0)),  # cannot be compared
        'LST': (0x0080, 8, op_wa, None, Timing(0, 0)),
        'LWP': (0x0090, 8, op_wa, None, Timing(0, 0))
    }

    opcodes_99000 = {
        # 99105 and 99110 instructions
        'MPYS': (0x01c0, 6, op_ga, None, Timing(0, 0)),  # Note that 9900 timing and 99000 timing
        'DIVS': (0x0180, 6, op_ga, None, Timing(0, 0)),  # cannot be compared
        'LST': (0x0080, 8, op_wa, None, Timing(0, 0)),
        'LWP': (0x0090, 8, op_wa, None, Timing(0, 0)),
        'BIND': (0x0140, 106, op_ga, None, Timing(0, 0)),
        'BLSK': (0x00b0, 108, op_wa, op_imm, Timing(0, 0)),
        'TMB': (0x0c09, 103, op_ga, op_cnt, Timing(0, 0)),
        'TCMB': (0xc0a, 103, op_ga, op_cnt, Timing(0, 0)),
        'TSMB': (0x0c0b, 103, op_ga, op_cnt, Timing(0, 0)),
        'AM': (0x002a, 101, op_ga, op_ga, Timing(0, 0)),
        'SM': (0x0029, 101, op_ga, op_ga, Timing(0, 0)),
        'SLAM': (0x001d, 109, op_ga, op_scnt, Timing(0, 0)),
        'SRAM': (0x001c, 109, op_ga, op_scnt, Timing(0, 0))
    }

    pseudos = {
        # 13. pseudo instructions
        'NOP': ('JMP', ['$+2']),
        'RT': ('B', ['*<R>11']),
        'SLL': ('SRL', None),
        'PIX': ('XOP', None)
    }

    def __init__(self, use_9995=False, use_f18a=False, use_99000=False):
        """create opcode set; note that asm and parser might change over lifetime of opcodes"""
        self.opcodes = Opcodes.opcodes_9900
        if use_9995:
            self.opcodes.update(Opcodes.opcodes_9995)
        if use_f18a:
            self.opcodes.update(Opcodes.opcodes_f18a)
        if use_99000:
            self.opcodes.update(Opcodes.opcodes_99000)
        self.asm = None

    def use_asm(self, asm):
        """set assembler to use"""
        self.asm = asm

    def process(self, label, mnemonic, operands):
        """get assembly asm for mnemonic"""
        self.asm.even()
        self.asm.process_label(label)
        if mnemonic in Opcodes.pseudos:
            m, ops = Opcodes.pseudos[mnemonic]
            if ops is not None:
                ops = [o.replace('<R>', 'R' if self.asm.parser.r_prefix else '') for o in ops]
            mnemonic, operands = m, ops or operands
        elif mnemonic in self.asm.parser.symbols.xops:
            mode = self.asm.parser.symbols.xops[mnemonic]
            mnemonic, operands = 'XOP', [operands[0], mode]
        if mnemonic in self.opcodes:
            try:
                opcode, fmt, parse_op1, parse_op2, timing = self.opcodes[mnemonic]
                if parse_op1 and len(operands) != (1 if parse_op2 is None else 2):
                    raise AsmError('Bad operand count')
                arg1 = parse_op1(self.asm.parser, operands[0]) if parse_op1 else None
                arg2 = parse_op2(self.asm.parser, operands[1]) if parse_op2 else None
                Optimizer.process(self.asm, mnemonic, opcode, fmt, arg1, arg2)
                self.generate(opcode, fmt, arg1, arg2, timing)
                return True
            except (IndexError, ValueError, TypeError):
                raise AsmError('Syntax error')
        else:
            raise AsmError('Invalid mnemonic: ' + mnemonic)

    def generate(self, opcode, fmt, arg1, arg2, timing):
        """generate byte asm"""
        # I. two general address instructions
        if fmt == 1:
            ts, s, sa = arg1
            td, d, da = arg2
            b = opcode | td << 10 | d << 6 | ts << 4 | s
            t = timing.time2(ts, sa, td, da)
            self.asm.emit(b, sa, da, cycles=t)
        # II. jump and bit I/O instructions
        elif fmt == 2:
            b = opcode | arg1 & 0xff
            t = timing.time0()
            self.asm.emit(b, cycles=t)
        # III. logical instructions
        elif fmt == 3:
            ts, s, sa = arg1
            d = arg2
            b = opcode | d << 6 | ts << 4 | s
            t = timing.time1(ts, sa)
            self.asm.emit(b, sa, cycles=t)
        # IV. CRU multi-bit instructions
        elif fmt == 4:
            ts, s, sa = arg1
            c = arg2
            b = opcode | c << 6 | ts << 4 | s
            t = timing.time1(ts, sa)
            self.asm.emit(b, sa, cycles=t)
        # V. register shift instructions
        elif fmt == 5:
            w = arg1
            c = arg2
            b = opcode | c << 4 | w
            t = timing.time0()
            self.asm.emit(b, cycles=t)
        # VI. single address instructions
        elif fmt == 6:
            ts, s, sa = arg1
            b = opcode | ts << 4 | s
            t = timing.time1(ts, sa)
            self.asm.emit(b, sa, cycles=t)
        # VII. control instructions
        elif fmt == 7:
            b = opcode
            t = timing.time0()
            self.asm.emit(b, cycles=t)
        # VIII. immediate instructions
        elif fmt == 8:
            b = opcode | arg1
            t = timing.time0()
            self.asm.emit(b, arg2, cycles=t)
        elif fmt == 81:
            b = opcode
            t = timing.time0()
            self.asm.emit(b, arg1, cycles=t)
        # IX. extended operations; multiply and divide
        elif fmt == 9:
            ts, s, sa = arg1
            r = arg2
            b = opcode | r << 6 | ts << 4 | s
            t = timing.time1(ts, sa)
            self.asm.emit(b, sa, cycles=t)
        # TMS99000
        elif fmt == 101:  # AM/SM
            ts, s, sa = arg1
            td, d, da = arg2
            b = td << 10 | d << 6 | ts << 4 | s
            self.asm.emit(opcode, b, sa, da)
        elif fmt == 103:  # T*B
            ts, s, sa = arg1
            if ts == 3:
                raise AsmError('Indirect autoincrement addressing not defined for T*MB mnemonics')
            disp = arg2
            b = disp << 6 | ts << 4 | s
            self.asm.emit(opcode, b, sa)
        elif fmt == 106:  # BIND
            ts, s, sa = arg1
            b = opcode | ts << 4 | s
            self.asm.emit(b, sa)
        elif fmt == 108:  # BLSK
            w = arg1
            imm = arg2
            b1 = opcode | w
            b2 = imm
            self.asm.emit(b1, b2)
        elif fmt == 109:  # S*AM
            ts, s, sa = arg1
            scnt = arg2
            b = scnt << 6 | ts << 4 | s
            self.asm.emit(opcode, b, sa)
        else:
            raise AsmError('Invalid opcode format ' + str(fmt))


class Directives(object):

    ignores = ['', 'PSEG', 'PEND', 'CSEG', 'CEND', 'DSEG', 'DEND', 'UNL', 'LIST', 'PAGE', 'TITL', 'LOAD', 'SREF']

    @staticmethod
    def DEF(asm, label, ops):
        if asm.symbols.pass_no == 1:
            asm.process_label(label)
        else:
            for op in ops:
                asm.symbols.add_def(op[:6] if asm.parser.strict else op)

    @staticmethod
    def REF(asm, label, ops):
        if asm.symbols.pass_no != 1:
            return
        for op in ops:
            asm.symbols.add_ref(op[:6] if asm.parser.strict else op)

    @staticmethod
    def EQU(asm, label, ops):
        if asm.symbols.pass_no != 1:
            value = asm.symbols.get_symbol(label)
            asm.listing.add(asm.symbols.LC, text1='', text2=value)
            return
        Directives.check_ops(asm, ops, min_count=1, max_count=1, warning_only=True)
        if not label:
            raise AsmError('Missing label')
        value = asm.parser.expression(ops[0], well_defined=True)
        asm.symbols.add_symbol(label, value, equ=Symbols.EQU)

    @staticmethod
    def WEQU(asm, label, ops):
        if asm.symbols.pass_no != 1:
            value = asm.symbols.get_symbol(label)
            asm.listing.add(asm.symbols.LC, text1='', text2=value)
            return
        Directives.check_ops(asm, ops, min_count=1, max_count=1, warning_only=True)
        if not label:
            raise AsmError('Missing label')
        value = asm.parser.expression(ops[0], well_defined=True)
        asm.symbols.add_symbol(label, value, equ=Symbols.WEQU)

    @staticmethod
    def DATA(asm, label, ops):
        asm.even()  # required for s# modifier
        asm.process_label(label, tracked=True)
        Directives.check_ops(asm, ops, min_count=1)
        for op in ops:
            word = asm.parser.expression(op)
            asm.word(word)

    @staticmethod
    def BYTE(asm, label, ops):
        asm.process_label(label, tracked=True)
        Directives.check_ops(asm, ops, min_count=1)
        for op in ops:
            byte_ = asm.parser.expression(op)
            asm.byte(byte_)

    @staticmethod
    def TEXT(asm, label, ops):
        asm.process_label(label, tracked=True)
        Directives.check_ops(asm, ops, min_count=1)
        for op in ops:
            text = asm.parser.text(op)
            for char_ in text:
                asm.byte(ord(char_))

    @staticmethod
    def STRI(asm, label, ops):
        asm.process_label(label, tracked=True)
        Directives.check_ops(asm, ops, min_count=1)
        text = ''.join(asm.parser.text(op) for op in ops)
        asm.byte(len(text))
        for char_ in text:
            asm.byte(ord(char_))

    @staticmethod
    def FLOA(asm, label, ops):
        asm.process_label(label, tracked=True)
        Directives.check_ops(asm, ops, min_count=1)
        for op in ops:
            bytes_ = asm.parser.radix100(op)
            for b in bytes_:
                asm.byte(b)

    @staticmethod
    def BSS(asm, label, ops):
        Directives.check_ops(asm, ops, min_count=1, max_count=1, warning_only=True)
        asm.process_label(label, tracked=True)
        size = asm.parser.value(ops[0])
        asm.block(size)

    @staticmethod
    def BES(asm, label, ops):
        Directives.check_ops(asm, ops, min_count=1, max_count=1, warning_only=True)
        size = asm.parser.value(ops[0])
        asm.block(size, offset=size)
        asm.process_label(label, tracked=True)

    @staticmethod
    def EVEN(asm, label, ops):
        asm.even()
        asm.process_label(label)  # differs from E/A manual!

    @staticmethod
    def AORG(asm, label, ops):
        Directives.check_ops(asm, ops, max_count=2)
        base = asm.parser.value(ops[0]) if ops else None
        if len(ops) > 1:
            raise AsmError('Cannot use bank with AORG directive (deprecated use)')
        asm.org(base, reloc=False)
        asm.process_label(label)

    @staticmethod
    def RORG(asm, label, ops):
        Directives.check_ops(asm, ops, max_count=1)
        base = asm.parser.value(ops[0]) if ops else None
        asm.org(base, reloc=True)
        asm.process_label(label)

    @staticmethod
    def DORG(asm, label, ops):
        Directives.check_ops(asm, ops, max_count=1)
        base = asm.parser.expression(ops[0], well_defined=True)
        reloc = isinstance(base, Address) and base.reloc
        asm.org(Util.val(base), dummy=True, reloc=reloc)
        asm.process_label(label)

    @staticmethod
    def XORG(asm, label, ops):
        Directives.check_ops(asm, ops, min_count=1, max_count=1)
        asm.process_label(label, real_LC=True)
        base = asm.parser.value(ops[0])
        asm.org(base, reloc=False, xorg=True)

    @staticmethod
    def BANK(asm, label, ops):
        Directives.check_ops(asm, ops, min_count=1, max_count=2)
        bank = asm.parser.bank(ops[0])
        if bank > Symbols.BANK_ALL or (bank == Symbols.BANK_ALL and not ops[0].isalpha()):
            raise AsmError(f'Bank number too large, must be less than { Symbols.BANK_ALL }')
        base = asm.symbols.switch_bank(bank, asm.parser.expression(ops[1], well_defined=True) if len(ops) > 1 else None)
        asm.org(base, bank=bank)
        asm.process_label(label, real_LC=True)

    @staticmethod
    def COPY(asm, label, ops):
        asm.process_label(label)
        if asm.parser.symbols.pass_no == 2:
            return
        Directives.check_ops(asm, ops, min_count=1, max_count=1)
        filename = asm.parser.filename_text(ops[0])
        asm.parser.open(filename=filename)

    @staticmethod
    def END(asm, label, ops):
        Directives.check_ops(asm, ops, max_count=1)
        asm.process_label(label)
        if ops and asm.symbols.pass_no > 1:
            asm.program.set_entry(asm.symbols.get_symbol(ops[0][:6] if asm.parser.strict else ops[0]))
        asm.parser.stop()

    @staticmethod
    def IDT(asm, label, ops):
        if asm.symbols.pass_no > 1:
            return
        Directives.check_ops(asm, ops, max_count=1)
        asm.process_label(label)
        text = asm.parser.text(ops[0]) if ops else '        '
        asm.program.set_name(text[:8])

    @staticmethod
    def SAVE(asm, label, ops):
        if asm.symbols.pass_no < 2:
            return
        Directives.check_ops(asm, ops, min_count=2, max_count=2)
        try:
            first = asm.parser.expression(ops[0]) if ops[0] else None
            last = asm.parser.expression(ops[1]) if ops[1] else None
        except IndexError:
            raise AsmError('Invalid arguments')
        if isinstance(first, Reference) or isinstance(last, Reference):
            raise AsmError('Invalid arguments')
        asm.program.saves.append((first, last))

    @staticmethod
    def DXOP(asm, label, ops):
        if asm.symbols.pass_no != 1:
            return
        Directives.check_ops(asm, ops, min_count=2, max_count=2)
        asm.process_label(label)
        try:
            mode = asm.parser.expression(ops[1], well_defined=True)
            asm.symbols.add_XOP(ops[0], str(mode))
        except IndexError:
            raise AsmError('Invalid arguments')

    @staticmethod
    def BCOPY(asm, label, ops):
        """extension: include binary file as BYTE stream"""
        Directives.check_ops(asm, ops, min_count=1, max_count=1)
        asm.process_label(label)
        filename = asm.parser.filename_text(ops[0])
        path = asm.parser.find(filename)
        try:
            with open(path, 'rb') as f:
                bs = f.read()
                for b in bs:
                    asm.byte(b)
        except IOError as e:
            raise AsmError(e)

    @staticmethod
    def AUTO(asm, label, ops):
        """place auto-generated constants here"""
        if asm.symbols.pass_no == 1 and asm.symbols.bank == Symbols.BANK_ALL:
            raise AsmError('Directive AUTO cannot be placed in shared bank area')
        asm.process_label(label)
        asm.auto_constants()

    @staticmethod
    def check_ops(asm, ops, min_count=None, max_count=None, warning_only=False):
        if min_count and len(ops) < min_count:
            raise AsmError('Missing operand(s)')
        if max_count and len(ops) > max_count:
            if warning_only:
                asm.parser.warn('Ignoring extra operands')
            else:
                raise AsmError('Bad operand count')

    @staticmethod
    def process(asm, label, mnemonic, operands):
        if mnemonic in Directives.ignores:
            asm.process_label(label)
            return True
        try:
            fn = getattr(Directives, mnemonic)
        except AttributeError:
            return False
        try:
            fn(asm, label, operands)
        except (IndexError, ValueError):
            raise AsmError('Syntax error')
        return True


# Symbol table

class Externals(object):
    """externally defined and referenced symbols"""

    def __init__(self, target, definitions=None):
        self.target = target
        self.references = []
        self.definitions = {
            'SCAN': (0x000e, -1),  # unit_id -1 = built-in
            'PAD': (0x8300, -1),
            'GPLWS': (0x83e0, -1),
            'SOUND': (0x8400, -1),
            'VDPRD': (0x8800, -1),
            'VDPSTA': (0x8802, -1),
            'VDPWD': (0x8c00, -1),
            'VDPWA': (0x8c02, -1),
            'SPCHRD': (0x9000, -1),
            'SPCHWT': (0x9400, -1),
            'GRMRD': (0x9800, -1),
            'GRMRA': (0x9802, -1),
            'GRMWD': (0x9c00, -1),
            'GRMWA': (0x9c02, -1)
        }
        if definitions:
            self.add_env(definitions)

    def add_env(self, definitions):
        """add external symbol definitions (-D)"""
        for defs in definitions:
            for d in defs.upper().split(','):
                try:
                    name, value_str = d.split('=')
                    value = Parser.external(value_str)
                except ValueError:
                    name, value = d, 1
                # add as Address(), to keep equality with DEFs inferred from 5/6 tags
                self.definitions[name] = Address(value, reloc=False), -1


class Symbols(object):
    """symbol table and line counter
       Each symbol entry is a tuple (value, equ-kind, used).
       Equ-kind symbols may be redefined, if EQU by the same value only.
       Used tracks if a symbol has been used (True/False).  If set to None, usage is not tracked.
       Each program unit owns its own symbol table.
    """
    unit_id = 0

    # symbol kind
    NONE = 0  # not an EQU symbol
    EQU = 1   # EQU symbols (can be redefined by same value)
    WEQU = 2  # weak EQU symbol (can be redefined by other value)
    BANK_ALL = 411  # shared code

    def __init__(self, externals, console, add_registers=False, strict=False):
        self.externals = externals
        self.console = console
        self.registers = {'R' + str(i): i for i in range(16)} if add_registers else {}
        self.strict = strict
        self.symbols = {n: (v, False, None) for n, v in self.registers.items()}  # registers are just symbols
        self.saved_LC = {True: 0, False: 0}  # key == relocatable
        self.xops = {}
        self.locations = []
        self.interm_source = []
        self.unit_id = Symbols.unit_id
        Symbols.unit_id += 1
        self.local_lid = 0
        self.pass_no = 0
        self.lidx = 0
        self.autoconsts = set()  # set of auto-generated constants
        self.autos_defined = set()
        self.autos_generated = set()
        self.LC = None  # current line counter
        self.bank = None  # current bank, or None
        self.bank_LC = None  # next LC for each bank
        self.bank_base = 0  # base addr of BANK <addr>
        self.segment_reloc = self.xorg_offset = self.pad_idx = None
        self.reset()

    def reset(self):
        """reset some properties for assembly pass 2"""
        self.LC = 0
        self.bank = None
        self.segment_reloc = True
        self.xorg_offset = None
        self.pad_idx = 0
        self.reset_banks()

    def reset_banks(self):
        """reset LC for all banks"""
        self.bank_LC = {Symbols.BANK_ALL: 0}  # next LC for each bank

    def effective_LC(self):
        """compute effective LC inside and outside of XORG sections"""
        return self.LC + (self.xorg_offset or 0)

    def save_LC(self):
        """save current reloc or non-reloc LC"""
        self.saved_LC[self.segment_reloc] = self.LC

    def restore_LC(self, base, reloc, bank):
        """restore LC for new segment"""
        self.xorg_offset = None
        self.segment_reloc = reloc
        if base is None:
            self.LC = self.saved_LC[reloc]
        elif bank is None:
            self.LC = base
        else:
            self.LC = base + self.bank_LC.get(bank, 0) if reloc else base  # bank is set in BANK dir

    def valid(self, name):
        """is name a valid symbol name?"""
        return ((not self.strict and name != '$' and name[0] not in "!@" and not re.search(r'[-+*/#"\']', name[1:])) or
                (name[0].isalpha() and name.isalnum()))

    def add_symbol(self, name, value, tracked=False, check=True, equ=None):
        """add symbol to symbol table"""
        if equ is None:
            equ = Symbols.NONE  # workaround for Python limitation
        if check and not self.valid(name):
            raise AsmError(f'Invalid symbol name {name}')
        try:
            defined_value, defined_equ, unused = self.symbols[name]
            # existing definition
            if isinstance(value, Reference):
                return name  # don't overwrite values by Reference
            elif isinstance(defined_value, Reference):
                pass  # resolve Reference, fall-through
            else:
                new_entry = self._valid_redefinition(defined_value, defined_equ, name, value, equ)
                if new_entry is None:
                    raise AsmError('Duplicate symbols: ' + name)
                else:
                    value, equ = new_entry
        except KeyError:
            # new definition
            unused = tracked or None  # true=unused, false=used, None=don't track
        if isinstance(value, Address):
            value.unit_id = self.unit_id
        self.symbols[name] = value, equ, unused
        return name

    def _valid_redefinition(self, defined_value, defined_equ, name, value, equ):
        """check if redefinition of symbol is allowed"""
        if equ == Symbols.NONE or defined_equ == Symbols.NONE:  # either symbol not an EQU
            return None  # duplicate symbol
        if defined_equ == Symbols.EQU:  # defined symbol is EQU
            if equ == Symbols.EQU:
                if defined_value != value:
                    raise AsmError(f"Value {value} of symbol {name} does no match previous definition {defined_value}")
                else:
                    return defined_value, defined_equ
            elif equ == Symbols.WEQU:
                self.console.warn('Ignoring WEQU directive trying to redefine EQU directive')
                return defined_value, defined_equ
        elif defined_equ == Symbols.WEQU:
            if equ == Symbols.EQU:
                self.console.warn(f'Replacing WEQU value {defined_value} by EQU value {value}')
                return value, equ
            elif equ == Symbols.WEQU:
                self.console.warn(f'Redefining WEQU value {defined_value} by {value}')
                return value, equ
        return None

    def add_label(self, label, real_LC=False, tracked=False, check=True):
        """add a new label symbol to symbol table"""
        addr = Address(self.LC if real_LC else self.effective_LC(),
                       self.bank,
                       self.segment_reloc and (real_LC or not self.xorg_offset),
                       self.unit_id)
        name = self.add_symbol(label, addr, tracked=tracked, check=check)
        self.locations.append((self.lidx, name))

    def add_local_label(self, label):
        """add a new local label symbol to symbol table"""
        self.local_lid += 1
        self.add_label(label + '$' + str(self.local_lid), check=False)

    def add_autoconst(self, auto: AutoConstant):
        """create auto-constant in symbol table"""
        if auto.bank in self.autos_generated:
            raise AsmError(f'Auto-generated constant placed after AUTO directive')
        if isinstance(auto.value, Address):
            raise AsmError('Modifier expressions cannot involve addresses')
        if not isinstance(auto.value, int):
            raise AsmError('Invalid modifier expression')
        self.autoconsts.add((auto.size, auto.value, auto.bank))

    def add_def(self, name):
        """add globally defined symbol (added to symbol table separately)"""
        if not self.valid(name):
            raise AsmError(f'Invalid symbol name {name}')
        if name in self.externals.definitions:
            _, unit_id = self.externals.definitions[name]
            if unit_id >= 0 and unit_id != self.unit_id:
                raise AsmError(f'Duplicate definitions for symbol {name}')
        value = self.get_symbol(name)
        self.externals.definitions[name] = (value, self.unit_id)

    def add_ref(self, name):
        """add referenced symbol (also adds as unknown value to symbol table)"""
        if not self.valid(name):
            raise AsmError(f'Invalid reference {name}')
        if name not in self.externals.references:
            self.externals.references.append(name)
            self.add_symbol(name, Reference(name))  # don't set reloc when defining reference

    def add_XOP(self, name, mode):
        """define XOP operation"""
        self.xops[name] = mode

    def pad(self):
        """add padding to symbol table for correct size computations"""
        self.add_label(f'_%pad{self.pad_idx}', check=False)
        self.pad_idx += 1

    def get_symbol(self, name):
        """retrieve value of given symbol, or None"""
        try:
            value, equ, unused = self.symbols[name]
            if unused:
                self.symbols[name] = (value, equ, False)  # symbol has been used
        except KeyError:
            try:
                value, _ = self.externals.definitions.get(name)
            except TypeError:
                value = None
        return value

    def get_local(self, name, distance):
        """return local label specified by current position and distance +/-n"""
        targets = [(loc, sym) for (loc, sym) in self.locations if sym[:len(name) + 1] == name + '$']
        try:
            i, lidx = next((j, loc) for j, (loc, name) in enumerate(targets) if loc >= self.lidx)
            if distance > 0 and lidx > self.lidx:
                distance -= 1  # i points to +! unless lidx == self.lidx
        except StopIteration:
            i = len(targets)  # beyond last label
        try:
            _, fullname = targets[i + distance]
        except IndexError:
            return None
        return self.get_symbol(fullname)

    def get_size(self, name):
        """return byte distance of given symbol to next defined symbol"""
        try:
            lpos = next(loc for (loc, sym) in self.locations if sym == name)
        except StopIteration:
            raise AsmError('Unknown label: ' + name)
        try:
            _, next_name = min(((loc - lpos, sym) for (loc, sym) in self.locations if loc > lpos),
                               key=lambda x: x[0])
        except ValueError:
            raise AsmError('Cannot determine size of symbol: ' + name)
        sym_addr, next_addr = self.get_symbol(name), self.get_symbol(next_name)
        return Util.val(next_addr) - Util.val(sym_addr)

    def switch_bank(self, bank, addr=None):
        """update current active bank, returns new LC addr"""
        if addr is not None:
            self.bank_LC = {b: addr for b in self.bank_LC}  # new base addr
        else:
            self.bank_LC[self.bank] = self.LC
            if bank == Symbols.BANK_ALL:
                addr = max(*self.bank_LC.values())
            else:
                bank_LC = self.bank_LC.get(bank)
                if bank_LC is None:  # new bank
                    # new bank starts end of last shared bank
                    # (which equals bank base if no shared bank present after last addr)
                    bank_LC = self.bank_LC[bank] = self.bank_LC[Symbols.BANK_ALL]
                addr = addr or max(bank_LC, self.bank_LC[Symbols.BANK_ALL])
        self.saved_LC[True] = self.saved_LC[False] = addr
        self.bank = bank
        return addr

    def get_unused(self):
        """return all symbol names that have not been used"""
        return [name for name, (_, _, unused) in self.symbols.items() if unused]

    def list(self, strict, equ=False):
        """generate symbol overview"""
        symbol_list = []
        references = []
        for symbol in sorted(self.symbols):
            if symbol in self.registers or '$' in symbol or '%' in symbol:
                continue  # skip registers, local and internal symbols
            addr, _, _ = self.symbols.get(symbol)
            if isinstance(addr, Address):
                # add extra information to addresses
                reloc = 'REL' if addr.reloc else '   '
                bank = 'B>{:02X}'.format(addr.bank) if addr.bank != Symbols.BANK_ALL and addr.bank is not None else ''
                addr = addr.addr
            elif isinstance(addr, Reference):
                # add value of references
                references.append(addr.name)
                continue
            else:
                # add immediate address value
                reloc = '   '
                bank = ''
            symbol_list.append((symbol, addr, reloc, bank))
        if strict:
            reffmt = lambda x: '       REF  {:s}'.format(x.upper())
            symfmt = ('{:<6} EQU  >{:04X}    * {} {}' if equ else
                      '    {:.<6} {} : {} {}')
        else:
            reffmt = lambda x: '       ref  {:s}'.format(x.lower())
            symfmt = ('{}:\n       equ  >{:04X}  ; {} {}' if equ else
                      '    {:.<20} >{:04X} : {} {}')
        return ('\n'.join(reffmt(ref) for ref in references) + '\n' +
                '\n'.join(symfmt.format(*sym) for sym in symbol_list) + '\n')


# Parser and Preprocessor

class Preprocessor(object):
    """xdt99-specific preprocessor extensions
       The preprocessor is only called for pass 1, in pass 2 all dot-commands have been eliminated!
    """

    def __init__(self, parser, listing):
        self.parser = parser   # the parser object
        self.listing = listing  # the listing object
        self.parse = True  # is parsing in progress (or disabled by .ifX/.endif)?
        self.parse_else = False  # has .else branch been parsed for current .if?
        self.parse_branches = []  # parse status before hitting .ifX
        self.parse_macro = None  # name of macro currently parsing
        self.macros = {}  # macros defined

    def args(self, ops):
        lhs = self.parser.expression(ops[0], well_defined=True, relaxed=True)
        rhs = self.parser.expression(ops[1], well_defined=True, relaxed=True) if len(ops) > 1 else 0
        return lhs, rhs

    def str_args(self, ops):
        return [self.parser.text(op) if self.parser.is_literal(op) else
                str(self.parser.expression(op, well_defined=True))
                for op in ops]

    def DEFM(self, asm, ops):
        if len(ops) != 1:
            raise AsmError('Invalid syntax')
        self.parse_macro = ops[0]
        if self.parse_macro in self.macros:
            raise AsmError('Duplicate macro name')
        self.macros[self.parse_macro] = []

    def ENDM(self, asm, ops):
        raise AsmError('Found .ENDM without .DEFM')

    def IFDEF(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = asm.symbols.get_symbol(ops[0]) is not None if self.parse else None
        self.parse_else = False

    def IFNDEF(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = asm.symbols.get_symbol(ops[0]) is None if self.parse else None
        self.parse_else = False

    def IFEQ(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = Util.cmp(*self.args(ops)) == 0 if self.parse else None
        self.parse_else = False

    def IFNE(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = Util.cmp(*self.args(ops)) != 0 if self.parse else None
        self.parse_else = False

    def IFGT(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = Util.cmp(*self.args(ops)) > 0 if self.parse else None
        self.parse_else = False

    def IFGE(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = Util.cmp(*self.args(ops)) >= 0 if self.parse else None
        self.parse_else = False

    def IFLT(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = Util.cmp(*self.args(ops)) < 0 if self.parse else None
        self.parse_else = False

    def IFLE(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = Util.cmp(*self.args(ops)) <= 0 if self.parse else None

    def ELSE(self, asm, ops):
        if not self.parse_branches or self.parse_else:
            raise AsmError("Misplaced .else")
        self.parse = not self.parse if self.parse is not None else None
        self.parse_else = True

    def ENDIF(self, asm, ops):
        try:
            self.parse, self.parse_else = self.parse_branches.pop()
        except IndexError:
            raise AsmError('Misplaced .endif')

    def PRINT(self, asm, ops):
        res = ' '.join(self.str_args(ops))
        sys.stdout.write(res + '\n')

    def ERROR(self, asm, ops):
        if self.parse:
            raise AsmError('Error state')

    def instantiate_macro_args(self, text, restore_lits=False):
        """replace macro parameters by macro arguments"""
        def get_macro_text(match):
            try:
                inst_text = self.parser.macro_args[int(match.group(1)) - 1]
                return self.parser.restore(inst_text) if restore_lits else inst_text
            except IndexError:
                return match.group()

        try:
            return re.sub(r'#(\d+)', get_macro_text, text)
        except ValueError:
            return text

    def instantiate_line(self, line):
        """instantiate macro parameters in entire line"""
        # temporary kludge, breaks comments
        parts = re.split(r"('(?:[^']|'')*'|\"[^\"]*\")", line)
        parts[::2] = [self.instantiate_macro_args(p, restore_lits=True) for p in parts[::2]]
        return ''.join(parts)

    def process(self, asm, label, mnemonic, operands, line):
        """process preprocessor commands (for pass 1)"""
        if self.parse_macro:
            if mnemonic == '.ENDM':
                self.parse_macro = None
            elif mnemonic == '.DEFM':
                raise AsmError('Cannot define macro within macro')
            else:
                self.macros[self.parse_macro].append(line)
            return False, False, None, None  # macro definition
        if self.parse and asm.parser.in_macro_instantiation and operands:
            operands = [self.instantiate_macro_args(op) for op in operands]
            line = self.instantiate_line(line)  # only for display
        if mnemonic and mnemonic[0] == '.':
            asm.process_label(label)
            name = mnemonic[1:]
            if name in self.macros:
                if self.parse:
                    self.parser.open(macro=name, macro_args=operands)
                    return False, label, None, line
            else:
                try:
                    fn = getattr(Preprocessor, name)
                except AttributeError:
                    raise AsmError('Invalid preprocessor directive')
                try:
                    fn(self, asm, operands)
                except (IndexError, ValueError):
                    raise AsmError('Syntax error')
            return False, False, None, None  # eliminate preprocessor commands
        else:
            return self.parse, False, operands, line  # normal statement


class Parser(object):
    """scanner and parser class"""
    OPEN = '$OPEN'  # constants inserted into source to denote new or resumes source units
    RESUME = '$RESM'

    def __init__(self, symbols, listing, console, path, includes=None, strict=False, r_prefix=False,
                 bank_cross_check=False):
        self.symbols = symbols
        self.listing = listing
        self.console = console
        self.path = path
        self.includes = includes or []  # do not include '.' -- current path added implicitly in find()
        self.prep = Preprocessor(self, listing)
        self.text_literals = []
        self.strict = strict
        self.r_prefix = r_prefix
        self.bank_cross_check = bank_cross_check
        self.warnings = []  # per line
        self.filename = None
        self.source = None
        self.macro_args = []
        self.in_macro_instantiation = False
        self.lino = -1
        self.suspended_files = []
        self.parse_branches = [True]

    def open(self, filename=None, macro=None, macro_args=None):
        """open new source file or macro buffer"""
        if len(self.suspended_files) > 100:
            raise AsmError('Too many nested files or macros')
        if filename:
            newfile = self.find(filename) if filename != '-' else '-'  # checks if file exists, throws exception if not
            # CAUTION: don't suspend source if file does not exist!
        else:
            newfile = None
        if self.source is not None:
            self.suspended_files.append((self.filename, self.path, self.source, self.macro_args, self.lino))
        if filename:
            self.path, self.filename = os.path.split(newfile)
            self.source = Util.readlines(newfile)  # might throw error
            self.in_macro_instantiation = False
        else:
            self.source = self.prep.macros[macro]
            self.macro_args = macro_args or []
            self.in_macro_instantiation = True
        self.symbols.interm_source.append((0, 0, None, Parser.OPEN, None, None, filename or macro, None))
        self.lino = 0

    def resume(self):
        """close current source file and resume previous one"""
        try:
            self.filename, self.path, self.source, self.macro_args, self.lino = self.suspended_files.pop()
            self.symbols.interm_source.append((0, 0, None, Parser.RESUME, None, None, self.filename, None))
            return True
        except IndexError:
            self.source = None  # indicates end-of-source to pass; keep self.path!
            return False

    def stop(self):
        """stop reading source"""
        while self.resume():
            pass

    def find(self, filename):
        """locate file that matches native filename or TI filename"""
        include_path = self.includes + ([self.path] if self.path else [])  # self.path changes during assembly
        ti_name = re.match(r'(?:DSK\d|DSK\.[^.]+)\.(.*)', filename)
        if ti_name:
            native_name = ti_name.group(1)
            extensions = ['', '.a99', '.A99', '.asm', '.ASM', '.s', '.S']
        else:
            native_name = filename
            extensions = ['']
        for i in include_path:
            for e in extensions:
                include_file = os.path.join(i, native_name + e)
                if os.path.isfile(include_file):
                    return include_file
                include_file = os.path.join(i, native_name.lower() + e)
                if os.path.isfile(include_file):
                    return include_file
        raise AsmError(f'File not found: {filename}')

    def read(self):
        """get next logical line from source files"""
        while self.source is not None:
            try:
                line = self.source[self.lino]
                self.lino += 1
                return self.lino, line.rstrip(), self.filename
            except IndexError:
                self.resume()
        return None, None, None

    def line(self, line):
        """parse single source line"""
        if not line or line[0] == '*':
            return None, None, None, None, False
        if self.strict:
            # blanks separate fields
            fields = re.split(r'\s+', self.escape(line), maxsplit=3)
            label, mnemonic, optext, comment = fields + [''] * (4 - len(fields))
            label = label[:6]
            operands = re.split(',', optext) if optext else []
        else:
            # comment field separated by two blanks
            parts = self.escape(line).split(';')
            fields = re.split(r'\s+', parts[0], maxsplit=2)
            label, mnemonic, optext = fields + [''] * (3 - len(fields))
            opfields = re.split(r' {2,}|\t', optext, maxsplit=1)
            operands = [op.strip() for op in opfields[0].split(',')] if opfields[0] else []
            comment = ' '.join(opfields[1:]) + ';'.join(parts[1:])
        return label, mnemonic, operands, comment, True

    def escape(self, text):
        """remove and save text literals from line"""
        parts = re.split(r"('(?:[^']|'')*'|\"[^\"]*\")", text)  # not-lit, lit, not-lit, lit, ...
        literals = [s[1:-1].replace("''", "'") for s in parts[1::2]]  # '' is ' within 'string'
        parts[1::2] = ["'{:d}'".format(len(self.text_literals) + i) for i in range(len(literals))]  # 'n' placeholder
        self.text_literals.extend(literals)
        return ''.join(parts).upper()

    def restore(self, text):
        """restore escaped text literals"""
        return re.sub(r"'(\d+)'", lambda m: "'" + self.text_literals[int(m.group(1))] + "'", text)

    def address(self, op):
        """parse general address into t-field, register, address value"""
        if op[0] == '@':  # memory addressing
            i = op.find('(')
            if i >= 0 and op[-1] == ')':
                register = self.register(op[i + 1:-1])
                if register == 0:
                    raise AsmError('Cannot index with register 0')
                offset = self.expression(op[1:i])
                if offset == 0:
                    self.warn('Using indexed address @0, could use *R instead')
                return 0b10, register, offset
            else:
                return 0b10, 0, self.expression(op[1:])
        elif op[0] == '*':  # indirect addressing
            if op[-1] == '+':
                return 0b11, self.register(op[1:-1]), None
            else:
                return 0b01, self.register(op[1:]), None
        elif op[:2] in ('B#', 'W#'):  # auto-generated constant (x# replaces @)
            auto = AutoConstant(self.expression(op[2:], well_defined=True),
                                size=op[0], bank=self.symbols.bank, symbols=self.symbols)
            if self.symbols.pass_no == 1:
                if self.symbols.bank in self.symbols.autos_defined:
                    raise AsmError('Auto-constant defined after AUTO directive')
                self.symbols.add_autoconst(auto)
            return 0b10, 0, auto
        else:
            return 0b00, self.register(op), None

    def relative(self, op):
        """parse relative address (LC displacement)"""
        if self.symbols.pass_no == 1:
            return 0
        addr = self.expression(op)
        if isinstance(addr, Address):
            if addr.reloc != self.symbols.segment_reloc:
                raise AsmError('Invalid relocatable address')
            addr = addr.addr
        # displacement on LC + 2
        disp = (addr - (self.symbols.effective_LC() + 2)) // 2
        if disp < -128 or disp > 127:  # word displacement
            raise AsmError('Out of range: ' + op + ' +/- ' + hex(disp))
        return disp

    def expression(self, expr, well_defined=False, absolute=False, relaxed=False, iop=False, allow_r0=False):
        """parse complex arithmetical expression"""
        if self.symbols.pass_no == 1 and not well_defined:
            return 0
        value = Word(0)
        stack = []
        reloc_count = 0
        sep_pattern = r"([-+*/])" if self.strict else r"([-+/%~&|^()]|\*\*?|[BW]#)"
        terms = ['+'] + [tok.strip() for tok in re.split(sep_pattern, expr)]
        i = 0
        while i < len(terms):
            op, term = terms[i:i + 2]
            i += 2
            negate = False
            corr = 0
            if op == ')':
                v, reloc = value.value, reloc_count
                value, reloc_count, op, negate, corr = stack.pop()
            else:
                # unary operators
                while not term and i < len(terms) and terms[i] in '+-~(':
                    term = terms[i + 1]
                    if terms[i] == '-':
                        negate = not negate
                    elif terms[i] == '~':
                        corr += 1 if negate else -1
                        negate = not negate
                    elif terms[i] == '(':
                        stack.append((value, reloc_count, op, negate, corr))
                        op, term, negate, corr = '+', terms[i + 1], False, 0
                        value, reloc_count = Word(0), 0
                    i += 2
                # process next term between operators
                term_val, x_bank_access = self.term(term, well_defined=well_defined, iop=iop, relaxed=relaxed,
                                                    allow_r0=allow_r0)
                if isinstance(term_val, Local):
                    dist = -term_val.distance if negate else term_val.distance
                    term_val = self.symbols.get_local(term_val.name, dist)
                    if term_val is None:
                        raise AsmError('Invalid local target')
                    negate = False
                if term_val is None:
                    raise AsmError('Invalid expression: ' + term)
                elif isinstance(term_val, Reference):
                    if len(terms) != 2 or well_defined:
                        raise AsmError('Invalid reference: ' + expr)
                    return term_val
                elif isinstance(term_val, Address):
                    if (self.bank_cross_check and
                            term_val.bank != Symbols.BANK_ALL and self.symbols.bank != Symbols.BANK_ALL and
                            term_val.bank != self.symbols.bank and not x_bank_access):
                        raise AsmError('Invalid cross-bank access')
                        # NOTE: Jumping from bank into shared is safe, but shared into bank in general isn't.
                        #       But if we didn't allow shared to bank, we couldn't leave shared sections!
                    v, reloc = term_val.addr, 1 if term_val.reloc else 0
                else:
                    v, reloc = term_val, 0

            w = Word((-v if negate else v) + corr)
            if op == '+':
                value.add(w)
                reloc_count += reloc if not negate else -reloc
            elif op == '-':
                value.sub(w)
                reloc_count -= reloc if not negate else -reloc
            elif op == '*':
                value.mul(op, w)
                if reloc_count > 0:
                    raise AsmError('Invalid address: ' + expr)
            elif op in '/%':
                value.div(op, w)
                if reloc_count > 0:
                    raise AsmError('Invalid address: ' + expr)
            elif op in '&|^':
                value.bit(op, w)
                if reloc_count > 0:
                    raise AsmError('Cannot use relocatable address in expression: ' + expr)
            elif op == '**':
                base, exp = Word(1), w.value
                for j in range(exp):
                    base.mul('*', value)
                value = base
            else:
                raise AsmError('Invalid operator: ' + op)
        if not 0 <= reloc_count <= (0 if absolute else 1):
            raise AsmError('Invalid address: ' + expr)
        return Address(value.value, self.symbols.bank, True, self.symbols.unit_id) if reloc_count else value.value

    def term(self, op, well_defined=False, iop=False, relaxed=False, allow_r0=False):
        """parse constant or symbol"""
        cross_bank_access = False
        if op[0] == '>':
            return int(op[1:], 16), False
        elif op == '$':
            return Address(self.symbols.effective_LC(),
                           self.symbols.bank,
                           self.symbols.segment_reloc and not self.symbols.xorg_offset,
                           self.symbols.unit_id), False
        elif op[0] == ':':
            return int(op[1:], 2), False
        elif op.isdigit():
            return int(op), False
        elif op[0] == op[-1] == "'":
            c = self.text_literals[int(op[1:-1])]
            if len(c) == 1:
                return ord(c[0]), False
            elif len(c) == 2:
                return ord(c[0]) << 8 | ord(c[1]), False
            elif len(c) == 0:
                return 0, False
            else:
                raise AsmError('Invalid text literal: ' + c)
        elif op[0] == '!':
            m = re.match('(!+)(.*)', op)
            return Local(m.group(2), len(m.group(1))), False
        elif op[:2] in ('B#', 'W#'):
            raise AsmError('Invalid auto-constant expression')
        elif op[:2] == 'S#':
            v = self.symbols.get_size(op[2:])
            return v, False
        elif op[0] == '#':
            # should have been eliminated by preprocessor
            raise AsmError(f'Invalid macro argument: {op}')
        else:
            if op[:2] == 'X#' and not self.strict:
                cross_bank_access = True
                op = op[2:]
            if op[0] == '@':
                raise AsmError("Invalid '@' found in expression")
            if iop and op in self.symbols.registers and not (op == 'R0' and allow_r0):
                self.warn(f'Register {op:s} used as immediate operand')
            v = self.symbols.get_symbol(op[:6] if self.strict else op)
            if v is None and (self.symbols.pass_no > 1 or well_defined):
                if relaxed:
                    return 0, False
                else:
                    raise AsmError('Unknown symbol: ' + op)
            return v, cross_bank_access

    def value(self, op):
        """parse well-defined value"""
        e = self.expression(op, well_defined=True)
        return Util.val(e)

    def register(self, op):
        """parse register"""
        if self.symbols.pass_no == 1:
            return 1  # don't return 0, as this is invalid for indexes @A(Rx)
        op = op.strip()
        try:
            if op[0] == '>':
                r = int(op[1:], 16)
            elif op[0] == ':':
                return int(op[1:], 2)
            elif op.isdigit():
                r = int(op)
            elif op[0] == '@':
                raise AsmError('Expected register, found address instead')
            else:
                r = self.symbols.get_symbol(op[:6] if self.strict else op)
                if r is None:
                    raise AsmError('Unknown symbol: ' + op)
                if isinstance(r, Address):
                    raise AsmError('Invalid term for register')
        except TypeError:
            raise AsmError('Invalid register:' + op)
        if self.r_prefix and op[0].upper() != 'R':
            self.warn('Treating as register, did you intend an @address?')
        if not 0 <= r <= 15:
            raise AsmError('Invalid register: ' + op)
        return r

    def bank(self, op):
        """parse bank: number or 'all'"""
        if op.isdigit():
            return int(op)
        elif op.lower() == 'all':
            return Symbols.BANK_ALL
        else:
            raise AsmError('Invalid bank value: ' + op)

    def text(self, op):
        """parse single-quoted text literal or byte string"""
        s = op[1:].strip() if op[0] == '-' else op
        v = None
        try:
            if s[0] == '>':
                s0 = s + '0'
                v = ''.join(chr(int(s0[i:i + 2], 16)) for i in range(1, len(s), 2))
            elif s[0] == s[-1] == "'":
                v = self.text_literals[int(s[1:-1])] or '\x00'  # '' equals '\x00'
        except (IndexError, ValueError):
            pass
        if v is not None:
            return v[:-1] + chr(-ord(v[-1]) % 0x100) if op[0] == '-' else v
        else:
            raise AsmError('Invalid text literal: ' + op)

    def radix100(self, op):
        """parse floating-point number and convert to radix-100 format"""
        sign, digits = (-1, op[1:]) if op[0] == '-' else (+1, op)  # sign
        # find hundreds
        try:
            int_part, frac_part = digits.strip('0').split('.')  # with decimal point
        except ValueError:
            int_part, frac_part = digits.lstrip('0'), ''  # no decimal point
        if not int_part:
            if not frac_part:
                return [0] * 8  # op is zero
            while frac_part[:2] == '00':  # only faction
                frac_part = frac_part[2:]
        elif len(int_part) % 2 == 1:
            int_part = '0' + int_part
        # build mantissa
        mantissa = int_part + frac_part + '00000000000000'
        hundreds = [int(mantissa[i:i + 2]) for i in range(0, 14, 2)]
        # get exponent
        try:
            exponent = int(math.floor(math.log(float(digits), 100)))  # digits != 0
        except ValueError:
            raise AsmError('Bad format for floating point number: ' + op)
        # invert first word if negative
        bytes_ = [exponent + 0x40] + hundreds
        if sign < 0:
            bytes_[1] = 0x100 - bytes_[1]  # cannot yield 0x100 for bytes_[1], since always != 0
            bytes_[0] = ~bytes_[0]
        # return radix-100 format
        return bytes_

    def filename_text(self, op):
        """parse double-quoted filename"""
        if not (len(op) >= 3 and op[0] == op[-1] == "'"):
            raise AsmError('Invalid filename: ' + op)
        return self.text_literals[int(op[1:-1])]

    def is_literal(self, op):
        """check if operand is literal"""
        return op[0] == op[-1] == "'"

    @staticmethod
    def external(op):
        """parse symbol constant (-D option)"""
        try:
            return int(op[1:], 16) if op[0] == '>' else int(op)
        except ValueError:
            return op

    def warn(self, message):
        self.warnings.append(message)

    @staticmethod
    def raise_invalid_statement():
        """raises exception, as expression"""
        raise AsmError('Invalid statement')


# Code generation

class Program(object):
    """code and related properties, including externals
       NOTE: A program consists of multiple program units,
             a program unit consists of multiple segments.
    """

    def __init__(self, target, segments=None, definitions=None):
        self.target = target
        self.segments = segments or []
        self.externals = Externals(target, definitions)
        self.saves = []  # save ranges
        self.idt = None
        self.entry = None  # start address of program
        self.unit_count = 0
        self.max_reloc_LC = {}  # by unit_id
        self.reloc_intervals = {}  # by unit_id
        self.absolute_intervals = []

    def __iter__(self):
        return iter(self.segments)

    def set_entry(self, entry):
        if self.entry is not None:
            raise AsmError('Multiple entries defined')
        self.entry = entry

    def set_name(self, name):
        if self.idt is None:
            self.idt = name

    def layout_program(self, base, resolve_conflicts):
        self.sort_segments()
        if resolve_conflicts:
            return self.get_resolved_unit_offsets(base)
        else:
            return self.get_default_unit_offsets(base)

    def sort_segments(self):
        """sort segments into reloc and absolute segments by unit_id, excluding empty root segments"""
        for segment in self.segments:
            unit_id = segment.symbols.unit_id
            self.unit_count = max(self.unit_count, unit_id + 1)
            if segment.dummy or (segment.root and segment.max_LC == 0):
                continue  # exclude dummy segments and empty root segments
            if segment.reloc:
                self.reloc_intervals.setdefault(unit_id, []).append((segment.min_LC, segment.max_LC))
                self.max_reloc_LC[unit_id] = max(self.max_reloc_LC.get(unit_id, 0), segment.max_LC)
            else:
                self.absolute_intervals.append((segment.min_LC, segment.max_LC))

    def get_default_unit_offsets(self, base):
        """return unit offsets, ignoring RORG/AORG conflicts"""
        offset = base
        offsets = {}
        for i in (None, *range(self.unit_count)):
            offsets[i] = offset
            offset += self.max_reloc_LC.get(i, 0)
        return offsets

    def get_resolved_unit_offsets(self, base):
        """return unit offsets so that no RORG/AORG conflicts remain"""
        offsets = {0: base}
        # process segments ordered by unit_id; sorting by start or end address is not required
        for i in range(99):  # limit no. of iterations
            conflict = False
            offset = offsets[0]
            for n in range(self.unit_count):
                for min_LC, max_LC in self.reloc_intervals.get(n, ()):
                    for min_abs_LC, max_abs_LC in self.absolute_intervals:
                        if not (min_LC + offset >= max_abs_LC or max_LC + offset <= min_abs_LC):
                            offset = max_abs_LC - min_LC  # don't apply RORG offset here
                            conflict = True
                if conflict or i == 0:
                    offsets[n] = offset
                    offset += self.max_reloc_LC.get(n, 0)
                else:
                    offset = offsets.get(n + 1, offset)
            if not conflict:
                break
        else:
            raise AsmError('Cannot find layout for program units')
        return offsets


class Segment(object):
    """stores the code of an xORG segment with meta information,
       also represents the top level unit of all generated code
    """

    def __init__(self, symbols, bank, reloc=False, dummy=False, root=False):
        self.bank = bank
        self.min_LC = None
        self.max_LC = None  # the next unused LC for that segment
        self.reloc = reloc
        self.dummy = dummy
        self.root = root  # initial segment, which may remain unused?
        self.code = {}  # {LC: word}
        self.symbols = symbols

    def close(self, LC):
        """mark segment code as complete"""
        self.min_LC = min(self.code, default=LC)
        self.max_LC = LC

    def set(self, LC, value, byte=False):
        """set code to byte, word, or special value"""
        if byte or not isinstance(value, int):
            self.code[LC] = value
        else:
            self.code[LC] = value >> 8
            self.code[LC + 1] = value & 0xff


class SymbolAssembler(object):
    """dummy code generation for keeping track of line counter"""

    def __init__(self, program, opcodes, symbols, parser, console):
        self.program = program
        self.opcodes = opcodes
        self.symbols = symbols
        self.parser = parser
        self.console = console
        self.segment = False  # no actual Segment required for symbols

    def assemble_pass_1(self, srcname):
        """pass 1: gather symbols, apply preprocessor"""
        self.parser.open(filename=srcname)
        self.symbols.pass_no = 1
        self.symbols.lidx = 0
        self.symbols.reset()
        self.org(0, reloc=True)
        prev_label = None
        while True:
            # get next source line
            lino, line, filename = self.parser.read()
            self.symbols.lidx += 1
            self.console.filename_text = filename
            self.console.lino = lino
            if lino is None:
                break
            try:
                # break line into fields
                label, mnemonic, operands, comment, stmt = self.parser.line(line)
                keep, add_label, operands, line = self.parser.prep.process(self, label, mnemonic, operands, line)
                if add_label:
                    self.symbols.interm_source.append((lino, self.symbols.lidx, label, "", [], line, label, True))
                if not keep:
                    continue
                self.symbols.interm_source.append((lino, self.symbols.lidx, label, mnemonic, operands,
                                                   line, filename, stmt))
                if not stmt:
                    continue
                # process continuation label
                if prev_label:
                    if label:
                        raise AsmError('Invalid continuation for label')
                    label, prev_label = prev_label, None
                elif label[-1:] == ':' and not mnemonic:
                    prev_label = label
                    continue
                if label[-1:] == ':':
                    label = label[:-1]
                # process mnemonic
                Directives.process(self, label, mnemonic, operands) or \
                    self.opcodes.process(label, mnemonic, operands) or \
                    Parser.raise_invalid_statement()
            except AsmError as e:
                self.console.error(str(e), 1, filename, lino, line)
        if self.parser.prep.parse_branches:
            self.console.error('***** Error: Missing .endif', 1, filename)
        if self.parser.prep.parse_macro:
            self.console.error('***** Error: Missing .endm', 1, filename)

    def org(self, base, reloc=False, bank=None, dummy=False, xorg=False):
        """open new segment"""
        if self.segment:
            self.symbols.save_LC()
            if bank is None:
                bank = self.symbols.bank
        if xorg:
            # for XORG, keep reloc status but save LC offset
            self.symbols.xorg_offset = base - self.symbols.LC
        else:
            self.symbols.restore_LC(base, reloc, bank)
        self.segment = not dummy
        if bank is not None:
            self.symbols.bank = bank

    def even(self):
        """even LC"""
        if self.symbols.LC % 2 == 1:
            self.symbols.pad()
            self.symbols.LC += 1

    def byte(self, byte):
        """increase LC by byte"""
        self.symbols.LC += 1

    def word(self, word):
        """increase LC by word"""
        self.even()
        self.symbols.LC += 2

    def block(self, size, offset=0):
        """increase LC by block size"""
        self.symbols.LC += size

    def emit(self, *words, cycles=0):
        """increase LC according to machine code generated"""
        self.even()
        self.symbols.LC += sum(2 for word in words if word is not None)
        # self.symbols.LC += (2 + (2 if saddr is not None else 0) +
        #                         (2 if daddr is not None else 0))

    def process_label(self, label, real_LC=False, tracked=False):
        """register label at current LC"""
        if not label:
            return
        if label[0] == '!':
            self.symbols.add_local_label(label[1:])
        else:
            self.symbols.add_label(label, real_LC, tracked=tracked)

    def auto_constants(self):
        """compure addresses of all constants, no further defs allowed"""
        if self.symbols.bank in self.symbols.autos_generated:
            raise AsmError('Multiple AUTO directives in current bank')
        for size, value, bank in sorted(self.symbols.autoconsts):
            if bank != self.symbols.bank:  # BANK_ALL has been excluded
                continue
            if size == 'W' and self.symbols.LC % 2:
                self.symbols.LC += 1  # padding, executed only once
            name = AutoConstant.get_name(size, value, bank)
            value = Address(addr=self.symbols.LC, bank=bank, reloc=self.symbols.segment_reloc,
                            unit_id=self.symbols.unit_id)
            self.symbols.add_symbol(name, value, check=False)
            self.symbols.LC += 2 if size == 'W' else 1
        self.symbols.autos_defined.add(self.symbols.bank)


class Assembler(object):
    """generate object code"""

    def __init__(self, program, opcodes, includes=None, r_prefix=False, strict=False, warnings=True, timing=True,
                 bank_cross_check=False, colors=None):
        self.program = program
        self.opcodes = opcodes
        self.includes = includes or []
        self.console = Console(warnings, colors=colors)
        self.symbols = None
        self.parser = None
        self.symasm = None
        self.listing = Listing(timing=timing)
        self.strict = strict
        self.r_prefix = r_prefix
        self.bank_cross_check = bank_cross_check
        self.segment = None

    def assemble(self, path, srcname):
        self.symbols = Symbols(self.program.externals, self.console, add_registers=self.r_prefix)
        self.parser = Parser(self.symbols, self.listing, self.console, path, includes=self.includes,
                             r_prefix=self.r_prefix, bank_cross_check=self.bank_cross_check, strict=self.strict)
        self.symasm = SymbolAssembler(self.program, self.opcodes, self.symbols, self.parser, self.console)  # pass 1
        self.opcodes.use_asm(self.symasm)
        self.symasm.assemble_pass_1(srcname)  # continue even with errors, to display them all
        self.opcodes.use_asm(self)
        self.assemble_pass_2()
        self.finalize()

    def assemble_pass_2(self):
        """second pass: generate machine code"""
        self.symbols.pass_no = 2
        self.symbols.reset()
        self.org(0, reloc=True, root=True)  # create root segment
        for lino, lidx, label, mnemonic, operands, line, filename, stmt in self.symbols.interm_source:
            if mnemonic == Parser.OPEN or mnemonic == Parser.RESUME:
                if mnemonic == Parser.OPEN:
                    self.listing.open(self.symbols.LC, filename)
                elif mnemonic == Parser.RESUME:
                    self.listing.resume(self.symbols.LC, filename)
                self.console.filename = filename
                continue
            self.symbols.lidx = lidx
            self.parser.warnings = []
            self.listing.prepare(self.symbols.LC, Line(lino=lino, line=line))
            if not stmt:
                continue
            if label and label[-1] == ':' and not mnemonic:
                continue
            try:
                Directives.process(self, label, mnemonic, operands) or \
                    self.opcodes.process(label, mnemonic, operands) or \
                    Parser.raise_invalid_statement()
            except AsmError as e:
                self.console.error(str(e), 2, filename, lino, line)
            for msg in self.parser.warnings:
                self.console.warn(msg, 2, filename, lino, line)
        unused = sorted(self.symbols.get_unused())
        if unused:
            self.console.warn('Unused constants: ' + ', '.join(unused), 2)

    def process_label(self, label, real_LC=False, tracked=False):
        """only in pass 1"""
        pass

    def org(self, base, bank=None, reloc=False, dummy=False, xorg=False, root=False):
        """define new segment"""
        if self.segment and not self.segment.dummy:
            if not root:
                self.segment.close(self.symbols.LC)
            if bank is None:
                self.symbols.save_LC()
        if xorg:
            # for XORG, keep reloc status but save LC offset
            self.symbols.xorg_offset = base - self.symbols.LC
        else:
            self.symbols.restore_LC(base, reloc, bank)
        if bank is not None:
            self.symbols.bank = bank
        self.segment = Segment(self.symbols, self.symbols.bank, reloc=self.symbols.segment_reloc,
                               dummy=dummy, root=root)
        if not dummy:
            self.program.segments.append(self.segment)

    def even(self):
        """even LC"""
        if self.symbols.LC % 2 == 1:
            self.symbols.LC += 1

    def byte(self, byte_):
        """create a byte"""
        byte_ &= 0xff
        self.segment.set(self.symbols.LC, byte_, byte=True)
        self.listing.add(self.symbols.LC, byte=byte_)
        self.symbols.LC += 1

    def word(self, word, timing=None):
        """create a word"""
        self.even()
        self.segment.set(self.symbols.LC, word)
        self.listing.add(self.symbols.LC, text1=self.symbols.LC, text2=word, timing=timing)
        self.symbols.LC += 2

    def block(self, size, offset=0):
        """define block, offset for BES directive"""
        block = Block(size)
        self.listing.add(self.symbols.LC, text1=self.symbols.LC + offset, text2=block)
        self.segment.set(self.symbols.LC, block)
        self.symbols.LC += size

    def emit(self, *words, cycles=0):
        """generate machine code"""
        for word in words:
            if word is not None:
                self.word(word)
        # self.word(opcode, cycles)  TODO
        # if mode is not None:
        #     self.word(mode)
        # if saddr is not None:
        #     self.word(saddr)
        # if daddr is not None:
        #     self.word(daddr)

    def auto_constants(self):
        """create code stanza for auto-constants"""
        def list_autoconsts(name, local_value, local_lc, byte=False):
            self.listing.prepare(self.symbols.LC, Line(line=name))
            if byte:
                self.listing.add(self.symbols.LC, text1=local_lc, byte=local_value)
            else:
                self.listing.add(self.symbols.LC, text1=local_lc, text2=f'{local_value:04X}')

        self.listing.open(self.symbols.LC, 'auto-generated constants')
        for size, value, bank in sorted(self.symbols.autoconsts):
            if bank != Symbols.BANK_ALL and self.symbols.bank != Symbols.BANK_ALL and bank != self.symbols.bank:
                continue
            if size == 'W' and self.symbols.LC % 2:
                # executed only once
                list_autoconsts('(padding)', 0, self.symbols.LC, byte=True)
                self.symbols.LC += 1
            display_name = size + '#' + str(value) if size != 'P' else ''
            list_autoconsts(display_name, value, self.symbols.LC, byte=size == 'B')
            if size == 'W':  # already even
                self.segment.set(self.symbols.LC, value)
                self.symbols.LC += 2
            else:  # B
                self.segment.set(self.symbols.LC, value, byte=True)
                self.symbols.LC += 1
        self.symbols.autos_generated.add(self.symbols.bank)

    def finalize(self):
        """complete code generation"""
        if self.segment:
            self.segment.close(self.symbols.LC)


class Records:
    """object code tag and record handling"""

    def __init__(self, reloc_size, idt, compressed):
        self.records = []
        if not idt:
            idt = '        '
        if compressed:
            self.record = b'\x01%b%-8b' % (Util.chrw(reloc_size), idt.encode())
            self.line_len = 77
        else:
            self.record = b'0%04X%-8b' % (reloc_size, idt.encode())
            self.line_len = 64
        self.compressed = compressed
        self.needs_LC = True

    def add(self, tag, value, LC=None, reloc=False, sym=None):
        """add tag to records"""
        add_LC = self.needs_LC and LC is not None
        tag_penalty = (5 if tag in b'9A' else 0) + (5 if add_LC else 0)
        if self.compressed:
            s = tag + Util.chrw(value)
            if tag in b'3456':
                tag_penalty += 31
        else:
            s = tag + (b'%04X' % value)
        if sym:
            try:
                s += b'%-6b' % sym.encode()
            except UnicodeEncodeError:
                raise AsmError(f"Cannot encode symbol '{sym:s}'")
        if len(self.record) + len(s) + tag_penalty > self.line_len:
            self.flush()
            add_LC = LC is not None
        if add_LC:
            tag_LC = ((b'A' if reloc else b'9') +
                      (Util.chrw(LC) if self.compressed else (b'%04X' % LC)))
            self.record += tag_LC + s
        else:
            self.record += s
        self.needs_LC = False

    def add_LC(self):
        """add LC tag for next object code tag"""
        self.needs_LC = True

    def append(self, record):
        """add predefined record"""
        self.records.append(record)

    def flush(self):
        """close current record and add checksum"""
        if not self.compressed:
            checksum = reduce(lambda s, c: s + c, self.record, ord('7'))
            self.record += b'7%04X' % ((~checksum + 1) & 0xffff)
        self.records.append(self.record + b'F' + b' ' * (69 - len(self.record)))
        self.record = b''
        self.add_LC()

    def dump(self):
        """dump records as DIS/FIX80"""
        if self.compressed:
            lines = ([b'%-80b' % line for line in self.records[:-1]] +
                     [b'%-75b %04d' % (self.records[-1], len(self.records))])
        else:
            lines = [b'%-75b %04d' % (line, i + 1)
                     for i, line in enumerate(self.records)]
        return b''.join(lines)


class Optimizer(object):
    """object code analysis and optimization (currently only checks)"""

    def __init__(self, console):
        self.console = console

    @staticmethod
    def process(asm, mnemonic, opcode, fmt, arg1, arg2):
        if mnemonic == 'B':
            if (arg1[0] == 0b10 and arg1[1] == 0 and isinstance(arg1[2], int) and
                    -128 <= (arg1[2] - (asm.symbols.effective_LC() + 2)) // 2 <= 128):
                # upper bound is 128 instead of 127, since replacing B by JMP
                # would also eliminate one word (the target of B)
                asm.parser.warn('Possible branch/jump optimization')


class Linker(object):
    """Object code and binary handling"""

    def __init__(self, program, base=0, warnings=True, resolve_conflicts=False, colors=False):
        self.program = program
        self.reloc_base = base
        self.console = Console(warnings, colors=colors)
        self.resolve_conflicts = resolve_conflicts
        self.symbols = None
        self.offsets = None  # dict of program relocation offsets
        self.bank_count = None

    def load(self, files):
        """link external object code, E/A #5 program file, or binary"""
        for filename, data in files:
            self.symbols = Symbols(self.program.externals, self.console)
            name, segments = self.load_object_code(data)
            self.program.segments.extend(segments)
            self.program.set_name(name)

    def load_object_code(self, objcode):
        """link object code"""
        segment = Segment(self.symbols, None, reloc=True)  # initial segment
        segments = [segment]
        LC = 0  # always start at 0, and relocate later if required
        reloc = new_reloc = True
        addr_change = None  # old LC, new LC, change_idx
        addr_change_chain = False
        try:
            name = objcode[5:13].decode()
        except UnicodeDecodeError:
            name = None
        if objcode[0] == 0x01:
            compressed = True
            taglen = 3
            get = lambda t: Util.ordw(t[1:3])
        else:
            compressed = False
            taglen = 5
            get = lambda t: int(t[1:5], 16)
        obj_size = Util.ordw(objcode[1:3]) if compressed else int(objcode[:5], 16)

        check_linos = True
        for lino, i in enumerate(range(0, len(objcode) - 80, 80)):  # ignore last line
            line = objcode[i:i + 80]
            if not compressed and line[-4:] != b'%04d' % (lino + 1) and check_linos:
                self.console.warn('Invalid line numner; object code file may be corrupted', pass_no='L', lino=lino)
                check_linos = False  # report only once
            start_idx = idx = taglen + 8 if lino == 0 else 0
            while True:
                tag = line[idx:idx + taglen]
                tagid = tag[0:1]
                # if data tags follows an actual address change:
                if tagid in b'BC' and addr_change:
                    old_LC, new_LC, change_idx = addr_change
                    if (not addr_change_chain and
                            (change_idx > start_idx or reloc != new_reloc or new_LC < old_LC)):
                        # create new segment
                        if segment:
                            segment.close(old_LC)  # current segment done
                        reloc = new_reloc
                        segment = Segment(self.symbols, None, reloc=reloc)
                        segments.append(segment)
                    addr_change = None
                if tagid in b'12':  # entry address
                    entry = Address(get(tag), reloc=tagid == b'2')
                    if self.program.entry is not None:
                        raise AsmError(f'Multiple entry addresses: >{self.program.entry:04X} and >{entry:04X}')
                    self.program.entry = entry
                    idx += taglen
                elif tagid in b'34':  # REF
                    try:
                        symbol = line[idx + taglen:idx + taglen + 6].decode().rstrip()
                    except UnicodeDecodeError:
                        raise AsmError('Invalid REF symbol: ' + str(line[idx + taglen:idx + taglen + 6]))
                    ref = Reference(symbol)
                    self.symbols.add_symbol(symbol, ref)
                    self.symbols.add_ref(symbol)
                    self.patch_ref(segments, get(tag), symbol)
                    idx += taglen + 6
                elif tagid in b'56':  # DEF
                    try:
                        symbol = line[idx + taglen:idx + taglen + 6].decode().rstrip()
                    except UnicodeDecodeError:
                        raise AsmError('Invalid DEF symbol: ' + str(line[idx + taglen:idx + taglen + 6]))
                    self.symbols.add_symbol(symbol, Address(get(tag), reloc=tagid == b'5'))
                    self.symbols.add_def(symbol)
                    idx += taglen + 6
                elif tagid == b'7':  # checksum
                    idx += taglen
                elif tagid in b'9A':  # set LC (also block, which just advances LC)
                    new_LC = get(tag)
                    new_reloc = tagid == b'A'
                    # NOTE:
                    # BSS/BES generates two address changes (start of block, end of block).
                    # If they are followed by another 9/A tag, first end and second start tag
                    # are merged.  If BSS is last statement of program, then only start of
                    # block is written, and end must be derived from reloc size.
                    # (Variable used: addr_change)
                    # *ORGs only generate a tag if followed by at least one word.  When
                    # multiple *ORGs occur, only the last one has relevance, assuming
                    # it is not the end of the program.
                    # A trailing 9/A tag does not indicate an *ORG directive, but a BSS.
                    if addr_change:
                        prev_old_LC, prev_new_LC, change_idx = addr_change
                        if prev_new_LC == new_LC:  # 2x BSS 1/BYTE in one word
                            segment.set(prev_new_LC, Block(1))  # 'B' tag will check for Block(1)
                        else:
                            segment.set(prev_new_LC, Block(new_LC - prev_new_LC))
                        addr_change_chain = True
                    addr_change = LC, new_LC, idx
                    LC = new_LC
                    idx += taglen
                elif tagid == b'B':  # data or non-relocatable address as arg
                    value = get(tag)
                    try:
                        if isinstance(segment.code[LC], Block) and segment.code[LC].size % 2 == 1:
                            assert value < 0x100
                            segment.set(LC + 1, value, byte=True)
                    except KeyError:
                        segment.set(LC, value)
                    LC += 2
                    idx += taglen
                elif tagid == b'C':  # relocatable address as arg
                    segment.set(LC, Address(get(tag), reloc=True, unit_id=self.symbols.unit_id))
                    LC += 2
                    idx += taglen
                elif tagid == b'F':
                    break
                else:
                    raise AsmError('Invalid object code tag: {}'.format(str(tagid)))
        LC = self.close_block(segment, addr_change, addr_change_chain, LC, obj_size, segment.reloc)
        segment.close(LC)
        self.adjust_obj_size(segments, obj_size)
        return name, segments

    @staticmethod
    def close_block(segment, addr_change, chain, LC, obj_size, reloc):
        """handle opened block"""
        try:
            old_LC, new_LC, change_idx = addr_change
            if not chain:
                segment.set(new_LC, Block(obj_size - LC))  # final block, size not included in tags
        except TypeError:
            pass
        return obj_size if reloc else LC

    @staticmethod
    def adjust_obj_size(segments, obj_size):
        """fix last reloc LCs to match relocatable object size"""
        for segment in reversed(segments):
            if segment.reloc:
                segment.max_LC = obj_size
                break

    def patch_ref(self, segments, addr, symbol):
        """instantiate ref chain with Reference objects"""
        # NOTE: Because 0 denotes the end of the patch chain,
        #       you cannot have a reference at address 0!
        while addr:  # neither 0 and nor None
            addr = self.patch_addr(segments, addr, symbol)

    @staticmethod
    def patch_addr(segments, addr, symbol):
        """replace one addr in ref chain by Reference, return next addr in chain"""
        for segment in segments:
            try:
                vaddr = Util.val(addr)
                if isinstance(segment.code[vaddr], Address):
                    next_addr = Util.val(segment.code[vaddr])
                else:
                    next_addr = (segment.code[vaddr] << 8) | segment.code[vaddr + 1]
                    del segment.code[vaddr + 1]
                segment.code[vaddr] = Reference(symbol)
                return next_addr
            except KeyError:
                pass  # addr not in this segment, try next
        return None

    def link(self, warn_about_unresolved_refs=False):
        """link object code"""
        self.offsets = self.program.layout_program(self.reloc_base, self.resolve_conflicts)
        self.resolve_references(warn_about_unresolved_refs)
        self.bank_count = self.get_bank_count()

    def get_offset(self, entity):
        """return link offset for segment"""
        if isinstance(entity, Segment):
            return self.offsets[entity.symbols.unit_id] if entity.reloc else 0
        else:
            return self.offsets[entity.unit_id] if entity.reloc else 0

    def resolve_addr(self, word):
        """resolve potential address and applying offset"""
        if isinstance(word, Address):
            return word.addr + (self.offsets[word.unit_id] if word.reloc else 0)
        else:
            return word

    def resolve_references(self, warn_about_unresolved_references=False):
        """resolve references against all updated known symbols"""
        symbols = set()
        for segment in self.program:
            for LC, entry in segment.code.copy().items():
                if isinstance(entry, Reference):
                    try:
                        value, _ = self.program.externals.definitions[entry.name]
                        segment.set(LC, value)
                    except KeyError:
                        symbols.add(entry.name)
        if symbols and warn_about_unresolved_references:
            self.console.warn('Unresolved references: ' + ', '.join(symbols), pass_no='L')

        # keep only unresolved references, and all definitions
        externals = self.program.externals
        externals.references = [symbol for symbol in externals.references if symbol not in externals.definitions]

    def get_bank_count(self):
        """get number of different banks"""
        return max((segment.bank + 1 for segment in self.program
                    if segment.bank is not None and segment.bank != Symbols.BANK_ALL), default=0)

    def generate_object_code(self, compressed=False):
        """generate object code (E/A option 3)"""
        reloc_LCs = [segment.max_LC + self.offsets[segment.symbols.unit_id]
                     for segment in self.program if segment.reloc and not segment.dummy]
        reloc_size = reloc_LCs[-1] if reloc_LCs else 0
        tags = Records(reloc_size, self.program.idt, compressed)
        # add code and data words section
        refs = {}  # reference chain in object code for each ref symbol
        for segment in self.program:
            if segment.bank:
                raise AsmError('Cannot create banked object code')
            if segment.dummy:
                continue
            offset = self.get_offset(segment)
            tags.add_LC()
            for LC, entry in segment.code.items():
                addr = LC + offset
                if isinstance(entry, AutoConstant):
                    entry = entry.resolve_addr()  # resolves to Address()
                if isinstance(entry, Address):
                    tags.add(b'C' if entry.reloc else b'B',
                             entry.addr + self.get_offset(entry), addr, segment.reloc)
                elif isinstance(entry, Reference):
                    prev_LC, prev_reloc = refs.get(entry.name, (0, False))  # addr and reloc for previous ref
                    tags.add(b'C' if prev_reloc else b'B', prev_LC, addr, segment.reloc)
                    refs[entry.name] = (addr, segment.reloc)  # addr and reloc for current ref
                elif isinstance(entry, Block):
                    tags.add(b'A' if segment.reloc else b'9', addr)
                    tags.add_LC()
                elif entry is not None:
                    if addr % 2 == 0:
                        entry <<= 8
                        lsb = segment.code.get(LC + 1)
                        if isinstance(lsb, int):
                            entry |= lsb
                            segment.code[LC + 1] = None  # do not process again
                    else:
                        pass  # leave entry as-is
                    tags.add(b'B', entry, Util.even(addr), segment.reloc)  # might be single byte after BSS block
        tags.flush()
        # program entry
        if self.program.entry:
            if isinstance(self.program.entry, Reference):
                raise AsmError(f'Undefined entry point {self.program.entry.name}')
            tags.add(b'2' if self.program.entry.reloc else b'1', self.program.entry.addr)
            tags.flush()
        # add def and ref symbols section
        for symbol, (value, unit_id) in self.program.externals.definitions.items():
            if value is None or unit_id < 0:  # don't include built-in or -D definitions
                continue
            reloc = isinstance(value, Address) and value.reloc
            if isinstance(value, Address):
                addr = value.addr + self.get_offset(value)
            else:
                addr = 0 if isinstance(value, Reference) else value  # unresolved reference
            tags.add(b'5' if reloc else b'6', addr, sym=symbol[:6])
        for symbol in self.program.externals.references:
            # resolved references have been removed by linker
            prev_LC, prev_reloc = refs.get(symbol, (0, False))  # if ref not used, tagged by '4'
            tags.add(b'3' if prev_reloc else b'4', prev_LC, sym=symbol[:6])
        # closing section
        tags.flush()
        tags.append(b':       xdt99 xas')
        return tags.dump()

    def generate_binaries(self, split_segments=False, save=None, minimize=False):
        """generate binary images per bank and per segment or SAVE"""
        saves = self.program.saves + ([save] if save else [])
        binaries = []
        for bank in (None, *range(self.bank_count)):
            memories = []
            if split_segments and not saves:  # saves would join splits again
                # process each segment individually
                for segment in sorted(self.program.segments,
                                      key=lambda s: (s.min_LC + self.get_offset(s))):  # sort by increasing min_addr
                    try:
                        min_addr, max_addr, memory = self.fill_memory(bank, segments=(segment,))
                    except TypeError:  # fill_memory returns None
                        continue
                    # merge with adjacent memories
                    # since memories.min_addr are increasing, memory can only match with most recent memories
                    try:
                        prev_min, prev_max, prev_memory = memories[-1]
                        if prev_min < max_addr and prev_max + 1 >= min_addr:
                            prev_memory.update(memory)
                            memories[-1] = prev_min, max_addr, prev_memory
                            continue
                    except IndexError:
                        pass
                    memories.append((min_addr, max_addr, memory))
            else:
                # process all segments together
                try:
                    min_addr, max_addr, memory = self.fill_memory(bank, segments=self.program.segments)
                except TypeError:  # fill_memory returns None
                    continue
                memories.append((min_addr, max_addr, memory))
            if saves:
                for save in saves:
                    new_binaries = self.build_binary(bank, memories, save_range=save, minimize=minimize)
                    binaries.extend(new_binaries)
            else:
                new_binaries = self.build_binary(bank, memories, minimize=minimize)
                binaries.extend(new_binaries)
        return binaries

    def fill_memory(self, bank, segments):
        """load object code into memory"""
        memory = {}
        min_addr = 0x10000
        max_addr = 0
        # NOTE: It might seem more efficient to update() all the segments into one base segment,
        #       but relocatable segments need to have an offset applied, so this is not possible.
        for segment in segments:
            if segment.dummy or not segment.code:
                continue
            # either both banks are None, or both are not None and both banks match
            if not ((segment.bank is None and self.bank_count == 0) if bank is None else
                    (segment.bank == Symbols.BANK_ALL or segment.bank == bank)):
                continue
            offset = self.get_offset(segment)
            min_addr = min(min_addr, segment.min_LC + offset)
            max_addr = max(max_addr, segment.max_LC + offset)
            for LC, entry in segment.code.items():
                addr = LC + offset
                if isinstance(entry, AutoConstant):
                    entry = entry.resolve_addr()
                if isinstance(entry, Address):
                    word = entry.addr + self.get_offset(entry)
                    memory[addr] = word >> 8
                    memory[addr + 1] = word & 0xff
                elif isinstance(entry, Reference):
                    self.console.warn(f'Unknown reference: {entry.name}, substituting null', pass_no='L')
                    memory[addr] = memory[addr + 1] = 0
                elif isinstance(entry, Block):
                    addr, size = (addr, (entry.size + 1) // 2) if addr % 2 == 0 else (addr + 1, entry.size // 2)
                    for i in range(size):
                        memory[addr + i] = 0
                elif entry is None:
                    pass
                else:
                    memory[addr] = entry
        return (min_addr, max_addr, memory) if memory else None

    def build_binary(self, bank, memories, save_range=None, minimize=False):
        if minimize:
            return self.build_minimal_binary(bank, memories, save_range)
        else:
            return self.build_full_binary(bank, memories, save_range)

    def build_full_binary(self, bank, memories, save_range=None):
        """create a binary from memories, for given save range
           Note: unset memory addresses will be zeroed.
        """
        binaries = []
        min_mem = min(n for n, _, _ in memories)
        max_mem = max(n for _, n, _ in memories)
        try:
            save_min, save_max = save_range
            min_addr = min_mem if save_min is None else self.resolve_addr(save_min)
            max_addr = max_mem if save_max is None else self.resolve_addr(save_max)
        except TypeError:
            min_addr, max_addr = min_mem, max_mem
        merged_memory = []
        for addr in range(min_addr, max_addr):
            values = {mem.get(addr, 0) for _, _, mem in memories}
            if len(values) != 1:
                raise AsmError(f'Ambiguous value at address @{ addr }')
            merged_memory.append(values.pop())
        binary = bytes(merged_memory)
        binaries.append((bank, min_addr, min_addr, binary))
        return binaries

    def build_minimal_binary(self, bank, memories, save_range=None):
        """create a binary from memories, for given save range (has saves <=> only one memory)
           Note: Saves are not padded, e.g., if code occupies the range >10->20 and the save range
           is >00->40, the resulting binary will still occupy range >10->20.
        """
        binaries = []
        for min_addr, max_addr, memory in memories:
            if save_range:
                save_min, save_max = save_range
                if save_min is not None:
                    min_addr = self.resolve_addr(save_min)
                if save_max is not None:
                    max_addr = self.resolve_addr(save_max)
            merged_memory = []
            gap = []
            offset = 0
            for addr in range(min_addr, max_addr):
                try:
                    value = memory[addr]
                    if merged_memory:
                        merged_memory.extend(gap)
                    else:
                        offset = len(gap)
                    merged_memory.append(value)
                    gap = []
                except KeyError:
                    gap.append(0)  # addr in none of the memories
            binary = bytes(merged_memory)
            binaries.append((bank, min_addr, min_addr + offset, binary))
        return binaries

    def generate_text(self, mode):
        """convert binary data into text representation"""
        if 'r' in mode:
            word = lambda i: Util.ordw(
                    mem[i + 1:((i - 1) if i > 0 else None):-1])  # byte-swapped
        else:
            word = lambda i: Util.ordw(mem[i:i + 2])

        fmt = '{:s}{:04x}' if '4' in mode else '{:s}{:02x}'
        tf = lambda x: x  # use value as-is

        if 'a' in mode:  # assembly
            hex_prefix = '>'
            data_prefix = '       data ' if '4' in mode else '       byte '
            section_prefix = ';      aorg >{:04x}\n'
            suffix = '\n'
        elif 'b' in mode:  # BASIC
            hex_prefix = ''
            data_prefix = 'DATA '
            section_prefix = 'REM >{:04X}\n'
            suffix = '\n'
            fmt = '{:s}{:d}'
            tf = lambda x: x - 0x10000 if x > 32767 else x  # hex to dec
        elif 'c' in mode:  # C
            hex_prefix = '0x'
            data_prefix = '  '
            section_prefix = '  // >{:04x}\n'
            suffix = ',\n'
        else:
            raise AsmError('Bad text format: ' + mode)

        binaries = self.generate_binaries(minimize=True)
        result = []
        for bank, save, addr, mem in binaries:
            if '4' in mode:  # words
                if len(mem) % 2:
                    mem += bytes(1)  # pad to even length
                ws = [fmt.format(hex_prefix, tf(word(i)))
                      for i in range(0, len(mem), 2)]
                lines = [data_prefix + ', '.join(ws[i:i + 4]) + suffix
                         for i in range(0, len(ws), 4)]
            else:  # bytes (default)
                bs = [fmt.format(hex_prefix, mem[i])
                      for i in range(0, len(mem))]
                lines = [data_prefix + ', '.join(bs[i:i + 8]) + suffix
                         for i in range(0, len(bs), 8)]
            section = section_prefix.format(addr) + ''.join(lines)
            result.append((bank, save, addr, section))
        return result

    def generate_image(self, chunk_size=0x2000):
        """generate memory image (E/A option 5)"""
        if self.bank_count > 1:
            raise AsmError('Cannot create banked program image')
        save, offset = self.get_image_parameters()
        binaries = self.generate_binaries(split_segments=True, save=save, minimize=True)
        chunks = [(addr + offset + i, data[i:i + chunk_size - 6])
                  for bank, _, addr, data in binaries
                  for i in range(0, len(data), chunk_size - 6)]
        images = [Util.chrw(0xffff if i + 1 < len(chunks) else 0) + Util.chrw(len(chunk) + 6) + Util.chrw(addr) + chunk
                  for i, (addr, chunk) in enumerate(chunks)]
        return images

    def get_image_parameters(self):
        """get start address and load offset for image"""
        sload = sfirst = slast = None
        for segment in self.program:
            if not sload:
                sload = segment.symbols.get_symbol('SLOAD')
            if not sfirst:
                sfirst = segment.symbols.get_symbol('SFIRST')
            if not slast:
                slast = segment.symbols.get_symbol('SLAST')
        for value in (sload, sfirst, slast):
            if isinstance(value, Address) and value.reloc:
                value.addr += self.offsets[value.unit_id]
        if sload is None or sfirst is None or slast is None:
            save = None
            offset = 0
        else:
            save = Util.val(sfirst), Util.val(slast)
            offset = Util.val(sload) - Util.val(sfirst)
        return save, offset

    def generate_XB_loader(self):
        """stash code in Extended BASIC program"""
        size = 0
        for segment in self.program:
            if segment.bank:
                raise AsmError('Cannot embed banked object code')
            if not segment.reloc:
                raise AsmError('Cannot embed non-relocatable code')
            if segment.max_LC > size:
                size = segment.max_LC
        last_addr = 0xffe8  # end of token table
        first_addr = last_addr - 4 - size
        loader = (
            # CALL INIT :: CALL LOAD(>3FF8,"XYZZY")::
            # CALL LOAD(>2004,>FF,>E4):: CALL LINK("XYZZY")
            b'\x9d\xc8\x04\x49\x4e\x49\x54\x82\x9d\xc8\x04\x4c\x4f\x41\x44' +
            b'\xb7\xc8\x05\x31\x36\x33\x37\x36\xb3\xc8\x02\x38\x38\xb3\xc8' +
            b'\x02\x38\x39\xb3\xc8\x02\x39\x30\xb3\xc8\x02\x39\x30\xb3\xc8' +
            b'\x02\x38\x39\xb3\xc8\x02\x33\x32\xb3\xc8\x03\x32\x35\x35\xb3' +
            b'\xc8\x03\x32\x32\x38\xb6\x82\x9d\xc8\x04\x4c\x4f\x41\x44\xb7' +
            b'\xc8\x04\x38\x31\x39\x36\xb3\xc8\x02\x36\x33\xb3\xc8\x03\x32' +
            b'\x34\x38\xb6\x82\x9d\xc8\x04\x4c\x49\x4e\x4b\xb7\xc7\x05\x58' +
            b'\x59\x5a\x5a\x59\xb6'
            )
        # build binary, relocated at first_addr
        self.offsets = {0: first_addr}  # rebase segments on first_addr
        _, _, _, payload = self.generate_binaries()[0]  # returns only one element
        token_table = (bytes((len(loader) + 1,)) + loader + bytes(256 - size + 1) + payload + b'\x04\x60' +
                       Util.chrw(first_addr))
        token_tab_addr = last_addr - len(token_table)
        lino_tab_addr = token_tab_addr - 4
        lino_table = b'\x00\x01' + Util.chrw(token_tab_addr + 1)
        checksum = (token_tab_addr - 1) ^ lino_tab_addr
        header = (b'\xab\xcd' + Util.chrw(lino_tab_addr) + Util.chrw(token_tab_addr - 1) +
                  Util.chrw(checksum) + Util.chrw(last_addr - 1))
        # convert data into INT/VAR 254 records
        chunks = [(lino_table + token_table)[i:i + 254]
                  for i in range(0, len(lino_table + token_table), 254)]
        return bytes((len(header),)) + header + b''.join(bytes((len(c),)) + c for c in chunks)

    def generate_cartridge(self, name):
        """generate RPK file for use as MESS rom cartridge"""
        if self.bank_count > 1:
            raise AsmError('Cannot create banked cartridge with -c')
        send = self.program.entry or Address(0x6030)
        entry = send.addr + 0x6030 if send.reloc else send.addr
        gpl_header = bytes((0xaa, 0x01, 0x00, 0x00, 0x00, 0x00, 0x60, 0x10)) + bytes(8)
        try:
            program_info = Util.chrw(0) + Util.chrw(entry) + bytes((len(name),)) + name.encode()
        except UnicodeEncodeError:
            raise AsmError(f'Bad program name "{name}"')
        padding = bytes(27 - len(name))
        binaries = self.generate_binaries()
        _, _, _, data = binaries[0]
        layout = f"""<?xml version='1.0' encoding='utf-8'?>
                    <romset version='1.0'>
                        <resources>
                            <rom id='romimage' file='{name:s}.bin'/>
                        </resources>
                        <configuration>
                            <pcb type='standard'>
                                <socket id='rom_socket' uses='romimage'/>
                            </pcb>
                        </configuration>
                    </romset>"""
        metainf = f"""<?xml version='1.0'?>
                     <meta-inf>
                         <name>{name:s}</name>
                     </meta-inf>"""
        return gpl_header + program_info + padding + data, layout, metainf


# Console and Listing

class Console(object):
    """collects warnings"""

    def __init__(self, enable_warnings=True, colors=None):
        self.console = []
        self.filename = None
        self.enabled = enable_warnings
        self.errors = False
        self.entries = False
        self.colors = ((platform.system() in ('Linux', 'Darwin')) if colors is None else  # no auto color on Windows
                       (colors == 'on'))

    def warn(self, message, pass_no=None, filename=None, lino=None, line=None):
        if self.enabled and pass_no != 1:
            self.console.append(('W', message, pass_no, filename, lino, line))
            self.entries = True

    def error(self, message, pass_no=None, filename=None, lino=None, line=None):
        self.console.append(('E', message, pass_no, filename, lino, line))
        self.entries = self.errors = True

    def color(self, severity):
        if not self.colors:
            return ''
        elif severity == 0:
            return '\x1b[0m'  # reset to normal
        elif severity == 1:
            return '\x1b[33m'  # yellow
        elif severity == 2:
            return '\x1b[31m'  # red
        else:
            return ''

    def print(self):
        """print all console error and warning messages to stderr"""
        for kind, message, pass_no, filename, lino, line in self.console:
            text, severity = ('Error', 2) if kind == 'E' else ('Warning', 1)
            s_filename = filename or '***'
            s_pass = pass_no if isinstance(pass_no, str) else str(pass_no) or '-'
            s_lino = f'{lino:04d}' if lino is not None else '****'
            s_line = line or ''
            sys.stderr.write(f'> {s_filename} <{s_pass}> {s_lino} - {s_line}\n' +
                             self.color(severity) + f'***** {text:s}: {message}\n' + self.color(0))
        error_count = sum(1 for kind, *_ in self.console if kind == 'E')
        sys.stderr.write(self.color(0))
        if error_count == 1:
            sys.stderr.write('1 Error found.\n')
        elif error_count > 1:
            sys.stderr.write(f'{error_count} Errors found.\n')


class Listing(object):
    """listing file"""

    def __init__(self, timing=True):
        self.listing = []
        self.timing_enabled = timing
        self.prepared_line = None
        self.byte = None  # or (LC, value)

    def open(self, LC, filename):
        """open new source unit"""
        if self.prepared_line:
            self.add(LC)
        self.listing.append(Line(line='> ' + filename, text1='****', text2='****'))

    def resume(self, LC, filename):
        """resume previous source unit"""
        if self.prepared_line:
            self.add(LC)
        self.listing.append(Line(line='< ' + filename, text1='', text2=''))

    def prepare(self, LC, line):
        """send lino and line data, will be merged with upcoming addr and word"""
        if self.prepared_line:
            self.add(LC)
        self.prepared_line = line

    def add(self, LC, text1=None, text2=None, byte=None, timing=None):
        """add single line"""
        if not self.prepared_line:
            self.prepared_line = Line()
        if byte is not None:
            if LC % 2 == 0:
                assert self.byte is None
                self.byte = LC, byte
                return
            else:
                try:
                    LC, pbyte = self.byte
                    self.prepared_line.text2 = '{:04X}'.format((pbyte << 8) | byte)
                    self.byte = None
                except TypeError:
                    LC, pbyte = LC, 0
                    self.prepared_line.text2 = f'  {byte:02X}'
                self.prepared_line.text1 = LC
        if text1 is not None:
            self.prepared_line.text1 = text1
        if isinstance(text2, Value):
            self.prepared_line.text2 = text2.value + 'v'
        elif text2 is not None:
            self.prepared_line.text2 = text2
        if timing is not None:
            self.prepared_line.timing = timing
        if self.byte is not None:
            LC, byte = self.byte
            self.prepared_line.text1 = LC
            self.prepared_line.text2 = ('{:02X}  ' if LC % 2 == 0 else '  {:02X}').format(byte)
            self.byte = None
        self.listing.append(self.prepared_line)
        self.prepared_line = None

    def list(self):
        """generate listing"""
        self.prepare(0, Line())
        listing = []
        for line in self.listing:
            t_lino = '' if line.lino is None else f'{line.lino:04d}'
            t_addr = '' if line.text1 is None else line.text1 if isinstance(line.text1, str) else f'{line.text1:04X}'
            t_timing = '' if line.timing is None else str(line.timing)
            word = line.text2
            if isinstance(word, AutoConstant):  # resolve auto-const address
                word = word.resolve_addr()
            if isinstance(word, Address):
                t_word = word.hex()
            elif isinstance(word, Reference):
                t_word = '0000e'
            elif isinstance(word, Block):
                t_word = '    '
            elif isinstance(word, int):
                t_word = f'{word:04X}'
            elif isinstance(word, str):
                t_word = word
            else:
                t_word = t_addr = ''
            listing.append('{:4s} {:4s} {:5s}{:>3s} {:s}'.format(
                    t_lino, t_addr, t_word, t_timing if self.timing_enabled else '', line.line or ''))
        return 'XAS99 CROSS-ASSEMBLER   VERSION ' + VERSION + '\n' + '\n'.join(listing) + '\n'


class Line(object):
    """source code line"""

    def __init__(self, lino=None, line=None, text1=None, text2=None, timing=None):
        self.lino = lino
        self.line = line
        self.text1 = text1
        self.text2 = text2
        self.timing = timing


# Command line processing

def main():
    import argparse
    import zipfile

    args = argparse.ArgumentParser(description='TMS9900 cross-assembler, v' + VERSION)
    args.add_argument('sources', metavar='<source>', nargs='*', help='assembly source code(s)')
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument('-b', '--binary', action='store_true', dest='bin',
                     help='create program binaries')
    cmd.add_argument('-i', '--image', action='store_true', dest='image',
                     help='create program image (E/A option 5)')
    cmd.add_argument('-c', '--cart', action='store_true', dest='cart',
                     help='create MESS cart image')
    cmd.add_argument('-t', '--text', dest='text', nargs='?', metavar='<format>',
                     help='create text file with binary values')
    cmd.add_argument('--embed-xb', action='store_true', dest='embed',
                     help='create Extended BASIC program with embedded code')
    link = args.add_mutually_exclusive_group()
    link.add_argument('-l', '--link', dest='linker', metavar='<file>', nargs='+',
                      help='link object code file(s)')
    link.add_argument('-ll', '--link-resolve', dest='linker_resolve', metavar='<file>', nargs='+',
                      help='link object code file(s), resolving conflicts')
    args.add_argument('-5', '--9995', action='store_true', dest='use_9995',
                      help='add TMS9995-specific instructions')
    args.add_argument('-18', '--f18a', action='store_true', dest='use_f18a',
                      help='add F18A-specific instructions')
    args.add_argument('-105', '--99000', action='store_true', dest='use_99000',
                      help='add TMS99000-specific instructions')
    args.add_argument('-s', '--strict', action='store_true', dest='strict',
                      help='strict TI mode; disable xas99 extensions')
    args.add_argument('-n', '--name', dest='name', metavar='<name>',
                      help='set program name, e.g., for cartridge')
    args.add_argument('-R', '--register-symbols', action='store_true', dest='r_prefix',
                      help='add register symbols (TI Assembler option R)')
    args.add_argument('-C', '--compress', action='store_true', dest='compressed',
                      help='compress object code (TI Assembler option C)')
    args.add_argument('-L', '--listing-file', dest='listing', metavar='<file>',
                      help='generate listing file (TI Assembler option L)')
    args.add_argument('-S', '--symbol-table', action='store_true', dest='symbols',
                      help='add symbol table to listing (TI Assembler option S)')
    args.add_argument('-E', '--symbol-equs', dest='equs', metavar='<file>',
                      help='put symbols in EQU file')
    args.add_argument('-M', '--minimal-chunks', action='store_true', dest='minchunk',
                      help='create minimal chunks when generating binaries with SAVE')
    args.add_argument('-X', '--cross-checks', action='store_true', dest='x_checks',
                      help='enable cross-bank checks for banked programs')
    args.add_argument('-q', action='store_true', dest='quiet',
                      help='quiet, do not print warnings')
    args.add_argument('-a', '--base', dest='base', metavar='<addr>',
                      help='set base address for relocatable code')
    args.add_argument('-I', '--include', dest='inclpath', metavar='<paths>',
                      help='listing of include search paths')
    args.add_argument('-D', '--define-symbol', nargs='+', dest='defs',
                      metavar='<sym=val>',
                      help='add symbol to symbol table')
    args.add_argument('--color', action='store', dest='color', choices=['off', 'on'],
                      help='enable or disable color output')
    args.add_argument('-o', '--output', dest='output', metavar='<file>',
                      help='set output file name or target directory')
    opts = args.parse_args()

    if not (opts.sources or opts.linker or opts.linker_resolve):
        args.error('One of <source> or -l/-ll is required.')
    if opts.base and (opts.cart or opts.embed):
        args.error('Cannot set base address when embedding or creating cart.')

    # setup
    errors = False
    target = ('image' if opts.image else
              'cart' if opts.cart else
              'bin' if opts.bin else
              'xb' if opts.embed else
              'obj')

    # assembly step
    program = Program(target=target, definitions=opts.defs)
    if opts.sources:
        root = os.path.dirname(os.path.realpath(__file__))  # installation dir (path to xas99)
        includes = [os.path.join(root, 'lib')] + (opts.inclpath.split(',') if opts.inclpath else [])
        opcodes = Opcodes(use_9995=opts.use_9995, use_f18a=opts.use_f18a, use_99000=opts.use_99000)
        asm = Assembler(program, opcodes, includes=includes, r_prefix=opts.r_prefix, strict=opts.strict,
                        warnings=not opts.quiet, timing=not opts.use_9995, bank_cross_check=opts.x_checks,
                        colors=opts.color)
        for source in opts.sources:
            dirname = os.path.dirname(source) or '.'
            basename = os.path.basename(source)
            try:
                asm.assemble(dirname, basename)
            except IOError as e:
                sys.exit('File error: {}: {}.'.format(e.filename_text, e.strerror))
            except AsmError as e:
                sys.exit('Error: {}.'.format(e))
            if asm.console.entries:
                asm.console.print()
            if asm.console.errors:
                sys.exit(1)
        barename = 'stdin' if opts.sources[0] == '-' else os.path.splitext(os.path.basename(opts.sources[0]))[0]
        name = opts.name or barename[:10].upper()
    else:
        asm = None
        barename = 'a'
        name = opts.name or 'A'

    # link step
    base = (Util.xint(opts.base) if opts.base else
            0xa000 if opts.image else
            0x6030 if opts.cart else
            0)
    linker = Linker(program, base=base, warnings=not opts.quiet, resolve_conflicts=opts.linker_resolve,
                    colors=opts.color)
    try:
        if opts.linker or opts.linker_resolve:
            data = [(filename, Util.readdata(filename)) for filename in (opts.linker or opts.linker_resolve)]
            linker.load(data)
        linker.link(warn_about_unresolved_refs=opts.image or opts.bin or opts.embed or opts.text or opts.cart)
        if linker.console.entries:
            linker.console.print()
    except AsmError as e:
        sys.exit(f'Error: {str(e)}.')

    # output
    if opts.output and os.path.isdir(opts.output):  # -o file or directory?
        path = opts.output
        opts.output = None
    else:
        path = ''
    out = []
    try:
        if opts.bin:
            binaries = linker.generate_binaries(minimize=opts.minchunk)
            if not binaries:
                out.append((Util.outname(barename, '.bin', redef=opts.output), bytes(0), 'wb'))
            else:
                use_base = Util.max_bins_per_bank(binaries) > 1
                for bank, save, addr, data in binaries:
                    tag = Util.name_suffix(base=addr, bank=bank, use_base=use_base, bank_count=linker.bank_count)
                    name = Util.outname(barename, '.bin', tag=tag, redef=opts.output)
                    out.append((name, data, 'wb'))
        elif opts.image:
            data = linker.generate_image()
            if not data:
                out.append((Util.outname(barename, '.img', redef=opts.output), bytes(0), 'wb'))
            else:
                for i, image in enumerate(data):
                    name = Util.outname(Util.sinc(barename, i), '.img',
                                        redef=opts.output, altname=Util.sinc(opts.output, i))
                    out.append((name, image, 'wb'))
        elif opts.text:
            texts = linker.generate_text(opts.text.lower())
            if not texts:
                out.append((Util.outname(barename, '.dat', redef=opts.output), '', 'w'))
            else:
                use_base = Util.max_bins_per_bank(texts) > 1
                for bank, save, addr, text in texts:
                    tag = Util.name_suffix(base=addr, bank=bank, use_base=use_base, bank_count=linker.bank_count)
                    name = Util.outname(barename, '.dat', tag=tag, redef=opts.output)
                    out.append((name, text, 'w'))
        elif opts.cart:
            data, layout, metainf = linker.generate_cartridge(name)
            output = opts.output or barename + '.rpk'
            with zipfile.ZipFile(output, 'w') as archive:
                archive.writestr(name + '.bin', data)
                archive.writestr('layout.xml', layout)
                archive.writestr('meta-inf.xml', metainf)
        elif opts.embed:
            prog = linker.generate_XB_loader()
            name = opts.output or barename + '.iv254'
            out.append((name, prog, 'wb'))
        else:
            data = linker.generate_object_code(opts.compressed)
            name = opts.output or barename + '.obj'
            out.append((name, data, 'wb'))

        for name, data, mode in out:
            Util.writedata(os.path.join(path, name), data, mode)
        if opts.listing:
            listing = asm.listing.list() + (asm.symbols.list(opts.strict) if opts.symbols else '')
            Util.writedata(opts.listing, listing, 'w')
        if opts.equs:
            Util.writedata(opts.equs, asm.symbols.list(opts.strict, equ=True), 'w')
    except AsmError as e:
        sys.exit(f'Error: {str(e):s}.')
    except IOError as e:
        sys.exit('File error: {:s}: {:s}.'.format(e.filename_text, e.strerror))

    # return status
    return 1 if errors else 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
