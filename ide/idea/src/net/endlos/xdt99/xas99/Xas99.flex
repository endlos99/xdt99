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

DIR_L = "DEF" | "REF" | "END"
DIR_E = "EQU" | "BSS" | "BES" | "AORG" | "DORG"
DIR_EO = "RORG"
DIR_ES = "DATA" | "BYTE"
DIR_S = "TITL" | "IDT" | "COPY" | "TEXT" | "IBYTE"
DIR_O = "EVEN" | "UNL" | "LIST" | "PAGE" | "DXOP"
DIR_X = "PSEG" | "PEND" | "CSEG" | "CEND" | "DSEG" | "DEND" | "LOAD" | "SREF"

PREP = "." [A-Za-z0-9]+

LINE_COMMENT = "*" [^\r\n]*
EOL_COMMENT = ";" [^\r\n]*

IDENT = ("!"+ | [A-Za-z_]) {ALPHA}*
INT = {DIGIT}+ | ">" {HEX}+ | ":" [01]+
TEXT = "'" ([^'\r\n] | "''")* "'" | "\"" [^\"\r\n]* "\""
REGISTER = [Rr] ([0-9] | 1[0-5])
OPMISC = [/%&|\^]
PPARG = [^, \t\r\n]+
PPPARM = "#" {DIGIT}+

ALPHA = [^@$!,;>:+\-*/\^&|~() \t\r\n]
DIGIT = [0-9]
HEX = [0-9A-Fa-f]

SPACE = " "
BLANK = {SPACE} | \t
WS = {BLANK}+
FIELDSEP = {BLANK}{BLANK}+ | \t
CRLF = \n | \r | \r\n

%state MNEMONIC
%state MNEMONICO
%state ARGUMENTS
%state COMMENT
%state PREPROC

%%

{EOL_COMMENT}                    { return Xas99Types.COMMENT; }
{CRLF}                           { yybegin(YYINITIAL); return Xas99Types.CRLF; }

<YYINITIAL> {LINE_COMMENT}       { return Xas99Types.LCOMMENT; }
<YYINITIAL> ":"                  { return Xas99Types.OP_COLON; }
<YYINITIAL> {IDENT}              { return Xas99Types.IDENT; }

<YYINITIAL> {WS}                 { yybegin(MNEMONIC); return TokenType.WHITE_SPACE; }

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

<MNEMONIC> {IDENT}               { yybegin(COMMENT); return Xas99Types.UNKNOWN; }
<MNEMONIC> {WS}                  { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE; }
<MNEMONICO> {WS}                 { yybegin(COMMENT); return TokenType.WHITE_SPACE; }

<ARGUMENTS> ","                  { return Xas99Types.OP_SEP; }
<ARGUMENTS> "@"                  { return Xas99Types.OP_AT; }
<ARGUMENTS> "*"                  { return Xas99Types.OP_AST; }
<ARGUMENTS> "+"                  { return Xas99Types.OP_PLUS; }
<ARGUMENTS> "-"                  { return Xas99Types.OP_MINUS; }
<ARGUMENTS> "~"                  { return Xas99Types.OP_NOT; }
<ARGUMENTS> "("                  { return Xas99Types.OP_LPAREN; }
<ARGUMENTS> ")"                  { return Xas99Types.OP_RPAREN; }
<ARGUMENTS> "$"                  { return Xas99Types.OP_LC; }
<ARGUMENTS> {OPMISC}             { return Xas99Types.OP_MISC; }
<ARGUMENTS> {REGISTER}           { return Xas99Types.REGISTER; }
<ARGUMENTS> {IDENT}              { return Xas99Types.IDENT; }
<ARGUMENTS> {INT}                { return Xas99Types.INT; }
<ARGUMENTS> {TEXT}               { return Xas99Types.TEXT; }
<ARGUMENTS> {PPPARM}             { return Xas99Types.PP_PARAM; }
<ARGUMENTS> {FIELDSEP}           { yybegin(COMMENT); return TokenType.WHITE_SPACE; }
<ARGUMENTS> {SPACE}              { return TokenType.WHITE_SPACE; }

<PREPROC> ","                    { return Xas99Types.PP_SEP; }
<PREPROC> {PPARG}                { return Xas99Types.PP_ARG; }
<PREPROC> {FIELDSEP}             { yybegin(COMMENT); return TokenType.WHITE_SPACE; }
<PREPROC> {SPACE}                { return TokenType.WHITE_SPACE; }

<COMMENT> [^\r\n]+               { yybegin(YYINITIAL); return Xas99Types.COMMENT; }

[^]                              { return TokenType.BAD_CHARACTER; }
