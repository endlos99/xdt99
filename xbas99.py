#!/usr/bin/env python3

# xbas99: TI BASIC and TI Extended BASIC tool
#
# Copyright (c) 2015-2022 Ralph Benzinger <xdt99@endlos.net>
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
import argparse
from xcommon import Util, RFile, CommandProcessor, Warnings, Console


VERSION = '3.5.4'

CONFIG = 'XBAS99_CONFIG'


# Error handling

class BasicError(Exception):
    pass


# Tokens

class Tokens:
    """TI BASIC and TI Extended BASIC tokens"""

    # follow token types
    STMT = 1  # statement (default)
    QSTR = 2  # quoted string
    USTR = 3  # unquoted string
    LINO = 4  # line number or label
    LORS = 5  # LINO or STMT
    RUNS = 6  # RUN statement (line number, string, or numeric variable allowed)
    COMMENT = 10  # comments
    IMAGE_STR = 11  # quoted or unquoted string line for IMAGE stmts
    DATA_STR = 12  # special case: DATA operands
    KEEP = 13  # keep previous follow token type
    GO_PRFX = 14  # GO prefix

    # unused token code for escaping statement separator '::'
    QS_VAL = 0xc7  # token value for quoted string
    US_VAL = 0xc8  # token value for unquoted string
    LINO_VAL = 0xc9  # token value for line number
    STMT_SEP = '\xaf'  # token representation of :: stmt separator

    # token listing and expected follow token class
    tokenlist = [
        ('ELSE ', LORS), (STMT_SEP + ' ', STMT), ('!', COMMENT), ('IF ', STMT),
        ('GO ', GO_PRFX), ('GOTO ', LINO), ('GOSUB ', LINO), ('RETURN ', LINO),
        ('DEF ', STMT), ('DIM ', STMT), ('END ', STMT), ('FOR ', STMT),
        ('LET ', STMT), ('BREAK ', LINO), ('UNBREAK ', LINO), ('TRACE ', STMT),
        ('UNTRACE ', STMT), ('INPUT ', STMT), ('DATA ', DATA_STR),
        ('RESTORE ', LINO), ('RANDOMIZE ', STMT), ('NEXT ', STMT),
        ('READ ', STMT), ('STOP ', STMT), ('DELETE ', STMT), ('REM', COMMENT),
        ('ON ', STMT), ('PRINT ', STMT), ('CALL ', USTR), ('OPTION ', STMT),
        ('OPEN ', STMT), ('CLOSE ', STMT), ('SUB ', USTR), ('DISPLAY ', STMT),
        ('IMAGE ', IMAGE_STR), ('ACCEPT ', STMT), ('ERROR ', LINO),
        ('WARNING ', STMT), ('SUBEXIT ', STMT), ('SUBEND ', STMT), ('RUN ', RUNS),
        ('LINPUT ', STMT), (None, None), (None, None), (None, None),
        (None, None), (None, None), ('THEN ', LORS), ('TO ', STMT),
        ('STEP ', STMT), (',', KEEP), (';', STMT), (':', STMT), (')', STMT),
        ('(', STMT), ('&', STMT), (None, None), ('OR', STMT), ('AND', STMT),
        ('XOR', STMT), ('NOT', STMT), ('=', STMT), ('<', STMT), ('>', STMT),
        ('+', STMT), ('-', STMT), ('*', STMT), ('/', STMT), ('^', STMT),
        (None, None), ('qs', None), ('us', None), ('ln', None), ('EOF', STMT),
        ('ABS', STMT), ('ATN', STMT), ('COS', STMT), ('EXP', STMT), ('INT', STMT),
        ('LOG', STMT), ('SGN', STMT), ('SIN', STMT), ('SQR', STMT), ('TAN', STMT),
        ('LEN', STMT), ('CHR$', STMT), ('RND', STMT), ('SEG$', STMT), ('POS', STMT),
        ('VAL', STMT), ('STR$', STMT), ('ASC', STMT), ('PI', STMT), ('REC', STMT),
        ('MAX', STMT), ('MIN', STMT), ('RPT$', STMT), (None, None), (None, None),
        (None, None), (None, None), (None, None), (None, None),
        ('NUMERIC', STMT), ('DIGIT', STMT), ('UALPHA', STMT), ('SIZE', STMT),
        ('ALL', STMT), ('USING ', LINO), ('BEEP', STMT), ('ERASE', STMT),
        ('AT', STMT), ('BASE', STMT), (None, None), ('VARIABLE', STMT),
        ('RELATIVE', STMT), ('INTERNAL', STMT), ('SEQUENTIAL', STMT),
        ('OUTPUT', STMT), ('UPDATE', STMT), ('APPEND', STMT), ('FIXED', STMT),
        ('PERMANENT', STMT), ('TAB', STMT), ('#', STMT), ('VALIDATE', STMT),
        (None, None)
        ]

    tokens = {w.strip(): (bytes((0x81 + i,)), t)
              for i, (w, t) in enumerate(tokenlist) if w is not None}
    literals = {0x81 + i: (w, t) for i, (w, t) in enumerate(tokenlist)}

    def __init__(self, strict):
        self.strict = strict

    def token(self, tok):
        """get BASIC token for text literal"""
        try:
            return self.tokens[tok.upper()]
        except KeyError:
            return None, None

    def is_token(self, tok):
        """get BASIC token for text literal"""
        return tok.upper() in self.tokens

    def qstr_token(self, s):
        """return quoted string token"""
        bs = self.deasciify(s)
        try:
            return bytes((self.QS_VAL,)) + bytes((len(bs),)) + bs
        except ValueError:
            raise BasicError('Quoted string too long')

    def ustr_token(self, s):
        """return unquoted string token"""
        bs = self.deasciify(s)
        try:
            return bytes((self.US_VAL,)) + bytes((len(bs),)) + bs
        except ValueError:
            raise BasicError('Unquoted string too long')

    def lino_token(self, s):
        """return line number token"""
        try:
            lino = int(s)
        except ValueError:
            lino = 0
        if not 1 <= lino <= 32767:
            raise BasicError(f'Invalid line number: {s}')
        return bytes((self.LINO_VAL,)) + Util.chrw(lino)

    def text(self, tokens):
        """return textual representation of BASIC token(s)"""
        lit_type, _ = self.literals[tokens[0]]
        try:
            if lit_type == 'qs':
                lit_value = tokens[1]
                return '"' + self.asciify(tokens[2:2 + lit_value]).replace('"', '""') + '"', lit_type, lit_value + 2
            elif lit_type == 'us':
                lit_value = tokens[1]
                return self.asciify(tokens[2:2 + lit_value]), lit_type, lit_value + 2
            elif lit_type == 'ln':
                return str(Util.ordw(tokens[1:3])), lit_type, 3
            else:
                return lit_type, None, 1  # for all other cases, lit_type == token
        except UnicodeDecodeError:
            raise BasicError('Non-ASCII characters found in program')

    def asciify(self, bs):
        """decode bytes into ASCII by escaping non-ASCII bytes"""
        if self.strict:
            try:
                return bs.decode('ascii')
            except UnicodeDecodeError:
                raise BasicError('Invalid non-ASCII characters found')
        s = []
        i = 0
        while i < len(bs):
            bb = bs[i:i + 2]
            if bb == b'\\x' or bb == b'\\d':
                s.append('\\\\' + chr(bb[1]))  # add extra '\' escape escape sequence
                i += 1
            elif 32 <= bb[0] < 128:
                s.append(chr(bb[0]))  # include ASCII chars in printable range verbatim
            else:
                s.append('\\x{:02x}'.format(bb[0]))  # create escape sequence
            i += 1
        return ''.join(s)

    def deasciify(self, s):
        """encode ascii into bytes, resolving escaped non-ASCII codes \\x99 and \\d999"""
        if self.strict:
            try:
                return s.encode('ascii')
            except UnicodeEncodeError:
                raise BasicError('Invalid non-ASCII characters found')
        t = []
        i = 0
        while i < len(s) - 1:
            c = s[i]
            if c == '\\':  # begin of escape sequence
                if s[i + 1:i + 3] in ('\\x', '\\d'):  # escaped char escape code
                    t.append(ord(c))
                    i += 2
                    continue
                base = s[i + 1]
                try:
                    if base == 'x':  # append hex value
                        s[i + 3]  # ensure value has 2 digits
                        t.append(int(s[i + 2:i + 4], 16))  # \xnn always between 0 and 255
                        i += 4
                        continue
                    elif base == 'd':  # append decimal value
                        s[i + 4]  # ensure value has 3 digits
                        v = int(s[i + 2:i + 5])
                        if not 0 <= v <= 255:
                            raise BasicError(f'Invalid value in character escape code: {v:d}')
                        t.append(v)
                        i += 5
                        continue
                    # other escape codes are left verbatim
                except (IndexError, ValueError):
                    raise BasicError('Malformed character escape code')
            t.append(ord(c))
            i += 1
        try:
            t.append(ord(s[i]))  # last char, which might be a single '\'
        except IndexError:
            pass
        try:
            return bytes(t)
        except ValueError:
            raise BasicError('Invalid non-escaped non-ASCII character in string')


# BASIC Program

class BasicProgram:

    # maximum number of bytes/tokens per BASIC line
    max_tokens_per_line = 254

    def __init__(self, long_fmt=False, labels=False, protected=False, strict=False, console=None):
        self.long_fmt = long_fmt
        self.labels = labels
        self.protected = protected
        self.strict = strict
        self.tokens = Tokens(strict)
        self.console = console or Xbas99Console()
        self.lines = {}
        self.label_lino = {}  # Dict[str, Tuple[int, bool]]
        self.text_literals = []
        self.rem_literals = []
        self.curr_lino = 100

    # convert program to source

    def load(self, data):
        """load tokenized BASIC program"""
        try:
            if self.long_fmt or data[1:3] == b'\xab\xcd':
                # convert long format INT/VAR 254 to PROGRAM
                program = []
                idx = 11
                while idx < len(data):
                    n = data[idx] + 1
                    program.append(data[idx + 1:idx + n])
                    idx += n
                data = b'XX' + data[5:7] + data[3:5] + b'XX' + b''.join(program)
            # extract line number table and token table
            ptr_tokens = Util.ordw(data[2:4]) + 1
            ptr_line_numbers = Util.ordw(data[4:6])
            no_lines = (ptr_tokens - ptr_line_numbers) // 4
            line_numbers = data[8:8 + no_lines * 4]
            tokens = data[8 + no_lines * 4:]
            # process line token table
            for i in range(no_lines):
                lino = Util.ordw(line_numbers[4 * i:4 * i + 2])
                ptr = Util.ordw(line_numbers[4 * i + 2:4 * i + 4])
                j = ptr - 1 - ptr_tokens
                line_len = tokens[j]
                if tokens[j + line_len]:
                    self.console.error('Missing line termination')
                self.lines[lino] = tokens[j + 1:j + line_len]
        except IndexError:
            self.console.error('Cannot read program file, bad format')

    def merge(self, data):
        """load tokenized BASIC program in merge format
           Merge format is stored as DIS/VAR 163, even though the data is binary, and
           type INT/VAR 163 would be more appropriate.  The problem with DISPLAY is that
           we must recognize the record terminator, which differs by platform: Linux
           and MacOS use \n, whereas Windows uses \r\n.  We will ignore older platforms
           which might use \r and \n\r.  Luckily, records are terminated by 0, so the
           locations of record terminators are known.
        """
        idx = 0
        while idx < len(data):
            lino = Util.ordw(data[idx:idx + 2])
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
                self.console.error('Missing line termination')

    def get_source(self):
        """return textual representation of token sequence"""
        text = [' ']  # dummy element
        for lino, tokens in sorted(self.lines.items()):
            text.append(f'{lino:d} ')
            softspace = False
            idx = 0
            while idx < len(tokens):
                save_idx = idx
                while idx < len(tokens) and tokens[idx] <= 0x80:
                    idx += 1
                if idx > save_idx:
                    try:
                        text.append((' ' if softspace else '') + tokens[save_idx:idx].decode('ascii'))  # var names
                    except UnicodeDecodeError:
                        raise BasicError('Non-ASCII characters found in program')
                    softspace = True
                else:
                    lit, lit_type, n = self.tokens.text(tokens[idx:])
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

    # convert source to program

    def get_labels(self, lines):
        """gather all label definitions, return remaining lines"""
        remaining = []
        self.curr_lino = 100
        for i, line in enumerate(lines):
            if not line.rstrip():
                continue
            m = re.match(r'(\w+):$', line)
            if m:
                label = m.group(1).upper()
                if self.tokens.is_token(label):
                    raise BasicError(f'Label {label} conflicts with reserved keyword')
                self.label_lino[label] = self.curr_lino, False  # lino x used
            else:
                if not line[:1].isspace():
                    raise BasicError(f'Missing indentation in line {i + 1}')
                remaining.append(line)
                self.curr_lino += 10
        return remaining

    def parse(self, lines):
        """parse and tokenize BASIC source"""
        if self.labels:
            lines = self.get_labels(lines)
        self.curr_lino = 100
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                lino, tokens = self.line(line)
                if lino is not None:  # None for label definitions
                    self.lines[lino] = tokens
            except BasicError as e:
                self.console.error(str(e), info=f'[{i + 1:d}] {line}')
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
        """parse single line of one or more BASIC statements"""
        # lexer of poorest man imaginable
        sep, _ = Tokens.tokens[',']
        tokens = []
        tok_type = Tokens.STMT
        parts = re.split(r'(\s+|"\d+"|[\d.]+[Ee]-\d+|[!,;:()&=<>+\-*/^#' + Tokens.STMT_SEP + r'])', text)
        i = 0
        while i < len(parts):
            word = parts[i]
            uword = word.upper()  # keywords and vars are case-insensitive, but not DATA, IMAGE, REM, ...
            if tok_type == Tokens.COMMENT:
                # include all following parts in comment
                try:
                    tokens.append(self.unescape(''.join(parts[i:])).encode('ascii'))
                except UnicodeEncodeError:
                    raise BasicError('Non-ASCII character found in comment')
                break
            elif not word.strip():
                pass  # skip empty parts
            elif tok_type == Tokens.STMT:
                # STMT base case
                token, follow = self.tokens.token(uword)
                if token:  # keywords and operators
                    tokens.append(token)
                    if follow != Tokens.KEEP:
                        tok_type = follow
                elif word[0] == word[-1] == '"':
                    tok_type = Tokens.QSTR  # for USING and RUN
                    continue
                elif self.is_number(uword):  # number literals
                    tokens.append(self.ustr(uword))
                else:
                    try:
                        tokens.append(uword.encode('ascii'))  # variable
                    except UnicodeEncodeError:
                        raise BasicError('Non-ASCII character found in variable name')
            elif tok_type == Tokens.GO_PRFX:
                if uword in ('TO', 'SUB'):
                    token, _ = self.tokens.token(uword)
                    tokens.append(token)
                    tok_type = Tokens.LINO
                else:
                    raise BasicError('Syntax error after GO')
            elif tok_type == Tokens.LORS:
                # lino or statements following THEN or ELSE
                if self.labels:
                    token, _ = self.tokens.token(uword)
                    if token is None:
                        if uword[0] == '@':
                            uword = uword[1:]  # remove @ from label
                        if uword in self.label_lino:
                            tok_type = Tokens.LINO
                        elif self.is_assignment(parts, i + 1):
                            tok_type = Tokens.STMT
                        else:
                            raise BasicError(f'Unknown label {uword}')
                    else:
                        tok_type = Tokens.STMT
                else:
                    tok_type = Tokens.LINO if word.isdigit() else Tokens.STMT
                continue
            elif tok_type == Tokens.IMAGE_STR:
                remaining = ''.join(parts[i:]).strip()
                if remaining:
                    tokens.append(self.qstr(remaining) if remaining[0] == '"' else
                                  self.ustr(remaining))
                break
            elif tok_type == Tokens.DATA_STR:
                remaining = [s.strip() for s in ''.join(parts[i:]).split(',')]
                data = [(self.qstr(s) if s[0] == '"' else self.ustr(s)) if s else b'' for s in remaining]
                tokens.append(sep.join(data))
                break
            elif tok_type == Tokens.QSTR or word[0] == '"':  # keep before USTR!
                # NOTE: there is actually no token with follow token QSTR
                tokens.append(self.qstr(word))
                tok_type = Tokens.STMT
            elif tok_type == Tokens.USTR:
                tokens.append(self.ustr(uword))
                tok_type = Tokens.STMT
            else:
                # LINO or RUNS
                token, follow = self.tokens.token(uword)
                if token is not None:
                    tokens.append(token)
                    tok_type = follow
                elif word.isdigit():
                    tokens.append(self.tokens.lino_token(uword))
                elif word[0] == word[-1] == '"':
                    tok_type = Tokens.QSTR  # for USING and RUN
                    continue
                elif word[-1] == '$':
                    tok_type = Tokens.STMT  # for USING and RUN
                    continue
                # keep tok_type, escapes at next token
                elif self.labels:
                    if uword[0] == '@':
                        uword = uword[1:]  # remove optional @
                    if uword.isalnum():
                        # NOTE: There is only one possible collision between label and variable: RUN A.
                        #       This conflict only occurs if label mode is active, but then RUN A with A
                        #       containing a line number makes no sense. --> No conflict at all!
                        try:
                            lino, used = self.label_lino[uword]
                            if not used:
                                self.label_lino[uword] = lino, True
                            tokens.append(self.tokens.lino_token(str(lino)))
                        except KeyError:
                            raise BasicError(f'Unknown label {uword}')
                    else:
                        raise BasicError('Bad label')
                elif tok_type == Tokens.RUNS:
                    tok_type = Tokens.STMT  # variable
                    continue
                else:
                    raise BasicError('Syntax error, line number expected')

            i += 1
        return tokens

    @staticmethod
    def is_number(text):
        """parse integer and floating point number"""
        return re.match(r'(\d+(\.\d*)?|\.\d+)(E-?\d+)?', text)

    @staticmethod
    def is_assignment(parts, i):
        """check if parts starting at i-1 are assignment"""
        subexpr = 0
        for word in parts[i:]:
            if word == '(':  # start of subexpr
                subexpr += 1
            elif word == ')':  # end of subexpr
                subexpr -= 1
            elif word == '=' and subexpr == 0:  # found = directly after variable
                return True
            elif subexpr == 0:  # keep going until subexpr is done
                return False
        return False  # unclosed subexpr, no = found in line

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
            return self.tokens.qstr_token(s)
        except (ValueError, IndexError):
            raise RuntimeError('Invalid text literal id ' + lit[1:-1])

    def ustr(self, lit):
        """build unquoted string token sequence"""
        return self.tokens.ustr_token(self.unescape(lit))

    def get_image(self):
        """create PROGRAM image from tokens"""
        last_addr = 0xffe8 if self.long_fmt else 0x37d8
        program = []
        idx = 0
        if self.long_fmt:
            size = sum(len(self.lines[i]) for i in self.lines) + 2 * len(self.lines)
            if size < 254:
                self.console.error('Program too short, will pad')
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
        lino_table = b''.join(Util.chrw(lino) + Util.chrw(token_tab_addr + i + 1) for i, lino, _ in program)
        checksum = (token_tab_addr - 1) ^ lino_tab_addr
        assert lino_tab_addr + len(lino_table) + len(token_table) == last_addr
        if self.protected:
            checksum = -checksum % 0x10000
        if self.long_fmt:
            header = (b'\xab\xcd' + Util.chrw(lino_tab_addr) + Util.chrw(token_tab_addr - 1) +
                      Util.chrw(checksum) + Util.chrw(last_addr - 1))
            chunks = [(lino_table + token_table)[i:i + 254]
                      for i in range(0, len(lino_table + token_table), 254)]
            return (bytes((len(header),)) + header +
                    b''.join(bytes((len(c),)) + c for c in chunks))
        else:
            header = (Util.chrw(checksum) + Util.chrw(token_tab_addr - 1) +
                      Util.chrw(lino_tab_addr) + Util.chrw(last_addr - 1))
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
                    result.append('^' + str(Util.ordw(tokens[idx + 1:idx + 3])))
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
            m = re.match(r'(\d+)\s+', line)  # check for line number at start of line
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


class Xbas99Console(Console):
    """collects errors and warnings"""

    def __init__(self, quiet=False, colors=None):
        super().__init__('xbas99', VERSION, {Warnings.DEFAULT: not quiet}, colors=colors)

    def warn(self, message):
        """issue warning message"""
        super().warn(None, 'Warning: ' + message)

    def error(self, message, info=None):
        """issue error message"""
        super().error(info, 'Error: ' + message)


# Command line processing

class Xbas99Processor(CommandProcessor):
    
    def __init__(self):
        super().__init__(BasicError)
        self.program = None

    def parse(self):
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
        args.add_argument('-s', '--strict', action='store_true', dest='strict',
                          help='disable xbas99 extensions')
        args.add_argument('-o', '--output', dest='output', metavar='<file>',
                          help='set output filename or target directory')
        args.add_argument('--color', action='store', dest='color', choices=['off', 'on'],
                          help='enable or disable color output')
        args.add_argument('-q', action='store_true', dest='quiet',
                          help='quiet, do not print warnings')
    
        try:
            default_opts = os.environ[CONFIG].split()
        except KeyError:
            default_opts = []
        self.opts = args.parse_args(args=default_opts + sys.argv[1:])  # passed opts override default opts
    
        if (self.opts.labels or self.opts.protect or self.opts.join) and self.opts.decode:
            args.error('Cannot use options --labels, --protect, --join while decoding programs.')
        if self.opts.labels and self.opts.join:
            args.error('Cannot join lines for programs using labels.')

    def run(self):
        basename = os.path.basename(self.opts.source)
        self.barename, ext = os.path.splitext(basename)
        self.console = Xbas99Console(self.opts.quiet, self.opts.color)
        self.program = BasicProgram(long_fmt=self.opts.long_, labels=self.opts.labels, protected=self.opts.protect,
                                    console=self.console)

    def prepare(self):
        if self.opts.decode or self.opts.print:
            self.decode()
        elif self.opts.dump:
            self.dump()
        else:
            self.create()

    def decode(self):
        image = Util.readdata(self.opts.source)
        if self.opts.merge:
            self.program.merge(image)
        else:
            self.program.load(image)
        self.result.append(RFile(data=self.program.get_source(),
                                 name='-' if self.opts.print else self.barename,
                                 ext='.b99',
                                 istext=True))

    def dump(self):
        image = Util.readdata(self.opts.source)
        self.program.load(image)
        self.result.append(RFile(data=self.program.dump_tokens(), name='-', istext=True))

    def create(self):
        if self.opts.merge:
            raise BasicError('Program creation in MERGE format is not supported')
        lines = [line.rstrip('\n') for line in Util.readlines(self.opts.source)]
        if self.opts.join:
            try:
                count, delta = self.opts.join.split(',')
                max_line_delta = Util.xint(count) if count else 3
                max_lino_delta = Util.xint(delta) if delta else 10
                lines = BasicProgram.join(lines, max_line_delta=max_line_delta, max_lino_delta=max_lino_delta)
            except ValueError:
                raise BasicError('Invalid join parameter')
        self.program.parse(lines)
        prg_data = self.program.get_image()
        self.result.append(RFile(data=prg_data, name=self.barename, ext='.prg'))

    def output(self):
        if self.opts.print:
            self.opts.output = '-'  # print writes to stdout, cannot be redirected
        elif not self.opts.decode:
            unused_labels = self.program.get_unused_labels()
            if unused_labels:
                self.console.warn('Unused labels: {}'.format(' '.join(unused_labels)))
        super().output()

    def errors(self):
        return 1 if self.console.errors else self.rc


if __name__ == '__main__':
    status = Xbas99Processor().main()
    sys.exit(status)
