#!/usr/bin/env python3

# xas99: A TMS9900 cross-assembler
#
# Copyright (c) 2015-2024 Ralph Benzinger <r@0x01.de>
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
import re
import math
import os
import argparse
import zipfile
from functools import reduce
from xcommon import Util, RFile, CommandProcessor, Warnings, Console


VERSION = '3.6.5'

CONFIG = 'XAS99_CONFIG'


# Exception Class

class AsmError(Exception):
    pass


# Misc. Objects

class Address:
    """absolute or relocatable address"""

    def __init__(self, addr, bank=None, reloc=False, unit_id=0):
        self.addr = addr
        self.bank = bank
        self.reloc = reloc
        self.unit_id = unit_id  # -1 for predefined and command-line defined symbols

    def __eq__(self, other):
        """required for externally defined symbols in Symbols"""
        return (isinstance(other, Address) and
                self.addr == other.addr and self.bank == other.bank and self.reloc == other.reloc and
                self.unit_id == other.unit_id)

    def hex(self):
        return '{:04X}{:s}'.format(self.addr, 'r' if self.reloc else ' ')

    @staticmethod
    def val(n):
        """dereference address"""
        return n.addr if isinstance(n, Address) else n
    

class Local:
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


class Reference:
    """external reference"""

    def __init__(self, name):
        self.name = name


class Value:
    """wraps value of auto-constants"""

    def __init__(self, value):
        self.value = value


class Block:
    """reserved block of bytes"""

    def __init__(self, size):
        self.size = size


class Word:
    """auxiliary class for word arithmetic"""

    def __init__(self, value):
        self.value = value % 0x10000  # always between >0000 and >ffff, but signed

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

    def udiv(self, op, arg):
        if arg.value == 0:
            raise AsmError('Division by zero')
        if op == '%%':
            self.value %= arg.value
        else:
            self.value //= arg.value

    def bit(self, op, arg):
        val = (self.value & arg.value if op == '&' else
               self.value | arg.value if op == '|' else
               self.value ^ arg.value if op == '^' else None)
        self.value = val % 0x10000

    def shift(self, op, arg):
        if arg < 0:
            AsmError('Cannot shift by negative values')
        if op == '>>':
            self.value >>= arg
        else:
            self.value = (self.value << arg) & 0xffff


# Opcodes and Directives

class Timing:

    OPCODE = 1
    MEMORY = 2
    MEMORY_2 = 3
    REGISTER = 4  # e.g., write without read-before-write
    REGISTER_2 = 5  # e.g., read-before-write
    ROM = 6
    CRU = 7
    UNKNOWN_S = 8  # e.g., *r1, @s(r1)
    UNKNOWN_D = 9

    MUX_WAITSTATES = 4

    asm = None  # current assembler

    def __init__(self, cycles, mem_accesses, byte=False, read=False):
        """capture the basic timing information for instruction execution
           All timing data is derived from TMS 9900 Microprocessor Data Manual, section 3.6.
           mem_accesses does not include accesses for arguments, including register accesses.
           Do not modify these instance variables, since this instrance is shared among all
           usages of a certain mnemonic.
        """
        self.LC = 0
        self.WP = 0
        self.byte = byte  # is byte-access?
        self.read = read  # if single argument read or write?
        self.cycles = cycles  # number of cycles needed w/o arguments
        self.mem_accesses = mem_accesses  # number of memory accesses needed w/o arguments

    @staticmethod
    def demuxed(addr):
        """addr is muxed (slow) or not (fast)?"""
        # don't know if demuxed for not-integer addresses (e.g., None when memory access for B *R11)
        return 0x2000 <= addr < 0x8000 or 0x9000 <= addr if isinstance(addr, int) else True

    @staticmethod
    def unknown(dest=False, count=1):
        """unknown memory accesses (could be demuxed or not)"""
        return (Timing.UNKNOWN_D,) * count if dest else (Timing.UNKNOWN_S,) * count

    def operand_cycles(self, t, byte=False):
        """additional cycles for operand (cycles in table A and B)
           Note that the additional cycles for writing the result has already been included in the
           base number of cycles in Opcodes, which corresponds to the listing in the Data Manual.
        """
        return (2, 6, 10, 8)[t] if byte else (2, 6, 10, 10)[t]  # symbolic and indexed have same number of cycles

    def operand_mem_accesses(self, t, index=0, read=False, dest=False):
        """additional memory accesses for operand (mem accesses in table A and B)
           Here we still need an additional memory access for write arguments.
        """
        # note that for write access, only the last address is written to
        if t == 0b00:  # register
            return (Timing.REGISTER,) if read else (Timing.REGISTER_2,)
        elif t == 0b01:  # indirect
            # read/write register and target addr
            return (Timing.REGISTER,) + self.unknown(dest) if read else (Timing.REGISTER,) + self.unknown(dest, count=2)
        elif t == 0b11:  # indirect auto-increment
            # read/write register and target addr, then write register
            return ((Timing.REGISTER_2,) + self.unknown(dest) if read else
                    (Timing.REGISTER_2,) + self.unknown(dest, count=2))
        elif t == 0b10:  # symbolic/indexed
            if index:
                # indexed: read/write symbol value, register, and target addr
                return ((Timing.REGISTER, Timing.OPCODE,) + self.unknown(dest) if read else
                        (Timing.REGISTER, Timing.OPCODE,) + self.unknown(dest, count=2))
            else:
                # symbolic: read/write symbol value and target addr
                return (Timing.OPCODE, Timing.MEMORY) if read else (Timing.OPCODE, Timing.MEMORY_2)

    def memory_cycles(self, accesses, addr=None):
        """number of waitstates based on address"""
        cycles = 0
        for access in accesses:
            if access == Timing.OPCODE:
                cycles += Timing.MUX_WAITSTATES if Timing.demuxed(self.LC) else 0
            elif access == Timing.REGISTER:
                cycles += Timing.MUX_WAITSTATES if Timing.demuxed(self.WP) else 0
            elif access == Timing.REGISTER_2:
                cycles += 2 * Timing.MUX_WAITSTATES if Timing.demuxed(self.WP) else 0  # read and write
            elif access == Timing.MEMORY:
                cycles += Timing.MUX_WAITSTATES if Timing.demuxed(addr) else 0
            elif access == Timing.MEMORY_2:
                cycles += 2 * Timing.MUX_WAITSTATES if Timing.demuxed(addr) else 0  # read and write
            elif access == Timing.ROM:
                pass  # no waitstates for ROM >0000->1FFF
            elif access == Timing.CRU:
                pass  # no waitstates for CRU
            elif access == Timing.UNKNOWN_S:  # source memory access to unknown address
                if self.asm.demux['S']:
                    cycles += Timing.MUX_WAITSTATES
            elif access == Timing.UNKNOWN_D:  # destination memory access to unknown address
                if self.asm.demux['D']:
                    cycles += Timing.MUX_WAITSTATES
        return cycles

    def time_noop(self):
        """number of cycles for execution (no operands)"""
        if self.asm.symbols.pass_no == 1:
            return 0
        return self.cycles + self.memory_cycles(self.mem_accesses)

    def time_1op(self, ts, s, sa):
        """number of cycles for execution (one operand)"""
        if self.asm.symbols.pass_no == 1:
            return 0
        # NOTE: represents tables A/B, but compensates for register read with zero wait state
        cycles = self.cycles + self.operand_cycles(ts, byte=self.byte)
        mem_cycles = (self.memory_cycles(self.mem_accesses, addr=Address.val(sa)) +
                      self.memory_cycles(self.operand_mem_accesses(ts, index=s, read=self.read), addr=Address.val(sa)))
        return cycles + mem_cycles

    def time_2ops(self, ts, s, sa, td, d, da):
        """number of cycles for execution (two operands)"""
        if self.asm.symbols.pass_no == 1:
            return 0
        cycles = self.cycles + self.operand_cycles(ts, byte=self.byte) + self.operand_cycles(td, byte=self.byte)
        mem_cycles = (self.memory_cycles(self.mem_accesses) +
                      self.memory_cycles(self.operand_mem_accesses(ts, index=s, read=True),
                                         addr=Address.val(sa)) +
                      self.memory_cycles(self.operand_mem_accesses(td, index=d, read=self.read, dest=True),
                                         addr=Address.val(da)))
        return cycles + mem_cycles

    def time_shift(self, count):
        """number of cycles for shift instruction"""
        if self.asm.symbols.pass_no == 1:
            return 0
        mem_accesses = self.mem_accesses + (Timing.REGISTER_2,)
        if count == 0:
            count = 16  # worst case, since contents of R0 unknown
            mem_accesses += (Timing.REGISTER,)  # also read R0
            self.cycles += 8  # more cycles for processing R0
        cycles = self.cycles + 2 * count
        mem_cycles = self.memory_cycles(mem_accesses)
        return cycles + mem_cycles

    def time_mcru(self, ts, s, sa, count, ldcr=False):
        """number of cycles for multi-cru instructions"""
        if self.asm.symbols.pass_no == 1:
            return 0
        if count == 0:
            count = 16  # worst case, since contents of R0 unknown
        byte_ = count <= 8  # do not modify self, as this object is shared among all LDCR or STCR mnemonics, resp.
        cycles = self.cycles + self.operand_cycles(ts, byte=byte_)
        mem_cycles = (self.memory_cycles(self.mem_accesses) +
                      self.memory_cycles(self.operand_mem_accesses(ts, index=s, read=self.read), addr=Address.val(sa)))
        if ldcr:  # LDCR
            cru_cycles = 2 * count
        else:  # STCR
            if count <= 8:
                cru_cycles = 2 * 8  # C and C' subtract each other out
            else:
                cru_cycles = 2 * 16
            if count == 8 or count == 16:
                cru_cycles += 2  # extra cycle if no shifting required
        return cycles + cru_cycles + mem_cycles

    @staticmethod
    def process(asm, mnemonic, source, destination):
        """check for special mnemonics"""
        if mnemonic == 'LWPI':
            asm.symbols.WP = source


class Opcodes:
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
        'A': (0xa000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,))),
        'AB': (0xb000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,), byte=True)),
        'ABS': (0x0740, 6, op_ga, None, Timing(12, (Timing.OPCODE,))),  # timing for worst case
        'AI': (0x0220, 8, op_wa, op_imm, Timing(14, (Timing.OPCODE,) * 2 + (Timing.REGISTER_2,))),
        'DEC': (0x0600, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'DECT': (0x0640, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'DIV': (0x3c00, 9, op_ga, op_wa, Timing(122, (Timing.OPCODE,) + (Timing.REGISTER_2,) * 2, read=True)),
        'INC': (0x0580, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'INCT': (0x05c0, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'MPY': (0x3800, 9, op_ga, op_wa, Timing(52, (Timing.OPCODE, Timing.REGISTER_2, Timing.REGISTER), read=True)),
        'NEG': (0x0500, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'S': (0x6000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,))),
        'SB': (0x7000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,), byte=True)),
        # 7. jump and branch
        'B': (0x0440, 6, op_ga, None, Timing(6, (Timing.OPCODE,), read=True)),
        'BL': (0x0680, 6, op_ga, None, Timing(10, (Timing.OPCODE, Timing.REGISTER), read=True)),
        'BLWP': (0x0400, 6, op_ga, None, Timing(24, (Timing.OPCODE,) + (Timing.REGISTER,) * 3, read=False)),
                                         # "new PC" memory read depends on operand, so treat it as write argument
        'JEQ': (0x1300, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),  # 8 cycles if jump not taken
        'JGT': (0x1500, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JHE': (0x1400, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JH': (0x1b00, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JL': (0x1a00, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JLE': (0x1200, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JLT': (0x1100, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JMP': (0x1000, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JNC': (0x1700, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JNE': (0x1600, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JNO': (0x1900, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JOP': (0x1c00, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'JOC': (0x1800, 2, op_disp, None, Timing(10, (Timing.OPCODE,))),
        'RTWP': (0x0380, 7, None, None, Timing(14, (Timing.OPCODE,) + (Timing.REGISTER,) * 3)),
        'X': (0x0480, 6, op_ga, None, None),  # cannot measure reliably
        'XOP': (0x2c00, 9, op_ga, op_xop,  # timing difference between Datasheet and Hardware Design
                Timing(34, (Timing.OPCODE,) + (Timing.ROM,) * 2 + (Timing.REGISTER,) * 4, read=True)),
        # 8. compare instructions
        'C': (0x8000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,), read=True)),
        'CB': (0x9000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,), byte=True, read=True)),
        'CI': (0x0280, 8, op_wa, op_imm, Timing(14, (Timing.OPCODE,) * 2 + (Timing.REGISTER,), read=True)),
        'COC': (0x2000, 3, op_ga, op_wa, Timing(12, (Timing.OPCODE, Timing.REGISTER), read=True)),
        'CZC': (0x2400, 3, op_ga, op_wa, Timing(12, (Timing.OPCODE, Timing.REGISTER), read=True)),
        # 9. control and cru instructions
        'LDCR': (0x3000, 4, op_ga, op_cnt, Timing(18, (Timing.OPCODE, Timing.REGISTER), read=True)),
        'SBO': (0x1d00, 2, op_cru, None, Timing(12, (Timing.OPCODE, Timing.REGISTER), read=True)),
        'SBZ': (0x1e00, 2, op_cru, None, Timing(12, (Timing.OPCODE, Timing.REGISTER), read=True)),
        'STCR': (0x3400, 4, op_ga, op_cnt, Timing(24, (Timing.OPCODE, Timing.REGISTER))),
        'TB': (0x1f00, 2, op_cru, None, Timing(12, (Timing.OPCODE, Timing.REGISTER), read=True)),  # read R12
        'CKOF': (0x03c0, 7, None, None, Timing(12, (Timing.OPCODE,))),
        'CKON': (0x03a0, 7, None, None, Timing(12, (Timing.OPCODE,))),
        'IDLE': (0x0340, 7, None, None, Timing(12, (Timing.OPCODE,))),
        'RSET': (0x0360, 7, None, None, Timing(12, (Timing.OPCODE,))),
        'LREX': (0x03e0, 7, None, None, Timing(12, (Timing.OPCODE,))),
        # 10. load and move instructions
        'LI': (0x0200, 8, op_wa, op_imm, Timing(12, (Timing.OPCODE,) * 2 + (Timing.REGISTER,))),  # no read-before-write
        'LIMI': (0x0300, 81, op_imm, None, Timing(14, (Timing.OPCODE,) * 2, read=True)),
        'LWPI': (0x02e0, 82, op_imm, None, Timing(10, (Timing.OPCODE,) * 2, read=True)),
        'MOV': (0xc000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,))),
        'MOVB': (0xd000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,), byte=True)),
        'STST': (0x02c0, 8, op_wa, None, Timing(8, (Timing.OPCODE,))),  # writes internally
        'STWP': (0x02a0, 8, op_wa, None, Timing(8, (Timing.OPCODE,))),  # writes internally
        'SWPB': (0x06c0, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        # 11. logical instructions
        'ANDI': (0x0240, 8, op_wa, op_imm, Timing(14, (Timing.OPCODE,) * 2 + (Timing.REGISTER_2,))),
        'ORI': (0x0260, 8, op_wa, op_imm, Timing(14, (Timing.OPCODE,) * 2 + (Timing.REGISTER_2,))),
        'XOR': (0x2800, 3, op_ga, op_wa, Timing(12, (Timing.OPCODE, Timing.REGISTER_2), read=True)),
        'INV': (0x0540, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'CLR': (0x04c0, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'SETO': (0x0700, 6, op_ga, None, Timing(8, (Timing.OPCODE,))),
        'SOC': (0xe000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,))),
        'SOCB': (0xf000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,), byte=True)),
        'SZC': (0x4000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,))),
        'SZCB': (0x5000, 1, op_ga, op_ga, Timing(10, (Timing.OPCODE,), byte=True)),
        # 12. shift instructions
        'SRA': (0x0800, 5, op_wa, op_scnt, Timing(12, (Timing.OPCODE,))),  # CNT stored in opcode
        'SRL': (0x0900, 5, op_wa, op_scnt, Timing(12, (Timing.OPCODE,))),  # ops and count timing added
        'SLA': (0x0a00, 5, op_wa, op_scnt, Timing(12, (Timing.OPCODE,))),  # in special time function
        'SRC': (0x0b00, 5, op_wa, op_scnt, Timing(12, (Timing.OPCODE,)))
        # end of opcodes
    }

    opcodes_f18a = {
        # F18A GPU instructions
        'CALL': (0x0c80, 6, op_ga, None, None),
        'RET': (0x0c00, 7, None, None, None),
        'PUSH': (0x0d00, 6, op_ga, None, None),
        'POP': (0x0f00, 6, op_ga, None, None),
        'SLC': (0x0e00, 5, op_wa, op_scnt, None)
    }

    opcodes_9995 = {
        # 9995 instructions
        'MPYS': (0x01c0, 6, op_ga, None, None),  # Note that 9900 timing and 9995 timing
        'DIVS': (0x0180, 6, op_ga, None, None),  # cannot be compared
        'LST': (0x0080, 8, op_wa, None, None),
        'LWP': (0x0090, 8, op_wa, None, None)
    }

    opcodes_99000 = {
        # 99105 and 99110 instructions
        'MPYS': (0x01c0, 6, op_ga, None, None),  # Note that 9900 timing and 99000 timing
        'DIVS': (0x0180, 6, op_ga, None, None),  # cannot be compared
        'LST': (0x0080, 8, op_wa, None, None),
        'LWP': (0x0090, 8, op_wa, None, None),
        'BIND': (0x0140, 106, op_ga, None, None),
        'BLSK': (0x00b0, 108, op_wa, op_imm, None),
        'TMB': (0x0c09, 103, op_ga, op_cnt, None),
        'TCMB': (0xc0a, 103, op_ga, op_cnt, None),
        'TSMB': (0x0c0b, 103, op_ga, op_cnt, None),
        'AM': (0x002a, 101, op_ga, op_ga, None),
        'SM': (0x0029, 101, op_ga, op_ga, None),
        'SLAM': (0x001d, 109, op_ga, op_scnt, None),
        'SRAM': (0x001c, 109, op_ga, op_scnt, None)
    }

    pseudos = {
        # 13. pseudo instructions
        'NOP': ('JMP', ['$+2'], 0),
        'RT': ('B', ['*<R>11'], 0),
        'SLL': ('SRL', None, 2),
        'PIX': ('XOP', None, 2)
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
        Timing.asm = asm

    def process(self, label, mnemonic, operands):
        """get assembly asm for mnemonic"""
        self.asm.even()
        self.asm.process_label(label)
        try:
            m, ops, op_count = Opcodes.pseudos[mnemonic]
            if self.asm.symbols.pass_no == 2 and self.asm.parser.relaxed and len(operands) != op_count:
                raise AsmError('Bad operand count')
            if ops is not None:
                ops = [o.replace('<R>', 'R' if self.asm.parser.r_prefix else '') for o in ops]
            mnemonic, operands = m, ops or operands
        except KeyError:
            try:
                mode = self.asm.parser.symbols.xops[mnemonic]
                mnemonic, operands = 'XOP', [operands[0], mode]
            except KeyError:
                pass
        try:
            opcode, fmt, parse_op1, parse_op2, timing = self.opcodes[mnemonic]
        except KeyError:
            raise AsmError('Invalid mnemonic: ' + mnemonic)
        if parse_op1 and len(operands) != (1 if parse_op2 is None else 2):
            raise AsmError('Bad operand count')
        arg1 = parse_op1(self.asm.parser, operands[0]) if parse_op1 else None
        arg2 = parse_op2(self.asm.parser, operands[1]) if parse_op2 else None
        Optimizer.process(self.asm, mnemonic, opcode, fmt, arg1, arg2)
        Timing.process(self.asm, mnemonic, arg1, arg2)
        self.generate(opcode, fmt, arg1, arg2, timing)
        return True

    def generate(self, opcode, fmt, arg1, arg2, timing):
        """generate byte asm"""
        if timing is not None:
            timing.LC = self.asm.symbols.effective_LC()
            timing.WP = self.asm.symbols.WP
        # I. two general address instructions
        if fmt == 1:
            ts, s, sa = arg1
            td, d, da = arg2
            b = opcode | td << 10 | d << 6 | ts << 4 | s
            t = 0 if timing is None else timing.time_2ops(ts, s, sa, td, d, da)
            self.asm.emit(b, sa, da, cycles=t)
        # II. jump and bit I/O instructions
        elif fmt == 2:
            b = opcode | arg1 & 0xff
            t = 0 if timing is None else timing.time_noop()
            self.asm.emit(b, cycles=t)
        # III. logical instructions
        elif fmt == 3:
            ts, s, sa = arg1
            d = arg2
            b = opcode | d << 6 | ts << 4 | s
            t = 0 if timing is None else timing.time_1op(ts, s, sa)
            self.asm.emit(b, sa, cycles=t)
        # IV. CRU multi-bit instructions
        elif fmt == 4:
            ts, s, sa = arg1
            c = arg2
            b = opcode | c << 6 | ts << 4 | s
            t = 0 if timing is None else timing.time_mcru(ts, s, sa, c, ldcr=opcode == 0x3000)
            self.asm.emit(b, sa, cycles=t)
        # V. register shift instructions
        elif fmt == 5:
            w = arg1
            c = arg2
            b = opcode | c << 4 | w
            t = 0 if timing is None else timing.time_shift(c)
            self.asm.emit(b, cycles=t)
        # VI. single address instructions
        elif fmt == 6:
            ts, s, sa = arg1
            b = opcode | ts << 4 | s
            t = 0 if timing is None else timing.time_1op(ts, s, sa)
            self.asm.emit(b, sa, cycles=t)
        # VII. control instructions
        elif fmt == 7:
            b = opcode
            t = 0 if timing is None else timing.time_noop()
            self.asm.emit(b, cycles=t)
        # VIII. immediate instructions
        elif fmt == 8:
            b = opcode | arg1
            t = 0 if timing is None else timing.time_noop()
            self.asm.emit(b, arg2, cycles=t)
        elif fmt == 81 or fmt == 82:
            b = opcode
            t = 0 if timing is None else timing.time_noop()
            self.asm.emit(b, arg1, cycles=t)
            if fmt == 82:
                self.asm.symbols.WP = arg1  # change workspace
        # IX. extended operations; multiply and divide
        elif fmt == 9:
            ts, s, sa = arg1
            r = arg2
            b = opcode | r << 6 | ts << 4 | s
            t = 0 if timing is None else timing.time_1op(ts, s, sa)
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


class Directives:

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
        asm.symbols.add_symbol(label, value, equ=Symbols.EQU, lino=asm.parser.lino, filename=asm.parser.filename)

    @staticmethod
    def WEQU(asm, label, ops):
        """weak EQU, may be redefined"""
        if asm.symbols.pass_no != 1:
            value = asm.symbols.get_symbol(label)
            asm.listing.add(asm.symbols.LC, text1='', text2=value)
            return
        Directives.check_ops(asm, ops, min_count=1, max_count=1, warning_only=True)
        if not label:
            raise AsmError('Missing label')
        value = asm.parser.expression(ops[0], well_defined=True)
        asm.symbols.add_symbol(label, value, equ=Symbols.WEQU, lino=asm.parser.lino, filename=asm.parser.filename)

    @staticmethod
    def REQU(asm, label, ops):
        if asm.symbols.pass_no != 1:
            try:
                value = asm.symbols.registers[label]
            except KeyError:
                value = 0  # error already reported by pass 1
            asm.listing.add(asm.symbols.LC, text1='', text2=value)
            return
        Directives.check_ops(asm, ops, min_count=1, max_count=1, warning_only=True)
        if not label:
            raise AsmError('Missing label')
        value = asm.parser.register(ops[0], well_defined=True)
        asm.symbols.add_register_alias(label, value)

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
        asm.org(Address.val(base), dummy=True, reloc=reloc)
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
        if asm.parser.symbols.pass_no == 2:
            return
        asm.process_label(label)
        Directives.check_ops(asm, ops, min_count=1, max_count=1)
        filename = asm.parser.get_filename(ops[0])
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
        # also process in pass 2, since BCOPY includes no source!
        filename = asm.parser.get_filename(ops[0])
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
                asm.console.warn('Ignoring extra operands')
            elif asm.symbols.pass_no == 1:
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

class Externals:
    """externally defined and referenced symbols"""

    def __init__(self, target):
        self.target = target
        self.references = []
        self.definitions = {}
        self.builtins = {  # const
            'SCAN': 0x000e,
            'PAD': 0x8300,
            'GPLWS': 0x83e0,
            'SOUND': 0x8400,
            'VDPRD': 0x8800,
            'VDPSTA': 0x8802,
            'VDPWD': 0x8c00,
            'VDPWA': 0x8c02,
            'SPCHRD': 0x9000,
            'SPCHWT': 0x9400,
            'GRMRD': 0x9800,
            'GRMRA': 0x9802,
            'GRMWD': 0x9c00,
            'GRMWA': 0x9c02,
        }


class Symbols:
    """symbol table and line counter
       Each symbol entry is a tuple (value, equ-kind, used).
       Equ-kind symbols may be redefined, if EQU by the same value only.
       Used tracks if a symbol has been used (True/False).  If set to None, usage is not tracked.
       Each program unit owns its own symbol table.
    """
    g_unit_id = 0

    # symbol kind
    NONE = 0  # not an EQU symbol
    EQU = 1   # EQU symbols (can be redefined by same value)
    WEQU = 2  # weak EQU symbol (can be redefined by other value)
    BANK_ALL = 411  # shared code

    def __init__(self, externals, console, extdefs=(), add_registers=False, strict=False, target=None):
        self.externals = externals
        self.console = console
        self.registers = {'R' + str(i): i for i in range(16)} if add_registers else {}
        self.strict = strict
        # symbols = {name: value, equ-kind, tracked-or-unused}
        # tracked-or-used = None=don't care, True=unused, False=used
        self.symbols = {n: (v, False, None) for n, v in self.registers.items()}  # registers are _also_ just symbols
        self.target = '_XAS99_' + (target or '')
        self.symbols[self.target] = 1, Symbols.NONE, None
        self.symbol_def_location = {}  # symbol locations (lino, filename)
        self.saved_LC = {True: 0, False: 0}  # key == relocatable
        self.xops = {}
        self.locations = []
        self.unit_id = Symbols.g_unit_id
        Symbols.g_unit_id += 1
        self.local_lid = 0
        self.pass_no = 0
        self.lidx = 0
        self.autoconsts = set()  # set of auto-generated constants
        self.autos_defined = set()
        self.autos_generated = set()
        self.WP = None  # current workspace pointer (for timing)
        self.LC = None  # current line counter
        self.bank = None  # current bank, or None
        self.bank_LC = None  # next LC for each bank
        self.bank_base = 0  # base addr of BANK <addr>
        self.segment_reloc = self.xorg_offset = self.pad_idx = None
        self.add_env(extdefs)
        self.reset()

    def add_env(self, extdefs):
        """add external symbol definitions (-D)"""
        for def_ in extdefs:
            try:
                name, value_str = def_.split('=')
                value = Parser.external(value_str)
            except ValueError:
                name, value = def_, 1
            self.add_symbol(name.upper(), Address(value, reloc=False))

    def reset(self):
        """initialize some properties before each pass"""
        self.LC = 0
        self.WP = 0x83e0
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
        return ((not self.strict and name != '$' and name[0] not in "!@0123456789" and
                 not re.search(r'[-+*/%&#|^~()"\',]', name)) or
                (self.strict and (name[0].isalpha() or name[0] == '$') and
                 not re.search(r'[-+*/%&|^~()\[\]@!"\'.,;:\\]', name)))

    def add_symbol(self, name, value, lino=None, filename=None, tracked=False, check=True, equ=None):
        """add symbol to symbol table"""
        if equ is None:
            equ = Symbols.NONE  # workaround for Python limitation
        if check and not self.valid(name):
            raise AsmError('Invalid symbol name: ' + name)
        if name in self.registers:
            raise AsmError('Duplicate symbol: ' + name)
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
                    raise AsmError('Duplicate symbol: ' + name)
                else:
                    value, equ = new_entry
        except KeyError:
            # new definition
            unused = tracked or None  # true=unused, false=used, None=don't track
        if isinstance(value, Address):
            value.unit_id = self.unit_id
        self.symbols[name] = value, equ, unused
        self.symbol_def_location[name] = None if lino is None else (lino, filename)
        return name

    def _valid_redefinition(self, defined_value, defined_equ, name, value, equ):
        """check if redefinition of symbol is allowed (only pass 1)"""
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

    def add_label(self, label, real_LC=False, tracked=False, check=True, lino=None, filename=None):
        """add a new label symbol to symbol table"""
        addr = Address(self.LC if real_LC else self.effective_LC(),
                       self.bank,
                       self.segment_reloc and (real_LC or not self.xorg_offset),
                       self.unit_id)
        name = self.add_symbol(label, addr, lino=lino, filename=filename, tracked=tracked, check=check)
        self.locations.append((self.lidx, name))

    def add_local_label(self, label):
        """add a new local label symbol to symbol table"""
        self.local_lid += 1
        self.add_label('_%l' + label + '$' + str(self.local_lid), check=False)

    def add_register_alias(self, alias, register, nocheck=False):
        """add a new register alias"""
        if not nocheck and (alias in self.registers or alias in self.symbols):
            raise AsmError('Duplicate symbol: ' + alias)
        self.registers[alias] = register

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
            raise AsmError('Invalid symbol name: ' + name)
        if name in self.externals.definitions:
            _, unit_id = self.externals.definitions[name]
            if unit_id >= 0 and unit_id != self.unit_id:
                raise AsmError(f'Duplicate definitions for symbol {name}')
        value = self.get_symbol(name)
        self.externals.definitions[name] = (value, self.unit_id)

    def add_ref(self, name):
        """add referenced symbol (also adds value to symbol table)"""
        if not self.valid(name):
            raise AsmError('Invalid reference: ' + name)
        try:
            value = self.externals.builtins[name]
            if name not in self.symbols:
                self.add_symbol(name, value)
        except KeyError:
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
                self.symbols[name] = value, equ, False  # symbol has been used
        except KeyError:
            value = None
        return value

    def get_locals(self, name, distance):
        """return local label specified by current position and distance +/-n"""
        targets = [(loc, sym) for (loc, sym) in self.locations if sym[3:len(name) + 4] == name + '$']
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
        return Address.val(next_addr) - Address.val(sym_addr)

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

    def get_unused_symbols(self):
        """return all symbol names that have not been used, grouped by filename"""
        unused_symbols = {}  # filename x symbols
        for symbol, (_, _, unused) in self.symbols.items():
            if not unused or symbol[:2] == '_%':
                continue  # skip used symbols and internal names
            try:
                lino, filename = self.symbol_def_location[symbol]
                name = f'{symbol}:{lino}'
            except (TypeError, KeyError):
                filename = None
                name = symbol
            unused_symbols.setdefault(filename, []).append(name)
        return unused_symbols

    def list(self, strict, as_equ_statements=False):
        """generate symbol overview"""
        symbol_list = []
        reference_list = []
        for symbol in sorted(self.symbols):
            if symbol in self.registers or '%' in symbol or symbol == self.target:
                continue  # skip registers and built-in, local and internal symbols
            addr, _, _ = self.symbols.get(symbol)
            if isinstance(addr, Address):
                # add extra information to addresses
                reloc = 'REL' if addr.reloc else '   '
                bank = 'B>{:02X}'.format(addr.bank) if addr.bank != Symbols.BANK_ALL and addr.bank is not None else ''
                addr = addr.addr
            elif isinstance(addr, Reference):
                # add value of references
                reference_list.append(addr.name)
                continue
            else:
                # add immediate address value
                reloc = '   '
                bank = ''
            symbol_list.append((symbol, addr, reloc, bank))
        reffmt = '       REF  {:s}\n'
        if strict:
            symfmt = ('{:<6} EQU  >{:04X}    * {} {}\n' if as_equ_statements else
                      '    {:.<6} {} : {} {}\n')
        else:
            symfmt = ('{}:\n       equ  >{:04X}  ; {} {}\n' if as_equ_statements else
                      '    {:.<20} >{:04X} : {} {}\n')
        result = (''.join(reffmt.format(ref) for ref in reference_list) +
                  ''.join(symfmt.format(*sym) for sym in symbol_list))
        return result if strict else result.lower()


# Parser and Preprocessor

class Preprocessor:
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
        self.parse_repeat = False  # parsing repeat section?
        self.repeat_count = 0  # number of repetitions
        self.macros = {'VERS': [f" text '{VERSION}'"]}  # macros defined (including predefined macros)

    def args(self, ops):
        lhs = self.parser.expression(ops[0], well_defined=True, relaxed=True)
        rhs = self.parser.expression(ops[1], well_defined=True, relaxed=True) if len(ops) > 1 else 0
        if isinstance(lhs, Reference) or isinstance(rhs, Reference):
            raise AsmError('Cannot use reference in preprocessor condition')
        return lhs, rhs

    def str_args(self, ops):
        return [self.parser.text(op) if self.parser.is_literal(op) else
                str(self.parser.expression(op, well_defined=True))
                for op in ops]

    def DEFM(self, asm, ops):
        """define macro"""
        if len(ops) != 1:
            raise AsmError('Invalid syntax')
        self.parse_macro = ops[0]
        if self.parse_macro in ('DEFM', 'ENDM', 'IFDEF', 'IFNDEF', 'IFEQ', 'IFNE', 'IFGE', 'IFGT', 'IFLE', 'IFLT',
                                'ELSE', 'ENDIF', 'REPT', 'ENDR', 'PRINT', 'ERROR'):
            raise AsmError('Invalid macro name')
        if self.parse_macro in self.macros:
            raise AsmError('Duplicate macro name')
        self.macros[self.parse_macro] = []

    def ENDM(self, asm, ops):
        raise AsmError('Found .ENDM without .DEFM')

    def REPT(self, asm, ops):
        """repeat section n times"""
        self.repeat_count = self.parser.expression(ops[0], well_defined=True)
        self.parse_repeat = True
        self.parse_macro = '.rept'  # use lower case name as impossible macro name
        self.macros['.rept'] = []  # collect repeated section as '.rept' macro

    def ENDR(self, asm, ops):
        raise AsmError('Found .ENDR without .REPT')

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
        self.parse = self.cmp(*self.args(ops)) == 0 if self.parse else None
        self.parse_else = False

    def IFNE(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) != 0 if self.parse else None
        self.parse_else = False

    def IFGT(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) > 0 if self.parse else None
        self.parse_else = False

    def IFGE(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) >= 0 if self.parse else None
        self.parse_else = False

    def IFLT(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) < 0 if self.parse else None
        self.parse_else = False

    def IFLE(self, asm, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) <= 0 if self.parse else None
        self.parse_else = False

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

    @staticmethod
    def cmp(x, y):
        return (Address.val(x) > Address.val(y)) - (Address.val(x) < Address.val(y))

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

    def process_repeat(self, mnemonic, line):
        if mnemonic == '.ENDR':
            self.parse_repeat = False
            self.parse_macro = None
            self.macros['.rept'] *= self.repeat_count  # repeat section
            self.parser.open(macro='.rept', macro_args=())  # open '.rept' macro
        elif mnemonic == '.REPT':
            raise AsmError('Cannot repeat within repeat section')
        elif mnemonic == '.DEFM':
            raise AsmError('Cannot define macro within repeat section')
        elif mnemonic == '.ENDM':
            raise AsmError('Found .ENDM without .DEFM')
        else:
            self.macros[self.parse_macro].append(line)
        return False, None, None  # start repetition

    def process_macro(self, mnemonic, line):
        if mnemonic == '.ENDM':
            self.parse_macro = None
        elif mnemonic == '.DEFM':
            raise AsmError('Cannot define macro within macro')
        elif mnemonic == '.REPT':
            raise AsmError('Cannot repeat section within macro')
        elif mnemonic == '.ENDR':
            raise AsmError('Found .ENDR without .REPT')
        else:
            self.macros[self.parse_macro].append(line)
        return False, None, None  # macro definition

    def process(self, asm, label, mnemonic, operands, line):
        """process preprocessor commands (for pass 1)"""
        if self.parse_repeat:
            return self.process_repeat(mnemonic, line)
        if self.parse_macro:
            return self.process_macro(mnemonic, line)
        if self.parse and asm.parser.in_macro_instantiation and operands:
            operands = [self.instantiate_macro_args(op) for op in operands]
            line = self.instantiate_line(line)  # only for display
        if mnemonic and mnemonic[0] == '.':
            asm.process_label(label)
            name = mnemonic[1:]
            if name in self.macros:
                if self.parse:
                    self.parser.open(macro=name, macro_args=operands, label=label, line=line)
                    return False, None, None
            else:
                try:
                    fn = getattr(Preprocessor, name)
                except AttributeError:
                    raise AsmError('Invalid preprocessor directive')
                try:
                    fn(self, asm, operands)
                except (IndexError, ValueError):
                    raise AsmError('Syntax error')
            return False, None, None  # eliminate preprocessor commands
        else:
            return self.parse, operands, line  # normal statement


class IntmLine:
    """intermediate source line"""

    OPEN = '$OPEN$'  # constants inserted into source to denote new or resumes source units
    RESUME = '$RESM$'

    def __init__(self, mnemonic, lino=0, lidx=0, label=None, operands=(), pragmas=None, line=None, filename=None,
                 path=None, is_statement=False):
        self.label = label
        self.mnemonic = mnemonic
        self.operands = operands
        self.pragmas = pragmas
        self.lino = lino
        self.lidx = lidx
        self.line = line
        self.filename = filename
        self.path = path
        self.is_statement = is_statement


class Parser:
    """scanner and parser class"""

    def __init__(self, symbols, listing, console, path, includes=None, strict=False, relaxed=False, r_prefix=False,
                 bank_cross_check=False):
        self.symbols = symbols
        self.listing = listing
        self.console = console
        self.path = path
        self.includes = includes or []  # do not include '.' -- current path added implicitly in find()
        self.prep = Preprocessor(self, listing)
        self.strict = strict
        self.relaxed = relaxed
        self.r_prefix = r_prefix
        self.bank_cross_check = bank_cross_check
        self.text_literals = []
        self.intermediate_source = []  # parsed source by pass 1
        self.filename = None
        self.source = None
        self.macro_args = []
        self.in_macro_instantiation = False
        self.lino = 0
        self.srcline = None
        self.suspended_files = []
        self.parse_branches = [True]

    def __iter__(self):
        return self

    def open(self, filename=None, macro=None, macro_args=None, label=None, line=None):
        """open new source file or macro buffer"""
        if len(self.suspended_files) > 100:
            raise AsmError('Too many nested files or macros')
        if filename:
            newfile = '-' if filename == '-' else self.find(self.fix_path_separator(filename))
            # CAUTION: don't suspend source if file does not exist!
        else:
            newfile = None
        if self.source is not None:
            self.suspended_files.append((self.filename, self.path, self.source,
                                         self.in_macro_instantiation, self.macro_args, self.lino))
        if filename:
            self.path, self.filename = os.path.split(newfile)
            self.source = Util.readlines(newfile)  # might throw error
            self.in_macro_instantiation = False
        else:
            self.source = self.prep.macros[macro]
            self.macro_args = macro_args or []
            self.in_macro_instantiation = True
            if label or line:
                self.intermediate_source.append(IntmLine('.', lino=self.lino, label=label, line=line))
        self.filename = filename or macro
        self.lino = 0
        self.intermediate_source.append(IntmLine(IntmLine.OPEN, filename=self.filename))

    def fix_path_separator(self, path):
        """replaces foreign file separators with system one"""
        if os.path.sep in path:
            # system path (does not recognize foreign path with \-escaped chars on Linux or regular / chars on Windows)
            return path
        else:
            # foreign path
            foreign_sep = '\\' if os.path.sep == '/' else '/'
            return path.replace(foreign_sep, os.path.sep)

    def resume(self):
        """close current source file and resume previous one"""
        try:
            (self.filename, self.path, self.source,
             self.in_macro_instantiation, self.macro_args, self.lino) = self.suspended_files.pop()
            self.intermediate_source.append(IntmLine(IntmLine.RESUME, filename=self.filename))
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
        include_path = list(self.includes)
        if self.path:
            include_path.append(self.path)  # self.path changes during assembly
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
        raise AsmError('File not found: ' + filename)

    def lines(self):
        """get next logical line from source files"""
        while self.source is not None:  # loop for resume(), which might restart generator
            try:
                line = self.source[self.lino]
                self.srcline = line.rstrip()
                self.lino += 1
                yield self.lino, self.srcline, self.filename
            except IndexError:
                self.resume()

    def intermediate_lines(self):
        """return preprocessed source code"""
        for imline in self.intermediate_source:
            self.filename = imline.filename
            self.lino = imline.lino
            self.srcline = imline.line
            self.path = imline.path
            self.symbols.lidx = imline.lidx
            yield imline

    def line(self, line):
        """parse single source line"""
        if not line or line[0] == '*':
            return None, None, None, None, False
        if self.strict:
            # blanks separate fields
            fields = re.split(r'\s+', self.escape(line), maxsplit=3)
            label, mnemonic, opfield, comment = fields + [''] * (4 - len(fields))
            label = label[:6]
            operands = re.split(',', opfield) if opfield else []
        elif self.relaxed:
            # arbitrary whitespace in operands, explicit ; comments
            instruction, *remainder = self.escape(line).split(';', maxsplit=1)
            fields = re.split(r'\s+', instruction, maxsplit=2)
            label, mnemonic, opfield = fields + [''] * (3 - len(fields))
            operands = [op.strip() for op in opfield.split(',')]
            comment = remainder[0] if remainder else ''
        else:
            # comment field separated by two blanks
            parts = self.escape(line).split(';')
            fields = re.split(r'\s+', parts[0], maxsplit=2)
            label, mnemonic, opfield = fields + [''] * (3 - len(fields))
            optexts = re.split(r' {2,}|\t', opfield, maxsplit=1)
            operands = [op.strip() for op in optexts[0].split(',')] if optexts[0] else []
            comment = ' '.join(optexts[1:]) + (';' + ';'.join(parts[1:]) if len(parts) > 1 else '')
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
        if not op:
            raise AsmError('Empty address')
        if op[0] == '@':  # memory addressing
            offset, register = self.index(op[1:])
            if register is not None:
                if register == 0:
                    raise AsmError('Cannot index with register 0')
                if offset == 0 and self.symbols.pass_no > 1:
                    self.console.warn('Using indexed address @0, could use *R instead', category=Warnings.BAD_USAGE)
                return 0b10, register, offset
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

    def index(self, op):
        """parse address offset and register index"""
        # make sure not to parse expression as invalid offset+index operand!
        if not op or op[-1] != ')':
            return None, None
        try:
            index = op.rindex('(')
        except ValueError:
            return None, None
        if index == 0:  # treating @(Rn) is expression @n!
            self.console.warn('Treating as symbol expression, did you intend register index?',
                              category=Warnings.BAD_USAGE)
        # if op is an expression, there is an operator before the '('
        i = index - 1
        while i >= 0 and op[i] == ' ':
            i -= 1
        if i < 0 or op[i] in '+-*/%&|^~':
            return None, None  # is expression
        offset = self.expression(op[0:index])
        register = self.register(op[index + 1:-1])
        return offset, register

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
        sep_pattern = r'([-+*/])' if self.strict else r'([-+~&|^()]|\*\*?|//?|%%?|<<|>>|[BW]#)'
        terms = ['+'] + [tok.strip() for tok in re.split(sep_pattern, expr)]
        self.check_arith_precedence(terms)
        i = 0
        while i < len(terms):
            op, term = terms[i:i + 2]
            i += 2
            negate = False
            complement_correction = 0
            if op == ')':
                v = value.value
                reloc = reloc_count
                try:
                    value, reloc_count, op, negate, complement_correction = stack.pop()
                except IndexError:
                    raise AsmError('Syntax error')
            else:
                # unary operators
                while not term and i < len(terms) and terms[i] in '+-~(':
                    term = terms[i + 1]
                    if terms[i] == '-':
                        negate = not negate
                    elif terms[i] == '~':
                        complement_correction += 1 if negate else -1
                        negate = not negate
                    elif terms[i] == '(':
                        stack.append((value, reloc_count, op, negate, complement_correction))
                        try:
                            term = terms[i + 1]
                        except IndexError:
                            raise AsmError('Syntax error')
                        op = '+'
                        negate = False
                        complement_correction = 0
                        value = Word(0)
                        reloc_count = 0
                    i += 2
                # process next term between operators
                term_val, x_bank_access = self.term(term, well_defined=well_defined, iop=iop, relaxed=relaxed,
                                                    allow_r0=allow_r0)
                if isinstance(term_val, Local):
                    dist = -term_val.distance if negate else term_val.distance
                    term_val = self.symbols.get_locals(term_val.name, dist)
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
                    v = term_val.addr
                    reloc = 1 if term_val.reloc else 0
                else:
                    v = term_val
                    reloc = 0

            v = (-v if negate else v) + complement_correction
            w = Word(v)
            if op == '+':
                value.add(w)
                reloc_count += reloc if not negate else -reloc
            elif op == '-':
                value.sub(w)
                reloc_count -= reloc if not negate else -reloc
            elif op == '*':
                if reloc_count > 0:
                    raise AsmError('Invalid address: ' + expr)
                value.mul(op, w)
            elif op in '/%':  # signed
                if reloc_count > 0:
                    raise AsmError('Invalid address: ' + expr)
                value.div(op, w)
            elif op == '//' or op == '%%':  # unsigned
                if reloc_count > 0:
                    raise AsmError('Invalid address: ' + expr)
                value.udiv(op, w)
            elif op in '&|^':
                if reloc_count > 0:
                    raise AsmError('Cannot use relocatable address in expression: ' + expr)
                value.bit(op, w)
            elif op == '**':  # exponentiation
                base = Word(1)
                exp = w.value
                for j in range(exp):
                    base.mul('*', value)
                value = base
            elif op == '>>' or op == '<<':  # shift
                value.shift(op, v)
            else:
                raise AsmError('Invalid operator: ' + op)
        if not 0 <= reloc_count <= (0 if absolute else 1):
            raise AsmError('Invalid address: ' + expr)
        return Address(value.value, self.symbols.bank, True, self.symbols.unit_id) if reloc_count else value.value

    def check_arith_precedence(self, operators, i=2):
        """check if usual * over + arithmetic precedence is violated"""
        possible_violation = False
        possible_sign = True
        while i < len(operators):
            op = operators[i]
            if not operators[i - 1] and possible_sign and (op == '+' or op == '-'):  # i always > 0
                i += 2  # skip signs
                continue
            if op == ')':
                return False, i + 2
            elif op == '+' or op == '-':
                possible_violation = True
            elif op in '*/%' and possible_violation:
                if self.symbols.pass_no > 1:
                    self.console.warn('Expression with non-standard evaluation', category=Warnings.ARITH)
                return True, None
            elif op == '(':
                violation, i = self.check_arith_precedence(operators, i + 2)
                if violation:
                    return True, None
                elif i is None:
                    return False, None
                else:
                    possible_sign = False  # no sign after ')'
                    continue
            elif op in '&|^~':
                possible_violation = False
            i += 2
            possible_sign = True
        return False, None

    def term(self, op, well_defined=False, iop=False, relaxed=False, allow_r0=False):
        """parse constant or symbol"""
        if not op:
            raise AsmError('Syntax Error')
        cross_bank_access = False
        if op[0] == '>':
            try:
                return int(op[1:], 16), False
            except ValueError:
                raise AsmError('Invalid hex integer literal: ' + op[1:])
        elif op == '$':
            return Address(self.symbols.effective_LC(),
                           self.symbols.bank,
                           self.symbols.segment_reloc and not self.symbols.xorg_offset,
                           self.symbols.unit_id), False
        elif op[0] == ':':
            try:
                return int(op[1:], 2), False
            except ValueError:
                raise AsmError('Invalid binary integer literal: ' + op[1:])
        elif op.isdigit():
            return int(op), False
        elif op[0] == op[-1] == "'" and len(op) > 1:
            try:
                c = self.text_literals[int(op[1:-1])]
            except (ValueError, IndexError):
                raise AsmError('Invalid text literal')
            if len(c) == 1:
                return ord(c[0]), False
            elif len(c) == 2:
                return ord(c[0]) << 8 | ord(c[1]), False
            elif len(c) == 0:
                return 0, False
            else:
                raise AsmError('Invalid text literal: ' + c)
        elif op[0] == '!':
            m = re.match(r'(!+)(.*)', op)
            return Local(m.group(2), len(m.group(1))), False
        elif op[:2] in ('B#', 'W#'):
            raise AsmError('Invalid auto-constant expression')
        elif op[:2] == 'S#':
            v = self.symbols.get_size(op[2:])
            return v, False
        elif op[0] == '#':
            # should have been eliminated by preprocessor
            raise AsmError(f'Invalid macro argument: {op}')
        if op[:2] == 'X#' and not self.strict:
            cross_bank_access = True
            op = op[2:]
        if op[0] == '@':
            raise AsmError("Invalid '@' found in expression")
        if iop and op in self.symbols.registers and not (op == 'R0' and allow_r0) and self.symbols.pass_no > 1:
            self.console.warn(f'Register {op:s} used as immediate operand', category=Warnings.BAD_USAGE)
        try:
            v = self.symbols.registers[op]
        except KeyError:
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
        return Address.val(e)

    def register(self, op, well_defined=False):
        """parse register"""
        if self.symbols.pass_no == 1 and not well_defined:
            return 1  # don't return 0, as this is invalid for indexes @A(Rx)
        isalias = False
        op = op.strip()
        if not op:
            raise AsmError('Empty register')
        try:
            if op[0] == '>':
                r = int(op[1:], 16)
            elif op[0] == ':':
                return int(op[1:], 2)
            elif op.isdigit():
                r = int(op)
            elif op[0] == '@':
                raise AsmError('Expected register, found address instead: ' + op)
            else:
                isalias = True
                try:
                    r = self.symbols.registers[op]
                except KeyError:
                    r = self.symbols.get_symbol(op)  # also allow symbols for compatibility with E/A
                    if r is None or isinstance(r, Address):
                        raise ValueError  # unknown symbol
        except (TypeError, ValueError):
            raise AsmError('Invalid register: ' + op)
        if self.r_prefix and not isalias and op[0].upper() != 'R' and self.symbols.pass_no > 1:
            self.console.warn(f'Treating {op} as register, did you intend an @address?', category=Warnings.BAD_USAGE)
        if not 0 <= r <= 15:
            raise AsmError('Invalid register: ' + op)
        return r

    def bank(self, op):
        """parse bank: number or 'all'"""
        try:
            return int(op)
        except ValueError:
            pass
        if op.upper() == 'ALL':
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
            while frac_part[:2] == '00':  # no integer part
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
            raise AsmError('Cannot convert floating point number to Radix 100: ' + op)
        # invert first word if negative
        bytes_ = [exponent + 0x40] + hundreds
        if sign < 0:
            bytes_[1] = 0x100 - bytes_[1]  # cannot yield 0x100 for bytes_[1], since always != 0
            bytes_[0] = ~bytes_[0]
        # return radix-100 format
        return bytes_

    def get_filename(self, op):
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

    def check_strict_comment(self):
        """check if statement is label with comment in strict mode"""
        pass

    @staticmethod
    def raise_invalid_statement():
        """raises exception, as expression"""
        raise AsmError('Invalid statement')


class Pragmas:
    """pragmas affecting the assembler"""

    def __init__(self, parser):
        self.parser = parser  # need access to parser state

    def evaluate(self, name, value):
        """enable or disable variables"""
        if name == 'WARNINGS':
            self.parser.console.warnings.set(setall=value == 'ON')
        elif name == 'WARN-OPTS':
            self.parser.console.warnings.set(Warnings.OPTIMIZATIONS, value == 'ON')
        elif name == 'WARN-USAGE':
            self.parser.console.warnings.set(Warnings.BAD_USAGE, value == 'ON')
        elif name == 'WARN-SYMBOLS':
            self.parser.console.warnings.set(Warnings.UNUSED_SYMBOLS, value == 'ON')
        elif name == 'WARN-ARITH':
            self.parser.console.warnings.set(Warnings.ARITH, value == 'ON')
        elif name == 'LWPI':
            try:
                self.parser.symbols.WP = Util.xint(value)  # set workspace address
            except ValueError:
                self.parser.console.warn('Bad value for LWPI pragma')
        else:
            self.parser.console.warn('Unknown pragma name: ' + name)

    def set_operand_demuxer(self, asm, ops):
        """set memory speed for 'unknown' operand targets"""
        for op in ops:
            if op is not None:
                asm.demux[op[0].upper()] = op[1] == '+'

    def process(self, asm, pragmas):
        """process list of pragmas (have been uppercased previously)"""
        if pragmas is None:
            return  # open and resuming of sources
        for pragma in pragmas:
            m = re.match(r'(S[+-])?(D[+-])?$', pragma)
            if m:
                self.set_operand_demuxer(asm, m.groups())
            else:
                try:
                    name, value = pragma.split('=')
                    self.evaluate(name.strip(), value.strip())
                except (TypeError, ValueError):
                    self.parser.console.warn('Malformed pragma: ' + pragma)

    def parse(self, comment):
        """retrieve all pragmas from comment"""
        if not comment:
            return None  # no comment
        if comment[:2] == ';:':  # pragma before comment
            try:
                pragmas, _ = comment[2:].split(';', maxsplit=1)
            except (TypeError, ValueError):
                pragmas = comment[2:]
        else:  # pragma after comment
            try:
                _, pragmas = comment.split(';:', maxsplit=1)
            except (TypeError, ValueError):
                return None  # no pragma
        return [pragma.strip() for pragma in pragmas.split(',')]


# Code generation

class Program:
    """code and related properties, including externals
       NOTE: A program consists of multiple program units,
             a program unit consists of multiple segments.
    """

    def __init__(self, target, segments=None):
        self.target = target
        self.segments = segments or []
        self.externals = Externals(target)
        self.saves = []  # save ranges
        self.idt = None
        self.entry = None  # start address of program
        self.unit_count = 0
        self.max_bank = 0
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
        """prepare linking process"""
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
            if segment.bank != Symbols.BANK_ALL:
                self.max_bank = max(self.max_bank, segment.bank or 0)
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


class Segment:
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


class Assembler:
    """generate object code"""

    def __init__(self, program, opcodes, target=None, includes=None, extdefs=(), r_prefix=False, strict=False,
                 relaxed=False, timing=True, bank_cross_check=False, console=None):
        self.program = program
        self.opcodes = opcodes
        self.includes = includes or []
        self.extdefs = extdefs
        self.console = console or Xas99Console()
        self.listing = Listing(timing=timing)
        self.strict = strict
        self.relaxed = relaxed
        self.r_prefix = r_prefix
        self.bank_cross_check = bank_cross_check
        self.target = target
        self.symbols = None
        self.parser = None
        self.pragmas = None
        self.symasm = None
        self.codeasm = None
        self.segment = None
        self.demux = None  # are unknown accesses for source, dest operand demuxed?

    def assemble(self, path, srcname):
        """assemble one base file"""
        self.symbols = Symbols(self.program.externals, self.console, extdefs=self.extdefs, add_registers=self.r_prefix,
                               strict=self.strict, target=self.target)  # new symbol table for each file
        self.parser = Parser(self.symbols, self.listing, self.console, path, includes=self.includes,
                             r_prefix=self.r_prefix, bank_cross_check=self.bank_cross_check, strict=self.strict,
                             relaxed=self.relaxed)
        self.console.set_parser(self.parser)
        self.pragmas = Pragmas(self.parser)
        self.symasm = Pass1Assembler(self.program, self.opcodes, self.symbols, self.parser, self.pragmas, self.console)
        self.codeasm = Pass2Assembler(self.program, self.opcodes, self.symbols, self.parser, self.pragmas,
                                      self.listing, self.console)
        self.opcodes.use_asm(self.symasm)
        self.symasm.assemble(srcname)  # continue even with errors, to display them all
        self.opcodes.use_asm(self.codeasm)
        self.codeasm.assemble()

    @staticmethod
    def get_target(bin=False, image=False, cart=False, text=False, embed=False):
        """return target format string"""
        if bin:
            return 'BIN'
        if image:
            return 'IMAGE'
        if cart:
            return 'CART'
        if text:
            return 'TEXT'
        if embed:
            return 'XB'
        return 'OBJ'


class Pass1Assembler:
    """dummy code generation for keeping track of line counter"""

    def __init__(self, program, opcodes, symbols, parser, pragmas, console):
        self.program = program
        self.opcodes = opcodes
        self.symbols = symbols
        self.parser = parser
        self.pragmas = pragmas
        self.console = console
        self.segment = False  # no actual Segment required for symbols

    def assemble(self, srcname):
        """pass 1: gather symbols, apply preprocessor"""
        self.symbols.pass_no = 1
        self.symbols.reset()
        self.symbols.lidx = 0
        self.org(0, reloc=True)
        self.parser.open(filename=srcname)
        prev_label = None
        for lino, line, filename in self.parser.lines():
            self.symbols.lidx += 1
            try:
                # break line into fields
                label, mnemonic, operands, comment, is_statement = self.parser.line(line)
                pragmas = self.pragmas.parse(comment)  # get all pragmas from comment into list
                process, operands, line = self.parser.prep.process(self, label, mnemonic, operands, line)
                if not process:
                    continue
                int_line = IntmLine(mnemonic, lino=lino, lidx=self.symbols.lidx, label=label, operands=operands,
                                    pragmas=pragmas, line=line, filename=filename, path=self.parser.path,
                                    is_statement=is_statement)
                self.parser.intermediate_source.append(int_line)
                if not is_statement:
                    continue
                # process continuation label
                if prev_label:
                    if label:
                        prev_label = None
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
                    self.parser.check_strict_comment() or \
                    Parser.raise_invalid_statement()
            except AsmError as e:
                self.console.error(str(e))
        if self.parser.prep.parse_branches:
            self.console.error('Missing .ENDIF', nopos=True)
        if self.parser.prep.parse_repeat:
            self.console.error('Missing .ENDR', nopos=True)
        elif self.parser.prep.parse_macro:
            self.console.error('Missing .ENDM', nopos=True)

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

    def process_label(self, label, real_LC=False, tracked=False):
        """register label at current LC"""
        if not label:
            return
        if label[0] == '!':
            self.symbols.add_local_label(label[1:])
        else:
            self.symbols.add_label(label, real_LC=real_LC, tracked=tracked, lino=self.parser.lino,
                                   filename=self.parser.filename)

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


class Pass2Assembler:
    """generate object code"""

    def __init__(self, program, opcodes, symbols, parser, pragmas, listing, console):
        self.program = program
        self.opcodes = opcodes
        self.symbols = symbols
        self.parser = parser
        self.pragmas = pragmas
        self.console = console
        self.listing = listing
        self.segment = None
        self.demux = None  # are unknown accesses for source, dest operand demuxed?

    def assemble(self):
        """second pass: generate machine code, ignore symbol definitions"""
        self.symbols.pass_no = 2
        self.symbols.reset()
        self.console.reset_warnings()
        self.org(0, reloc=True, root=True)  # create root segment
        for imline in self.parser.intermediate_lines():
            if imline.mnemonic == IntmLine.OPEN:  # markers to indicate start ...
                self.listing.open(self.symbols.LC, imline.filename)
                continue
            elif imline.mnemonic == IntmLine.RESUME:  # ... and end of include file or macro
                self.listing.resume(self.symbols.LC, imline.filename)
                continue
            try:
                if imline.mnemonic[0] == '.':  # macro call, only kept for inclusion in list file
                    self.listing.prepare(None, Line(lino=imline.lino, line=imline.line))
                    continue
            except (TypeError, IndexError):
                pass
            self.demux_reset()
            self.pragmas.process(self, imline.pragmas)
            self.listing.prepare(self.symbols.LC, Line(lino=imline.lino, line=imline.line))
            if not imline.is_statement:
                continue
            # NOTE: Pass 2 can discard any label information, since (1) Assembler.process_label is empty,
            #       and (2) the EQU directive ignores the label for pass 2.
            #       Also, the syntax check for bad label continuation is not required, since output will
            #       be discarded if error in pass 1 occurred.
            if imline.label and imline.label[-1] == ':':
                if not imline.mnemonic:
                    continue
                else:
                    imline.label = imline.label[:-1]
            try:
                Directives.process(self, imline.label, imline.mnemonic, imline.operands) or \
                  self.opcodes.process(imline.label, imline.mnemonic, imline.operands) or \
                  Parser.raise_invalid_statement()
            except AsmError as e:
                self.console.error(str(e))
        # complete code generation
        if self.segment:
            self.segment.close(self.symbols.LC)
        # unused symbols per filename
        for fn, symbols in self.symbols.get_unused_symbols().items():
            symbols_text = ', '.join(symbols)
            self.console.warn('Unused constants: ' + (symbols_text if self.parser.strict else symbols_text.lower()),
                              category=Warnings.UNUSED_SYMBOLS, filename=fn, nopos=True)

    def process_label(self, label, real_LC=False, tracked=False):
        """no new symbols in pass 2"""
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
        if not words:
            return
        self.word(words[0], cycles)  # opcode with timing information
        for word in words[1:]:
            if word is not None:
                self.word(word)

    def auto_constants(self):
        """create code stanza for auto-constants"""
        def list_autoconsts(name, local_value, local_lc, byte=False):
            auto_name = name if self.parser.strict else name.lower()
            self.listing.prepare(self.symbols.LC, Line(line=auto_name))
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

    def demux_reset(self):
        """reset operand demuxed state"""
        self.demux = {'S': True, 'D': True}  # memory demuxed for operands?


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


class Optimizer:
    """object code analysis and optimization, currently checks only (in both passes)"""

    @staticmethod
    def process(asm, mnemonic, opcode, fmt, arg1, arg2):
        if asm.symbols.pass_no == 2 and mnemonic == 'B':  # need forward symbols for branch optimization
            t, index, *_ = arg1
            if not (t == 0b10 and index == 0):  # @symbol, no index
                return
            addr = Address.val(arg1[2])  # branch address
            # since branches cannot cross bank boundaries, no cross-bank check is necessary
            if not isinstance(addr, int):
                return
            if -128 <= (addr - asm.symbols.effective_LC() - 2) // 2 <= 128:
                # upper bound is 128 instead of 127, since replacing B by JMP
                # would also eliminate one word (the target of B)
                asm.console.warn('Possible branch/jump optimization', category=Warnings.OPTIMIZATIONS)


class Linker:
    """Object code and binary handling"""

    def __init__(self, program, base=0, resolve_conflicts=False, console=None):
        self.program = program
        self.reloc_base = base
        self.console = console or Xas99Console()
        self.resolve_conflicts = resolve_conflicts
        self.symbols = None
        self.offsets = None  # dict of program relocation offsets
        self.bank_count = None  # number of banks; 0 if no/one bank

    def load(self, files):
        """link external object code, E/A #5 program file, or binary"""
        for filename, data in files:
            self.symbols = Symbols(self.program.externals, self.console)  # new symbols for each file
            name, segments = self.load_object_code(data)
            self.program.segments.extend(segments)
            self.program.set_name(name)

    def load_object_code(self, objcode):
        """link object code"""
        segment = Segment(self.symbols, None, reloc=True)  # initial segment
        segments = [segment]
        LC = 0  # pick some initial value, won't have any effect for E/A and xas99 object code anyway
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
                self.console.lwarn('Invalid line numner; object code file may be corrupted', lino=lino)
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
        #       we cannot have a reference at address 0
        #       (we issue warnings at assembly time instead)
        while addr:  # neither 0 nor None
            addr = self.patch_addr(segments, addr, symbol)

    @staticmethod
    def patch_addr(segments, addr, symbol):
        """replace one addr in ref chain by Reference, return next addr in chain"""
        vaddr = Address.val(addr)
        for segment in segments:
            try:
                if isinstance(segment.code[vaddr], Address):
                    next_addr = Address.val(segment.code[vaddr])
                else:
                    next_addr = (segment.code[vaddr] << 8) | segment.code[vaddr + 1]
                    del segment.code[vaddr + 1]
                segment.code[vaddr] = Reference(symbol)
                return next_addr
            except KeyError:
                pass  # addr not in this segment, try next
        return None

    def link(self, warn_unresolved_refs=False):
        """link object code"""
        self.offsets = self.program.layout_program(self.reloc_base, self.resolve_conflicts)
        self.resolve_references(warn_unresolved_refs)
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
            self.console.lwarn('Unresolved references: ' + ', '.join(symbols))

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
                    if addr == 0:
                        self.console.warn("Found reference at address >0, won't be able to resolve when linking",
                                          nopos=True)
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
        saves = self.program.saves
        if save is not None:
            saves.append(save)
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
                    self.console.lwarn(f'Unknown reference: {entry.name}, substituting null')
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

    def generate_joined_binary(self, start_addr=None, minimize=False):
        """join banked binaries into single binary file with padding
           start address of resulting binary is >x000, length is multiple of >2000 unless minimized
        """
        binaries = self.generate_binaries()  # bank, save_addr, min_addr, binary
        if start_addr is None:
            start_addr = Util.align(min(min_addr for _, _, min_addr, _ in binaries))
        if self.bank_count:
            binary = b''.join(self.join_bank_chunks(binaries, bank, start_addr,
                                                    minimize=minimize and bank == self.bank_count - 1)
                              for bank in range(self.bank_count))
        else:
            binary = self.join_bank_chunks(binaries, None, start_addr, minimize=minimize)
        return start_addr, binary

    def join_bank_chunks(self, binaries, bank, start_addr, minimize=False):
        """join disjoint chunks to single aligned full-size bank"""
        parts = []
        chunks = sorted((first_addr, data) for bank_, _, first_addr, data in binaries if bank_ == bank)
        last_addr = start_addr
        for first_addr, data in chunks:
            parts.append(bytes(first_addr - last_addr))
            parts.append(data)
            last_addr = first_addr + len(data)
        if not minimize:
            parts.append(bytes(-last_addr % 0x2000))
        return b''.join(parts)

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
            save = Address.val(sfirst), Address.val(slast)
            offset = Address.val(sload) - Address.val(sfirst)
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
            # CALL INIT :: CALL LOAD(>3FF8,"XYZZY"):: CALL LOAD(>2004,>FF,>E4):: CALL LINK("XYZZY")
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

    @staticmethod
    def get_cart_base(program):
        """find reloc base address"""
        for segment in program:
            if segment.dummy or not segment.code:
                continue
            if not segment.reloc:
                return 0  # for mixed reloc/non-reloc, do not relocate at all
            try:
                if segment.min_LC == 0 and segment.code[0] == 0xaa:
                    return 0x6000  # move header to cart range
            except (IndexError, TypeError):
                pass
            try:
                if segment.min_LC == 0x6000 and segment.code[0x6000] == 0xaa:
                    return 0  # keep as-is
            except (IndexError, TypeError):
                pass
        return 0x6030  # no header found, so add one

    def generate_cartridge(self, name):
        """generate RPK file for use as MESS rom cartridge"""
        layout = f"""<?xml version='1.0' encoding='utf-8'?>
                    <romset version='1.0'>
                        <resources>
                            <rom id='romimage' file='{name:s}.bin'/>
                        </resources>
                        <configuration>
                            <pcb type='{'paged378' if self.bank_count >= 2 else 'standard'}'>
                                <socket id='rom_socket' uses='romimage'/>
                            </pcb>
                        </configuration>
                    </romset>"""
        metainf = f"""<?xml version='1.0'?>
                     <meta-inf>
                         <name>{name:s}</name>
                     </meta-inf>"""
        base_addr, cart_image = self.generate_joined_binary(minimize=True)
        if base_addr != 0x6000:  # aligned to multiple of >2000 by joined_binary
            raise AsmError('Invalid address range for cart image')
        if len(cart_image) > 0x2000 * (self.bank_count or 1):
            raise AsmError(f'Image too large for cart with {self.bank_count or "no"} banks')
        if cart_image[0] != 0xaa:
            # create simple GPL header for specified entry (replaces first >30 bytes in image)
            if any(b != 0 for b in cart_image[:0x30]):
                self.console.warn('Generated GPL header overwrites non-zero data')
            entry = self.program.entry or Address(self.reloc_base)  # or first word of cart
            start_addr = entry.addr + self.reloc_base if entry.reloc else entry.addr
            try:
                menu = Util.chrw(0) + Util.chrw(start_addr) + bytes((len(name),)) + name.encode(encoding='ascii')
            except UnicodeEncodeError:
                raise AsmError(f'Program name "{name}" is not ASCII')
            cart_image = (bytes((0xaa, 0x01, 0x00, 0x00, 0x00, 0x00, 0x60, 0x10)) + bytes(8) +
                          menu +
                          bytes(27 - len(name)) +  # pad header to size of 0x30 bytes
                          cart_image[0x30:])
        return cart_image, layout, metainf


# Console and Listing

class Xas99Console(Console):
    """collects errors and warnings"""

    def __init__(self, warnings=None, colors=None):
        self.parser = None
        super().__init__('xas99', VERSION, warnings=warnings, colors=colors)

    def set_parser(self, parser):
        self.parser = parser  # assembler or linker

    def warn(self, message, category=Warnings.DEFAULT, filename=None, nopos=False):
        if nopos:
            info, message = self._format(message, self.parser.symbols.pass_no, filename, None, None)
        else:
            info, message = self._format(message, self.parser.symbols.pass_no, filename or self.parser.filename,
                                         self.parser.lino, self.parser.srcline)
        super().warn(info, message, category)

    def lwarn(self, message, lino=None):
        """warning issued by linker"""
        info, message = self._format(message, 'L', None, lino, None)
        super().warn(info, message)

    def error(self, message, nopos=False):
        if nopos:
            info, message = self._format(message, self.parser.symbols.pass_no, None, None, None, error=True)
        else:
            info, message = self._format(message, self.parser.symbols.pass_no, self.parser.filename,
                                         self.parser.lino, self.parser.srcline, error=True)
        super().error(info, message)

    def _format(self, message, pass_no, filename, lino, line, error=False):
        """format info and error message"""
        text = 'Error' if error else 'Warning'
        s_filename = filename or '***'
        s_pass = pass_no if isinstance(pass_no, str) else str(pass_no) or '*'
        s_lino = f'{lino:04d}' if lino is not None else '****'
        s_line = line or ''
        return f'> {s_filename} <{s_pass}> {s_lino} - {s_line}', f'***** {text:s}: {message}'


class Listing:
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


class Line:
    """source code line"""

    def __init__(self, lino=None, line=None, text1=None, text2=None, timing=None):
        self.lino = lino
        self.line = line
        self.text1 = text1
        self.text2 = text2
        self.timing = timing


# Command line processing

class Xas99Processor(CommandProcessor):

    def __init__(self):
        super().__init__(AsmError)
        self.asm = None
        self.linker = None

    def parse(self):
        args = argparse.ArgumentParser(description='TMS9900-family cross-assembler, v' + VERSION)
        args.add_argument('sources', metavar='<source>', nargs='*', help='assembly source code(s)')
        cmd = args.add_mutually_exclusive_group()
        cmd.add_argument('-b', '--binary', action='store_true', dest='bin',
                         help='create program binaries')
        cmd.add_argument('-B', '--single-binary', action='store_true', dest='joinbin',
                         help='create single joined program binary')
        cmd.add_argument('-i', '--image', action='store_true', dest='image',
                         help='create program image (E/A option 5)')
        cmd.add_argument('-c', '--cart', action='store_true', dest='cart',
                         help='create MAME cart image')
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
        args.add_argument('-105', '--99105', action='store_true', dest='use_99000',
                          help='add TMS99105/110-specific instructions')
        args.add_argument('-s', '--strict', action='store_true', dest='strict',
                          help='strict TI mode; disable xas99 extensions')
        args.add_argument('-r', '--relaxed', action='store_true', dest='relaxed',
                          help='relaxed syntax mode with extra whitespace and explicit comments')
        args.add_argument('-n', '--name', dest='name', metavar='<name>',
                          help='set program name, e.g., for cartridge')
        args.add_argument('-a', '--base', dest='base', metavar='<addr>',
                          help='set base address for relocatable code')
        args.add_argument('-R', '--register-symbols', action='store_true', dest='r_prefix',
                          help='add register symbols (TI Assembler option R)')
        args.add_argument('-C', '--compress', action='store_true', dest='compressed',
                          help='compress object code (TI Assembler option C)')
        args.add_argument('-L', '--listing-file', dest='listing', metavar='<file>',
                          help='generate listing file (TI Assembler option L)')
        args.add_argument('-S', '--symbol-table', action='store_true', dest='symbols',
                          help='add symbol table to listing (TI Assembler option S)')
        args.add_argument('-I', '--include', dest='inclpath', nargs='+', metavar='<path>',
                          help='listing of include search paths')
        args.add_argument('-D', '--define-symbol', dest='defs', nargs='+', metavar='<sym[=val]>',
                          help='add symbol to symbol table')
        args.add_argument('-E', '--symbol-equs', dest='equs', metavar='<file>',
                          help='put symbols in EQU file')
        args.add_argument('-M', '--minimized-binary', action='store_true', dest='minm',
                          help='create minimized SAVE binaries or joined binary')
        args.add_argument('-X', '--cross-checks', action='store_true', dest='x_checks',
                          help='enable cross-bank checks for banked programs')
        args.add_argument('-q', action='store_true', dest='quiet',
                          help='quiet, do not show warnings')
        args.add_argument('--quiet-opts', action='store_true', dest='quiet_opt',
                          help='quiet, do not show optimization warnings')
        args.add_argument('--quiet-unused-syms', action='store_true', dest='quiet_use',
                          help='quiet, do not show unused symbols warnings')
        args.add_argument('--quiet-usage', action='store_true', dest='quiet_ops',
                          help='quiet, do not show potential incorrect usage of arguments warnings')
        args.add_argument('--quiet-arith', action='store_true', dest='quiet_arith',
                          help='quiet, do not show non-standard arithmetic precedence warnings')
        args.add_argument('--color', action='store', dest='color', choices=['off', 'on'],
                          help='enable or disable color output')
        args.add_argument('-o', '--output', dest='output', metavar='<file>',
                          help='set output file name or target directory')
        try:
            default_opts = os.environ[CONFIG].split()
        except KeyError:
            default_opts = []
        self.opts = args.parse_args(args=default_opts + sys.argv[1:])  # passed opts override default opts
        # restore source files parsed as list option
        self.fix_greedy_list_parsing('sources', 'inclpath', 'defs')

        if not (self.opts.sources or self.opts.linker or self.opts.linker_resolve):
            args.error('One of <source> or -l/-ll is required.')
        if self.opts.base and self.opts.embed:
            args.error('Cannot set base address when embedding or creating cart.')

    def run(self):
        # setup
        warnings = Warnings({Warnings.DEFAULT: True,
                             Warnings.OPTIMIZATIONS: not self.opts.quiet_opt,
                             Warnings.BAD_USAGE: not self.opts.quiet_ops,
                             Warnings.UNUSED_SYMBOLS: not self.opts.quiet_use,
                             Warnings.ARITH: not self.opts.quiet_arith},
                            none=self.opts.quiet)
        self.console = Xas99Console(warnings, self.opts.color)
        foreign_architecture = self.opts.use_9995 or self.opts.use_f18a or self.opts.use_99000
        target = Assembler.get_target(bin=self.opts.bin, image=self.opts.image, cart=self.opts.cart,
                                      text=self.opts.text, embed=self.opts.embed)
        program = Program(target=target)

        # assembly step
        if self.opts.sources:
            root = os.path.dirname(os.path.realpath(__file__))  # installation dir (path to xas99)
            includes = [os.path.join(root, 'lib')] + Util.get_opts_list(self.opts.inclpath)
            opcodes = Opcodes(use_9995=self.opts.use_9995, use_f18a=self.opts.use_f18a, use_99000=self.opts.use_99000)
            self.asm = Assembler(program, opcodes,
                                 target=target,
                                 includes=includes,
                                 extdefs=Util.get_opts_list(self.opts.defs),
                                 r_prefix=self.opts.r_prefix,
                                 strict=self.opts.strict,
                                 relaxed=self.opts.relaxed,
                                 timing=not foreign_architecture,
                                 bank_cross_check=self.opts.x_checks,
                                 console=self.console)
            for source in self.opts.sources:
                dirname = os.path.dirname(source) or '.'
                basename = os.path.basename(source)
                try:
                    self.asm.assemble(dirname, basename)
                except IOError as e:
                    sys.exit('File error: {}: {}.'.format(e.get_filename, e.strerror))
                except AsmError as e:
                    sys.exit('Error: {}.'.format(e))
                if self.asm.console.entries:
                    self.asm.console.print()
                if self.asm.console.errors:
                    sys.exit(1)
                self.asm.console.reset()
            if self.opts.sources[0] == '-':
                self.barename = 'stdin'
            else:
                self.barename, _ = os.path.splitext(os.path.basename(self.opts.sources[0]))
            self.name = self.opts.name or self.barename[:10].upper()
        else:
            self.asm = None
            self.barename = 'a'
            self.name = self.opts.name or 'A'
    
        # link step
        self.linker = Linker(program, base=self.reloc_base(self.opts, program),
                             resolve_conflicts=self.opts.linker_resolve, console=self.console)
        try:
            if self.opts.linker or self.opts.linker_resolve:
                data = [(filename, Util.readdata(filename))
                        for filename in (self.opts.linker or self.opts.linker_resolve)]
                self.linker.load(data)
            self.linker.link(warn_unresolved_refs=
                             self.opts.image or self.opts.bin or self.opts.embed or self.opts.text or self.opts.cart)
            if self.linker.console.entries:
                self.linker.console.print()
        except AsmError as e:
            sys.exit(self.console.colstr(f'Error: {str(e)}.'))

    def reloc_base(self, opts, program):
        if opts.base:
            return Util.xint(self.opts.base)
        elif opts.image:
            return 0xa000
        elif opts.cart:
            return Linker.get_cart_base(program)
        else:
            return 0

    def prepare(self):
        if self.opts.bin:
            self.bin()
        elif self.opts.joinbin:
            self.joinbin()
        elif self.opts.text:
            self.text()
        elif self.opts.image:
            self.image()
        elif self.opts.cart:
            self.cart()
        elif self.opts.embed:
            self.embed()
        else:
            self.obj_code()
        if self.opts.listing:
            self.listing()
        if self.opts.equs:
            self.equs()

    def bin(self):
        binaries = self.linker.generate_binaries(minimize=self.opts.minm)
        if not binaries:
            self.result.append(RFile(bytes(0), self.barename, '.bin'))
        else:
            use_base = Program.max_bins_per_bank(binaries) > 1
            for bank, save, addr, data in binaries:
                tag = Util.name_suffix(base=addr, bank=bank, use_base=use_base, bank_count=self.linker.bank_count,
                                       max_bank=self.linker.program.max_bank)
                self.result.append(RFile(data, self.barename, '.bin', suffix=tag))

    def joinbin(self):
        _, binary = self.linker.generate_joined_binary(minimize=self.opts.minm)
        self.result.append(RFile(binary, self.barename, '.bin'))

    def text(self):
        texts = self.linker.generate_text(self.opts.text.lower())
        if not texts:
            self.result.append(RFile('', self.barename, '.dat', istext=True))
        else:
            use_base = Program.max_bins_per_bank(texts) > 1
            for bank, save, addr, text in texts:
                tag = Util.name_suffix(base=addr, bank=bank, use_base=use_base, bank_count=self.linker.bank_count,
                                       max_bank=self.linker.program.max_bank)
                self.result.append(RFile(text, self.barename, '.dat', suffix=tag, istext=True))

    def image(self):
        data = self.linker.generate_image()
        if not data:
            self.result.append(RFile(bytes(0), self.barename, '.img'))
        else:
            for i, image in enumerate(data):
                self.result.append(RFile(image, Util.sinc(self.barename, i), '.img',
                                         altname=Util.sinc(self.opts.output, i)))

    def cart(self):
        data, layout, metainf = self.linker.generate_cartridge(self.name)
        with zipfile.ZipFile(Util.outname(self.barename, '.rpk', output=self.opts.output), 'w') as archive:
            archive.writestr(self.name + '.bin', data)
            archive.writestr('layout.xml', layout)
            archive.writestr('meta-inf.xml', metainf)

    def embed(self):
        xb_program = self.linker.generate_XB_loader()
        self.result.append(RFile(xb_program, self.barename, '.iv254'))

    def obj_code(self):
        code = self.linker.generate_object_code(self.opts.compressed)
        self.result.append(RFile(code, self.barename, '.obj'))

    def listing(self):
        listing = self.asm.listing.list() + (self.asm.symbols.list(self.opts.strict) if self.opts.symbols else '')
        self.result.append(RFile(listing, self.barename, '.lst', istext=True, output=self.opts.listing))

    def equs(self):
        equs = self.asm.symbols.list(self.opts.strict, as_equ_statements=True)
        self.result.append(RFile(equs, self.barename, '.equ', istext=True, output=self.opts.equs))


if __name__ == '__main__':
    status = Xas99Processor().main()
    sys.exit(status)
