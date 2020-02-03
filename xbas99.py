#!/usr/bin/env python

# xbas99: TI BASIC and TI Extended BASIC tool
#
# Copyright (c) 2015-2020 Ralph Benzinger <xdt99@endlos.net>
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
import os.path


VERSION = '3.0.0'


# Utility functions

def ordw(word):
    """word ord"""
    return (word[0] << 8) | word[1]


def chrw(word):
    """word chr"""
    return bytes((word >> 8, word & 0xff))


def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip('>'), 16 if s[:2] == '0x' or s[:1] == '>' else 10)


def trunc(i, m):
    """round integer down to multiple of m"""
    return i - i % m


def sinc(s, i):
    """string sequence increment"""
    return s[:-1] + chr(ord(s[-1]) + i)


def readdata(filename, lines=False):
    """read data from file or STDIN (or return supplied data)"""
    if filename == '-':
        if lines:
            return sys.stdin.readlines()
        else:
            return sys.stdin.buffer.read()
    else:
        with open(filename, 'r' if lines else 'rb') as f:
            return f.readlines() if lines else f.read()


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


# Error handling

class BasicError(Exception):
    pass


# Tokens

class Tokens:
    """TI BASIC and TI Extended BASIC tokens"""

    # follow token types
    VAR = 0  # variable (default)
    QSTR = 1  # quoted string
    USTR = 2  # unquoted string
    LINO = 3  # line number
    COMMENT = 4  # comments
    IMAGE_STR = 5  # quoted or unquoted string line for IMAGE stmts
    DATA_STR = 6  # special case: DATA operands
    KEEP = 7  # keep previous follow token type
    GO_PREF = 8  # GO prefix

    # unused token code for escaping statement separator '::'
    QS_VAL = 0xc7  # token value for quoted string
    US_VAL = 0xc8  # token value for unquoted string
    LINO_VAL = 0xc9  # token value for line number
    STMT_SEP = '\xaf'  # token representation of :: stmt separator

    # token listing
    tokenlist = [
        ('ELSE ', LINO), (STMT_SEP + ' ', VAR), ('!', COMMENT), ('IF ', VAR),
        ('GO ', GO_PREF), ('GOTO ', LINO), ('GOSUB ', LINO), ('RETURN ', LINO),
        ('DEF ', VAR), ('DIM ', VAR), ('END ', VAR), ('FOR ', VAR),
        ('LET ', VAR), ('BREAK ', LINO), ('UNBREAK ', LINO), ('TRACE ', VAR),
        ('UNTRACE ', VAR), ('INPUT ', VAR), ('DATA ', DATA_STR),
        ('RESTORE ', LINO), ('RANDOMIZE ', VAR), ('NEXT ', VAR),
        ('READ ', VAR), ('STOP ', VAR), ('DELETE ', VAR), ('REM', COMMENT),
        ('ON ', VAR), ('PRINT ', VAR), ('CALL ', USTR), ('OPTION ', VAR),
        ('OPEN ', VAR), ('CLOSE ', VAR), ('SUB ', USTR), ('DISPLAY ', VAR),
        ('IMAGE ', IMAGE_STR), ('ACCEPT ', VAR), ('ERROR ', LINO),
        ('WARNING ', VAR), ('SUBEXIT ', VAR), ('SUBEND ', VAR), ('RUN ', LINO),
        ('LINPUT ', VAR), (None, None), (None, None), (None, None),
        (None, None), (None, None), ('THEN ', LINO), ('TO ', VAR),
        ('STEP ', VAR), (',', KEEP), (';', VAR), (':', VAR), (')', VAR),
        ('(', VAR), ('&', VAR), (None, None), ('OR', VAR), ('AND', VAR),
        ('XOR', VAR), ('NOT', VAR), ('=', VAR), ('<', VAR), ('>', VAR),
        ('+', VAR), ('-', VAR), ('*', VAR), ('/', VAR), ('^', VAR),
        (None, None), ('qs', None), ('us', None), ('ln', None), ('EOF', VAR),
        ('ABS', VAR), ('ATN', VAR), ('COS', VAR), ('EXP', VAR), ('INT', VAR),
        ('LOG', VAR), ('SGN', VAR), ('SIN', VAR), ('SQR', VAR), ('TAN', VAR),
        ('LEN', VAR), ('CHR$', VAR), ('RND', VAR), ('SEG$', VAR), ('POS', VAR),
        ('VAL', VAR), ('STR$', VAR), ('ASC', VAR), ('PI', VAR), ('REC', VAR),
        ('MAX', VAR), ('MIN', VAR), ('RPT$', VAR), (None, None), (None, None),
        (None, None), (None, None), (None, None), (None, None),
        ('NUMERIC', VAR), ('DIGIT', VAR), ('UALPHA', VAR), ('SIZE', VAR),
        ('ALL', VAR), ('USING ', LINO), ('BEEP', VAR), ('ERASE', VAR),
        ('AT', VAR), ('BASE', VAR), (None, None), ('VARIABLE', VAR),
        ('RELATIVE', VAR), ('INTERNAL', VAR), ('SEQUENTIAL', VAR),
        ('OUTPUT', VAR), ('UPDATE', VAR), ('APPEND', VAR), ('FIXED', VAR),
        ('PERMANENT', VAR), ('TAB', VAR), ('#', VAR), ('VALIDATE', VAR),
        (None, None)
        ]

    tokens = {w.strip(): (bytes((0x81 + i,)), t)
              for i, (w, t) in enumerate(tokenlist) if w is not None}
    literals = {0x81 + i: (w, t) for i, (w, t) in enumerate(tokenlist)}

    @classmethod
    def token(cls, tok):
        """get BASIC token for text literal"""
        try:
            return cls.tokens[tok.upper()]
        except KeyError:
            return None, None

    @classmethod
    def qstr_token(cls, s):
        """return quoted string token"""
        try:
            return bytes((cls.QS_VAL,)) + bytes((len(s),)) + s.encode('ascii')
        except UnicodeEncodeError:
            raise BasicError('Cannot include non-ASCII characters in program')

    @classmethod
    def ustr_token(cls, s):
        """return unquoted string token"""
        try:
            return bytes((cls.US_VAL,)) + bytes((len(s),)) + s.encode('ascii')
        except UnicodeEncodeError:
            raise BasicError('Cannot include non-ASCII characters in program')

    @classmethod
    def lino_token(cls, s):
        """return line number token"""
        try:
            lino = int(s)
        except ValueError:
            lino = 0
        if not 1 <= lino <= 32767:
            raise BasicError(f'Invalid line number: {s}')
        return bytes((cls.LINO_VAL,)) + chrw(lino)

    @classmethod
    def literal(cls, tokens):
        """return textual representation of BASIC token(s)"""
        lit_type, _ = cls.literals[tokens[0]]
        try:
            if lit_type == 'qs':
                lit_value = tokens[1]
                return '"' + tokens[2:2 + lit_value].decode('ascii').replace('"', '""') + '"', lit_type, lit_value + 2
            elif lit_type == 'us':
                lit_value = tokens[1]
                return tokens[2:2 + lit_value].decode('ascii'), lit_type, lit_value + 2
            elif lit_type == 'ln':
                return str(ordw(tokens[1:3])), lit_type, 3
            else:
                return lit_type, None, 1  # for all other cases, lit_type == token
        except UnicodeDecodeError:
            raise BasicError('Non-ASCII characters found in program')


# BASIC Program

class BasicProgram:

    # maximum number of bytes/tokens per BASIC line
    max_tokens_per_line = 254

    def __init__(self, data=None, source=None, long_fmt=False, labels=False):
        self.labels = labels
        self.lines = {}
        self.label_lino = {}
        self.text_literals = []
        self.rem_literals = []
        self.errors = []
        self.curr_lino = 100
        if data is not None:
            # get source from token stream
            try:
                self.load(data, long_fmt)
            except IndexError:
                self.error('Cannot read program file')
        elif source is not None:
            # get token stream from source
            if labels:
                source = self.get_labels(source)
            self.parse(source)

    def error(self, text):
        """add error message"""
        if text not in self.errors:
            self.errors.append(text)

    # convert program to source
    def load(self, data, long_fmt):
        """load tokenized BASIC program"""
        if long_fmt or data[1:3] == b'\xab\xcd':
            # convert long format INT/VAR 254 to PROGRAM
            program = []
            idx = 11
            while idx < len(data):
                n = data[idx] + 1
                program.append(data[idx + 1:idx + n])
                idx += n
            data = b'XX' + data[5:7] + data[3:5] + b'XX' + b''.join(program)
        # extract line number table and token table
        ptr_tokens = ordw(data[2:4]) + 1
        ptr_line_numbers = ordw(data[4:6])
        no_lines = (ptr_tokens - ptr_line_numbers) // 4
        line_numbers = data[8:8 + no_lines * 4]
        tokens = data[8 + no_lines * 4:]
        # process line token table
        for i in range(no_lines):
            lino = ordw(line_numbers[4 * i:4 * i + 2])
            ptr = ordw(line_numbers[4 * i + 2:4 * i + 4])
            j = ptr - 1 - ptr_tokens
            line_len = tokens[j]
            if tokens[j + line_len]:
                self.error('Missing line termination')
            self.lines[lino] = tokens[j + 1:j + line_len]

    def merge(self, data):
        """load tokenized BASIC program in merge format
           Merge format is stored as DIS/VAR 254, even though the data is binary, and
           type INT/VAR 254 would be more appropriate.  The problem with DISPLAY is that
           we must recognize the record terminator, which differs by platform: Linux
           and MacOS use \n, whereas Windows uses \r\n.  We will ignore older platforms
           which might use \r and \n\r.  Luckily, records are terminated by 0, so the
           locations of record terminators are known.
        """
        idx = 0
        while idx < len(data):
            lino = ordw(data[idx:idx + 2])
            if lino == 0xffff:
                break
            mark_idx = idx = idx + 2
            while data[idx]:
                if data[idx] == Tokens.QS_VAL or data[idx] == Tokens.US_VAL:
                    idx += 1 + data[idx + 1] + 1
                elif data[idx] == Tokens.LINO_VAL:
                    idx += 3
                else:
                    idx += 1
            self.lines[lino] = data[mark_idx:idx]
            if data[idx + 1:idx + 2] == b'\n':
                idx += 2
            elif data[idx + 1:idx + 3] == b'\r\n':  # \r must be start of \r\n
               idx += 3
            else:
                self.error('Missing line termination')

    def get_source(self):
        """return textual representation of token sequence"""
        text = [' ']  # dummy element
        for lino, tokens  in sorted(self.lines.items()):
            text.append(f'{lino:d} ')
            softspace = False
            idx = 0
            while idx < len(tokens):
                save_idx = idx
                while idx < len(tokens) and tokens[idx] <= 0x80:
                    idx += 1
                if idx > save_idx:
                    try:
                        text.append((' ' if softspace else '') + tokens[save_idx:idx].decode('ascii'))
                    except UnicodeDecodeError:
                        raise BasicError('Non-ASCII characters found in program')
                    softspace = True
                else:
                    lit, lit_type, n = Tokens.literal(tokens[idx:])
                    # try to mimic TI BASIC's seemingly random distribution of spaces
                    is_text = lit[0] in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + Tokens.STMT_SEP) and lit_type is None
                    if (((is_text or lit == '#' or lit_type == 'us' or lit_type == 'ln') and softspace) or
                            (lit == ':' and text[-1][-1] == ':') or
                            (lit == '!' and text[-1][-1] != ' ')):
                        text.append(' ' + lit)
                    else:
                        text.append(lit)
                    softspace = ((is_text and lit[-1] != ' ' and lit != 'REM') or
                                 (lit_type == 'us' or lit_type == 'qs' or lit_type == 'ln'))
                    idx += n
            text.append('\n')
        return self.fix_colons(''.join(text[1:]))

    @staticmethod
    def fix_colons(text):
        """fix spacing of : and :: tokens"""
        text_1 = text.replace(':' + Tokens.STMT_SEP, ': ::')
        text_2 = text_1.replace(Tokens.STMT_SEP, '::')
        return text_2

    # source -> program

    def get_labels(self, lines):
        """gather all label definitions, return remaining lines"""
        remaining = []
        self.curr_lino = 100
        for i, line in enumerate(lines):
            if not line.rstrip():
                continue
            m = re.match(r'(\w+):$', line)
            if m:
                self.label_lino[m.group(1)] = self.curr_lino, False  # lino x used
            else:
                if not line[:1].isspace():
                    raise BasicError(f'Missing indention in line {i + 1}')
                remaining.append(line)
                self.curr_lino += 10
        return remaining

    def parse(self, lines):
        """parse and tokenize BASIC source"""
        self.curr_lino = 100
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                lino, tokens = self.line(line)
                if lino is not None:  # None for label definitions
                    self.lines[lino] = tokens
            except BasicError as e:
                self.error(f'[{i + 1:d}] {line}\nError: {str(e):}')
            self.curr_lino += 10

    def line(self, line):
        """parse single BASIC line"""
        text = self.escape(line.rstrip())
        if self.labels:
            lino = self.curr_lino
            tokens = self.statements(text.lstrip())
        else:
            m = re.match(r'(\d+)\s+(.+)', text)
            if not m:
                raise BasicError('Missing line number')
            lino = int(m.group(1))
            tokens = self.statements(m.group(2))
        if len(tokens) > BasicProgram.max_tokens_per_line:
            raise BasicError('Line too long')
        return lino, tokens

    def statements(self, text):
        """parse one or more BASIC statements"""
        sep, _ = Tokens.tokens[',']
        tokens = []
        # poorest man imaginable's lexer
        parts = re.split(r'(\s+|"\d+"|[0-9.]+[Ee]-[0-9]+|[!,;:()&=<>+\-*/^#' + Tokens.STMT_SEP + r'])', text)
        tok_type = Tokens.VAR
        for i, word in enumerate(parts):
            uword = word.upper()  # keywords and vars are case-insensitive, but not DATA, IMAGE, REM, ...
            if tok_type == Tokens.COMMENT:
                try:
                    tokens.append(self.unescape(''.join(parts[i:])).encode('ascii'))
                except UnicodeEncodeError:
                    raise BasicError('Non-ASCII character found in comment')
                break
            if not word.strip():
                continue
            if tok_type == Tokens.GO_PREF and uword in ('TO', 'SUB'):  # following 'GO' token
                token, _ = Tokens.token(uword)
                tokens.append(token)
                tok_type = Tokens.LINO
                continue
            if tok_type == Tokens.LINO:
                if word[0] == '@' and word[1:].isalnum():  # label
                    try:
                        label_lino, used = self.label_lino[uword[1:]]
                        word = str(label_lino)
                        if not used:
                            self.label_lino[uword[1:]] = word, True
                    except KeyError:
                        raise BasicError(f'Unknown label {word[1:]}')
                if word[0] == word[-1] == '"':
                    tok_type = Tokens.QSTR
                elif word.isdigit():
                    tokens.append(Tokens.lino_token(word))
                    tok_type = Tokens.LINO  # falls back to VAR, if no match
                    continue
                # fall-through to QSTR or VAR case
            if tok_type == Tokens.IMAGE_STR:
                remaining = ''.join(parts[i:]).strip()
                if remaining:
                    tokens.append(self.qstr(remaining) if remaining[0] == '"' else
                                  self.ustr(remaining))
                break
            if tok_type == Tokens.DATA_STR:
                remaining = [s.strip() for s in ''.join(parts[i:]).split(',')]
                data = [(self.qstr(s) if s[0] == '"' else self.ustr(s)) if s else b'' for s in remaining]
                tokens.append(sep.join(data))
                break
            if tok_type == Tokens.QSTR or word[0] == '"':  # keep before USTR!
                # NOTE: there is actually no token with follow token QSTR
                tokens.append(self.qstr(word))
                tok_type = Tokens.VAR
                continue
            if tok_type == Tokens.USTR:
                tokens.append(self.ustr(uword))
                tok_type = Tokens.VAR
                continue

            # VAR base case
            token, follow = Tokens.token(uword)
            if token:  # keywords and operators
                tokens.append(token)
            elif re.match(r'[0-9.]+', word):  # number literals
                tokens.append(self.ustr(uword))
            else:
                try:
                    tokens.append(uword.encode('ascii'))  # plain VARs
                except UnicodeEncodeError:
                    raise BasicError('Non-ASCII character found in variable name')
            if follow != Tokens.KEEP:
                tok_type = follow
        return tokens

    def escape(self, text):
        """remove and save ambiguous constructs from line"""
        # substitute text literals
        parts = re.split(r'("(?:[^"]|"")*")', text)
        lits = [s[1:-1].replace('""', '"') for s in parts[1::2]]
        parts[1::2] = ['"' + str(len(self.text_literals) + i) + '"' for i in range(len(lits))]
        self.text_literals.extend(lits)
        return ''.join(parts).replace('::', Tokens.STMT_SEP)

    def unescape(self, text):
        """rebuild original text from escaped string"""
        return re.sub(r'"(\d+)"',
                      lambda m: '"' + self.text_literals[int(m.group(1))] + '"',
                      self.fix_colons(text))

    def qstr(self, lit):
        """build quoted string token sequence"""
        try:
            s = self.text_literals[int(lit[1:-1])]
            return Tokens.qstr_token(s)
        except (ValueError, IndexError):
            raise RuntimeError('Invalid text literal id ' + lit[1:-1])

    def ustr(self, lit):
        """build unquoted string token sequence"""
        return Tokens.ustr_token(self.unescape(lit))

    def get_image(self, long_fmt=False, protected=False):
        """create PROGRAM image from tokens"""
        last_addr = 0xffe8 if long_fmt else 0x37d8
        program = []
        idx = 0
        if long_fmt:
            size = sum(len(self.lines[i]) for i in self.lines) + 2 * len(self.lines)
            if size < 254:
                self.error('Program too short, will pad')
                pad_len = 254 - size
                program.append((0, 32767, bytes((pad_len - 1, 0x83)) + b'\x21' * (pad_len - 3) + bytes(1)))
                idx = pad_len
        for lino, tokens in sorted(self.lines.items(), reverse=True):
            token_bytes = b''.join(tokens)
            program.append((idx, lino, bytes((len(token_bytes) + 1,)) + token_bytes + bytes(1)))
            idx += len(token_bytes) + 2
        token_tab_addr = last_addr - idx
        lino_tab_addr = token_tab_addr - 4 * len(program)
        token_table = b''.join(tokens for p, lino, tokens in program)
        lino_table = b''.join(chrw(lino) + chrw(token_tab_addr + i + 1) for i, lino, _ in program)
        checksum = (token_tab_addr - 1) ^ lino_tab_addr
        assert lino_tab_addr + len(lino_table) + len(token_table) == last_addr
        if protected:
            checksum = -checksum % 0x10000
        if long_fmt:
            header = (b'\xab\xcd' + chrw(lino_tab_addr) + chrw(token_tab_addr - 1) +
                      chrw(checksum) + chrw(last_addr - 1))
            chunks = [(lino_table + token_table)[i:i + 254]
                      for i in range(0, len(lino_table + token_table), 254)]
            return (bytes((len(header),)) + header +
                    b''.join(bytes((len(c),)) + c for c in chunks))
        else:
            header = (chrw(checksum) + chrw(token_tab_addr - 1) +
                      chrw(lino_tab_addr) + chrw(last_addr - 1))
            return header + lino_table + token_table

    def dump_tokens(self):
        """dump pretty-printed token stream sorted by line number"""
        lines = []
        line, _ = Tokens.tokens['ln']
        ssep, _ = Tokens.tokens[Tokens.STMT_SEP]
        for lino in sorted(self.lines):
            tokens = self.lines[lino]
            result = []
            idx = 0
            while idx < len(tokens):
                t = tokens[idx]
                if t < 32:
                    result.append(f'#{t:d}')
                elif t <= 0x80:
                    result.append(t.decode())
                elif t == line:
                    result.append('^' + str(ordw(tokens[idx + 1:idx + 3])))
                    idx += 2
                elif t == ssep:
                    result.append('::')
                else:
                    result.append(Tokens.literals[t][0].rstrip())
                idx += 1
            lines.append('{:d}: {:s}\n'.format(lino, ' '.join(result)))
        return ''.join(lines)

    @staticmethod
    def join(lines, max_line_delta=3, max_lino_delta=100):
        """join split source lines heuristically"""
        joined_lines = []  # lino x line
        delta_line = 0
        prev_lino = None  # lino of last appended line
        # TODO: for optimal results, use proper backtracking
        for line in lines:
            if not line.strip():
                prev_lino = None
                continue
            m = re.match('(\d+)\s+', line)  # check for line number at start of line
            if not m:
                if prev_lino is None:
                    # we might backtrack here to increase parser robustness
                    raise BasicError('Cannot find start of program')
                else:
                    # merge current and last stored line
                    last_lino, last_line = joined_lines[-1]
                    joined_lines[-1] = last_lino, last_line + line
                    delta_line += 1
            else:
                lino = int(m.group(1))
                if (prev_lino is None or
                        prev_lino < lino <= prev_lino + max_lino_delta or
                        delta_line + 1 > max_line_delta):
                    # store current line
                    joined_lines.append((lino, line))
                    delta_line = 0
                    prev_lino = lino
                elif (len(joined_lines) > 2 and
                        lino - max_lino_delta <= joined_lines[-2][0] < lino <= prev_lino):
                    # merge last two lines stored
                    (llast_lino, llast_line), (_, last_line) = joined_lines[-2:]
                    joined_lines[-2] = llast_lino, llast_line + last_line
                    joined_lines[-1] = lino, line
                else:
                    # merge current and last stored line
                    last_lino, last_line = joined_lines[-1]
                    joined_lines[-1] = last_lino, last_line + line
                    delta_line += 1
        return [line for lino, line in joined_lines]

    def get_unused_labels(self):
        """return list of labels not referenced"""
        return [label for label, (lino, used) in self.label_lino.items() if not used]


# Command line processing

def main():
    import argparse

    args = argparse.ArgumentParser(description='TI BASIC and TI Extended BASIC tool, v' + VERSION)
    args.add_argument('source', metavar='<source>', help='TI BASIC or TI Extended BASIC program')
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument('-c', '--create', action='store_true', dest='create',
                     help='create TI (Extended) BASIC program file (default)')
    cmd.add_argument('-d', '--decode', action='store_true', dest='decode',
                     help='decode TI (Extended) BASIC program')
    cmd.add_argument('-p', '--print', action='store_true', dest='print',
                     help='print decoded TI (Extended) BASIC program')
    cmd.add_argument('--dump', action='store_true', dest='dump',
                     help=argparse.SUPPRESS)
    args.add_argument('-l', '--labels', action='store_true', dest='labels',
                      help='use labels instead of line numbers')
    args.add_argument('--protect', action='store_true', dest='protect',
                      help='listing-protect program')
    args.add_argument('--merge', action='store_true', dest='merge',
                      help='use merge format')
    args.add_argument('-L', '--long', action='store_true', dest='long_',
                      help='force long program format')
    args.add_argument('-j', '--join-lines', dest='join', nargs='?', metavar='<count?,delta?>',
                      help='join split source lines; <count> is max number of lines to merge, '
                           '<delta> is max line number delta of consecutive lines')
    args.add_argument('-o', '--output', dest='output', metavar='<file>',
                      help='set output filename or target directory')
    opts = args.parse_args()

    if (opts.labels or opts.protect or opts.join) and not opts.create:
        args.error('Options --labels, --protect, --join only apply'
                   'to creating programs.')
    if opts.labels and opts.join:
        args.error('Cannot join lines for programs using labels.')

    basename = os.path.basename(opts.source)
    barename, ext = os.path.splitext(basename)

    if opts.output and os.path.isdir(opts.output):  # -o file or directory?
        path = opts.output
        opts.output = None
    else:
        path = ''

    try:
        if opts.print or opts.decode:
            # read program
            if opts.source == '-':
                image = sys.stdin.buffer.read()
            else:
                with open(opts.source, 'rb') as fin:
                    image = fin.read()
            if opts.merge:
                program = BasicProgram()
                program.merge(image)
            else:
                program = BasicProgram(data=image, long_fmt=opts.long_)
            data = program.get_source()
            name = '-' if opts.print else opts.output or barename + '.b99'
            mode = 'w'
        elif opts.dump:
            with open(opts.source, 'rb') as fin:
                image = fin.read()
            program = BasicProgram(data=image)
            data = program.dump_tokens()
            name = opts.output or '-'
            mode = 'w'
        else:
            # create program
            if opts.merge:
                raise BasicError('Program creation in MERGE format is not supported')
            lines = [l.rstrip('\n') for l in readdata(opts.source, lines=True)]
            if opts.join:
                try:
                    count, delta = opts.join.split(',')
                    max_line_delta = xint(count) if count else 3
                    max_lino_delta = xint(delta) if delta else 10
                    lines = BasicProgram.join(lines, max_line_delta=max_line_delta, max_lino_delta=max_lino_delta)
                except ValueError:
                    raise BasicError('Invalid join parameter')
            program = BasicProgram(source=lines, labels=opts.labels)
            data = program.get_image(long_fmt=opts.long_, protected=opts.protect)
            name = opts.output or barename + '.prg'
            mode = 'wb'

        if program and program.errors:
            sys.stderr.write('\n'.join(program.errors) + '\n')
        writedata(os.path.join(path, name), data, mode=mode)

        unused_labels = program.get_unused_labels()
        if unused_labels:
            sys.stderr.write('Warning: Unused labels: {}\n'.format(' '.join(unused_labels)))

    except BasicError as e:
        sys.exit(f'Error: {str(e)}.')
    except IOError as e:
        sys.exit(f'File error: {e.filename:s}: {e.strerror:s}.')

    # return status
    return 1 if program.errors else 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
