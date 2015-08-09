package net.endlos.xdt99.xas99;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import com.intellij.psi.TokenType;

%%

%class Xas99Lexer
%implements FlexLexer
%unicode
%function advance
%type IElementType
%eof{  return;
%eof}

%ignorecase

INSTR_I = "A" | "AB" | "C" | "CB" | "MOV" | "MOVB" | "S" | "SB" | "SOC" | "SOCB" | "SZC" | "SZCB"
INSTR_II = "JEQ" | "JGT" | "JH" | "JHE" | "JL" | "JLE" | "JLT" | "JMP" | "JNC" | "JNE" | "JNO" | "JOC" | "JOP" |
           "SBO" | "SBZ" | "TB"
INSTR_III = "COC" | "CZC" | "XOR"
INSTR_IV = "LDCR" | "STCR"
INSTR_V = "SLA" | "SRA" | "SRC" | "SRL"
INSTR_VI = "ABS" | "B" | "BL" | "BLWP" | "CLR" | "DEC" | "DECT" | "INC" | "INCT" | "INV" | "NEG" | "SETO" | "SWPB" | "X"
INSTR_VII = "CKON" | "CKOF" | "IDLE" | "LREX" | "RSET" | "RTWP"
INSTR_VIII = "AI" | "ANDI" | "CI" | "LI" | "ORI"
INSTR_VIII_I = "LIMI" | "LWPI"
INSTR_VIII_R = "STST" | "STWP"
INSTR_IX = "MPY" | "DIV"
INSTR_IX_X = "XOP"
INSTR_O = "NOP" | "RT"

DIR_L = "DEF" | "REF"
DIR_E = "EQU" | "BSS" | "BES" | "AORG" | "DORG"
DIR_EO = "RORG"
DIR_ES = "DATA" | "BYTE"
DIR_S = "TITL" | "IDT" | "COPY" | "TEXT" | "IBYTE"
DIR_O = "EVEN" | "END" | "UNL" | "LIST" | "PAGE" | "DXOP"
DIR_X = "PSEG" | "PEND" | "CSEG" | "CEND" | "DSEG" | "DEND" | "LOAD" | "SREF"

PREP = ".IFDEF" | ".IFNDEF" | ".IFEQ" | ".IFNE" | ".IFGT" | ".IFGE" | ".ELSE" | ".ENDIF"

LINE_COMMENT = "*" [^\r\n]*
EOL_COMMENT = {BLANK}* ";" [^\r\n]*

IDENT = {ALPHA}({ALPHA}|{DIGIT})*
INT = {DIGIT}{DIGIT}* | ">" {HEX}{HEX}* | ":" [01][01]*
TEXT = "'" ([^'\r\n] | "''")* "'" | "\"" [^\"\r\n]* "\""
REGISTER = [Rr] ([0-9] | 1[0-5])
OPER = [/%&|\^]

ALPHA = [A-Za-z_]
DIGIT = [0-9]
HEX = [0-9A-Fa-f]

BLANK = " " | \t
WS = {BLANK}{BLANK}*
FSEP = {BLANK}{WS}
CRLF = \n | \r | \r\n
ANY = [^\r\n]

%state MNEMONIC
%state MNEMONICO
%state ARGUMENTS
%state COMMENT
%state PREPROC

%%

{EOL_COMMENT}                    { return Xas99Types.EOL_COMMENT; }
{CRLF}                           { yybegin(YYINITIAL); return Xas99Types.CRLF; }

<YYINITIAL> {LINE_COMMENT}       { return Xas99Types.LINE_COMMENT; }
<YYINITIAL> {IDENT}              { return Xas99Types.IDENT; }

<YYINITIAL> {WS}                 { yybegin(MNEMONIC); return Xas99Types.FIELD_SEP; }

<MNEMONIC> {INSTR_I}             { return Xas99Types.INSTR_I; }
<MNEMONIC> {INSTR_II}            { return Xas99Types.INSTR_II; }
<MNEMONIC> {INSTR_III}           { return Xas99Types.INSTR_III; }
<MNEMONIC> {INSTR_IV}            { return Xas99Types.INSTR_IV; }
<MNEMONIC> {INSTR_V}             { return Xas99Types.INSTR_V; }
<MNEMONIC> {INSTR_VI}            { return Xas99Types.INSTR_VI; }
<MNEMONIC> {INSTR_VII}           { yybegin(MNEMONICO); return Xas99Types.INSTR_VII; }
<MNEMONIC> {INSTR_VIII}          { return Xas99Types.INSTR_VIII; }
<MNEMONIC> {INSTR_VIII_I}        { return Xas99Types.INSTR_VIII_I; }
<MNEMONIC> {INSTR_VIII_R}        { return Xas99Types.INSTR_VIII_R; }
<MNEMONIC> {INSTR_IX}            { return Xas99Types.INSTR_IX; }
<MNEMONIC> {INSTR_IX_X}          { return Xas99Types.INSTR_IX_X; }
<MNEMONIC> {INSTR_O}             { yybegin(MNEMONICO); return Xas99Types.INSTR_O; }

<MNEMONIC> {DIR_L}               { return Xas99Types.DIR_L; }
<MNEMONIC> {DIR_E}               { return Xas99Types.DIR_E; }
<MNEMONIC> {DIR_EO}              { return Xas99Types.DIR_EO; }
<MNEMONIC> {DIR_ES}              { return Xas99Types.DIR_ES; }
<MNEMONIC> {DIR_S}               { return Xas99Types.DIR_S; }
<MNEMONIC> {DIR_O}               { yybegin(MNEMONICO); return Xas99Types.DIR_O; }
<MNEMONIC> {DIR_X}               { yybegin(MNEMONICO); return Xas99Types.DIR_X; }

<MNEMONIC> {PREP}                { yybegin(PREPROC); return Xas99Types.PREP; }

<MNEMONIC> {WS}                  { yybegin(ARGUMENTS); return Xas99Types.FIELD_SEP; }
<MNEMONICO> {WS}                 { yybegin(COMMENT); return Xas99Types.FIELD_SEP; }

<ARGUMENTS> {BLANK}? {REGISTER}  { yybegin(ARGUMENTS); return Xas99Types.REGISTER; }
<ARGUMENTS> {BLANK}? {IDENT}     { yybegin(ARGUMENTS); return Xas99Types.IDENT; }
<ARGUMENTS> {BLANK}? {INT}       { yybegin(ARGUMENTS); return Xas99Types.INT; }
<ARGUMENTS> {BLANK}? {TEXT}      { yybegin(ARGUMENTS); return Xas99Types.TEXT; }
<ARGUMENTS> {BLANK}? ","         { yybegin(ARGUMENTS); return Xas99Types.OP_SEP; }
<ARGUMENTS> {BLANK}? "@"         { yybegin(ARGUMENTS); return Xas99Types.OP_AT; }
<ARGUMENTS> {BLANK}? "*"         { yybegin(ARGUMENTS); return Xas99Types.OP_AST; }
<ARGUMENTS> {BLANK}? "+"         { yybegin(ARGUMENTS); return Xas99Types.OP_PLUS; }
<ARGUMENTS> {BLANK}? "-"         { yybegin(ARGUMENTS); return Xas99Types.OP_MINUS; }
<ARGUMENTS> {BLANK}? "~"         { yybegin(ARGUMENTS); return Xas99Types.OP_NOT; }
<ARGUMENTS> {BLANK}? "("         { yybegin(ARGUMENTS); return Xas99Types.OP_LPAREN; }
<ARGUMENTS> {BLANK}? ")"         { yybegin(ARGUMENTS); return Xas99Types.OP_RPAREN; }
<ARGUMENTS> {BLANK}? "$"         { yybegin(ARGUMENTS); return Xas99Types.OP_LC; }
<ARGUMENTS> {BLANK}? {OPER}      { yybegin(ARGUMENTS); return Xas99Types.OP_MISC; }
<ARGUMENTS> {FSEP}               { yybegin(COMMENT); return Xas99Types.FIELD_SEP; }

<PREPROC> {ANY}{ANY}*            { return Xas99Types.PREP_ARG; }

<COMMENT> [^\r\n]+               { yybegin(YYINITIAL); return Xas99Types.EOL_COMMENT; }

.                                { return TokenType.BAD_CHARACTER; }
