#!/usr/bin/env python3

# xga99: A GPL cross-assembler
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
import os.path
import math
import re
import argparse
import zipfile
from xcommon import CommandProcessor, RFile, Util, Warnings, Console


VERSION = '3.6.5'

CONFIG = 'XGA99_CONFIG'


# Error handling

class AsmError(Exception):
    pass


# Addresses

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

    def __eq__(self, other):
        return (isinstance(other, Address) and
                self.addr == other.addr and
                self.local == other.local)

    def __ne__(self, other):
        return not self == other

    def hex(self):
        """return address as two-address tuple"""
        return '{:02X}'.format(self.addr >> 8), '{:02X}'.format(self.addr & 0xff)

    @staticmethod
    def val(n):
        """dereference address"""
        return n.addr if isinstance(n, Address) else n


class Local:
    """local label reference"""

    def __init__(self, name, distance):
        self.name = name
        self.distance = distance


# Opcodes and Directives

class Opcodes:
    op_imm = lambda parser, x: (parser.expression(x[0]),)
    op_immb = lambda parser, x: (parser.byte_expression(x[0]),)
    op_immb_gs = lambda parser, x: (parser.byte_expression(x[0]),
                                    parser.gaddress(x[1], is_gs=True))
    op_opt_255 = lambda parser, x: (parser.byte_expression(x[0]) if x else 255,)
    op_gd = lambda parser, x: (parser.gaddress(x[0], is_gs=False),)
    op_gs_gd = lambda parser, x: (parser.gaddress(x[0], is_gs=True),
                                  parser.gaddress(x[1], is_gs=False))
    op_gs_dgd = lambda parser, x: (parser.gaddress(x[0], is_gs=True, is_d=True),
                                   parser.gaddress(x[1], is_gs=False))
    op_lab = lambda parser, x: (parser.label(x[0]),)
    op_move = lambda parser, x: parser.move(x)

    opcodes = {
        # 4.1 compare and test instructions
        'H': (0x09, 5, None),
        'GT': (0x0a, 5, None),
        'CARRY': (0x0c, 5, None),
        'OVF': (0x0d, 5, None),
        'CEQ': (0xd4, 1, op_gs_gd),
        'DCEQ': (0xd5, 1, op_gs_dgd),
        'CH': (0xc4, 1, op_gs_gd),
        'DCH': (0xc5, 1, op_gs_dgd),
        'CHE': (0xc8, 1, op_gs_gd),
        'DCHE': (0xc9, 1, op_gs_dgd),
        'CGT': (0xcc, 1, op_gs_gd),
        'DCGT': (0xcd, 1, op_gs_dgd),
        'CGE': (0xd0, 1, op_gs_gd),
        'DCGE': (0xd1, 1, op_gs_dgd),
        'CLOG': (0xd8, 1, op_gs_gd),
        'DCLOG': (0xd9, 1, op_gs_dgd),
        'CZ': (0x8e, 6, op_gd),
        'DCZ': (0x8f, 6, op_gd),
        # 4.2 program control instructions
        'BS': (0x60, 4, op_lab),
        'BR': (0x40, 4, op_lab),
        'B': (0x05, 3, op_lab),
        'CASE': (0x8a, 6, op_gd),
        'DCASE': (0x8b, 6, op_gd),
        'CALL': (0x06, 3, op_lab),
        'FETCH': (0x88, 6, op_gd),
        'RTN': (0x00, 5, None),
        'RTNC': (0x01, 5, None),
        # 4.4 arithmetic and logical instructions
        'ADD': (0xa0, 1, op_gs_gd),
        'DADD': (0xa1, 1, op_gs_dgd),
        'SUB': (0xa4, 1, op_gs_gd),
        'DSUB': (0xa5, 1, op_gs_dgd),
        'MUL': (0xa8, 1, op_gs_gd),
        'DMUL': (0xa9, 1, op_gs_dgd),
        'DIV': (0xac, 1, op_gs_gd),
        'DDIV': (0xad, 1, op_gs_dgd),
        'INC': (0x90, 6, op_gd),
        'DINC': (0x91, 6, op_gd),
        'INCT': (0x94, 6, op_gd),
        'DINCT': (0x95, 6, op_gd),
        'DEC': (0x92, 6, op_gd),
        'DDEC': (0x93, 6, op_gd),
        'DECT': (0x96, 6, op_gd),
        'DDECT': (0x97, 6, op_gd),
        'ABS': (0x80, 6, op_gd),
        'DABS': (0x81, 6, op_gd),
        'NEG': (0x82, 6, op_gd),
        'DNEG': (0x83, 6, op_gd),
        'INV': (0x84, 6, op_gd),
        'DINV': (0x85, 6, op_gd),
        'AND': (0xb0, 1, op_gs_gd),
        'DAND': (0xb1, 1, op_gs_dgd),
        'OR': (0xb4, 1, op_gs_gd),
        'DOR': (0xb5, 1, op_gs_dgd),
        'XOR': (0xb8, 1, op_gs_gd),
        'DXOR': (0xb9, 1, op_gs_dgd),
        'CLR': (0x86, 6, op_gd),
        'DCLR': (0x87, 6, op_gd),
        'ST': (0xbc, 1, op_gs_gd),
        'DST': (0xbd, 1, op_gs_dgd),
        'EX': (0xc0, 1, op_gs_gd),
        'DEX': (0xc1, 1, op_gs_dgd),
        'PUSH': (0x8c, 6, op_gd),
        'MOVE': (0x20, 9, op_move),
        'SLL': (0xe0, 1, op_gs_gd),  # opGdGs in TI Guide ff.
        'DSLL': (0xe1, 1, op_gs_dgd),
        'SRA': (0xdc, 1, op_gs_gd),
        'DSRA': (0xdd, 1, op_gs_dgd),
        'SRL': (0xe4, 1, op_gs_gd),
        'DSRL': (0xe5, 1, op_gs_dgd),
        'SRC': (0xe8, 1, op_gs_gd),
        'DSRC': (0xe9, 1, op_gs_dgd),
        # 4.5 graphics and miscellaneous instructions
        'COINC': (0xed, 1, op_gs_dgd),
        'BACK': (0x04, 2, op_immb),
        'ALL': (0x07, 2, op_immb),
        'RAND': (0x02, 2, op_opt_255),
        'SCAN': (0x03, 5, None),
        'XML': (0x0f, 2, op_immb),
        'EXIT': (0x0b, 5, None),
        'I/O': (0xf6, 8, op_immb_gs),  # opGsImm
        # BASIC
        'PARSE': (0x0e, 2, op_immb),
        'CONT': (0x10, 5, None),
        'EXEC': (0x11, 5, None),
        'RTNB': (0x12, 5, None),
        # undocumented
        'SWGR': (0xf8, 1, op_gs_gd),
        'DSWGR': (0xf9, 1, op_gs_dgd),
        'RTGR': (0x13, 5, None)
        # end of opcodes
    }

    pseudos = {
        # 4.3 bit manipulation and pseudo instruction
        'RB': ('AND', ['2**($1)^>FFFF', '$2']),
        'SB': ('OR', ['2**($1)', '$2']),
        'TBR': ('CLOG', ['2**($1)', '$2']),
        'HOME': ('DCLR', ['@YPT']),
        'POP': ('ST', ['*STATUS', '$1'])
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
        'HTEXT': (0x00, op_text),
        'VTEXT': (0x20, op_text),
        'HCHAR': (0x40, op_char),
        'VCHAR': (0x60, op_char),
        'COL+': (0x80, op_incr),
        'ROW+': (0xa0, op_incr),
        'HSTR': (0xe0, op_hstr),
        # 'FOR': (0xc0, op_value),  # -> directive
        # 'FEND': (0xfb, None),  # -> directive
        'BIAS': (0xfc, op_bias),
        'ROW': (0xfe, op_value),
        'COL': (0xff, op_value)
    }

    @staticmethod
    def process(asm, label, mnemonic, operands):
        """get assembly code for mnemonic"""
        asm.process_label(label)
        if mnemonic in Opcodes.pseudos:
            mnemonic, substs = Opcodes.pseudos[mnemonic]
            operands = [re.sub(r'\$(\d+)',
                               lambda m: operands[int(m.group(1)) - 1], subst)
                        for subst in substs]
        if asm.parser.fmt_mode:
            try:
                opcode, parse = Opcodes.fmt_codes[mnemonic]
                args = parse(asm.parser, operands) if parse else ()
            except (KeyError, ValueError, IndexError):
                raise AsmError('Syntax error in FMT mode')
            Opcodes.generate(asm, opcode, 7, args)
        else:
            try:
                opcode, fmt, parse = Opcodes.opcodes[mnemonic]
                args = parse(asm.parser, operands) if parse else ()
            except (KeyError, ValueError, IndexError):
                raise AsmError('Syntax error')
            Opcodes.generate(asm, opcode, fmt, args)

    @staticmethod
    def generate(asm, opcode, fmt, args):
        """generate byte code"""
        if fmt == 1:
            assert isinstance(args[0], Operand)
            s = 1 if args[0].immediate else 0
            asm.emit(opcode | s << 1, args[1], args[0])
        elif fmt == 2:
            asm.emit(opcode, args[0])
        elif fmt == 3:
            asm.emit(opcode, Address(args[0]))
        elif fmt == 4:
            asm.emit(opcode, Address(args[0], local=True))
        elif fmt == 5:
            asm.emit(opcode)
        elif fmt == 6:
            asm.emit(opcode, args[0])
        elif fmt == 7:
            oo = args[0] - 1 if len(args) > 0 else 0
            asm.emit(opcode | oo, *args[1:])
        elif fmt == 8:
            asm.emit(opcode, args[1], args[0] & 0xff)
        elif fmt == 9:
            oo, ln, gd, gs = args
            asm.emit(opcode | oo, ln, gd, gs)
        else:
            raise AsmError(f'Unsupported opcode format {fmt}')


class Directives:
    @staticmethod
    def EQU(asm, label, ops):
        value = asm.parser.expression(ops[0])
        asm.symbols.add_symbol(label, value)

    @staticmethod
    def DATA(asm, label, ops):
        asm.process_label(label, tracked=True)
        asm.emit(*[Address(asm.parser.expression(op)) for op in ops])

    @staticmethod
    def BYTE(asm, label, ops):
        asm.process_label(label, tracked=True)
        asm.emit(*[asm.parser.expression(op) & 0xff for op in ops])

    @staticmethod
    def TEXT(asm, label, ops):
        asm.process_label(label, tracked=True)
        for op in ops:
            text = asm.parser.text(op)
            asm.emit(*[ord(c) for c in text])

    @staticmethod
    def STRI(asm, label, ops):
        asm.process_label(label, tracked=True)
        text = ''.join(asm.parser.text(op) for op in ops)
        asm.emit(len(text), *[ord(c) for c in text])

    @staticmethod
    def FLOAT(asm, label, ops):
        asm.process_label(label, tracked=True)
        for op in ops:
            bytes_ = asm.parser.radix100(op)
            asm.emit(*bytes_)

    @staticmethod
    def BSS(asm, label, ops):
        asm.process_label(label, tracked=True)
        size = asm.parser.expression(ops[0])
        asm.emit(*[0x00 for _ in range(size)])

    @staticmethod
    def GROM(asm, label, ops):
        value = asm.parser.value(ops[0])
        grom = (value << 13) if value < 8 else value & 0xe000
        asm.org(grom, 0x0000)
        asm.process_label(label)

    @staticmethod
    def AORG(asm, label, ops):
        offset = asm.parser.value(ops[0])
        if not 0 <= offset < 0x2000:
            raise AsmError(f'AORG offset {offset:04X} out of range')
        asm.org(asm.grom, offset)
        asm.process_label(label)

    @staticmethod
    def TITLE(asm, label, ops):
        asm.process_label(label)
        text = asm.parser.text(ops[0])
        asm.program.title = text[:12]

    @staticmethod
    def FMT(asm, label, ops):
        asm.process_label(label)
        asm.parser.fmt_mode = True
        asm.emit(0x08)

    @staticmethod
    def FOR(asm, label, ops):
        asm.process_label(label)
        asm.parser.for_loops.append(Address(asm.symbols.LC + 1))
        count = asm.parser.expression(ops[0])
        asm.emit(0xC0 + count - 1)

    @staticmethod
    def FEND(asm, label, ops):
        asm.process_label(label)
        if asm.parser.for_loops:
            addr = asm.parser.for_loops.pop()
            if ops:
                addr = Address(asm.parser.label(ops[0]))
            asm.emit(0xFB, addr)
        elif asm.parser.fmt_mode:
            asm.emit(0xFB)
            asm.parser.fmt_mode = False
        else:
            raise AsmError('Syntax error: unexpected FEND')

    @staticmethod
    def COPY(asm, label, ops):
        asm.process_label(label)
        filename = asm.parser.get_filename(ops[0])
        asm.parser.open(filename=filename)

    @staticmethod
    def BCOPY(asm, label, ops):
        """extension: include binary file as BYTE stream"""
        asm.process_label(label)
        filename = asm.parser.get_filename(ops[0])
        path = asm.parser.find(filename)  # might throw exception
        try:
            with open(path, 'rb') as f:
                bs = f.read()
                asm.emit(*bs)
        except IOError as e:
            raise AsmError(e)

    @staticmethod
    def END(asm, label, ops):
        asm.process_label(label)
        if ops:
            asm.program.entry = asm.symbols.get_symbol(ops[0], required=True)
        asm.parser.stop()

    ignores = [
        '', 'PAGE', 'LIST', 'UNL', 'LISTM', 'UNLM'
        ]

    @staticmethod
    def process(asm, label, mnemonic, operands):
        """process directives"""
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

class Symbols:
    """symbol table and line counter"""

    def __init__(self, definitions=None, ryte_symbols=False):
        self.symbols = {}  # name: (value, used)
        self.symbol_def_location = {}  # symbol definition location (lino, filename)
        self.updated = False  # has at least one value changed?
        self.pass_no = 0
        self.LC = 0
        self.lidx = 0
        self.locations = []  # listing of (lidx, name), must not be deleted between passes
        self.definitions = {
            'MAXMEM': 0x8370,   # CPU RAM
            'DATSTK': 0x8372,
            'SUBSTK': 0x8373,
            'KEYBRD': 0x8374,
            'KEY': 0x8375,
            'JOYY': 0x8376,
            'JOYX': 0x8377,
            'RANDOM': 0x8378,
            'TIMER': 0x8379,
            'MOTION': 0x837a,
            'VDPSTT': 0x837b,
            'STATUS': 0x837c,
            'CB': 0x837d,
            'YPT': 0x837e,
            'XPT': 0x837f,
            'FAC': 0x834a,  # floating point arithmetic
            'ARG': 0x835c,
            'SGN': 0x8375,
            'EXP': 0x8376,
            'VSPTR': 0x836e,
            'FPERAD': 0x836c,
            'ERCODE': 0x8354,  # RAG assembler
            'VPAB': 0x8356,
            'VSTACK': 0x836e
        }
        self.ryte_data_defs = {
            'ACCTON': 0x0034,
            'ATN': 0x0032,
            'BADTON': 0x0036,
            'BITREV': 0x003B,
            'CFI': 0x0012,
            'CNS': 0x0014,
            'COS': 0x002c,
            'CSN': 0x0010,
            'DIVZER': 0x0001,
            'ERRIOV': 0x0003,
            'ERRLOG': 0x0006,
            'ERRNIP': 0x0005,
            'ERRSNN': 0x0002,
            'ERRSQR': 0x0004,
            'EXPF': 0x0028,
            'FADD': 0x0006,
            'FCOMP': 0x000a,
            'FDIV': 0x0009,
            'FMUL': 0x0008,
            'FSUB': 0x0007,
            'GETSPACE': 0x0038,
            'INT': 0x0022,
            'LINK': 0x0010,
            'LOCASE': 0x0018,
            'LOG': 0x002a,
            'MEMSIZ': 0x8370,
            'NAMLNK': 0x003d,
            'PAD': 0x8300,
            'PWR': 0x0024,
            'RETURN': 0x0012,
            'SADD': 0x000b,
            'SCOMP': 0x000f,
            'SDIV': 0x000e,
            'SIN': 0x002e,
            'SMUL': 0x000d,
            'SOUND': 0x8400,
            'SQR': 0x0026,
            'SSUB': 0x000c,
            'STCASE': 0x0016,
            'TAN': 0x0030,
            'TRIGER': 0x0007,
            'UPCASE': 0x004a,
            'WRNOV': 0x0001
        }
        if definitions:
            self.add_env(definitions)
        if ryte_symbols:
            self.definitions.update(self.ryte_data_defs)

    def reset(self):
        self.updated = False

    @staticmethod
    def valid(name):
        """is name a valid symbol name?"""
        return (name[:1].isalpha() or name[0] == '_') and not re.search(r'[-+*/&|^~()#"\']', name)

    def add_symbol(self, name, value, tracked=False, check=True, lino=None, filename=None):
        """add symbol to symbol table or update existing symbol"""
        curr_value, unused = self.symbols.get(name, (None, False))
        if self.pass_no == 0:
            if check and not Symbols.valid(name):
                raise AsmError(f'Invalid symbol name: {name}')
            if curr_value is not None:
                raise AsmError(f'Multiple symbols: {name}')
            self.symbols[name] = value, tracked or None
            self.symbol_def_location[name] = None if lino is None else (lino, filename)
        elif curr_value != value:
            self.symbols[name] = value, unused
            self.updated = True
        return name

    def add_label(self, label, tracked=False, check=True, lino=None, filename=None):
        """add label, in every pass to update its LC"""
        name = self.add_symbol(label, Address(self.LC), tracked=tracked, check=check, lino=lino, filename=filename)
        if (self.lidx, name) not in self.locations:
            self.locations.append((self.lidx, name))

    def add_local_label(self, label):
        """add local label, in every pass to update its LC"""
        self.add_label(label + '$' + str(self.lidx), check=False)

    def add_env(self, definitions):
        """add external symbol definitions (-D)"""
        for def_ in definitions:
            try:
                name, value_str = def_.split('=')
                value = Parser.external(value_str)
            except (ValueError, IndexError):
                name, value = def_, 1
            self.definitions[name.upper()] = value

    def get_symbol(self, name, required=False, for_pass_0=False, rc_pass_0=0):
        if self.pass_no == 0 and not for_pass_0:  # required in pass 0
            return rc_pass_0
        try:
            value, unused = self.symbols[name]
            if unused:
                self.symbols[name] = value, False
        except KeyError:
            value = self.definitions.get(name)
            if required and value is None:
                raise AsmError(f'Unknown symbol: {name}')
        return value

    def get_local(self, name, distance):
        if self.pass_no == 0:
            return 0
        targets = [(loc, sym) for (loc, sym) in self.locations if sym[:len(name) + 1] == name + '$']
        try:
            i, lidx = next((j, l) for j, (l, n) in enumerate(targets) if l >= self.lidx)
            if distance > 0 and lidx > self.lidx:
                distance -= 1  # i points to +! unless lidx == self.lidx
        except StopIteration:
            i = len(targets)  # beyond last label
        try:
            _, fullname = targets[i + distance]
        except IndexError:
            return None
        return self.get_symbol(fullname)

    def get_unused_symbols(self):
        """return all symbol names that have not been used"""
        unused_symbols = {}  # filename x symbols
        for symbol, (_, unused) in self.symbols.items():
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

    def is_symbol(self, name):
        return name in self.symbols or name in self.definitions

    def list(self, equ=False):
        """generate symbols"""
        symlist = []
        for symbol in sorted(self.symbols):
            if symbol[0] == '$' or symbol[0] == '_':
                continue  # skip local and internal symbols
            value, _ = self.symbols[symbol]
            symlist.append((symbol, Address.val(value)))
        fmt = '{}:\n       EQU  >{:04X}' if equ else '    {:.<20} >{:04X}'
        return '\n'.join(fmt.format(*symbol) for symbol in symlist)

    def clone(self):
        """internal method"""
        return {val: sym for val, (sym, _) in self.symbols.items()}

    def diff(self, syms1, syms2):
        """internal method"""
        print('*** ' + str(self.pass_no))
        for sym in syms1:
            val1 = Address.val(syms1[sym])
            val2 = Address.val(syms2[sym])
            if val1 != val2:
                print(f'{sym}: >{val1:X} -> >{val2:X}')


# Parser and Preprocessor

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
            raise AsmError('Unknown syntax style ' + style)

    xdt99 = SyntaxVariant(  # includes RAG and RyteData
        ga=r'(?:(@|\*|V@|V\*|G@)|(#|R@))([^(]+)(?:\(@?([^)]+)\))?$',
        gprefix='G@',
        moveops=r'([^,]+),\s*([^,]+),\s*([^,]+)$',
        tdelim="'",
        # regex replacements applied to escaped mnemonic and op fields
        repls=[
            (r'^HMOVE\b', 'HSTR'),  # renamed HMOVE -> HSTR
            (r'^ORG\b', 'AORG'),  # TI
            (r'^TITL\b', 'TITLE'),  # RYTE DATA
            (r'^HTEX\b', 'HTEXT'),
            (r'^VTEX\b', 'VTEXT'),
            (r'^HCHA\b', 'HCHAR'),
            (r'^VCHA\b', 'VCHAR'),
            (r'^SCRO\b', 'BIAS'),
            (r'^CARR\b', 'CARRY'),
            (r'&([01]+)', r':\1'),
            (r'^IDT\b', 'TITLE'),  # RAG
            (r'^IO\b', 'I/O'),
            (r'^IROW\b', 'ROW+'),
            (r'^ICOL\b', 'COL+')
            ]
        )

    mizapf = SyntaxVariant(
        ga=r'(?:([@*]|VDP[@*]|GR[OA]M@)|(VREG))([^(]+)(?:\(@?([^)]+)\))?$',
        gprefix='GROM@',
        moveops=r'(.+)\s+BYTES\s+FROM\s+(.+)\s+TO\s+(.+)$',
        tdelim='"',
        repls=[
            (r'^PRINTH\s+(.+)\sTIMES\s+(.+)\b', r'HCHAR \1,\2'),
            (r'^PRINTV\s+(.+)\sTIMES\s+(.+)\b', r'VCHAR \1,\2'),
            (r'^FOR\s+(.+)\sTIMES\s+DO\b', r'FOR \1'),
            (r'^PRINTH\b', r'HTEXT'),
            (r'^PRINTV\b', r'VTEXT'),
            (r'^DOWN\b', 'ROW+'),
            (r'^RIGHT\b', 'COL+'),
            (r'^END\b', 'FEND'),
            (r'^HMOVE\b', 'HSTR'),
            (r'^XGPL\b', 'BYTE')
            ]
        )


class Preprocessor:
    """xdt99-specific preprocessor extensions"""

    def __init__(self, parser):
        self.parser = parser
        self.parse = True
        self.parse_branches = []
        self.parse_else = False
        self.parse_macro = None
        self.parse_repeat = False  # parsing repeat section?
        self.repeat_count = 0  # number of repetitions
        self.macros = {'VERS': [f" text '{VERSION}'"]}  # macros defined (with predefined macros)

    def args(self, ops):
        lhs = self.parser.expression(ops[0], for_pass_0=True)
        rhs = self.parser.expression(ops[1], for_pass_0=True) if len(ops) > 1 else 0
        return lhs, rhs

    def DEFM(self, code, ops):
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

    def ENDM(self, code, ops):
        raise AsmError('Found .ENDM without .DEFM')

    def REPT(self, asm, ops):
        """repeat section n times"""
        self.repeat_count = self.parser.expression(ops[0], for_pass_0=True)
        self.parse_repeat = True
        self.parse_macro = '.rept'  # use lower case name as impossible macro name
        self.macros['.rept'] = []  # collect repeated section as '.rept' macro

    def ENDR(self, asm, ops):
        raise AsmError('Found .ENDR without .REPT')

    def IFDEF(self, code, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = code.symbols.is_symbol(ops[0]) if self.parse else None
        self.parse_else = False

    def IFNDEF(self, code, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = not code.symbols.is_symbol(ops[0]) if self.parse else None
        self.parse_else = False

    def IFEQ(self, code, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) == 0 if self.parse else None
        self.parse_else = False

    def IFNE(self, code, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) != 0 if self.parse else None
        self.parse_else = False

    def IFGT(self, code, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) > 0 if self.parse else None
        self.parse_else = False

    def IFGE(self, code, ops):
        self.parse_branches.append((self.parse, self.parse_else))
        self.parse = self.cmp(*self.args(ops)) >= 0 if self.parse else None
        self.parse_else = False

    def ELSE(self, code, ops):
        if not self.parse_branches or self.parse_else:
            raise AsmError("Misplaced .else")
        self.parse = not self.parse if self.parse is not None else None
        self.parse_else = True

    def ENDIF(self, code, ops):
        try:
            self.parse, self.parse_else = self.parse_branches.pop()
        except IndexError:
            raise AsmError('Misplaced .endif')

    def ERROR(self, code, ops):
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
            return re.sub(r'\$(\d+)', get_macro_text, text)
        except ValueError:
            return text

    def instantiate_line(self, line):
        # temporary kludge, breaks comments
        parts = re.split(r"('(?:[^']|'')*'|\'[^\']*\')", line)
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
        return False, None, None

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
        return False, None, None

    def process(self, asm, label, mnemonic, operands, line):
        """process preprocessor directive"""
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
            else:
                try:
                    fn = getattr(Preprocessor, name)
                except AttributeError:
                    raise AsmError('Invalid preprocessor directive')
                try:
                    fn(self, asm, operands)
                except (IndexError, ValueError):
                    raise AsmError('Syntax error')
            return False, None, None
        else:
            return self.parse, operands, line


class IntmLine:
    """intermediate source line"""

    OPEN = '$OPEN$'  # constants inserted into source to denote new or resumes source units
    RESUME = '$RESM$'

    def __init__(self, mnemonic, lino=0, lidx=0, label=None, operands=(), line=None, filename=None, path=None,
                 is_statement=False):
        self.label = label
        self.mnemonic = mnemonic
        self.operands = operands
        self.lino = lino
        self.lidx = lidx
        self.line = line
        self.filename = filename
        self.path = path
        self.is_statement = is_statement


class Parser:
    """scanner and parser class"""

    def __init__(self, symbols, console, syntax, path, includes=None, strict=False, relaxed=False):
        self.symbols = symbols
        self.console = console
        self.syntax = Syntax.get(syntax)
        self.path = self.initial_path = path  # current file path, used for includes
        self.includes = includes or []  # do not include '.'
        self.strict = strict
        self.relaxed = relaxed
        self.prep = Preprocessor(self)
        self.text_literals = []
        self.filename = None  # current file name
        self.source = None  # current source file in pass 0
        self.intermediate_source = []  # preprocessed GPL source file
        self.macro_args = []
        self.in_macro_instantiation = False
        self.lino = -1  # current line number
        self.srcline = None
        self.suspended_files = []
        self.fmt_mode = False  # parsing in FMT instruction?
        self.for_loops = []  # tracks open for loops

    def reset(self):
        """reset state for new assembly pass"""
        self.fmt_mode = False
        self.for_loops = []
        self.path = self.initial_path

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
            self.source = Util.readlines(newfile)
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
        if os.path.sep not in path:
            # foreign path
            foreign_sep = '\\' if os.path.sep == '/' else '/'
            return path.replace(foreign_sep, os.path.sep)
        else:
            # system path (does not recognize foreign path with \-escaped chars on Linux or regular / chars on Windows)
            return path

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
        include_path = self.includes + ([self.path] if self.path else [])  # self.path changes during assembly
        ti_name = re.match(r'(?:DSK\d|DSK\.[^.]+)\.(.*)', filename)
        if ti_name:
            native_name = ti_name.group(1)
            extensions = ['', '.g99', '.G99', '.gpl', '.GPL', '.g', '.G']
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

    def lines(self):
        """get next logical line from source files"""
        self.symbols.lidx = 0
        while self.source is not None:
            try:
                line = self.source[self.lino]
                self.srcline = line.rstrip()
                self.lino += 1
                self.symbols.lidx += 1
                yield self.lino, self.srcline, self.filename
            except IndexError:
                self.resume()

    def intermediate_lines(self):
        """return preprocessed source code"""
        for imline in self.intermediate_source:
            self.lino = imline.lino
            self.srcline = imline.line
            self.filename = imline.filename
            self.path = imline.path
            self.symbols.lidx = imline.lidx
            yield imline

    def line(self, line):
        """parse single source line"""
        if not line or line[0] == '*':
            return None, None, None, None, False
        if self.strict:
            if line.lstrip()[:1] == '*':
                return None, None, None, None, False
            label, *parts = re.split(r'\s+', self.escape(line))
            mnem, ops, *cparts = parts + ['', '']
            if ops == '*':
                # '*' followed by space is start of comment
                comment = ''.join([ops, *cparts])
                instrtext = mnem
            else:
                comment = ''.join(cparts)
                instrtext = (mnem + ' ' + ops) if ops else mnem
            # convert to native syntax
            for pat, repl in self.syntax.repls:
                instrtext = re.sub(pat, repl, instrtext)
            # analyze instruction
            mnemonic, *ops = re.split(r'\s+', instrtext)
            operands = ops[0].split(',') if ops else []
        else:
            instruction, *line_comment = self.escape(line).split(';', maxsplit=1)
            comment = line_comment[0] if line_comment else ''
            label, *remainder = re.split(r'\s+', instruction, maxsplit=1)
            instrtext = remainder[0] if remainder else ''
            # convert to native syntax
            for pat, repl in self.syntax.repls:
                instrtext = re.sub(pat, repl, instrtext)
            # analyze instruction
            mnemonic, *opsremainder = re.split(r'\s+', instrtext, maxsplit=1)
            opfield = opsremainder[0] if opsremainder else ''
            # operands
            if self.relaxed:
                operands = [op.strip() for op in opfield.split(',')] if opfield else []
            else:  # opfield may still contain non-delimited comments
                optext, *inl_comments = re.split(r' {2,}|\t', opfield, maxsplit=1)
                operands = [op.strip() for op in optext.split(',')] if optext else []
                comment = ' '.join(inl_comments) + comment
        return label, mnemonic, operands, comment, True

    def escape(self, text):
        """remove and save text literals from line"""
        parts = re.split(r"('(?:[^']|'')*'|\"[^\"]*\")", text)  # not-lit, lit, not-lit, lit, ...
        literals = [s[1:-1].replace(self.syntax.tdelim * 2, self.syntax.tdelim)
                    for s in parts[1::2]]  # unquote text delimiters
        parts[1::2] = ['{:s}{:d}{:s}'.format(self.syntax.tdelim, len(self.text_literals) + i, self.syntax.tdelim)
                       for i in range(len(literals))]
        self.text_literals.extend(literals)
        return ''.join(parts).upper()

    def restore(self, text):
        """restore escaped text literals"""
        return re.sub(r"'(\d+)'",
                      lambda m: self.syntax.tdelim + self.text_literals[int(m.group(1))] + self.syntax.tdelim,
                      text)

    def label(self, op):
        """parse label"""
        s = op[len(self.syntax.gprefix):] if op.startswith(self.syntax.gprefix) else op
        addr = self.expression(s)
        return Address.val(addr)

    def move(self, ops):
        """parse MOVE instruction: count, gs, gd"""
        m = re.match(self.syntax.moveops, ','.join(ops))
        if not m:
            raise AsmError('Syntax error in MOVE')
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
        if self.symbols.pass_no > 0 and count > max_count:
            raise AsmError(f'Count cannot exceed {max_count:d} here')
        return count

    def fmttext(self, ops):
        """parse FMT text"""
        ts = [self.text(op) for op in ops]
        if any(len(t) > 32 for t in ts):
            raise AsmError('Text length cannot exceed 32 characters')
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
            addr = m.group(1) or 'C'
            vram = addr[0] == 'V'
            grom = addr[0] == 'G'
            vreg = m.group(2) is not None
            indirect = addr[-1] == '*'
            value = self.expression(m.group(3))
            index = self.expression(m.group(4)) if m.group(4) else None
            if index is not None and 0x00 <= index <= 0xff:
                index += 0x8300
            elif self.symbols.pass_no > 0 and index is not None and not 0x8300 <= index <= 0x83ff:
                raise AsmError(f'Index out of range: >{index:04X}')
            if vreg and not (is_move and not is_gs):
                raise AsmError('Invalid VDP register outside MOVE')
            if self.symbols.pass_no > 0 and vreg and not 0 <= value <= 7:
                raise AsmError(f'VDP register out of range: {value:d}')
            if grom and not is_move:
                raise AsmError('Invalid GROM address outside MOVE')
            if plain_only and (grom or vram or vreg or indirect or index):
                raise AsmError("Invalid address format, only '@>xxxx' allowed here")
            return Operand(value, vram=vram, grom=grom, vreg=vreg, indirect=indirect, index=index)
        if is_gs:
            # immediate value as address
            if is_move:
                self.console.warn(f"Treating '{op:s}' as ROM address, did you intend a GROM address?")
            value = self.expression(op)
            return Operand(value, imm=2 if is_d else 1)
        raise AsmError('Invalid G{:s} address operand: {:s}'.format('s' if is_gs else 'd', op))

    def expression(self, expr, for_pass_0=False):
        """parse complex arithmetical expression"""
        value = Word(0, pass_no=self.symbols.pass_no)
        stack = []
        terms = ['+'] + [tok.strip() for tok in re.split(r'([-+~&|^()]|\*\*?|//?|%%?|<<|>>)', expr)]
        self.check_arith_precedence(terms)
        i = 0
        while i < len(terms):
            op, term = terms[i:i + 2]
            i += 2
            negate = False
            corr = 0
            if op == ')':
                v = value.value
                value, op, negate, corr = stack.pop()
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
                        stack.append((value, op, negate, corr))
                        op, term, negate, corr = '+', terms[i + 1], False, 0
                        value = Word(0)
                    i += 2
                term_val = self.term(term, for_pass_0)
                if isinstance(term_val, Local):
                    dist = -term_val.distance if negate else term_val.distance
                    term_val = self.symbols.get_local(term_val.name, dist)
                    negate = False
                if term_val is None:
                    raise AsmError('Invalid expression: ' + term)
                v = Address.val(term_val)
            v = (-v if negate else v) + corr
            w = Word(v)
            if op == '+':
                value.add(w)
            elif op == '-':
                value.sub(w)
            elif op in '*/%':
                value.mul(op, w)
            elif op in '&|^':
                value.bit(op, w)
            elif op == '**':
                base, exp = Word(1), w.value
                for j in range(exp):
                    base.mul('*', value)
                value = base
            elif op == '//' or op == '%%':
                value.udiv(op, v)
            elif op == '<<' or op == '>>':
                value.shift(op, v)
            else:
                raise AsmError('Invalid operator: ' + op)
        return value.value

    def byte_expression(self, expr, for_pass_0=False):
        """parse complex arithmetical expression yield byte value"""
        value = self.expression(expr, for_pass_0=for_pass_0)
        return value & 0xff

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
                self.console.warn('Expression with non-standard evaluation')
                return True, None
            elif op == '(':
                violation, i = self.check_arith_precedence(operators, i + 2)
                if violation:
                    return True, None
                else:
                    possible_sign = False  # no sign after ')'
                    continue
            elif op in '&|^~':
                possible_violation = False
            i += 2
            possible_sign = True
        return False, None

    def term(self, op, for_pass_0=False):
        """parse term"""
        if op[0] == '>':
            return int(op[1:], 16)
        elif op[0] == ':':
            return int(op[1:], 2)
        elif op.isdigit():
            return int(op)
        elif op == '$':
            return Address(self.symbols.LC)
        elif op[0] == '!':
            m = re.match('(!+)(.*)', op)
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
                raise AsmError('Invalid text literal: ' + c)
        else:
            v = self.symbols.get_symbol(op, required=True, for_pass_0=for_pass_0)
            return v

    def value(self, op):
        """parse well-defined value"""
        e = self.expression(op)
        return Address.val(e)

    def text(self, op):
        """parse quoted text literal or byte string"""
        try:
            if op[0] == '>':
                op0 = op + '0'
                return ''.join(chr(int(op0[i:i + 2], 16))
                               for i in range(1, len(op), 2))
            elif op[0] == op[-1] == self.syntax.tdelim:
                return self.text_literals[int(op[1:-1])]
        except (IndexError, ValueError):
            pass
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
            bytes_[0] = ~bytes_[0] & 0xff
        # return radix-100 format
        return bytes_

    def get_filename(self, op):
        """parse double-quoted filename"""
        if len(op) < 3:
            raise AsmError('Invalid filename: ' + op)
        if op[0] == op[-1] == self.syntax.tdelim:
            return self.text_literals[int(op[1:-1])]
        return op[1:-1]

    @staticmethod
    def external(op):
        """parse symbol constant (-D option)"""
        try:
            return int(op[1:], 16) if op[0] == '>' else int(op)
        except ValueError:
            return op


class Operand:
    """general source or destination address or imm value"""

    def __init__(self, addr, vram=False, grom=False, vreg=False, imm=0, indirect=False, index=None):
        self.addr = addr
        self.vram = vram
        self.grom = grom  # implies not indirect
        self.vreg = vreg
        self.immediate = imm  # byte size, or zero
        self.indirect = indirect
        self.index = index
        self.bytes = self.generate()
        assert not any(isinstance(b, Address) for b in self.bytes)
        self.size = len(self.bytes)

    def __eq__(self, other):
        return (isinstance(other, Operand) and
                self.addr == other.addr and self.vram == other.vram and
                self.grom == other.grom and self.vreg == other.vreg and
                self.immediate == other.immediate and
                self.indirect == other.indirect and
                self.index == other.index)

    def __ne__(self, other):
        return not self == other

    def generate(self):
        """generate byte list for operand"""
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


# Code generation

class Program:
    """code and related properties, including externals
       NOTE: A program consists of multiple program units,
             a program unit consists of multiple segments.
    """

    def __init__(self):
        self.segments = []
        self.title = None
        self.entry = None  # start address of program

    def __iter__(self):
        return iter(self.segments)

    def reset(self):
        """reset state"""
        self.segments = []


class Segment:
    """stores the code of an xORG segment with meta information,
       also represents the top level unit of all generated code
    """

    def __init__(self, grom, offset, code):
        self.grom = grom
        self.offset = offset
        self.code = code  # {LC: word}


class Assembler:
    """generate GPL virtual machine code"""

    def __init__(self, syntax, grom, aorg, target, path, includes=None, definitions=(), strict=False, relaxed=False,
                 ryte_symbols=False, debug=False, console=None):
        self.syntax = syntax
        self.includes = includes
        self.grom = grom
        self.offset = aorg
        self.strict = strict
        self.relaxed = relaxed
        self.debug_passes = debug
        self.target = target
        self.program = Program()
        self.symbols = Symbols(definitions, ryte_symbols=ryte_symbols)
        self.console = console or Xga99Console()
        self.parser = Parser(self.symbols, self.console, syntax=self.syntax, strict=strict, relaxed=relaxed,
                             path=path, includes=self.includes)
        self.console.set_parser(self.parser)
        self.listing = Listing()
        self.segment = None
        self.code = None

    def assemble(self, source_name):
        self.symbols.add_symbol('_XGA99_' + self.target, 1)
        self.pass_0(source_name)
        if self.console.errors:
            return  # abort if errors in pass 0
        self.pass_n()
        self.finalize()

    def pass_0(self, source_name):
        """initial pass of assembly scanning symbols"""
        self.symbols.pass_no = 0
        self.org(self.grom, self.offset)
        self.parser.open(filename=source_name)
        prev_label = None
        for lino, line, filename in self.parser.lines():
            try:
                # break line into fields
                label, mnemonic, operands, comment, is_statement = self.parser.line(line)
                keep, operands, line = self.parser.prep.process(self, label, mnemonic, operands, line)
                if not keep:
                    continue
                intm_line = IntmLine(mnemonic, lino=lino, lidx=self.symbols.lidx, label=label, operands=operands,
                                     line=line, filename=filename, path=self.parser.path, is_statement=is_statement)
                self.parser.intermediate_source.append(intm_line)  # store pre-processed line for subsequent passes
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
                # process directives only
                Directives.process(self, label, mnemonic, operands) or \
                    Opcodes.process(self, label, mnemonic, operands)
            except AsmError as e:
                self.console.error(str(e))
        if self.parser.prep.parse_branches:
            self.console.error('Missing .ENDIF', nopos=True)
        if self.parser.prep.parse_repeat:
            self.console.error('Missing .ENDR', nopos=True)
        elif self.parser.prep.parse_macro:
            self.console.error('Missing .ENDM', nopos=True)

    def pass_n(self):
        """subsequent passes generating GPL virtual machine code"""
        syms_before = self.symbols.clone() if self.debug_passes else None
        while True:
            self.program.reset()  # reset state
            self.symbols.reset()
            self.parser.reset()
            self.listing.reset()
            self.segment = None
            self.org(self.grom, self.offset)
            prev_label = None
            abort = False
            self.symbols.pass_no += 1
            if self.symbols.pass_no > 32:
                sys.exit(self.console.colstr('Too many assembly passes, aborting :-('))
            for imline in self.parser.intermediate_lines():
                try:
                    if imline.mnemonic == IntmLine.OPEN:  # markers to indicate start ...
                        self.listing.open(self.symbols.LC, imline.filename)
                        continue
                    elif imline.mnemonic == IntmLine.RESUME:  # ... and end of include file or macro
                        self.listing.resume(self.symbols.LC, imline.filename)
                        continue
                    self.listing.prepare(self.symbols.LC, Line(lino=imline.lino, line=imline.line))
                    if not imline.is_statement:
                        continue
                    # NOTE: Unlike xas99, we need to keep the complete label login in pass_n, since labels are
                    #       re-evaluated for each pass.  This also applies to EQUs, which always need labels.
                    label = imline.label  # create copy to not change intermediate source
                    if prev_label:
                        if label:
                            prev_label = None
                            raise AsmError('Invalid continuation for label')
                        label, prev_label = prev_label, None
                    elif label[-1:] == ':' and not imline.mnemonic:
                        prev_label = label
                        continue
                    if label[-1:] == ':':
                        label = label[:-1]
                    # process directives and opcodes
                    Directives.process(self, label, imline.mnemonic, imline.operands) or \
                        Opcodes.process(self, label, imline.mnemonic, imline.operands)
                except AsmError as e:
                    self.console.error(str(e))
                    abort = True
            if self.parser.fmt_mode:
                self.console.warn('Source ends with open FMT block', nopos=True, force=True)
            if self.debug_passes:
                syms_after = self.symbols.clone()
                self.symbols.diff(syms_before, syms_after)
                syms_before = syms_after
            if abort or not self.symbols.updated:
                break

    def process_label(self, label, tracked=False):
        if not label:
            return
        if label[0] == '!':
            self.symbols.add_local_label(label[1:])
        else:
            self.symbols.add_label(label, tracked=tracked, lino=self.parser.lino, filename=self.parser.filename)

    def org(self, grom, offset):
        """create new code segment"""
        if self.segment:
            self.segment.LC = self.symbols.LC  # update final LC
        self.grom = grom
        self.offset = offset
        self.symbols.LC = grom + offset
        self.code = {}
        self.segment = Segment(grom, offset, self.code)
        self.program.segments.append(self.segment)

    def emit(self, *bytes_):
        """generate byte code"""
        for i, byte_ in enumerate(bytes_):
            self.code[self.symbols.LC] = byte_
            self.listing.add(text1=self.symbols.LC, text2=byte_)
            self.symbols.LC += (byte_.size if isinstance(byte_, Operand) else
                                byte_.size if isinstance(byte_, Address) else
                                0 if byte_ is None else 1)

    def finalize(self):
        """wrap-up code generation"""
        if self.segment:
            self.segment.LC = self.symbols.LC
        for fn, symbols in self.symbols.get_unused_symbols().items():
            symbols_text = ', '.join(symbols)
            self.console.warn('Unused constants: ' + (symbols_text.upper() if self.strict else symbols_text.lower()),
                              filename=fn, nopos=True, force=True)

    @staticmethod
    def get_target(cart, text):
        """return target format string"""
        if cart:
            return 'CART'
        if text:
            return 'TEXT'
        return 'GBC'


class Linker:
    """generate byte code"""

    def __init__(self, program, symbols, console):
        self.program = program
        self.symbols = symbols
        self.console = console

    def fill_memory(self):
        """load segments into memory"""
        memories = {}
        # put bytes into memory
        for segment in self.program:
            memory = memories.setdefault(segment.grom >> 13, {})  # use GROM ids 0 .. 7
            for LC, byte_ in segment.code.items():
                if isinstance(byte_, Address):
                    if byte_.local:
                        memory[LC - 1] |= (byte_.addr >> 8) & 0x1f  # path prev opcode
                        memory[LC] = byte_.addr & 0xff
                    else:
                        memory[LC] = byte_.addr >> 8
                        memory[LC + 1] = byte_.addr & 0xff
                elif isinstance(byte_, Operand):
                    for i, b in enumerate(byte_.bytes):
                        assert 0 <= b < 256
                        memory[LC + i] = b
                else:
                    assert 0 <= byte_ < 256
                    memory[LC] = byte_
        return memories

    def generate_byte_code(self, split_groms=False, padded_groms=False, aligned=False):
        """generate GPL byte code for each GROM
           split GROMs: one file per GROM
           full GROMs: every GROM starts at N * >2000
        """
        binaries = []
        memories = self.fill_memory()
        for grom, memory in memories.items():
            if not memory:
                continue
            min_addr = min(memory.keys())
            max_addr = max(memory.keys()) + 1
            binary = bytes(memory.get(addr, 0) for addr in range(min_addr, max_addr))
            if padded_groms:
                binary = bytes(min_addr % 0x2000) + binary + bytes(-max_addr % 0x2000)
                min_addr = Util.trunc(min_addr, 0x2000)
                max_addr = min_addr + 0x2000
            binaries.append(ByteCode(grom, min_addr, max_addr, binary))
        if split_groms:
            return binaries
        binaries.sort()
        all_min_addr = binaries[0].min_addr
        all_max_addr = binaries[-1].max_addr  # inclusive
        min_grom = binaries[0].grom
        if aligned:
            all_min_addr = Util.trunc(all_min_addr, 0x2000)
        chunks = []
        last_addr = all_min_addr
        for binary in binaries:
            chunks.append(bytes(binary.min_addr - last_addr))
            chunks.append(binary.byte_code)
            last_addr = binary.max_addr
        joined_binary = b''.join(chunks)
        return ByteCode(min_grom, all_min_addr, all_max_addr, joined_binary),

    def generate_gpl_header(self, base_addr, name):
        """generate GPL header"""
        entry = self.program.entry or self.symbols.get_symbol('START') or base_addr + 0x30
        gpl_header = bytes((0xaa, 1, 0, 0, 0, 0)) + Util.chrw(base_addr + 0x10) + bytes(8)
        try:
            menu_name = name[:0x15].encode('ascii')
        except UnicodeEncodeError:
            raise AsmError('Cart name contains non-ASCII chars')
        menu = bytes(2) + Util.chrw(Address.val(entry)) + bytes((len(menu_name),)) + menu_name
        padding = bytes(0x30 - len(gpl_header) - len(menu))
        return gpl_header + menu + padding

    def generate_cart(self, name):
        """generate RPK file for use as MAME cartridge"""
        layout = f"""<?xml version='1.0' encoding='utf-8'?>
                    <romset version='1.0'>
                        <resources>
                            <rom id='gromimage' file='{name}.bin'/>
                        </resources>
                        <configuration>
                            <pcb type='standard'>
                                <socket id='grom_socket' uses='gromimage'/>
                            </pcb>
                        </configuration>
                    </romset>"""
        metainf = f"""<?xml version='1.0'?>
                     <meta-inf>
                         <name>{name}</name>
                     </meta-inf>"""
        byte_code, = self.generate_byte_code(aligned=True)
        # check all n * >2000 addresses in byte code for >AA header
        # byte_code.min_addr is multiple of >2000
        if all(byte_code.byte_code[base - byte_code.min_addr] != 0xaa
               for base in range(byte_code.min_addr, byte_code.max_addr + 1, 0x2000)):
            # generate GPL header if GROM addr does not exist or is not >AA
            if any(b for b in byte_code.byte_code[:0x30]):
                self.console.warn('Generated GPL header overwrites non-zero data')
            header = self.generate_gpl_header(byte_code.min_addr, name)
            data = header + byte_code.byte_code[0x30:]
        else:
            data = byte_code.byte_code
        # MESS RPK format only supports GROM start addr >6000 right now, so pad if necessary
        if byte_code.min_addr < 0x6000:
            raise AsmError('MESS carts only support GROMs 3 and higher')
        pad = bytes(byte_code.min_addr - 0x6000)
        return pad + data, layout, metainf

    def generate_text(self, mode, split_groms=True):
        """convert binary data into text representation"""
        if 'r' in mode:
            word = lambda i: Util.ordw(binary.byte_code[i + 1:((i - 1) if i > 0 else None):-1])  # byte-swapped
        else:
            word = lambda i: Util.ordw(binary.byte_code[i:i + 2])
        if '4' in mode:
            value_fmt = '{:s}{:04x}'
        else:
            value_fmt = '{:s}{:02x}'
        val = lambda x: x  # use value as-is
        if 'a' in mode:  # assembly
            hex_prefix = '>'
            data_prefix = '       {} '.format('byte' if '2' in mode else 'data')
            suffix = '\n'
        elif 'b' in mode:  # BASIC
            hex_prefix = ''
            data_prefix = 'DATA '
            suffix = '\n'
            value_fmt = '{:s}{:d}'
            val = lambda x: x - 0x10000 if x > 32767 else x  # hex to dec
        elif 'c' in mode:  # C
            hex_prefix = '0x'
            data_prefix = '  '
            suffix = ',\n'
        else:
            raise AsmError('Bad text format: ' + mode)

        result = []
        byte_code = self.generate_byte_code(split_groms=True)
        for binary in byte_code:
            text = ''
            if 'a' in mode:
                text += f';      grom >%{binary.grom:04x}\n'
            if '4' in mode:  # words
                if len(binary.byte_code) % 2:
                    binary.byte_code += bytes(1)  # pad to even length
                ws = [value_fmt.format(hex_prefix, val(word(i))) for i in range(0, len(binary.byte_code), 2)]
                lines = [data_prefix + ', '.join(ws[i:i + 4]) + suffix
                         for i in range(0, len(ws), 4)]
            else:  # bytes (default)
                bs = [value_fmt.format(hex_prefix, binary.byte_code[i]) for i in range(0, len(binary.byte_code))]
                lines = [data_prefix + ', '.join(bs[i:i + 8]) + suffix
                         for i in range(0, len(bs), 8)]
            text += ''.join(lines)
            result.append((binary.grom, text))
        if split_groms:
            return result
        return (None, '\n'.join(text for grom, text in result)),


class ByteCode:
    """stores result of GPL assembly"""

    def __init__(self, grom, min_addr, max_addr, data):
        self.grom = grom
        self.min_addr = min_addr
        self.max_addr = max_addr
        self.byte_code = data

    def __lt__(self, other):
        return self.grom < other.grom

    @staticmethod
    def suffix(grom):
        """return file suffix from grom"""
        return '_g' + str(grom) if grom else ''


class Word:
    """auxiliary class for word arithmetic"""

    def __init__(self, value, pass_no=None):
        self.value = value & 0xffff
        self.pass_no = pass_no

    def sign(self):
        return -1 if self.value & 0x8000 else +1

    def abs(self):
        return -self.value % 0x10000 if self.value & 0x8000 else self.value

    def add(self, arg):
        self.value = (self.value + arg.value) & 0xffff

    def sub(self, arg):
        self.value = (self.value - arg.value) & 0xffff

    def mul(self, op, arg):
        if op in '/%' and arg.value == 0:
            if self.pass_no == 0:
                return 0  # temporary value
            else:
                raise AsmError('Division by zero')
        sign = arg.sign() if op == '%' else self.sign() * arg.sign()
        val = (self.abs() * arg.abs() if op == '*' else
               self.abs() // arg.abs() if op == '/' else
               self.abs() % arg.abs() if op == '%' else None)
        self.value = (val if sign > 0 else -val) & 0xffff

    def udiv(self, op, arg):
        if arg == 0:
            if self.pass_no == 0:
                return 0  # temporary value
            else:
                raise AsmError('Division by zero')
        if op == '%%':
            self.value %= arg
        else:
            self.value //= arg

    def bit(self, op, arg):
        val = (self.value & arg.value if op == '&' else
               self.value | arg.value if op == '|' else
               self.value ^ arg.value if op == '^' else None)
        self.value = val & 0xffff

    def shift(self, op, arg):
        if arg < 0:
            AsmError('Cannot shift by negative values')
        if op == '>>':
            self.value >>= arg
        else:
            self.value = (self.value << arg) & 0xffff


# Console and Listing

class Xga99Console(Console):
    """collects errors and warnings"""

    def __init__(self, warnings=None, colors=None):
        self.parser = None
        super().__init__('xga99', VERSION, warnings or {}, colors=colors)

    def set_parser(self, parser):
        self.parser = parser  # assembler or linker

    def warn(self, message, filename=None, nopos=False, force=False):
        """record warnings only for pass 1 to avoid duplicates"""
        if self.parser.symbols.pass_no != 1 and not force:
            return
        pass_no = None if force else self.parser.symbols.pass_no
        if nopos:
            info, message = self._format(message, pass_no, filename, None, None)
        else:
            info, message = self._format(message, pass_no, filename or self.parser.filename, self.parser.lino,
                                         self.parser.srcline)
        super().warn(info, message)

    def error(self, message, nopos=False):
        """record errors for all passes"""
        if nopos:
            info, message = self._format(message, self.parser.symbols.pass_no, None, None, None, error=True)
        else:
            info, message = self._format(message, self.parser.symbols.pass_no, self.parser.filename,
                                         self.parser.lino, self.parser.srcline, error=True)
        super().error(info, message)

    def _format(self, message, pass_no, filename, lino, line, error=False):
        """print all console messages to stderr"""
        text = 'Error' if error else 'Warning'
        s_filename = filename or '***'
        s_pass = str(pass_no) if pass_no is not None else '*'
        s_lino = f'{lino:04d}' if lino is not None else '****'
        s_line = line or ''
        return f'> {s_filename} <{s_pass}> {s_lino} - {s_line}', f'***** {text:s}: {message}'


class Listing:
    """listing file"""

    def __init__(self):
        self.listing = []
        self.prepared_line = None

    def reset(self):
        """reset listing for next pass"""
        self.listing = []
        self.prepared_line = None

    def open(self, LC, filename):
        """add new source unit to listing"""
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

    def add(self, text1=None, text2=None):
        """add single line"""
        if not self.prepared_line:
            self.prepared_line = Line()
        if text1 is not None:
            self.prepared_line.text1 = text1
        if text2 is not None:
            self.prepared_line.text2 = text2
        self.listing.append(self.prepared_line)
        self.prepared_line = None

    def list(self):
        """generate listing"""
        self.prepare(0, Line())
        listing = []
        prev_line = None
        for line in self.listing:
            t_lino = '' if line.lino is None else f'{line.lino:04d}'
            t_addr = self.format_text(line.text1)
            extra_bytes = ()
            byte_ = line.text2
            if isinstance(byte_, Address):
                t_byte, *extra_bytes = byte_.hex()
                if byte_.local:
                    listing[-1] = (listing[-1][:10] +
                                   '{:02X}'.format(prev_line.text2 | int(t_byte, 16)) +
                                  listing[-1][12:])  # patch previous byte with first operand byte
                    t_byte, extra_bytes = extra_bytes[0], ()
            elif isinstance(byte_, Operand):
                t_byte, *extra_bytes = [f'{b:02X}' for b in byte_.bytes]
            elif isinstance(byte_, int):
                t_byte = f'{byte_:02X}'
            elif isinstance(byte_, str):
                t_byte = byte_
            else:
                t_addr = t_byte = ''
            listing.append('{:4s} {:4s} {:2s}  {:s}'.format(t_lino, t_addr, t_byte, line.line or ''))
            for i, byte_ in enumerate(extra_bytes):
                listing.append('     {:4s} {:2s}'.format(self.format_text(line.text1, i + 1), byte_))
            prev_line = line
        return 'XGA99 CROSS-ASSEMBLER   VERSION ' + VERSION + '\n' + '\n'.join(listing) + '\n'

    @staticmethod
    def format_text(text, delta=0):
        """format hex addr, text, or None uniformly"""
        return ('' if text is None else
                text if isinstance(text, str) else
                f'{text + delta:04X}')


class Line:
    """source code line"""

    def __init__(self, lino=None, line=None, text1=None, text2=None, end_of_source=False):
        self.lino = lino
        self.line = line
        self.text1 = text1
        self.text2 = text2
        self.end_of_source = end_of_source
        self.text1 = self.text2 = None


# Command line processing

class Xga99Processor(CommandProcessor):
    """process command line"""

    def __init__(self):
        super().__init__(AsmError)
        self.asm = None
        self.linker = None

    def parse(self):
        """syntax and parsing"""
        args = argparse.ArgumentParser(description='GPL cross-assembler, v' + VERSION)
        args.add_argument('source', metavar='<source>', help='GPL source code')
        cmd = args.add_mutually_exclusive_group()
        cmd.add_argument('-c', '--cart', action='store_true', dest='cart',
                         help='create MAME cartridge image with auto GPL header')
        cmd.add_argument('-t', '--text', dest='text', nargs='?', metavar='<format>',
                         help='create text file with binary values')
        args.add_argument('-s', '--strict', action='store_true', dest='strict',
                          help='use strict syntax, disable xga99 extensions')
        args.add_argument('-n', '--name', dest='name', metavar='<name>',
                          help='set program name')
        args.add_argument('-B', '--fully-padded', action='store_true', dest='pad',
                          help='pad GROMs to size of >2000 bytes')
        args.add_argument('-G', '--grom', dest='grom', metavar='<GROM>',
                          help='set GROM base address')
        args.add_argument('-A', '--aorg', dest='aorg', metavar='<origin>',
                          help='set AORG offset in GROM for byte code')
        args.add_argument('-y', '--syntax', dest='syntax', default='xdt99', metavar='<style>',
                          help='set syntax style (xdt99, rag, mizapf)')
        args.add_argument('-r', '--relaxed', action='store_true', dest='relaxed',
                          help='relaxed syntax mode with extra whitespace and explicit comments')
        args.add_argument('-I', '--include', dest='inclpath', nargs='+', metavar='<path>',
                          help='listing of include search paths')
        args.add_argument('-D', '--define-symbol', dest='defs', nargs='+', metavar='<sym[=val]>',
                          help='add symbol to symbol table')
        args.add_argument('-g', '--split-groms', action='store_true', dest='splitgroms',
                          help='put each GROM into separate file')
        args.add_argument('-L', '--listing', dest='listing', metavar='<file>',
                          help='generate listing file')
        args.add_argument('-S', '--symbol-table', action='store_true', dest='symtab',
                          help='add symbol table to listing file')
        args.add_argument('-E', '--symbol-file', dest='equs', metavar='<file>',
                          help='put symbols in EQU file')
        args.add_argument('-R', '--ryte-data-symbols', action='store_true', dest='rytesyms',
                          help='add Ryte Data symbols')
        args.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                          help='quiet; do not show warnings')
        args.add_argument('--color', action='store', dest='color', choices=['off', 'on'],
                          help='enable or disable color output')
        args.add_argument('--debug-passes', action='store_true', dest='debug',
                          help=argparse.SUPPRESS)
        args.add_argument('-o', '--output', dest='output', metavar='<file>',
                          help='set output file name')
        try:
            default_opts = os.environ[CONFIG].split()
        except KeyError:
            default_opts = []
        self.opts = args.parse_args(args=default_opts + sys.argv[1:])  # passed opts override default opts
        # restore source files parsed as list option
        self.fix_greedy_list_parsing('sources', 'inclpath', 'defs')

    def run(self):
        # setup
        dirname = os.path.dirname(self.opts.source) or '.'
        basename = os.path.basename(self.opts.source)
        self.barename = os.path.splitext(basename)[0]
        self.name = self.opts.name or self.barename[:16].upper()
        grom = Util.xint(self.opts.grom) if self.opts.grom is not None else 0x6000 if self.opts.cart else 0x0000
        aorg = Util.xint(self.opts.aorg) if self.opts.aorg is not None else 0x0000
        root = os.path.dirname(os.path.realpath(__file__))  # installation dir (path to xga99)
        includes = [os.path.join(root, 'lib')] + Util.get_opts_list(self.opts.inclpath)
        target = Assembler.get_target(self.opts.cart, self.opts.text)

        warnings = Warnings({Warnings.DEFAULT: not self.opts.quiet})
        self.console = Xga99Console(warnings, colors=self.opts.color)

        # assembly
        self.asm = Assembler(syntax=self.opts.syntax,
                             grom=grom,
                             aorg=aorg,
                             target=target,
                             path=dirname,
                             includes=includes,
                             definitions=Util.get_opts_list(self.opts.defs),
                             strict=self.opts.strict,
                             relaxed=self.opts.relaxed,
                             ryte_symbols=self.opts.rytesyms,
                             debug=self.opts.debug,
                             console=self.console)
        self.asm.assemble(basename)
        if self.console.errors:
            return True  # abort
        self.linker = Linker(self.asm.program, self.asm.symbols, self.console)

    def prepare(self):
        if self.opts.cart:
            self.cart()
        elif self.opts.text:
            self.text()
        else:
            self.byte_code()
        if self.opts.listing:
            self.listing()
        if self.opts.equs:
            self.equs()

    def cart(self):
        """generate cart archive"""
        data, layout, metainf = self.linker.generate_cart(self.name)
        try:
            with zipfile.ZipFile(Util.outname(self.barename, '.rpk', output=self.opts.output), 'w') as archive:
                archive.writestr(self.name + '.bin', data)
                archive.writestr('layout.xml', layout)
                archive.writestr('meta-inf.xml', metainf)
        except IOError as e:
            sys.exit(f'File error: {e.filename}: {e.strerror}.')
        return []

    def text(self):
        """generate text file"""
        binaries = self.linker.generate_text(self.opts.text.lower(), split_groms=self.opts.splitgroms)
        for grom, data in binaries:
            self.result.append(RFile(data, self.barename, '.dat', suffix=ByteCode.suffix(grom), istext=True))

    def byte_code(self):
        """generate byte code"""
        for binary in self.linker.generate_byte_code(split_groms=self.opts.splitgroms, padded_groms=self.opts.pad):
            suffix = ByteCode.suffix(binary.grom) if self.opts.splitgroms else ''
            self.result.append(RFile(binary.byte_code, self.barename, '.gbc', suffix=suffix))

    def listing(self):
        """generate listing"""
        listing = self.asm.listing.list() + (self.asm.symbols.list() if self.opts.symtab else '')
        self.result.append(RFile(listing, self.barename, '.lst', output=self.opts.listing, istext=True))

    def equs(self):
        """generate equs"""
        equs = self.asm.symbols.list(equ=True)
        self.result.append(RFile(equs, self.barename, '.equ', output=self.opts.equs, istext=True))


if __name__ == '__main__':
    status = Xga99Processor().main()
    sys.exit(status)
