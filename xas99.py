#!/usr/bin/env python

# xas99: A TMS9900 cross-assembler
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
import re
import os.path

VERSION = "1.8.2"


# Utility functions

def ordw(word):
    """word ord"""
    return ord(word[0]) << 8 | ord(word[1])


def chrw(word):
    """word chr"""
    return chr(word >> 8) + chr(word & 0xFF)


def pad(n, m):
    """return increment to next multiple of m"""
    return -n % m


def used(n, m):
    """integer division rounding up"""
    return (n + m - 1) / m


def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip(">"), 16 if s[:2] == "0x" or s[:1] == ">" else 10)


def sinc(s, i):
    """string sequence increment"""
    return s[:-1] + chr(ord(s[-1]) + i)


def writedata(n, d, m="wb"):
    """write data to file or STDOUT"""
    if n == "-":
        sys.stdout.write(d)
    else:
        with open(n, m) as f:
            f.write(d)


def readlines(n, m="r"):
    """read lines from file or STDIN"""
    if n == "-":
        return sys.stdin.readlines()
    else:
        with open(n, m) as f:
            return f.readlines()


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


class BuildError(Exception):
    pass


# Symbol table

class Address:
    """absolute or relocatable address"""

    def __init__(self, addr, bank=None, relocatable=False):
        self.addr = addr
        self.bank = bank
        self.relocatable = relocatable

    def hex(self):
        return "%04X%c" % (self.addr, "r" if self.relocatable else " ")


class DelayedAddress:

    def __init__(self, name, size, value):
        self.name = name
        self.size = size
        self.value = value
        self.addr = 0

    def patch(self, addr):
        self.addr = addr


class Reference:
    """external reference"""

    def __init__(self, name):
        self.name = name


class Local:
    """local label reference"""

    def __init__(self, name, distance):
        self.name = name
        self.distance = distance


class Block:
    """reserved block of bytes"""

    def __init__(self, size):
        self.size = size


class Line:
    """source code line"""

    def __init__(self, lino, line, eos=False):
        self.lino = lino
        self.line = line
        self.eos = eos
        self.text1 = self.text2 = None


class Symbols:
    """symbol table and line counter
       Each symbol entry is a tuple (value, weak, used)
       Weak symbols may be redefined if they have the same value.
       Used tracks if a symbol has been used (True/False).  If set to None, usage is not tracked.
    """

    def __init__(self, add_registers=False, add_defs=()):
        self.registers = {"R" + str(i): i for i in xrange(16)} if add_registers else {}
        self.symbols = {n: (v, False, None) for n, v in self.registers.iteritems()}  # registers are just non-weak symbols
        self.exts = {
            "VSBW": 0x210C, "VMBW": 0x2110, "VSBR": 0x2114, "VMBR": 0x2118,
            "VWTR": 0x211C, "KSCAN": 0x2108, "GPLLNK": 0x2100, "XMLLNK": 0x2104,
            "DSRLNK": 0x2120, "LOADER": 0x2124, "UTLTAB": 0x2022, "SCAN": 0x000E,
            "PAD": 0x8300, "GPLWS": 0x83E0, "SOUND": 0x8400,
            "VDPRD": 0x8800, "VDPSTA": 0x8802, "VDPWD": 0x8C00, "VDPWA": 0x8C02,
            "SPCHRD": 0x9000, "SPCHWT": 0x9400, "GRMRD": 0x9800, "GRMRA": 0x9802,
            "GRMWD": 0x9C00, "GRMWA": 0x9C02
            }
        for defs in add_defs:
            for d in defs.upper().split(","):
                parts = d.split("=")
                val = Parser.symconst(parts[1]) if len(parts) > 1 else 1
                self.symbols[parts[0]] = val, True, None  # predefined symbols are weak
        self.autogens = []  # unique list of auto-generated constants
        self.refdefs = []
        self.xops = {}
        self.idt = "        "
        self.locations = []
        self.local_lid = 0
        self.reset_LC()

    def reset_LC(self):
        self.LC = 0
        self.wp = 0x83e0
        self.bank = None
        self.reloc_LC = True
        self.xorg_offset = None
        self.reset_banks()

    def reset_banks(self):
        self.bank_LC = {None: 0}  # next LC for each bank

    def effective_LC(self):
        return self.LC + (self.xorg_offset or 0)

    def add_symbol(self, name, value, weak=False, tracked=False):
        try:
            defined_value, defined_weak, unused = self.symbols[name]
            # existing definition
            if not defined_weak:
                raise AsmError("Multiple symbols: " + name)
            if value != defined_value:
                print value, defined_value
                raise AsmError("Value of weak symbol %s and new value don't match" % name)
            # reset weak value
        except KeyError:
            # new definition
            unused = True if tracked else None
        self.symbols[name] = value, weak, unused
        return name

    def add_label(self, lidx, label, real_LC=False, tracked=False):
        addr = Address(self.LC if real_LC else self.effective_LC(),
                       self.bank,
                       self.reloc_LC and (real_LC or not self.xorg_offset))
        name = self.add_symbol(label, addr, tracked=tracked)  # labels are never weak
        self.locations.append((lidx, name))

    def add_local_label(self, lidx, label):
        self.local_lid += 1
        self.add_label(lidx, label + "$" + str(self.local_lid))

    def add_autogen(self, name):
        size = name[0]
        try:
            value = str(xint(name[2:]))  # equalize 16 and >10
        except ValueError:
            if len(name) != 3:
                raise AsmError("Bad value for auto-generated constant: " + name)
            value = str(ord(name[2]) if size == "B" else ord(name[2]) << 8)
        if (value, size) not in self.autogens:
            self.autogens.append((value, size))
        return DelayedAddress(size + "#" + value, size, value)

    def add_def(self, name):
        if name in self.refdefs:
            raise AsmError("Multiple symbols")
        self.refdefs.append(name)

    def add_ref(self, name):
        if name in self.refdefs:
            return
        self.refdefs.append(name)
        self.add_symbol(name, Reference(name))

    def add_XOP(self, name, mode):
        self.xops[name] = mode

    def get_symbol(self, name):
        try:
            value, weak, unused = self.symbols[name]
            if unused:
                self.symbols[name] = (value, name, False)  # symbol has been used
        except KeyError:
            value = None
        return value

    def get_local(self, name, lpos, distance):
        targets = [(l, n) for (l, n) in self.locations
                   if n[:len(name) + 1] == name + "$"]
        try:
            i, lidx = next((j, l) for j, (l, n) in enumerate(targets)
                           if l >= lpos)
            if distance > 0 and lidx > lpos:
                distance -= 1  # i points to +! unless lidx == lpos
        except StopIteration:
            i = len(targets)  # beyond last label
        try:
            _, fullname = targets[i + distance]
        except IndexError:
            return None
        return self.get_symbol(fullname)

    def switch_bank(self, bank, addr=None):
        if addr is None:
            addr = 0
        self.bank_LC[self.bank] = self.LC
        if bank is None:  # ALL
            return max(addr, *self.bank_LC.values())
        else:
            bank_LC = self.bank_LC.get(bank)
            if bank_LC is None:
                bank_LC = self.bank_LC[bank] = self.bank_LC[None]
            return max(addr, bank_LC, self.bank_LC[None])

    def get_unused(self):
        """return all symbol names that have not been used"""
        return [name for name, (_, _, unused) in self.symbols.iteritems() if unused]


# Code generation

class Objdummy:
    """dummy code generation for keeping track of line counter"""

    def __init__(self, symbols):
        self.symbols = symbols
        self.saved_LC = {True: 0x0000, False: 0x0000}
        self.segment(0x0000, relocatable=True, init=True)

    def segment(self, base, relocatable=False, bank=None,
                dummy=False, xorg=False, init=False):
        if not init:
            self.saved_LC[self.symbols.reloc_LC] = self.symbols.LC
        if xorg:
            # for XORG, keep reloc status but save LC offset
            self.symbols.xorg_offset = base - self.symbols.LC
        else:
            self.symbols.xorg_offset = None
            self.symbols.reloc_LC = relocatable
            self.symbols.LC = (base if base is not None else
                               self.saved_LC[relocatable])
            self.symbols.bank = bank

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

    def emit(self, opcode, saddr=None, daddr=None, cycles=0):
        self.even()
        self.symbols.LC += 2 + (
            2 if saddr is not None else 0) + (
            2 if daddr is not None else 0)

    def process_label(self, lidx, label, real_LC=False, tracked=False):
        if not label:
            return
        if label[0] == "!":
            self.symbols.add_local_label(lidx, label[1:])
        else:
            self.symbols.add_label(lidx, label, real_LC, tracked=tracked)

    def list(self, lino, line=None, eos=False, text1=None, text2=None):
        pass


class Objcode:
    """generate object code"""

    def __init__(self, symbols, strict=False):
        self.symbols = symbols
        self.entry = None
        self.segments = []
        self.saves = []
        self.saved_LC = {True: 0x0000, False: 0x0000}
        self.segment(0, relocatable=True, init=True)
        self.done = False
        self.strict = strict
        self.unused_symbols = []

    def process_label(self, lidx, label, real_LC=False, tracked=False):
        pass

    def segment(self, base, relocatable=False, bank=None,
                dummy=False, xorg=False, init=False):
        if not init:
            self.saved_LC[self.symbols.reloc_LC] = self.symbols.LC
            self.segments.append((self.symbols.bank, self.symbols.LC,
                                  self.symbols.reloc_LC, self.dummy, self.code))
        if xorg:
            # for XORG, keep reloc status but save LC offset
            self.symbols.xorg_offset = base - self.symbols.LC
        else:
            self.symbols.xorg_offset = None
            self.symbols.reloc_LC = relocatable
            self.symbols.LC = (base if base is not None else
                               self.saved_LC[relocatable])
            self.symbols.bank = bank
        self.dummy = dummy
        self.code = []

    def even(self):
        if self.symbols.LC % 2 == 1:
            self.symbols.LC += 1

    def byte(self, byte):
        byte %= 0x100
        if self.symbols.LC % 2 == 0:
            self.code.append((self.symbols.LC, byte << 8, 0))
        else:
            # find previous byte
            i = -1
            try:
                while isinstance(self.code[i][1], Line):
                    i -= 1
                prev_LC, prev_word, cycles = self.code[i]
            except IndexError:
                prev_LC, prev_word, cycles = -1, None, 0
            if self.symbols.LC == prev_LC + 1 and isinstance(prev_word, int):
                self.code[i] = (self.symbols.LC - 1, prev_word | byte, cycles)
            else:
                self.code.append((self.symbols.LC - 1, byte, cycles))
        self.symbols.LC += 1

    def word(self, word, cycles=0):
        self.even()
        self.code.append((self.symbols.LC, word, cycles))
        self.symbols.LC += 2

    def block(self, size):
        self.code.append((self.symbols.LC, Block(size), 0))
        self.symbols.LC += size

    def emit(self, opcode, saddr=None, daddr=None, cycles=0):
        self.word(opcode, cycles)
        if saddr is not None:
            self.word(saddr)
        if daddr is not None:
            self.word(daddr)

    def list(self, lino, line=None, eos=False, text1=None, text2=None):
        """create list file entry"""
        if lino is None:
            # custom line without lino and LC == lino
            l = Line(None, line, eos)
            self.code.append((0, l, 0))  # LC, value, timing
        elif lino == 0:
            # change of source
            l = Line(lino, line, eos)
            l.text1 = l.text2 = "****"
            self.code.append((0, l, 0))
        elif lino > 0:
            # regular statement
            self.code.append((self.symbols.LC, Line(lino, line, eos), 0))
        else:
            # followup lines to statement
            lastline = self.code[-1][1]
            assert isinstance(lastline, Line)
            lastline.text1, lastline.text2 = text1, text2

    def prepare(self):
        """wrap-up code generation"""
        if not self.done:
            self.segment(None, relocatable=False, dummy=False)
            self.done = True
        self.resolve_delayed()

    def resolve_delayed(self):
        """patch DelayedAddresses in code"""
        for _, _, _, _, code in self.segments:
            for i, (LC, word, cycles) in enumerate(code):
                if isinstance(word, DelayedAddress):
                    addr = self.symbols.get_symbol(word.name)
                    if addr is None:
                        assert False, "bad symbol " + word.name
                    code[i] = LC, addr, cycles  # update word part

    def generate_dump(self):
        """generate raw dump of internal data structures (debug)"""
        self.prepare()
        dump = ""
        for bank, final_LC, reloc, dummy, code in self.segments:
            dump += "%s%cORG%s:\n" % (
                "\n" if dump and dump[-1] != "\n" else "",
                "R" if reloc else "D" if dummy else "A",
                "" if bank is None else " @ Bank " + str(bank))
            i, ttotal = 0, 0
            for LC, w, t in code:
                if isinstance(w, Line):
                    continue
                ttotal += t
                if i % 8 == 0:
                    dump += "%04X:  " % LC
                if isinstance(w, Address):
                    dump += w.hex() + " "
                elif isinstance(w, Reference):
                    dump += "%-6s" % (w.name[:6])
                elif isinstance(w, Block):
                    dump += "%04X# " % w.size
                else:
                    dump += "%04X  " % w
                if i % 8 == 7:
                    dump += "[%4d]\n" % ttotal
                    ttotal = 0
                i += 1
        return dump if dump[-1] == "\n" else dump + "\n"

    def generate_object_code(self, compressed=False):
        """generate object code (E/A option 3)"""
        self.prepare()
        reloc_LCs = [final_LC for bank, final_LC, reloc, dummy, code
                    in self.segments if reloc]
        relocSize = reloc_LCs[-1] if reloc_LCs else 0
        tags = Records(relocSize, self.symbols.idt, compressed)
        # add code and data words section
        refs = {}
        for bank, final_LC, reloc, dummy, code in self.segments:
            if bank:
                raise BuildError("Cannot create banked object code")
            if dummy:
                continue
            tags.add_LC()
            for LC, w, _ in code:
                if isinstance(w, Address):
                    tags.add("C" if w.relocatable else "B", w.addr, LC, reloc)
                elif isinstance(w, Reference):
                    prev_LC, prev_reloc = refs.get(w.name, (0, False))
                    tags.add("C" if prev_reloc else "B", prev_LC, LC, reloc)
                    refs[w.name] = (LC, reloc)
                elif isinstance(w, Block):
                    tags.add("A" if reloc else "9", LC)
                    tags.add_LC()
                elif isinstance(w, Line):
                    pass
                else:
                    tags.add("B", w, LC, reloc)
        tags.flush()
        # program entry
        if self.entry:
            tags.add("2" if self.entry.relocatable else "1", self.entry.addr)
            tags.flush()
        # add def and ref symbols section
        for s in self.symbols.refdefs:
            symbol = self.symbols.get_symbol(s)
            if isinstance(symbol, Reference):
                prev_LC, prev_reloc = refs.get(s, (0, False))
                tags.add("3" if prev_reloc else "4", prev_LC, sym=s[:6])
            elif symbol:
                reloc = isinstance(symbol, Address) and symbol.relocatable
                addr = symbol.addr if isinstance(symbol, Address) else symbol
                tags.add("5" if reloc else "6", addr, sym=s[:6])
        # closing section
        tags.flush()
        tags.append(":       xdt99 xas")
        return tags.dump()

    def fill_memory(self, memory, code, relocatable, base_addr):
        """load object code into memory"""
        offset = base_addr if relocatable else 0
        for LC, w, _ in code:
            addr = LC + offset
            if isinstance(w, Address):
                memory[addr] = w.addr + base_addr if w.relocatable else w.addr
            elif isinstance(w, Reference):
                if w.name not in self.symbols.exts:
                    raise BuildError("Unknown reference: " + w.name)
                memory[addr] = self.symbols.exts.get(w.name, 0x0000)
            elif isinstance(w, Block):
                a, s = (addr, (w.size + 1) / 2) if addr % 2 == 0 else \
                       (addr + 1, w.size / 2)
                for i in xrange(s / 2):
                    memory[a + i] = 0x0000
            elif isinstance(w, Line):
                pass
            else:
                memory[addr] = w

    def generate_binaries(self, base_addr, ext_saves=None):
        """
        generate raw memory images
        """
        self.prepare()

        # get first and last address of binary
        blobs = []
        saves = self.saves or ext_saves
        bank_count = max([bank for bank, _, _, _, _ in self.segments if bank is not None] or [0]) + 1

        if self.saves or ext_saves:
            # create one binary per bank
            mems = {bank: {} for bank in xrange(bank_count)}
            for bank, final_LC, relocatable, dummy, code in self.segments:
                if dummy:
                    continue
                banks = range(bank_count) if bank is None else [bank]
                for b in banks:
                    self.fill_memory(mems[b], code, relocatable, base_addr)

            # apply SAVE directive filter
            for bank in mems:
                for min_addr, max_addr in saves:
                    addrs = [a for a in mems[bank].keys()
                             if min_addr <= a < max_addr]
                    if addrs:
                        blobs.append([min_addr, max_addr, bank, mems[bank]])

        else:
            # create one blob per segment
            for bank, final_LC, relocatable, dummy, code in self.segments:
                if dummy:
                    continue
                mem = {}
                self.fill_memory(mem, code, relocatable, base_addr)
                if mem:
                    addrs = mem.keys()
                    blobs.append([min(addrs), max(addrs) + 2, bank, mem])

            # merge adjoining segments (espc. for XORGs)
            i = 0
            while i < len(blobs):
                j = 0
                while j < len(blobs):
                    if i != j and (blobs[i][1] == blobs[j][0] and
                                   blobs[i][2] == blobs[j][2]):
                        blobs[i][1] = blobs[j][1]
                        blobs[i][3].update(blobs[j][3])
                        del blobs[j]
                        i, j = 0, 0
                    else:
                        j += 1
                i += 1

        # fill unfilled memory locations with >0000
        binaries = [(min_addr, bank,
                     "".join([chrw(mem[addr]) if addr in mem else "\x00\x00"
                              for addr in xrange(min_addr, max_addr, 2)]))
                    for min_addr, max_addr, bank, mem in blobs]
        return binaries, bank_count

    def generate_text(self, data, mode):
        """convert binary data into text representation"""
        text = lines = ""
        for addr, bank, mem in data:
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
                text += ";      aorg >%04x\n" % addr
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

    def generate_image(self, base_addr, chunk_size=0x2000):
        """generate memory image (E/A option 5)"""
        try:
            sfirst = self.symbols.get_symbol("SFIRST")
            slast = self.symbols.get_symbol("SLAST")
            save = [(sfirst.addr + base_addr if sfirst.relocatable else
                     sfirst.addr,
                     slast.addr + base_addr if slast.relocatable else
                     slast.addr)]
        except AttributeError:
            save = None
        binaries, bank_count = self.generate_binaries(base_addr, ext_saves=save)
        if bank_count > 1:
            raise BuildError("Cannot create banked program image")
        # split binaries into chunks for E/A 5 loader
        chunks = [(addr + i, data[i:i + chunk_size - 6])
                  for addr, bank, data in binaries
                  for i in xrange(0, len(data), chunk_size - 6)]
        # add meta data information to each chunk (next?, length, addr)
        images = [("\xff\xff" if i + 1 < len(chunks) else "\x00\x00") +
                  chrw(len(c) + 6) + chrw(a) + c
                  for i, (a, c) in enumerate(chunks)]
        return images

    def generate_XB_loader(self):
        """stash code in Extended BASIC program"""
        self.prepare()
        size = 0
        for bank, final_LC, reloc, dummy, code in self.segments:
            if bank:
                raise BuildError("Cannot create banked object code")
            if not reloc:
                raise BuildError(
                    "Cannot create BASIC program for non-relocatable code")
            if final_LC > size:
                size = final_LC
        last_addr = 0xFFE8  # end of token table
        first_addr = last_addr - 4 - size
        loader = (
            # CALL INIT :: CALL LOAD(>3FF8,"XYZZY ")::
            # CALL LOAD(>2004,>FF,>E4):: CALL LINK("XYZZY")
            "\x9d\xc8\x04\x49\x4e\x49\x54\x82\x9d\xc8\x04\x4c\x4f\x41\x44" +
            "\xb7\xc8\x05\x31\x36\x33\x37\x36\xb3\xc8\x02\x38\x38\xb3\xc8" +
            "\x02\x38\x39\xb3\xc8\x02\x39\x30\xb3\xc8\x02\x39\x30\xb3\xc8" +
            "\x02\x38\x39\xb3\xc8\x02\x33\x32\xb3\xc8\x03\x32\x35\x35\xb3" +
            "\xc8\x03\x32\x32\x38\xb6\x82\x9d\xc8\x04\x4c\x4f\x41\x44\xb7" +
            "\xc8\x04\x38\x31\x39\x36\xb3\xc8\x02\x36\x33\xb3\xc8\x03\x32" +
            "\x34\x38\xb6\x82\x9d\xc8\x04\x4c\x49\x4e\x4b\xb7\xc7\x05\x58" +
            "\x59\x5a\x5a\x59\xb6"
            )
        payload = self.generate_image(first_addr, 0x6000)[0][6:]
        token_table = (chr(len(loader) + 1) + loader + "\x00" +
                      "\x00" * (256 - size) +
                      payload +
                      "\x04\x60" + chrw(first_addr))
        token_tab_addr = last_addr - len(token_table)
        lino_tab_addr = token_tab_addr - 4
        lino_table = "\x00\x01" + chrw(token_tab_addr + 1)
        checksum = (token_tab_addr - 1) ^ lino_tab_addr
        header = ("\xab\xcd" + chrw(lino_tab_addr) + chrw(token_tab_addr - 1) +
                  chrw(checksum) + chrw(last_addr - 1))
        chunks = [(lino_table + token_table)[i:i + 254]
                  for i in xrange(0, len(lino_table + token_table), 254)]
        return (chr(len(header)) + header +
                "".join([chr(len(c)) + c for c in chunks]))

    def generate_jumpstart(self):
        """generate disk image for Jumpstart cartridge"""
        segments = self.generate_image(0xa000, 0x6000)
        if len(segments) > 32 / 4:
            raise BuildError(
                "Cannot create jumpstart disk with more than 8 segments")
        e = self.entry or Address(0xa000)
        start = e.addr + 0xa000 if e.relocatable else e.addr
        chunks, sectors = [], []
        for image in segments:
            addr, data = image[4:6], image[6:]
            if ordw(addr) % 256 != 0:
                raise BuildError("Segments must start at multiples of >100")
            size = used(len(data), 256)
            chunks.append(addr + chrw(size))
            sectors.append(data + "\x00" * pad(len(data), 256))
        disk = (
            # sector 0
            "xas99-JS" + chrw(0xc2b9) +           # 10 bytes
            chrw(360) + "\x09DSK \x28\x01\x01" +  # 10 bytes
            chrw(start) +                         #  2 bytes
            "".join(chunks) + "\x00\x00" + "\xff" * (232 - 4 * len(chunks)) +
            # sector 1
            "\x00" * 256 +
            # data sectors
            "".join(sectors)
            )
        assert len(disk) % 256 == 0
        return disk + "\x00" * (360 * 256 - len(disk))

    def generate_symbols(self, equ=False):
        """generate symbols"""
        # merge all defined symbols
        symbols = self.symbols.symbols
        # get their values
        regs = self.symbols.registers  # no not include these
        symlist = []
        for s in sorted(symbols):
            if s in regs or s[0] == '$' or s[0] == "_":
                continue  # skip registers, local and internal symbols
            addr, _, _ = symbols.get(s)
            if isinstance(addr, Address):
                # add extra information to addresses
                a, r, b = (addr.addr,
                           "REL" if addr.relocatable else "   ",
                           "B>%02X" % addr.bank if addr.bank is not None else "")
            elif isinstance(addr, Reference):
                # add value of references
                a, r, b = (self.symbols.exts.get(addr.name), "REF", "")
            else:
                # add immediate address value
                a, r, b = addr, "   ", ""
            symlist.append((s, a, r, b))
        if self.strict:
            fmt = ("{:<6} EQU  >{:04X}    * {} {}" if equ else
                   "    {:.<6} {} : {} {}")
        else:
            fmt = ("{}:\n       equ  >{:04X}  ; {} {}" if equ else
                   "    {:.<20} >{:04X} : {} {}")
        return "\n".join([fmt.format(*s) for s in symlist])

    def generate_list(self, gen_symbols):
        """generate listing"""
        listing = []
        for bank, final_LC, reloc, dummy, code in self.segments:
            words, slino, sline, skip = [], None, None, False
            for LC, w, t in code:
                if isinstance(w, Line):
                    if slino is not None:
                        a0, w0, t0 = words[0] if words else ("", "", 0)
                        listing.append("%4s %-4s %-5s %-2s %s" % (
                            slino, a0, w0, t0 or "", sline))
                        for ai, wi, ti in words[1:]:
                            assert ti == 0
                            listing.append("     %-4s %-5s" % (ai, wi))
                        if w.eos:
                            break
                    slino = "%04d" % w.lino if w.lino else "****"
                    sline = w.line
                    if not (w.text1 is None and w.text2 is None):
                        words = [("%04X" % LC if w.text1 is None else w.text1,
                                  "" if w.text2 is None else
                                  w.text2 if isinstance(w.text2, str) else
                                  w.text2.hex() if isinstance(w.text2, Address)
                                  else "%04X" % w.text2,
                                  t or "")]
                        skip = True
                    else:
                        words = []
                        skip = False
                elif skip:
                    pass
                elif isinstance(w, Address):
                    words.append(("%04X" % LC, w.hex(), t))
                elif isinstance(w, Reference):
                    words.append(("%04X" % LC, "XXXX", t))
                elif isinstance(w, Block):
                    words.append(("%04X" % LC, "....", t))
                else:
                    words.append(("%04X" % LC, "%04X" % w, t))
        symbols = "\n" + self.generate_symbols() + "\n" if gen_symbols else ""
        return ("XAS99 CROSS-ASSEMBLER   VERSION " + VERSION + "\n" +
                "\n".join(listing) + "\n" + symbols)

    def generate_cartridge(self, name):
        """generate RPK file for use as MESS rom cartridge"""
        self.prepare()
        send = self.entry or Address(0x6030)
        entry = send.addr + 0x6030 if send.relocatable else send.addr
        gpl = "\xaa\x01\x00\x00\x00\x00\x60\x10" + "\x00" * 8
        proginfo = "\x00\x00%s%c%s" % (chrw(entry), len(name), name)
        pad = "\x00" * (27 - len(name))
        images = self.generate_image(0x6030, 0xFFFF)
        if len(images) > 1:
            raise BuildError("Cannot create cartridge with multiple segments")
        code = images[0][6:]
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


class Optimizer:
    """object code analysis and optimization (currently only checks)"""

    @staticmethod
    def process(parser, code, mnemonic, opcode, fmt, arg1, arg2):
        if mnemonic == "B":
            if (arg1[0] == 0b10 and isinstance(arg1[2], int) and
                    -128 <= (arg1[2] - (code.symbols.effective_LC() + 2)) / 2 <= 128):
                # upper bound is 128 instead of 127, since replacing B by JMP
                # would also eliminate one word (the target of B)
                parser.warn("Possible branch/jump optimization")


class Records:
    """object code tag and record handling"""

    def __init__(self, relocSize, idt, compressed):
        self.records = []
        if compressed:
            self.record = "\x01%s%-8s" % (chrw(relocSize), idt)
            self.linlen = 77
        else:
            self.record = "0%04X%-8s" % (relocSize, idt)
            self.linlen = 64
        self.compressed = compressed
        self.needs_LC = True

    def add(self, tag, value, LC=None, reloc=False, sym=None):
        """add tag to records"""
        add_LC = self.needs_LC and LC is not None
        tag_penalty = ((5 if tag in "9A" else 0) +
                      (5 if add_LC else 0))
        if self.compressed:
            s = tag + chrw(value)
            if tag in "3456":
                tag_penalty += 31
        else:
            s = tag + ("%04X" % value)
        if sym:
            s += "%-6s" % sym
        if len(self.record) + len(s) + tag_penalty > self.linlen:
            self.flush()
            add_LC = LC is not None
        if add_LC:
            tagLC = (("A" if reloc else "9") +
                     (chrw(LC) if self.compressed else "%04X" % LC))
            self.record += tagLC + s
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
            checksum = reduce(lambda s, c: s + ord(c), self.record, ord("7"))
            self.record += "7%04X" % (~checksum + 1 & 0xFFFF)
        self.records.append(self.record + "F" + " " * (69 - len(self.record)))
        self.record = ""
        self.add_LC()

    def dump(self):
        """dump records as DIS/FIX80"""
        if self.compressed:
            lines = (["%-80s" % line for line in self.records[:-1]] +
                     ["%-75s %04d" % (self.records[-1], len(self.records))])
        else:
            lines = ["%-75s %04d" % (line, i + 1)
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


# Directives

class Directives:
    @staticmethod
    def DEF(parser, code, label, ops):
        if parser.pass_no != 1:
            return
        code.process_label(parser.lidx, label)
        for op in ops:
            code.symbols.add_def(op[:6] if parser.strict else op)

    @staticmethod
    def REF(parser, code, label, ops):
        if parser.pass_no != 1:
            return
        for op in ops:
            code.symbols.add_ref(op[:6] if parser.strict else op)

    @staticmethod
    def EQU(parser, code, label, ops):
        if parser.pass_no != 1:
            value = code.symbols.get_symbol(label)
            code.list(-1, text1="", text2=value)
            return
        value = parser.expression(ops[0], well_defined=True)
        code.symbols.add_symbol(label, value)

    @staticmethod
    def WEQU(parser, code, label, ops):
        if parser.pass_no != 1:
            value = code.symbols.get_symbol(label)
            code.list(-1, text1="", text2=value)
            return
        value = parser.expression(ops[0], well_defined=True)
        code.symbols.add_symbol(label, value, weak=True)

    @staticmethod
    def DATA(parser, code, label, ops):
        code.even()
        code.process_label(parser.lidx, label, tracked=True)
        for op in ops:
            w = parser.expression(op)
            code.word(w)

    @staticmethod
    def BYTE(parser, code, label, ops):
        code.process_label(parser.lidx, label, tracked=True)
        for op in ops:
            b = parser.expression(op)
            code.byte(b)

    @staticmethod
    def TEXT(parser, code, label, ops):
        code.process_label(parser.lidx, label, tracked=True)
        code.list(-1, text2="....")
        for op in ops:
            text = parser.text(op)
            for c in text:
                code.byte(ord(c))

    @staticmethod
    def STRI(parser, code, label, ops):
        code.process_label(parser.lidx, label, tracked=True)
        code.list(-1, text2="....")
        for op in ops:
            text = parser.text(op)
            code.byte(len(text))
            for c in text:
                code.byte(ord(c))

    @staticmethod
    def BSS(parser, code, label, ops):
        code.process_label(parser.lidx, label, tracked=True)
        size = parser.value(ops[0])
        code.block(size)

    @staticmethod
    def BES(parser, code, label, ops):
        size = parser.value(ops[0])
        code.block(size)
        code.process_label(parser.lidx, label, tracked=True)

    @staticmethod
    def EVEN(parser, code, label, ops):
        code.even()
        code.process_label(parser.lidx, label)  # differs from E/A manual!

    @staticmethod
    def AORG(parser, code, label, ops):
        base = parser.value(ops[0]) if ops else None
        if len(ops) > 1:  # keep for compatibility
            bank = parser.value(ops[1])
            parser.warn("AORG with bank is obsolete, use BANK directive instead")
        else:
            bank = None
        code.list(0, eos=True)
        code.segment(base, relocatable=False, bank=bank)
        if base is not None:
            code.symbols.reset_banks()
        code.process_label(parser.lidx, label)

    @staticmethod
    def RORG(parser, code, label, ops):
        base = parser.value(ops[0]) if ops else None
        code.list(0, eos=True)
        code.segment(base, relocatable=True)
        code.process_label(parser.lidx, label)

    @staticmethod
    def DORG(parser, code, label, ops):
        base = parser.value(ops[0]) if ops else None
        code.list(0, eos=True)
        code.segment(base, dummy=True)
        code.process_label(parser.lidx, label)

    @staticmethod
    def XORG(parser, code, label, ops):
        if not ops:
            raise AsmError("Missing argument")
        code.process_label(parser.lidx, label, real_LC=True)
        base = parser.value(ops[0])
        code.list(0, eos=True)
        code.segment(base, relocatable=False, xorg=True)

    @staticmethod
    def BANK(parser, code, label, ops):
        if not ops:
            raise AsmError("Missing argument")
        code.process_label(parser.lidx, label, real_LC=True)
        bank = parser.bank(ops[0])
        code.list(0, eos=True)
        base = code.symbols.switch_bank(bank)
        code.segment(base, relocatable=False, bank=bank)

    @staticmethod
    def COPY(parser, code, label, ops):
        code.process_label(parser.lidx, label)
        filename = parser.filename(ops[0])
        parser.open(filename=filename)

    @staticmethod
    def END(parser, code, label, ops):
        code.process_label(parser.lidx, label)
        if ops:
            code.entry = code.symbols.get_symbol(
                ops[0][:6] if parser.strict else ops[0])
        parser.stop()

    @staticmethod
    def IDT(parser, code, label, ops):
        if parser.pass_no != 1:
            return
        code.process_label(parser.lidx, label)
        text = parser.text(ops[0]) if ops else "        "
        code.symbols.idt = text[:8]

    @staticmethod
    def SAVE(parser, code, label, ops):
        if parser.pass_no != 2:
            return
        try:
            first, last = parser.expression(ops[0]), parser.expression(ops[1])
        except IndexError:
            raise AsmError("Invalid arguments")
        code.saves.append((first, last))

    @staticmethod
    def DXOP(parser, code, label, ops):
        if parser.pass_no != 1:
            return
        code.process_label(parser.lidx, label)
        try:
            mode = parser.expression(ops[1], well_defined=True)
            code.symbols.add_XOP(ops[0], str(mode))
        except IndexError:
            raise AsmError("Invalid arguments")

    @staticmethod
    def BCOPY(parser, code, label, ops):
        """extension: include binary file as BYTE stream"""
        code.process_label(parser.lidx, label)
        filename = parser.filename(ops[0])
        path = parser.find(filename)
        try:
            with open(path, "rb") as f:
                bs = f.read()
                for b in bs:
                    code.byte(ord(b))
        except IOError as e:
            raise AsmError(e)

    ignores = [
        "",
        "PSEG", "PEND", "CSEG", "CEND", "DSEG", "DEND",
        "UNL", "LIST", "PAGE", "TITL", "LOAD", "SREF"
        ]

    @staticmethod
    def process(parser, code, label, mnemonic, operands):
        if mnemonic in Directives.ignores:
            code.process_label(parser.lidx, label)
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
    """xdt99-specific preprocessor extensions
       NOTE: The preprocessor is only called for pass 1, in pass 2 all
             dot-commands have been eliminated!
    """

    def __init__(self, parser):
        self.parser = parser
        self.parse = True
        self.parse_branches = []
        self.parse_macro = None
        self.macros = {}

    def args(self, ops):
        lhs = self.parser.expression(ops[0], well_defined=True, relaxed=True)
        rhs = self.parser.expression(ops[1], well_defined=True, relaxed=True) if len(ops) > 1 else 0
        return lhs, rhs

    def str_args(self, ops):
        return [self.parser.text(op) if self.parser.is_literal(op) else
                str(self.parser.expression(op, well_defined=True))
                for op in ops]

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
        self.parse = (code.symbols.get_symbol(ops[0]) is not None if self.parse
                      else None)

    def IFNDEF(self, code, ops):
        self.parse_branches.append(self.parse)
        self.parse = (code.symbols.get_symbol(ops[0]) is None if self.parse
                      else None)

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

    def PRINT(self, code, ops):
        res = " ".join(self.str_args(ops))
        sys.stdout.write(res + "\n")

    def ERROR(self, code, ops):
        if self.parse:
            raise AsmError("Error state")

    def instmargs(self, text):
        try:
            return re.sub(r"#(\d+)",
                          lambda m: self.parser.margs[int(m.group(1)) - 1],
                          text)
        except (ValueError, IndexError):
            return text

    def instline(self, line):
        # temporary kludge, breaks comments
        parts = re.split(r"('(?:[^']|'')*'|\"[^\"]*\")", line)
        parts[::2] = [self.instmargs(p) for p in parts[::2]]
        return "".join(parts)

    def process(self, code, label, mnemonic, operands, line):
        if self.parse_macro:
            if mnemonic == ".ENDM":
                self.parse_macro = None
            elif mnemonic == ".DEFM":
                raise AsmError("Cannot define macro within macro")
            else:
                self.macros[self.parse_macro].append(line)
            return False, None, None
        if self.parse and operands and '#' in line:
            operands = [self.instmargs(op) for op in operands]
            line = self.instline(line)
        if mnemonic and mnemonic[0] == '.':
            code.process_label(self.parser.lidx, label)
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


# Opcodes

class Timing:

    WAITSTATES = 4

    def __init__(self, cycles, mem_accesses, read=False, byte=False, x2=False):
        self.cycles = cycles
        self.mem_accesses = mem_accesses
        self.addl_cycles = [0, 4, 8, 6] if byte else [0, 4, 8, 8]
        self.addl_mem = ([0, 2, 4, 2] if x2 else
                        [0, 1, 2, 1] if read else [0, 2, 3, 2])

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


class Opcodes:
    op_ga = lambda parser, x: parser.address(x)  # [0x0000 .. 0xFFFF]
    op_wa = lambda parser, x: parser.register(x)  # [0 .. 15]
    op_iop = lambda parser, x: parser.expression(x, iop=True)  # [0x0000 .. 0xFFFF]
    op_lwpi = lambda parser, x: parser.lwpi(x)  # [0x0000 .. 0xFFFF]
    op_cru = lambda parser, x: parser.expression(x, iop=True)  # [-128 .. 127]
    op_disp = lambda parser, x: parser.relative(x)  # [-254 .. 256]
    op_cnt = lambda parser, x: parser.expression(x, iop=True)  # [0 .. 15]
    op_scnt = lambda parser, x: parser.expression(x, iop=True, allow_r0=True)  # [0 .. 15]
    op_xop = lambda parser, x: parser.expression(x, iop=True)  # [1 .. 2]

    opcodes = {
        # 6. arithmetic
        "A": (0xA000, 1, op_ga, op_ga, Timing(14, 1)),
        "AB": (0xB000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        "ABS": (0x0740, 6, op_ga, None, Timing(14, 1)),  # 4 in E/A Manual
        "AI": (0x0220, 8, op_wa, op_iop, Timing(14, 2)),
        "DEC": (0x0600, 6, op_ga, None, Timing(10, 1)),
        "DECT": (0x0640, 6, op_ga, None, Timing(10, 1)),
        "DIV": (0x3C00, 9, op_ga, op_wa, Timing(124, 1, read=True)),
        "INC": (0x0580, 6, op_ga, None, Timing(10, 1)),
        "INCT": (0x05C0, 6, op_ga, None, Timing(10, 1)),
        "MPY": (0x3800, 9, op_ga, op_wa, Timing(52, 1, read=True)),
        "NEG": (0x0500, 6, op_ga, None, Timing(12, 1)),
        "S": (0x6000, 1, op_ga, op_ga, Timing(14, 1)),
        "SB": (0x7000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        # 7. jump and branch
        "B": (0x0440, 6, op_ga, None, Timing(8, 1, read=True)),
        "BL": (0x0680, 6, op_ga, None, Timing(12, 1, read=True)),
        "BLWP": (0x0400, 6, op_ga, None, Timing(26, 1, read=True, x2=True)),
        "JEQ": (0x1300, 2, op_disp, None, Timing(10, 1)),
        "JGT": (0x1500, 2, op_disp, None, Timing(10, 1)),
        "JHE": (0x1400, 2, op_disp, None, Timing(10, 1)),
        "JH": (0x1B00, 2, op_disp, None, Timing(10, 1)),
        "JL": (0x1A00, 2, op_disp, None, Timing(10, 1)),
        "JLE": (0x1200, 2, op_disp, None, Timing(10, 1)),
        "JLT": (0x1100, 2, op_disp, None, Timing(10, 1)),
        "JMP": (0x1000, 2, op_disp, None, Timing(10, 1)),
        "JNC": (0x1700, 2, op_disp, None, Timing(10, 1)),
        "JNE": (0x1600, 2, op_disp, None, Timing(10, 1)),
        "JNO": (0x1900, 2, op_disp, None, Timing(10, 1)),
        "JOP": (0x1C00, 2, op_disp, None, Timing(10, 1)),
        "JOC": (0x1800, 2, op_disp, None, Timing(10, 1)),
        "RTWP": (0x0380, 7, None, None, Timing(14, 1)),
        "X": (0x0480, 6, op_ga, None, Timing(8, 1, read=True)),  # approx.
        "XOP": (0x2C00, 9, op_ga, op_xop, Timing(36, 2)),
        # 8. compare instructions
        "C": (0x8000, 1, op_ga, op_ga, Timing(14, 1, read=True)),
        "CB": (0x9000, 1, op_ga, op_ga, Timing(14, 1, read=True, byte=True)),
        "CI": (0x0280, 8, op_wa, op_iop, Timing(14, 2)),
        "COC": (0x2000, 3, op_ga, op_wa, Timing(14, 1)),
        "CZC": (0x2400, 3, op_ga, op_wa, Timing(14, 1)),
        # 9. control and cru instructions
        "LDCR": (0x3000, 4, op_ga, op_cnt, Timing(52, 1)),
        "SBO": (0x1D00, 2, op_cru, None, Timing(12, 2)),
        "SBZ": (0x1E00, 2, op_cru, None, Timing(12, 2)),
        "STCR": (0x3400, 4, op_ga, op_cnt, Timing(60, 1)),
        "TB": (0x1F00, 2, op_cru, None, Timing(12, 2)),
        "CKOF": (0x03C0, 7, None, None, Timing(12, 1)),
        "CKON": (0x03A0, 7, None, None, Timing(12, 1)),
        "IDLE": (0x0340, 7, None, None, Timing(12, 1)),
        "RSET": (0x0360, 7, None, None, Timing(12, 1)),
        "LREX": (0x03E0, 7, None, None, Timing(12, 1)),
        # 10. load and move instructions
        "LI": (0x0200, 8, op_wa, op_iop, Timing(12, 2)),
        "LIMI": (0x0300, 81, op_iop, None, Timing(16, 2)),
        "LWPI": (0x02E0, 81, op_lwpi, None, Timing(10, 2)),
        "MOV": (0xC000, 1, op_ga, op_ga, Timing(14, 1)),
        "MOVB": (0xD000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        "STST": (0x02C0, 8, op_wa, None, Timing(8, 1)),
        "STWP": (0x02A0, 8, op_wa, None, Timing(8, 1)),
        "SWPB": (0x06C0, 6, op_ga, None, Timing(10, 1)),
        # 11. logical instructions
        "ANDI": (0x0240, 8, op_wa, op_iop, Timing(14, 2)),
        "ORI": (0x0260, 8, op_wa, op_iop, Timing(14, 2)),
        "XOR": (0x2800, 3, op_ga, op_wa, Timing(14, 1, read=True)),
        "INV": (0x0540, 6, op_ga, None, Timing(10, 1)),
        "CLR": (0x04C0, 6, op_ga, None, Timing(10, 1)),
        "SETO": (0x0700, 6, op_ga, None, Timing(10, 1)),
        "SOC": (0xE000, 1, op_ga, op_ga, Timing(14, 1)),
        "SOCB": (0xF000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        "SZC": (0x4000, 1, op_ga, op_ga, Timing(14, 1)),
        "SZCB": (0x5000, 1, op_ga, op_ga, Timing(14, 1, byte=True)),
        # 12. shift instructions
        "SRA": (0x0800, 5, op_wa, op_scnt, Timing(52, 1)),
        "SRL": (0x0900, 5, op_wa, op_scnt, Timing(52, 1)),
        "SLA": (0x0A00, 5, op_wa, op_scnt, Timing(52, 1)),
        "SRC": (0x0B00, 5, op_wa, op_scnt, Timing(52, 1)),
        # F18A GPU instructions
        "CALL": (0x0C80, 6, op_ga, None, Timing(0, 0)),
        "RET": (0x0C00, 7, None, None, Timing(0, 0)),
        "PUSH": (0x0D00, 6, op_ga, None, Timing(0, 0)),
        "POP": (0x0F00, 6, op_ga, None, Timing(0, 0)),
        "SLC": (0x0E00, 5, op_wa, op_scnt, Timing(0, 0))
        # end of opcodes
    }

    pseudos = {
        # 13. pseudo instructions
        "NOP": ("JMP", ["$+2"]),
        "RT": ("B", ["*<R>11"]),
        "PIX": ("XOP", None)
    }

    @staticmethod
    def process(parser, code, label, mnemonic, operands):
        """get assembly code for mnemonic"""
        code.even()
        code.process_label(parser.lidx, label)
        if mnemonic in Opcodes.pseudos:
            m, ops = Opcodes.pseudos[mnemonic]
            if ops is not None:
                ops = [o.replace("<R>", "R" if parser.use_R else "")
                       for o in ops]
            mnemonic, operands = m, ops or operands
        elif mnemonic in parser.symbols.xops:
            mode = parser.symbols.xops[mnemonic]
            mnemonic, operands = "XOP", [operands[0], mode]
        if mnemonic in Opcodes.opcodes:
            try:
                opcode, fmt, parse1, parse2, timing = Opcodes.opcodes[mnemonic]
                arg1 = parse1(parser, operands[0]) if parse1 else None
                arg2 = parse2(parser, operands[1]) if parse2 else None
                Optimizer.process(parser, code, mnemonic, opcode, fmt, arg1, arg2)
                Opcodes.generate(code, opcode, fmt, arg1, arg2, timing)
            except (IndexError, ValueError):
                raise AsmError("Syntax error")
        else:
            raise AsmError("Invalid mnemonic: " + mnemonic)

    @staticmethod
    def generate(code, opcode, fmt, arg1, arg2, timing):
        """generate byte code"""
        # I. two general address instructions
        if fmt == 1:
            ts, s, sa = arg1
            td, d, da = arg2
            b = opcode | td << 10 | d << 6 | ts << 4 | s
            t = timing.time2(ts, sa, td, da)
            code.emit(b, sa, da, cycles=t)
        # II. jump and bit I/O instructions
        elif fmt == 2:
            b = opcode | arg1 & 0xFF
            t = timing.time0()
            code.emit(b, cycles=t)
        # III. logical instructions
        elif fmt == 3:
            ts, s, sa = arg1
            d = arg2
            b = opcode | d << 6 | ts << 4 | s
            t = timing.time1(ts, sa)
            code.emit(b, sa, cycles=t)
        # IV. CRU multi-bit instructions
        elif fmt == 4:
            ts, s, sa = arg1
            c = arg2
            b = opcode | c << 6 | ts << 4 | s
            t = timing.time1(ts, sa)
            code.emit(b, sa, cycles=t)
        # V. register shift instructions
        elif fmt == 5:
            w = arg1
            c = arg2
            b = opcode | c << 4 | w
            t = timing.time0()
            code.emit(b, cycles=t)
        # VI. single address instructions
        elif fmt == 6:
            ts, s, sa = arg1
            b = opcode | ts << 4 | s
            t = timing.time1(ts, sa)
            code.emit(b, sa, cycles=t)
        # VII. control instructions
        elif fmt == 7:
            b = opcode
            t = timing.time0()
            code.emit(b, cycles=t)
        # VIII. immediate instructions
        elif fmt == 8:
            b = opcode | arg1
            t = timing.time0()
            code.emit(b, arg2, cycles=t)
        elif fmt == 81:
            b = opcode
            t = timing.time0()
            code.emit(b, arg1, cycles=t)
        # IX. extended operations; multiply and divide
        elif fmt == 9:
            ts, s, sa = arg1
            r = arg2
            b = opcode | r << 6 | ts << 4 | s
            t = timing.time1(ts, sa)
            code.emit(b, sa, cycles=t)
        else:
            raise AsmError("Invalid opcode format " + str(fmt))


# Parsing

class Parser:
    """scanner and parser class"""

    def __init__(self, symbols, path=None, includes=None, strict=False,
                 warnings=True, use_R=False):
        self.prep = Preprocessor(self)
        self.warnings = []
        self.symbols = symbols
        self.text_literals = []
        self.fn = None
        self.path = path
        self.source = None
        self.margs = []
        self.lino = -1
        self.suspended_files = []
        self.include_path = includes or ["."]
        self.strict = strict
        self.warnings_enabled = warnings
        self.parse_branches = [True]
        self.pass_no = 0
        self.lidx = 0
        self.use_R = use_R

    def warn(self, message):
        # warn in pass 2 to avoid duplicates and to prevent false expr values 0
        if self.warnings_enabled and self.pass_no == 2:
            self.warnings.append(message)

    def open(self, filename=None, macro=None, ops=None):
        """open new source file or macro buffer"""
        if len(self.suspended_files) > 100:
            raise AsmError("Too many nested files or macros")
        if self.source is not None:
            self.suspended_files.append((self.fn, self.path, self.source,
                                         self.margs, self.lino))
        if filename:
            newfile = "-" if filename == "-" else self.find(filename)
            self.path, fn = os.path.split(newfile)
            self.fn = "> " + fn
            try:
                self.source = readlines(newfile, "r")
            except IOError as e:
                raise AsmError(e)
        else:
            # set self.fn here to indicate macro instantiation in list file
            self.source = self.prep.macros[macro]
            self.margs = ops or []
        self.lino = 0

    def resume(self):
        """close current source file and resume previous one"""
        try:
            self.fn, self.path, self.source, self.margs, self.lino = \
                self.suspended_files.pop()
            return True
        except IndexError:
            self.fn, self.path, self.source, self.margs, self.lino = \
                None, None, None, None, -1
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
            extensions = ["", ".a99", ".A99", ".asm", ".ASM", ".s", ".S"]
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
        if self.strict:
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
        return label, mnemonic, operands, comment, True

    def escape(self, text):
        """remove and save text literals from line"""
        parts = re.split(r"('(?:[^']|'')*'|\"[^\"]*\")", text)  # not-lit, lit, not-lit, lit, ...
        literals = [s[1:-1].replace("''", "'") for s in parts[1::2]]  # '' is ' within 'string'
        parts[1::2] = ["'%s'" % (len(self.text_literals) + i) for i in xrange(len(literals))]  # 'n' lit placeholder
        self.text_literals.extend(literals)
        return "".join(parts).upper()

    def restore(self, text):
        """restore escaped text literals"""
        return re.sub(r"'(\d+)'",
                      lambda m: self.text_literals[int(m.group(1))],
                      text)

    def parse(self, dummy, code):
        """parse source code and generate object code"""
        source, errors = self.pass_1(dummy, code)
        errors = self.pass_2(source, code, errors)
        self.autogens(code)
        return errors

    def pass_1(self, dummy, code):
        "pass 1: gather symbols, apply preprocessor"
        source, errors = [], []
        # first pass: scan symbols
        self.pass_no = 1
        self.lidx = 0
        self.symbols.reset_LC()
        prev_label = None
        while True:
            # get next source line
            lino, line, filename = self.read()
            if lino is None:
                break
            try:
                # break line into fields
                label, mnemonic, operands, comment, stmt = self.line(line)
                keep, operands, line = self.prep.process(dummy, label, mnemonic,
                                                         operands, line)
                if not keep:
                    continue
                source.append((lino, label, mnemonic, operands, line, filename,
                               stmt))
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
                # process mnemonic
                Directives.process(self, dummy, label, mnemonic, operands) or \
                    Opcodes.process(self, dummy, label, mnemonic, operands)
            except AsmError as e:
                errors.append("%s <1> %04d - %s\n***** %s\n" % (
                    filename, lino, line, e.message))
        return source, errors

    def pass_2(self, source, code, errors):
        """second pass: generate code"""
        self.pass_no = 2
        self.lidx = 0
        self.symbols.reset_LC()
        prev_file = None
        for lino, label, mnemonic, operands, line, filename, stmt in source:
            if filename != prev_file:
                code.list(0, line=filename)
                prev_file = filename
            code.list(lino, line=line)
            if not stmt:
                continue
            self.lidx += 1
            if label and label[-1] == ":" and not mnemonic:
                continue
            try:
                Directives.process(self, code, label, mnemonic, operands) or \
                    Opcodes.process(self, code, label, mnemonic, operands)
            except AsmError as e:
                errors.append("%s <2> %04d - %s\n***** %s\n" % (
                    filename, lino, line, e.message))
            for msg in self.warnings:
                sys.stderr.write("%s <2> %04d - Warning: %s\n" % (
                    filename, lino, msg))
            self.warnings = []  # warnings per line
        code.list(0, eos=True)
        if self.warnings_enabled:
            unused = sorted(self.symbols.get_unused())
            if unused:
                sys.stderr.write("Warning: Unreferenced constants: " + " ".join(unused) + "\n")
        return errors

    def autogens(self, code):
        """append code stanza for autogen constants"""

        def list_autogen(value, size, local_lc):
            label = size + "#" + value + ":"
            code.list(None, line=label.lower())
            code.list(None,
                      line="    %s %-5s   ; >%X" % (("data" if size == "W" else "byte"), value, int(value)),
                      text1=local_lc, text2=hex(int(value)).upper())

        if not self.symbols.autogens:
            return
        autogen_LC = code.symbols.LC
        code.segment(autogen_LC)
        code.list(0, line="> auto-generated constants")
        stashed_byte = None
        for value, size in self.symbols.autogens + [("-0", "B")]:  # add dummy element to flush stashed byte
            name = size + "#" + value
            if size == "B" and stashed_byte is None:
                stashed_byte = (name, value)  # can only generate words
                continue
            if size == "W":
                list_autogen(value, size, autogen_LC)
                code.code.append((autogen_LC, int(value), 0))
                self.symbols.add_symbol(name, autogen_LC)  # added once, since autogens elems are unique
            else:
                stashed_symbol, stashed_value = stashed_byte
                list_autogen(stashed_value, size, autogen_LC)
                self.symbols.add_symbol(stashed_symbol, autogen_LC)
                code.code.append((autogen_LC, (int(stashed_value) << 8) | int(value), 0))
                if value != "-0":  # ignore sentinel except for emitting
                    list_autogen(value, size, autogen_LC + 1)
                    self.symbols.add_symbol(name, autogen_LC + 1)
                stashed_byte = None
            autogen_LC += 2
        code.list(0, eos=True)

    def lwpi(self, op):
        """parse as iop, then set new WP in symbol table"""
        wp = self.expression(op, iop=True)
        self.symbols.wp = wp
        return wp

    def address(self, op):
        """parse general address into t-field, register, address value"""
        if op[0] == "@":  # memory addressing
            i = op.find("(")
            if i >= 0 and op[-1] == ")":
                register = self.register(op[i + 1:-1])
                if register == 0:
                    raise AsmError("Cannot index with register 0")
                offset = self.expression(op[1:i])
                if offset == 0:
                    self.warn("Using indexed address @0, could use *R instead")
                return 0b10, register, offset
            else:
                return 0b10, 0, self.expression(op[1:])
        elif op[0] == "*":  # indirect addressing
            if op[-1] == "+":
                return 0b11, self.register(op[1:-1]), None
            else:
                return 0b01, self.register(op[1:]), None
        elif op[:2] == "L#":  # LSB register access
            reg = self.register(op[2:])
            return 0b10, 0, self.symbols.wp + 2 * reg + 1
        elif op[:2] in ("B#", "W#"):  # auto-generated constant
            return 0b10, 0, self.expression(op)
        else:
            return 0b00, self.register(op), None

    def relative(self, op):
        """parse relative address (LC displacement)"""
        if self.pass_no == 1:
            return 0
        addr = self.expression(op)
        if isinstance(addr, Address):
            if addr.relocatable != self.symbols.reloc_LC:
                raise AsmError("Invalid relocatable address")
            addr = addr.addr
        # displacement on LC + 2
        disp = (addr - (self.symbols.effective_LC() + 2)) / 2
        if disp < -128 or disp > 127:  # word displacement
            raise AsmError("Out of range: " + op + " +/- " + hex(disp))
        return disp

    def expression(self, expr, well_defined=False, absolute=False,
                   relaxed=False, iop=False, allow_r0=False):
        """parse complex arithmetical expression"""
        if self.pass_no == 1 and not well_defined:
            return 0
        value, reloc_count = Word(0), 0
        terms = ["+"] + [tok.strip() for tok in
                         re.split(r"([-+*/])" if self.strict else
                                  r"([-+/%~&|^()]|\*\*?)", expr)]

        i, stack = 0, []
        while i < len(terms):
            op, term, negate, corr = terms[i], terms[i + 1], False, 0
            i += 2
            if op == ")":
                v, reloc = value.value, reloc_count
                value, reloc_count, op, negate, corr = stack.pop()
            else:
                # unary operators
                while not term and i < len(terms) and terms[i] in "+-~(":
                    term = terms[i + 1]
                    if terms[i] == "-":
                        negate = not negate
                    elif terms[i] == "~":
                        negate, corr = not negate, corr + (1 if negate else -1)
                    elif terms[i] == "(":
                        stack.append((value, reloc_count, op, negate, corr))
                        op, term, negate, corr = "+", terms[i + 1], False, 0
                        value, reloc_count = Word(0), 0
                    i += 2
                term_val, cross_bank_access = self.term(term, well_defined=well_defined,
                                                        iop=iop, relaxed=relaxed, allow_r0=allow_r0)
                if isinstance(term_val, Local):
                    dist = -term_val.distance if negate else term_val.distance
                    term_val = self.symbols.get_local(term_val.name, self.lidx, dist)
                    negate = False
                if term_val is None:
                    raise AsmError("Invalid expression: " + term)
                elif isinstance(term_val, Reference):
                    if len(terms) != 2 or well_defined:
                        raise AsmError("Invalid reference: " + expr)
                    return term_val
                elif isinstance(term_val, Address):
                    if (term_val.bank is not None and self.symbols.bank is not None and
                            term_val.bank != self.symbols.bank and not cross_bank_access):
                        raise AsmError("Invalid cross-bank access")
                        # NOTE: Jumping from bank into shared is safe, but shared into bank in general isn't.
                        #       But if we didn't allow shared to bank, we couldn't leave shared sections!
                    v, reloc = term_val.addr, 1 if term_val.relocatable else 0
                else:
                    v, reloc = term_val, 0

            if isinstance(v, DelayedAddress):
                if len(terms) > 2:
                    raise AsmError("Cannot use auto-generated constants in expressions")
                return v  # short cut for autogens

            w = Word((-v if negate else v) + corr)
            if op == "+":
                value.add(w)
                reloc_count += reloc if not negate else -reloc
            elif op == "-":
                value.sub(w)
                reloc_count -= reloc if not negate else -reloc
            elif op in "*/%":
                value.mul(op, w)
                if reloc_count > 0:
                    raise AsmError("Invalid address: " + expr)
            elif op in "&|^":
                value.bit(op, w)
                if reloc_count > 0:
                    raise AsmError("Cannot use relocatable address in expression: " + expr)
            elif op == "**":
                base, exp = Word(1), w.value
                for j in xrange(exp):
                    base.mul("*", value)
                value = base
            else:
                raise AsmError("Invalid operator: " + op)
        if not 0 <= reloc_count <= (0 if absolute else 1):
            raise AsmError("Invalid address: " + expr)
        return Address(value.value, self.symbols.bank, True) if reloc_count else value.value

    def term(self, op, well_defined=False, iop=False, relaxed=False, allow_r0=False):
        """parse constant or symbol"""
        cross_bank_access = False
        if op[0] == ">":
            return int(op[1:], 16), False
        elif op == "$":
            return Address(self.symbols.effective_LC(),
                           self.symbols.bank,
                           self.symbols.reloc_LC and not self.symbols.xorg_offset), False
        elif op[0] == ":":
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
                raise AsmError("Invalid text literal: " + c)
        elif op[0] == "!":
            m = re.match("(!+)(.*)", op)
            return Local(m.group(2), len(m.group(1))), False
        elif op[:2] == "W#" or op[:2] == "B#":
            v = self.symbols.add_autogen(op)
            return v, False
        elif op[0] == "#":
            # should have been eliminated by preprocessor
            raise AsmError("Invalid macro argument")
        else:
            if op[:2] == 'X#' and not self.strict:
                cross_bank_access = True
                op = op[2:]
            if iop and op in self.symbols.registers and not (op == "R0" and allow_r0):
                self.warn("Register %s used as immediate operand" % op)
            v = self.symbols.get_symbol(op[:6] if self.strict else op)
            if v is None and (self.pass_no > 1 or well_defined):
                if relaxed:
                    return 0, False
                else:
                    raise AsmError("Unknown symbol: " + op)
            return v, cross_bank_access

    def value(self, op):
        """parse well-defined value"""
        e = self.expression(op, well_defined=True)
        return e.addr if isinstance(e, Address) else e

    def register(self, op):
        """parse register"""
        if self.pass_no == 1:
            return 1  # don't return 0, as this is invalid for indexes @A(Rx)
        op = op.strip()
        if self.use_R and op[0].upper() != 'R':
            self.warn("Treating as register, did you intend an @address?")
        if op[0] == ">":
            r = int(op[1:], 16)
        elif op[0] == ":":
            return int(op[1:], 2)
        elif op.isdigit():
            r = int(op)
        else:
            r = self.symbols.get_symbol(op[:6] if self.strict else op)
            if r is None:
                raise AsmError("Unknown symbol: " + op)
        if not 0 <= r <= 15:
            raise AsmError("Invalid register: " + op)
        return r

    def bank(self, op):
        """parse bank: number or 'all'"""
        if op.isdigit():
            return int(op)
        elif op.lower() == "all":
            return None
        else:
            raise AsmError("Invalid bank value: " + op)

    def text(self, op):
        """parse single-quoted text literal or byte string"""
        s = op[1:].strip() if op[0] == "-" else op
        v = None
        try:
            if s[0] == ">":
                s0 = s + "0"
                v = "".join([chr(int(s0[i:i + 2], 16))
                             for i in xrange(1, len(s), 2)])
            elif s[0] == s[-1] == "'":
                v = self.text_literals[int(s[1:-1])] or '\x00'  # '' equals '\x00'
        except (IndexError, ValueError):
            pass
        if v is not None:
            return v[:-1] + chr(-ord(v[-1]) % 0x100) if op[0] == "-" else v
        else:
            raise AsmError("Invalid text literal: " + op)

    def filename(self, op):
        """parse double-quoted filename"""
        if not (len(op) >= 3 and op[0] == op[-1] == "'"):
            raise AsmError("Invalid filename: " + op)
        return self.text_literals[int(op[1:-1])]

    def is_literal(self, op):
        """check if operand is literal"""
        return op[0] == op[-1] == "'"

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

    def __init__(self, target="", optr=False, defs=None, includes=None,
                 strict=False, warnings=True):
        self.optr = optr  # -R specified
        self.defs = ["_xas99_" + target] + defs
        self.includes = includes  # list of include paths to search for COPY
        self.strict = strict  # -s specified
        self.warnings = warnings

    def assemble(self, path, srcname):
        symbols = Symbols(add_registers=self.optr, add_defs=self.defs)
        code = Objcode(symbols, self.strict)
        dummy = Objdummy(symbols)
        parser = Parser(symbols, path=path, includes=self.includes,
                        strict=self.strict, warnings=self.warnings,
                        use_R=self.optr)

        try:
            parser.open(srcname)
        except AsmError as e:
            raise IOError(1, e, srcname)
        errors = parser.parse(dummy, code)
        return code, errors


# Command line processing

def main():
    import argparse, zipfile

    args = argparse.ArgumentParser(
        description="TMS9900 cross-assembler, v" + VERSION)
    args.add_argument("source", metavar="<source>",
                      help="assembly source code")
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument("-b", "--binary", action="store_true", dest="bin",
                     help="create program binaries")
    cmd.add_argument("-i", "--image", action="store_true", dest="image",
                     help="create program image (E/A option 5)")
    cmd.add_argument("-c", "--cart", action="store_true", dest="cart",
                     help="create MESS cart image")
    cmd.add_argument("-t", "--text", dest="text", nargs="?", metavar="<format>",
                     help="create text file with binary values")
    cmd.add_argument("--embed-xb", action="store_true", dest="embed",
                     help="create Extended BASIC program with embedded code")
    cmd.add_argument("--jumpstart", action="store_true", dest="jstart",
                     help="create disk image for xdt99 Jumpstart cartridge")
    cmd.add_argument("--dump", action="store_true", dest="dump",
                     help=argparse.SUPPRESS)  # debugging
    args.add_argument("-s", "--strict", action="store_true", dest="strict",
                      help="strict TI mode; disable xas99 extensions")
    args.add_argument("-n", "--name", dest="name", metavar="<name>",
                      help="set program name, e.g., for cartridge")
    args.add_argument("-R", "--register-symbols", action="store_true", dest="optr",
                      help="add register symbols (TI Assembler option R)")
    args.add_argument("-C", "--compress", action="store_true", dest="optc",
                      help="compress object code (TI Assembler option C)")
    args.add_argument("-L", "--list-file", dest="optl", metavar="<file>",
                      help="generate list file (TI Assembler option L)")
    args.add_argument("-S", "--symbol-table", action="store_true", dest="opts",
                      help="add symbol table to listing (TI Assembler option S)")
    args.add_argument("-E", "--symbol-equs", dest="equs", metavar="<file>",
                      help="put symbols in EQU file")
    args.add_argument("-w", action="store_true", dest="nowarn",
                      help="hide warnings")
    args.add_argument("--base", dest="base", metavar="<addr>",
                      help="set base address for relocatable code")
    args.add_argument("-I", "--include", dest="inclpath", metavar="<paths>",
                      help="list of include search paths")
    args.add_argument("-D", "--define-symbol", nargs="+", dest="defs",
                      metavar="<sym=val>",
                      help="add symbol to symbol table")
    args.add_argument("-o", "--output", dest="output", metavar="<file>",
                      help="set output file name")
    opts = args.parse_args()

    # setup
    dirname = os.path.dirname(opts.source) or "."
    basename = os.path.basename(opts.source)
    barename = "stdin" if opts.source == "-" else os.path.splitext(basename)[0]
    name = opts.name or barename[:10].upper()
    inclpath = [dirname] + (opts.inclpath.split(",") if opts.inclpath else [])

    # assembly
    target = ("image" if opts.image else
              "cart" if opts.cart else
              "bin" if opts.bin else
              "xb" if opts.embed else
              "js" if opts.jstart else
              "obj")
    asm = Assembler(target=target,
                    optr=opts.optr,
                    defs=opts.defs or [],
                    includes=inclpath,
                    strict=opts.strict,
                    warnings=not opts.nowarn)
    try:
        code, errors = asm.assemble(dirname, basename)
    except IOError as e:
        sys.exit("File error: %s: %s." % (e.filename, e.strerror))

    # output
    out = []
    try:
        if errors:
            sys.stderr.write("".join(errors))
        elif opts.dump:
            sys.stdout.write(code.generate_dump())
        elif opts.cart:
            data, layout, metainf = code.generate_cartridge(name)
            output = opts.output or barename + ".rpk"
            with zipfile.ZipFile(output, "w") as archive:
                archive.writestr(name + ".bin", data)
                archive.writestr("layout.xml", layout)
                archive.writestr("meta-inf.xml", metainf)
        elif opts.bin:
            data, bank_count = code.generate_binaries(xint(opts.base) if opts.base else 0x0000)
            mid = ""
            for addr, bank, mem in data:
                if len(data) > 1:
                    mid = (("_%04x" % addr) +
                           ("_b%d" % bank if bank_count > 1 and bank is not None else ""))
                if opts.output:
                    name = "-" if opts.output == "-" else opts.output + mid
                else:
                    name = barename + mid + ".bin"
                out.append((name, mem))
        elif opts.image:
            data = code.generate_image(xint(opts.base) if opts.base else 0xa000)
            for i, image in enumerate(data):
                if opts.output:
                    name = "-" if opts.output == "-" else sinc(opts.output, i)
                else:
                    name = sinc(barename, i) + ".img"
                out.append((name, image))
        elif opts.text:
            data, bank_count = code.generate_binaries(xint(opts.base) if opts.base else 0x0000)
            name = opts.output or barename + ".dat"
            mode = opts.text.lower()
            text = code.generate_text(data, mode)
            out.append((name, text))
        elif opts.embed:
            prog = code.generate_XB_loader()
            name = opts.output or barename + ".iv254"
            out.append((name, prog))
        elif opts.jstart:
            disk = code.generate_jumpstart()
            name = opts.output or barename + ".dsk_id"
            out.append((name, disk))
        else:
            data = code.generate_object_code(opts.optc)
            name = opts.output or barename + ".obj"
            out.append((name, data))
        for name, data in out:
            writedata(name, data, "wb")
        if opts.optl:
            listing = code.generate_list(opts.opts)
            writedata(opts.optl, listing, "w")
        if opts.equs:
            writedata(opts.equs, code.generate_symbols(equ=True))
    except BuildError as e:
        sys.exit("Error: %s." % e)
    except IOError as e:
        sys.exit("File error: %s: %s." % (e.filename, e.strerror))

    # return status
    return 1 if errors else 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
