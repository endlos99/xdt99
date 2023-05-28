#!/usr/bin/env python3

# xcommon: Common utility functions for xdt99
#
# Copyright (c) 2015-2023 Ralph Benzinger <r@0x01.de>
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
import os
import re
import argparse
import glob
import platform


# xdt99 common assets

class CommandProcessor:
    """command line processor"""

    def __init__(self, exception=RuntimeError):
        """common variables"""
        self.exception = exception
        self.rc = 0
        self.opts = None
        self.barename = None
        self.name = None
        self.console = None
        self.result = []

    def main(self):
        """entry point"""
        try:
            self.parse() or self.run() or self.prepare()  # abort if one returns True
            self.output()  # outputs result and error messages
            return self.errors()
        except IOError as e:
            sys.exit(self.console.colstr(f'File error: {e.filename}: {e.strerror}'))
        except self.exception as e:
            sys.exit(self.console.colstr('Error: ' + str(e)))

    def parse(self):
        """syntax definition and parsing by argparse"""
        pass

    def run(self):
        """main action (assembly, disassembly, modification, ...)"""
        pass

    def prepare(self):
        """prepare result files depending on selected format"""
        pass

    def output(self):
        """output results and error messages"""
        for file in self.result:
            file.write(self.opts.output)  # default output name if not set explicitly before
        if self.console:
            self.console.print()

    def errors(self):
        """errors during processing?"""
        try:
            if self.console.errors:
                return 1
        except AttributeError:
            pass
        return self.rc

    def fix_greedy_list_parsing(self, main_name, *opts_names):
        """Greedy parsing of options with list arguments may add positional arguments to list options.
           As solution, lists may be terminated by trailing ';' after last list argument, e.g.:
              -I foo/ bar/ baz/;
              -D x=1 y=2 z=3 ;
           This function will split lists at this ';' and put the remaining arguments in opts.source.
        """
        main = getattr(self.opts, main_name, [])
        for opts_name in opts_names:
            opts_list = getattr(self.opts, opts_name)
            if opts_list is None:
                continue
            for i, arg in enumerate(opts_list):
                if arg[-1] == ';':
                    main.extend(opts_list[i + 1:])
                    opts_list = opts_list[:i]
                    if arg != ';':
                        opts_list.append(arg[:-1])
                    setattr(self.opts, opts_name, opts_list)
                    break
        setattr(self.opts, main_name, main)


class RFile:
    """wrapper for output file properties"""

    def __init__(self, data, name, ext='', suffix='', output=None, altname=None, istext=False):
        self.data = data
        self.name = name
        self.ext = ext
        self.suffix = suffix
        self.output = output
        self.altname = altname
        self.istext = istext

    def outname(self, output=None):
        return Util.outname(self.name, ext=self.ext, suffix=self.suffix, altname=self.altname,
                            output=self.output or output)

    def write(self, output=None, encoding=None):
        if self.output is None:
            self.output = output
        Util.writedata(self.outname(self.output), self.data, istext=self.istext, encoding=encoding)


class RContainer(RFile):
    """wrapper for output container or file"""

    def __init__(self, data, name, ext='', suffix='', output=None, altname=None, istext=False, iscontainer=False,
                 topc=False, tiname=False):
        super().__init__(data, name, ext=ext, suffix=suffix, output=output, altname=altname, istext=istext)
        self.iscontainer = iscontainer
        self.topc = topc  # convert name to PC name ...
        self.tiname = tiname  # ... or use TI-style name without extension

    def outname(self, output=None):
        if self.topc:
            if self.tiname:
                self.name = self.name.upper()
                self.ext = ''
            else:
                self.name = self.name.lower()
        return super().outname(output)

    def write(self, output=None, encoding=None):
        # remove path to create local files, unless the original container should be overwritten
        if not self.iscontainer or output or self.output:
            self.name = os.path.basename(self.name)
        super().write(output=output, encoding=encoding)

    @staticmethod
    def create_for_stdout(file, encoding):
        """simplify creating text or binary result file for STDOUT"""
        if file.is_display() and encoding:
            return RContainer(file.get_contents(), '-', istext=True)
        else:
            return RContainer(file.get_contents(), '-')


class GlobStore(argparse.Action):
    """argparse globbing for Windows platforms"""

    def __call__(self, parser, namespace, values, option_string=None):
        if os.name == 'nt':
            names = [glob.glob(fn) if '*' in fn or '?' in fn else [fn] for fn in values]
            values = [f for n in names for f in n]
        setattr(namespace, self.dest, values)


class Warnings:
    """warning categories and which ones to suppress"""

    DEFAULT = 0
    OPTIMIZATIONS = 1
    BAD_USAGE = 2
    UNUSED_SYMBOLS = 3
    ARITH = 4
    ALLOCATION = 5
    GEOMETRY = 6
    IMAGE = 7
    _MAX = 8

    def __init__(self, warnings=None, none=False, setall=False):
        """set state for warning categories"""
        if none:
            self._warnings = {warn: False for warn in warnings}
        elif setall:
            self._warnings = {warn: True for warn in range(Warnings._MAX)}
        else:
            self._warnings = warnings  # initial state
        self.warnings = dict(self._warnings)  # current state

    def set(self, warning=DEFAULT, value=False, setall=None):
        """enable or disable one or all warnings"""
        if setall is not None:
            self.warnings = {warn: setall for warn in self.warnings}
        else:
            self.warnings[warning] = value

    def reset(self):
        """copy current warning settings"""
        self.warnings = dict(self._warnings)

    def __getitem__(self, category):
        try:
            return self.warnings[category]
        except KeyError:
            return False


class Console:
    """collects errors and warnings"""

    INFO = 0  # also equals severity
    WARNING = 1
    ERROR = 2

    def __init__(self, tool, version, warnings=None, colors=None, verbose=False):
        self.tool = tool
        self.version = version
        self.verbose = verbose
        if warnings:
            self.warnings = warnings
        else:
            self.warnings = Warnings({Warnings.DEFAULT: True})
        self.console = []
        self.filename = None
        self.errors = False
        self.entries = False
        self.print_version = True  # should version info be printed
        if colors is None:
            if os.environ.get('TERM') == 'dumb':  # $TERM=dumb indicates user wants no color
                self.colors = False
            else:
                self.colors = sys.stderr.isatty() and platform.system() in ('Linux', 'Darwin')  # no auto color on Win
        else:
            self.colors = colors == 'on'

    def reset(self):
        """clear errors and warnings"""
        self.console = []
        self.errors = self.entries = False
        self.print_version = False

    def reset_warnings(self):
        """reset enabled warnings"""
        self.warnings.reset()

    def info(self, info, message, category=Warnings.DEFAULT):
        """informational message, if verbose and enabled"""
        if not self.verbose or not self.warnings[category]:
            return
        self._add((Console.INFO, info, message, category))

    def warn(self, info, message, category=Warnings.DEFAULT):
        """warnings message, if enabled"""
        if not self.warnings[category]:
            return
        self._add((Console.WARNING, info, message, category))
        self.entries = True

    def error(self, info, message):
        """error message"""
        self._add((Console.ERROR, info, message, None))
        self.entries = self.errors = True

    def _add(self, entry):
        """prevent duplicate messages for same line"""
        if self.console and self.console[-1] == entry:
            return
        self.console.append(entry)

    def clear(self, category):
        """clear errors or warnings of given category"""
        self.console = [(kind, info, message, cat)
                        for (kind, info, message, cat) in self.console if cat != category]
        self.entries = any(self.console)
        self.errors = any(kind for (kind, *_) in self.console if kind == Console.ERROR)

    def merge(self, console):
        """merge other console into self"""
        self.console.extend(console.console)
        if console.errors:
            self.errors = True
        if console.entries:
            self.entries = True

    def _color(self, severity):
        """return ANSI color string"""
        if not self.colors:
            return ''
        elif severity == Console.INFO:
            return '\x1b[0m'  # reset to normal
        elif severity == Console.WARNING:
            return '\x1b[33m'  # yellow
        elif severity == Console.ERROR:
            return '\x1b[31m'  # red
        else:
            return ''

    def colstr(self, s, severity=ERROR):
        """wrap string in color"""
        return self._color(severity) + s + self._color(0)

    def print(self):
        """print all console error and warning messages to stderr"""
        if not self.console:
            return
        if self.version and self.print_version:
            sys.stderr.write(f': {self.tool}, version {self.version}\n')
        for severity, info, message, _ in self.console:
            if info:
                sys.stderr.write(info + '\n')
            sys.stderr.write(self._color(severity) + message + self._color(0) + '\n')
        error_count = sum(1 for kind, *_ in self.console if kind == Console.ERROR)
        if error_count == 1:
            sys.stderr.write('1 Error found.\n')
        elif error_count > 1:
            sys.stderr.write(f'{error_count} Errors found.\n')


class Util:
    """common utility function"""

    # constants for readdata and writedata
    TEXT = True
    BINARY = False

    @staticmethod
    def even(n):
        """round value down to even value"""
        return n - n % 2

    @staticmethod
    def align(addr, base=0x2000):
        """align addr to n * base"""
        return addr - addr % base

    @staticmethod
    def ordw(word):
        """word ord"""
        return (word[0] << 8) | word[1]

    @staticmethod
    def rordw(word):
        """reverse word ord"""
        return word[1] << 8 | word[0]

    @staticmethod
    def rordl(word):
        """reverse long ord"""
        return word[3] << 24 | word[2] << 16 | word[1] << 8 | word[0]

    @staticmethod
    def chrw(word):
        """word chr"""
        return bytes((word >> 8, word & 0xff))

    @staticmethod
    def rchrw(word):
        """reverse word chr"""
        return bytes((word & 0xff, word >> 8))

    @staticmethod
    def ordn(bytes_):
        """convert byte sequence into value"""
        value = 0
        for b in bytes_:
            value = (value << 8) + b
        return value

    @staticmethod
    def chrn(value, size=2):
        """convert value into byte sequence"""
        return bytes(((value >> ((i - 1) * 8)) & 0xff) for i in range(size, 0, -1))

    @staticmethod
    def bval(bytes_):
        """n-length ord"""
        return [b for b in bytes_]

    @staticmethod
    def pad(n, m):
        """return increment to next multiple of m"""
        return -n % m

    @staticmethod
    def xint(s):
        """return hex or decimal value"""
        if s is None:
            return 0
        elif s[:2] == '0x':
            return int(s[2:], 16)
        elif s[:1] == '>':
            return int(s[1:], 16)
        else:
            return int(s)

    @staticmethod
    def trunc(i, m):
        """round integer down to multiple of m"""
        return i - i % m

    @staticmethod
    def top(i, m):
        """round integer up to multiple of m"""
        return i + -i % m

    @staticmethod
    def used(n, m):
        """integer division rounding up"""
        return (n + m - 1) // m

    @staticmethod
    def upmod(n, mod):
        """modulo, but 1..mod"""
        return n % mod or mod

    @staticmethod
    def chop(s, n):
        """generator that produces n-sized parts of s"""
        while True:
            part, s = s[:n], s[n:]
            if not part:
                break
            yield part

    @staticmethod
    def flatten(list_of_lists):
        """flattens listing of lists into listing"""
        return [item for list_ in list_of_lists for item in list_]

    @staticmethod
    def escape(bytes_):
        """escape non-printable characters"""
        bytes_ = bytes_.replace(b"'", b"''")
        return "'" + ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_) + "'"

    @staticmethod
    def name_suffix(base=None, bank=None, use_base=False, bank_count=0, max_bank=0):
        bank_len = len(str(max_bank))  # avoid log()ing ...
        return (('' if not use_base else f'_{base:04x}') +
                ('' if bank is None or bank_count <= 1 else f'_b{bank:0{bank_len}d}'))

    @staticmethod
    def barename(path):
        """return filename without path and extension"""
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def outname(basename, ext, suffix='', output=None, altname=None):
        """return output filename"""
        if output == '-':
            return output
        filename = basename + suffix + ext
        if output is None:
            return filename
        if os.path.isdir(output):
            return os.path.join(output, filename)
        if suffix:
            filename, ext = os.path.splitext(output)
            return filename + suffix + ext
        return altname or output

    @staticmethod
    def tiname(s, n=0):
        """create TI filename from local filename"""
        return 'STDIN' if s == '-' else Util.to_ti(os.path.splitext(os.path.basename(s))[0][:10].upper(), n)

    @staticmethod
    def pcname(name, ext='', tiname=False):
        """return upper or lower case name"""
        n = Util.to_pc(name)
        return n.upper() if tiname else n.lower() + ext

    @staticmethod
    def to_pc(n):
        """escaoe TI filename for PC"""
        return None if n is None else n.replace('/', '.')

    @staticmethod
    def to_ti(s, n=0):
        """escape PC name for TI"""
        return None if s is None else Util.strseq(s.replace('.', '/'), n)

    @staticmethod
    def strseq(s, n):
        """create nth string in sequence by increasing last char"""
        return s[:-1] + chr(ord(s[-1]) + n)

    @staticmethod
    def sinc(s, i):
        """string sequence increment"""
        return None if s is None else s[:-1] + chr(ord(s[-1]) + i)

    @staticmethod
    def readdata(filename, astext=False, encoding=None):
        """read data from file or STDIN or return supplied data
           Since many TI text files also contain >=128 chars, text files must have an encoding.
        """
        if astext and encoding:  # many text files
            if filename == '-':
                data = sys.stdin.read()
            else:
                with open(filename, 'r') as f:
                    data = f.read()
            try:
                data = data.encode(encoding)
            except UnicodeEncodeError:
                sys.exit('Bad encoding: ' + encoding)
        else:
            if filename == '-':
                data = sys.stdin.buffer.read()
            else:
                with open(filename, 'rb') as f:
                    data = f.read()
        return data

    @staticmethod
    def writedata(filename, data, istext=False, encoding=None):
        """write data to file or STDOUT
           if text and encoding is provided: encode text and output as binary
           otherwise:                        output text and binary as is
        """
        if istext and encoding:
            try:
                data = data.encode(encoding)
            except UnicodeEncodeError:
                sys.exit('Bad encoding: ' + encoding)
            istext = False
        if istext:
            if filename == '-':
                sys.stdout.write(data)
            else:
                with open(filename, 'w') as f:
                    f.write(data)
        else:
            if filename == '-':
                sys.stdout.buffer.write(data)
            else:
                with open(filename, 'wb') as f:
                    f.write(data)

    @staticmethod
    def readlines(filename):
        """read lines from file or STDIN"""
        if filename == '-':
            return sys.stdin.readlines()
        else:
            with open(filename, 'r') as f:
                return f.readlines()

    @staticmethod
    def glob(container, patterns):
        """glob files"""
        wildcards = [pattern for pattern in patterns if re.search(r'[?*]', pattern)]
        glob_re = '|'.join(re.escape(p).replace(r'\*', '.*').replace(r'\?', '.')
                           for p in wildcards) + '$'
        matches = [name for name in container.catalog if re.match(glob_re, name)]
        plains = [pattern for pattern in patterns if pattern not in wildcards]
        return matches + plains

    @staticmethod
    def get_opts_list(args):
        """get items from space and comma seperated list"""
        if args is None:
            return []
        else:
            return [item for arg in args for item in arg.split(',')]
