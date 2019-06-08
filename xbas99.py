#!/usr/bin/env python

# xbas99: TI BASIC and TI Extended BASIC tool
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


VERSION = "2.0.0"


# Utility functions

def ordw(word):
    """word ord"""
    return ord(word[0]) << 8 | ord(word[1])


def chrw(word):
    """word chr"""
    return chr(word >> 8) + chr(word & 0xff)


def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip(">"), 16 if s[:2] == "0x" or s[:1] == ">" else 10)


def trunc(i, m):
    """round integer down to multiple of m"""
    return i - i % m


def sinc(s, i):
    """string sequence increment"""
    return s[:-1] + chr(ord(s[-1]) + i)


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
    LINEVAR = 4  # variable line (for comments)
    LINE_STR = 5  # quoted or unquoted string line (for IMAGE stmts)
    DATA_STR = 6  # special case: DATA operands
    KEEP = 7  # keep previous follow token type

    # unused token code for escaping statement separator "::"
    STMT_SEP = "\xaf"

    # token list
    tokenlist = [
        ("ELSE ", LINO), (STMT_SEP + " ", VAR), ("!", LINEVAR), ("IF ", VAR),
        ("GO ", LINO), ("GOTO ", LINO), ("GOSUB ", LINO), ("RETURN ", LINO),
        ("DEF ", VAR), ("DIM ", VAR), ("END ", VAR), ("FOR ", VAR),
        ("LET ", VAR), ("BREAK ", LINO), ("UNBREAK ", LINO), ("TRACE ", VAR),
        ("UNTRACE ", VAR), ("INPUT ", VAR), ("DATA ", DATA_STR),
        ("RESTORE ", LINO), ("RANDOMIZE ", VAR), ("NEXT ", VAR),
        ("READ ", VAR), ("STOP ", VAR), ("DELETE ", VAR), ("REM", LINEVAR),
        ("ON ", VAR), ("PRINT ", VAR), ("CALL ", USTR), ("OPTION ", VAR),
        ("OPEN ", VAR), ("CLOSE ", VAR), ("SUB ", USTR), ("DISPLAY ", VAR),
        ("IMAGE ", LINE_STR), ("ACCEPT ", VAR), ("ERROR ", LINO),
        ("WARNING ", VAR), ("SUBEXIT ", VAR), ("SUBEND ", VAR), ("RUN ", LINO),
        ("LINPUT ", VAR), (None, None), (None, None), (None, None),
        (None, None), (None, None), ("THEN ", LINO), ("TO ", KEEP),
        ("STEP ", VAR), (",", KEEP), (";", VAR), (":", VAR), (")", VAR),
        ("(", VAR), ("&", VAR), (None, None), ("OR", VAR), ("AND", VAR),
        ("XOR", VAR), ("NOT", VAR), ("=", VAR), ("<", VAR), (">", VAR),
        ("+", VAR), ("-", VAR), ("*", VAR), ("/", VAR), ("^", VAR),
        (None, None), ("qs", None), ("us", None), ("ln", None), ("EOF", VAR),
        ("ABS", VAR), ("ATN", VAR), ("COS", VAR), ("EXP", VAR), ("INT", VAR),
        ("LOG", VAR), ("SGN", VAR), ("SIN", VAR), ("SQR", VAR), ("TAN", VAR),
        ("LEN", VAR), ("CHR$", VAR), ("RND", VAR), ("SEG$", VAR), ("POS", VAR),
        ("VAL", VAR), ("STR$", VAR), ("ASC", VAR), ("PI", VAR), ("REC", VAR),
        ("MAX", VAR), ("MIN", VAR), ("RPT$", VAR), (None, None), (None, None),
        (None, None), (None, None), (None, None), (None, None),
        ("NUMERIC", VAR), ("DIGIT", VAR), ("UALPHA", VAR), ("SIZE", VAR),
        ("ALL", VAR), ("USING ", LINO), ("BEEP", VAR), ("ERASE", VAR),
        ("AT", VAR), ("BASE", VAR), (None, None), ("VARIABLE", VAR),
        ("RELATIVE", VAR), ("INTERNAL", VAR), ("SEQUENTIAL", VAR),
        ("OUTPUT", VAR), ("UPDATE", VAR), ("APPEND", VAR), ("FIXED", VAR),
        ("PERMANENT", VAR), ("TAB", VAR), ("#", VAR), ("VALIDATE", VAR),
        (None, None)
        ]

    tokens = {w.strip(): (chr(0x81 + i), t)
              for i, (w, t) in enumerate(tokenlist) if w is not None}
    literals = {chr(0x81 + i): (w, t) for i, (w, t) in enumerate(tokenlist)}

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
        return "\xc7" + chr(len(s)) + s

    @classmethod
    def ustr_token(cls, s):
        """return unquoted string token"""
        return "\xc8" + chr(len(s)) + s

    @classmethod
    def lino_token(cls, s):
        """return line number token"""
        try:
            lino = int(s)
        except ValueError:
            lino = -1
        if not 1 <= lino <= 32767:
            raise BasicError("Invalid line number")
        return "\xc9" + chrw(lino)

    @classmethod
    def literal(cls, tokens):
        """return textual representation of BASIC token(s)"""
        lit_type, _ = cls.literals[tokens[0]]
        if lit_type == "qs":
            lit_value = ord(tokens[1])
            return '"' + tokens[2:2 + lit_value].replace('"', '""') + '"', lit_type, lit_value + 2
        elif lit_type == "us":
            lit_value = ord(tokens[1])
            return tokens[2:2 + lit_value], lit_type, lit_value + 2
        elif lit_type == "ln":
            return str(ordw(tokens[1:3])), lit_type, 3
        else:
            return lit_type, None, 1


# BASIC Program

class BasicProgram:

    # maximum number of bytes/tokens per BASIC line
    max_tokens_per_line = 254

    def __init__(self, data=None, source=None, long_fmt=False):
        self.lines = {}
        self.textlits = []
        self.warnings = []
        if data:
            try:
                self.load(data, long_fmt)
            except IndexError:
                self.warn("Cannot read program file")
        elif source:
            self.parse(source)

    def warn(self, text):
        """add warning message"""
        if text not in self.warnings:
            self.warnings.append(text)

    # convert program to source
    def load(self, data, long_fmt):
        """load tokenized BASIC program"""
        if long_fmt or data[1:3] == "\xab\xcd":
            # convert long format INT/VAR 254 to PROGRAM
            program, idx = "", 11
            while idx < len(data):
                n = ord(data[idx]) + 1
                program += data[idx + 1:idx + n]
                idx += n
            data = "XX" + data[5:7] + data[3:5] + "XX" + program

        # extract line number table and token table
        ptr_tokens = ordw(data[2:4]) + 1
        ptr_line_numbers = ordw(data[4:6])
        no_lines = (ptr_tokens - ptr_line_numbers) / 4
        line_numbers = data[8:8 + no_lines * 4]
        tokens = data[8 + no_lines * 4:]
        # process line token table
        for i in xrange(no_lines):
            lino = ordw(line_numbers[4 * i:4 * i + 2])
            ptr = ordw(line_numbers[4 * i + 2:4 * i + 4])
            j = ptr - 1 - ptr_tokens
            line_Len = ord(tokens[j])
            if tokens[j + line_Len] != "\x00":
                self.warn("Missing line termination")
            self.lines[lino] = tokens[j + 1:j + line_Len]

    def merge(self, data):
        """load tokenized BASIC program in merge format"""
        qstr, _ = Tokens.tokens["qs"]
        ustr, _ = Tokens.tokens["us"]
        line, _ = Tokens.tokens["ln"]
        eol_len = len(os.linesep)
        p = 0
        while p < len(data):
            lino = ordw(data[p:p + 2])
            if lino == 0xffff:
                break
            q = p = p + 2
            while data[p] != "\x00":
                if data[p] == qstr or data[p] == ustr:
                    p += 1 + ord(data[p + 1]) + 1
                elif data[p] == line:
                    p += 3
                else:
                    p += 1
            if data[p + 1:p + 1 + eol_len] != os.linesep:
                # NOTE: BASIC programs in MERGE format are stored as DIS/VAR,
                # even though they contain binary data -> read in "rb" mode
                # and check for end-of-line char sequence
                self.warn("Missing line termination")
            self.lines[lino] = data[q:p]
            p += 1 + eol_len

    def get_source(self):
        """return textual representation of token sequence"""
        text = [" "]  # dummy element
        for lino in sorted(self.lines):
            text.append("%d " % lino)
            tokens, p, softspace = self.lines[lino], 0, False
            while p < len(tokens):
                q = p
                while p < len(tokens) and tokens[p] <= "\x80":
                    p += 1
                if p > q:
                    text.append(" " + tokens[q:p] if softspace else
                                tokens[q:p])
                    softspace = True
                else:
                    lit, lit_type, n = Tokens.literal(tokens[p:])
                    is_text = lit[0] in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" + Tokens.STMT_SEP) and lit_type is None
                    if (((is_text or lit == "#" or
                            lit_type == "us" or lit_type == "ln") and softspace) or
                            (lit == ":" and text[-1][-1] == ":") or
                            (lit == "!" and text[-1][-1] != " ")):
                        text.append(" " + lit)
                    else:
                        text.append(lit)
                    softspace = (is_text and lit[-1] != " " and lit != "REM") or (
                                 lit_type == "us" or lit_type == "qs" or lit_type == "ln")
                    p += n
            text.append("\n")
        return self.fix_colons("".join(text[1:]))

    def fix_colons(self, text):
        """fix spacing of : and :: tokens"""
        s1 = text.replace(":" + Tokens.STMT_SEP, ": ::")
        s2 = s1.replace(Tokens.STMT_SEP, "::")
        return s2

    # source -> program

    def parse(self, lines):
        """parse and tokenize BASIC source code"""
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                lino, tokens = self.line(line)
                self.lines[lino] = tokens
            except BasicError as e:
                self.warn("%s: [%d] %s" % (str(e), i, line[:-1]))

    def line(self, line):
        """parse single BASIC line"""
        text = self.escape(line)
        m = re.match(r"(\d+)\s+(.+)", text)
        if not m:
            raise BasicError("Missing line number")
        lino, tokens = int(m.group(1)), self.stmts(m.group(2))
        if len(tokens) > BasicProgram.max_tokens_per_line:
            raise BasicError("Line too long")
        return lino, tokens

    def stmts(self, text):
        """parse one or more BASIC statements"""
        sep, _ = Tokens.token(",")
        tokens = []
        # poorest man imaginable's lexer
        parts = re.split(r'(\s+|"\d+"|[0-9.]+E-[0-9]+|[!,;:()&=<>+\-*/^#' +
                         Tokens.STMT_SEP + r'])',
                         text)
        tok_type = Tokens.VAR
        for i, word in enumerate(parts):
            if tok_type == Tokens.LINEVAR:
                tokens.extend(self.unescape("".join(parts[i:])))
                break
            if not word.strip():
                continue
            if (tok_type == Tokens.LINO or tok_type == Tokens.USTR) and word.isdigit():  # USTR covers "GO SUB"
                tokens.extend(Tokens.lino_token(word))
                tok_type = Tokens.LINO
            elif tok_type == Tokens.LINE_STR:
                remaining = "".join(parts[i:]).strip()
                if remaining:
                    tokens.extend(self.qstr(remaining) if remaining[0] == '"' else
                                  self.ustr(remaining))
                break
            elif tok_type == Tokens.DATA_STR:
                remaining = [s.strip() for s in "".join(parts[i:]).split(",")]
                data = [(self.qstr(s) if s[0] == '"' else self.ustr(s))
                        if s else "" for s in remaining]
                tokens.extend(sep.join(data))
                break
            elif tok_type == Tokens.QSTR or word[0] == '"':  # keep before USTR!
                # NOTE: there is actually no token with follow token QSTR
                tokens.extend(self.qstr(word))
                tok_type = Tokens.VAR
            elif tok_type == Tokens.USTR:
                tokens.extend(self.ustr(word.upper()))
                tok_type = Tokens.VAR
            else:
                token, follow = Tokens.token(word)
                if token:  # keywords and operators
                    tokens.append(token)
                elif re.match(r"[0-9.]+", word):  # number literals
                    tokens.extend(self.ustr(word.upper()))
                else:
                    tokens.extend(word.upper())  # plain VARs
                if follow != Tokens.KEEP:
                    tok_type = follow
        return tokens

    def escape(self, text):
        """remove and save ambiguous constructs from line"""
        parts = re.split(r'("(?:[^"]|"")*")', text)
        lits = [s[1:-1].replace('""', '"') for s in parts[1::2]]
        parts[1::2] = ['"' + str(len(self.textlits) + i) + '"'
                       for i in xrange(len(lits))]
        self.textlits.extend(lits)
        return "".join(parts).replace("::", Tokens.STMT_SEP)

    def unescape(self, s):
        """rebuild original text from escaped string"""
        text = re.sub(r'"(\d+)"',
                      lambda m: '"' + self.textlits[int(m.group(1))] + '"',
                      self.fix_colons(s))
        return text

    def qstr(self, lit):
        """build quoted string token sequence"""
        try:
            s = self.textlits[int(lit[1:-1])]
            return Tokens.qstr_token(s)
        except (ValueError, IndexError):
            raise RuntimeError("Invalid text literal id %s" % lit[1:-1])

    def ustr(self, lit):
        """build unquoted string token sequence"""
        return Tokens.ustr_token(self.unescape(lit))

    def get_image(self, long_fmt=False, protected=False):
        """create PROGRAM image from tokens"""
        last_addr = 0xffe8 if long_fmt else 0x37d8
        prog, p = [], 0
        if long_fmt:
            size = sum([len(self.lines[i]) for i in self.lines]) + 2 * len(self.lines)
            if size < 254:
                self.warn("Program too short, will pad")
                pad_len = 254 - size
                prog.append((0, 32767, chr(pad_len - 1) + "\x83" +
                             "\x21" * (pad_len - 3) + "\x00"))
                p = pad_len
        for lino in sorted(self.lines, reverse=True):
            line = self.lines[lino]
            prog.append((p, lino, chr(len(line) + 1) + "".join(line) + "\x00"))
            p += len(line) + 2
        token_tab_addr = last_addr - p
        lino_tab_addr = token_tab_addr - 4 * len(prog)
        token_table = "".join([tokens for p, lino, tokens in prog])
        lino_table = "".join([chrw(lino) + chrw(token_tab_addr + p + 1)
                             for p, lino, tokens in prog])
        checksum = (token_tab_addr - 1) ^ lino_tab_addr
        assert lino_tab_addr + len(lino_table) + len(token_table) == last_addr
        if protected:
            checksum = -checksum % 0x10000
        if long_fmt:
            header = ("\xab\xcd" + chrw(lino_tab_addr) + chrw(token_tab_addr - 1) +
                      chrw(checksum) + chrw(last_addr - 1))
            chunks = [(lino_table + token_table)[i:i + 254]
                      for i in xrange(0, len(lino_table + token_table), 254)]
            return (chr(len(header)) + header +
                    "".join([chr(len(c)) + c for c in chunks]))
        else:
            header = (chrw(checksum) + chrw(token_tab_addr - 1) +
                      chrw(lino_tab_addr) + chrw(last_addr - 1))
            return header + lino_table + token_table

    def dump_tokens(self):
        """dump pretty-printed token stream sorted by line number"""
        lines = []
        line, _ = Tokens.tokens["ln"]
        ssep, _ = Tokens.tokens[Tokens.STMT_SEP]
        for lino in sorted(self.lines):
            tokens = self.lines[lino]
            p, result = 0, []
            while p < len(tokens):
                t = tokens[p]
                if t < " ":
                    result.append("#%d" % ord(t))
                elif t <= "\x80":
                    result.append(t)
                elif t == line:
                    result.append("^" + str(ordw(tokens[p + 1:p + 3])))
                    p += 2
                elif t == ssep:
                    result.append("::")
                else:
                    result.append(Tokens.literals[t][0].rstrip())
                p += 1
            lines.append("%d: %s\n" % (lino, " ".join(result)))
        return "".join(lines)

    @staticmethod
    def join(lines, min_lino_delta=1, max_lino_delta=3):
        """join split source lines heuristically"""
        joined = []
        prev_lino = None
        for line in lines:
            if not line.strip():
                prev_lino = None
                continue
            m = re.match("(\d+)\s+", line)
            next_lino = int(m.group(1)) if m else -1
            if (prev_lino and
                    not min_lino_delta <= next_lino - prev_lino <= max_lino_delta):
                joined[-1] = joined[-1][:-1] + line
            else:
                joined.append(line)
                prev_lino = next_lino
        return joined


# Command line processing

def main():
    import argparse

    args = argparse.ArgumentParser(
        description="TI BASIC and TI Extended BASIC tool, v" + VERSION)
    args.add_argument("source", metavar="<source>",
                      help="TI BASIC or TI Extended BASIC program")
    cmd = args.add_mutually_exclusive_group()
    cmd.add_argument("-l", "--list", action="store_true", dest="list_",
                     help="list TI (Extended) BASIC program")
    cmd.add_argument("-d", "--decode", action="store_true", dest="decode",
                     help="decode TI (Extended) BASIC program")
    cmd.add_argument("-c", "--create", action="store_true", dest="create",
                     help="create TI (Extended) BASIC program file (default)")
    cmd.add_argument("--dump", action="store_true", dest="dump",
                     help="dump (Extended) BASIC token stream")
    args.add_argument("--protect", action="store_true", dest="protect",
                      help="list-protect program")
    args.add_argument("--merge", action="store_true", dest="merge",
                      help="use merge format")
    args.add_argument("--long", action="store_true", dest="long_",
                      help="force long program format")
    args.add_argument("-j", "--join-lines", dest="join", metavar="<delta>",
                      help="join split source lines (for -e)")
    args.add_argument("-o", "--output", dest="output", metavar="<file>",
                      help="set output filename")
    opts = args.parse_args()

    basename = os.path.basename(opts.source)
    barename, ext = os.path.splitext(basename)

    try:
        if opts.list_ or opts.decode:
            # read program
            if opts.source == "-":
                image = sys.stdin.read()
            else:
                with open(opts.source, "rb") as fin:
                    image = fin.read()
            if opts.merge:
                program = BasicProgram()
                program.merge(image)
            else:
                program = BasicProgram(data=image, long_fmt=opts.long_)
            data = program.get_source()
            output = "-" if opts.list_ else opts.output or barename + ".b99"
        elif opts.dump:
            with open(opts.source, "rb") as fin:
                image = fin.read()
            program = BasicProgram(data=image)
            data = program.dump_tokens()
            output = opts.output or "-"
        else:
            # create program
            if opts.merge:
                raise BasicError(
                    "Program creation in MERGE format is not supported")
            with open(opts.source, "r") as fin:
                lines = fin.readlines()
            if opts.join:
                try:
                    delta = xint(opts.join)
                    lines = BasicProgram.join(lines, max_lino_delta=delta)
                except ValueError:
                    raise BasicError("Invalid line delta for join")
            program = BasicProgram(source=lines)
            data = program.get_image(long_fmt=opts.long_, protected=opts.protect)
            output = opts.output or barename + ".prg"

        if program and program.warnings:
            sys.stderr.write("".join([
                "Warning: %s\n" % w for w in program.warnings]))
        if output == "-":
            print data.rstrip()
        else:
            with open(output, "wb") as fout:
                fout.write(data)

    except BasicError as e:
        sys.exit("Error: %s." % e)
    except IOError as e:
        sys.exit("File error: %s: %s." % (e.filename, e.strerror))

    # return status
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
