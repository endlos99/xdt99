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
INSTR_F18A_IA = "SLC" | "PIX"
INSTR_F18A_VI = "CALL" | "PUSH" | "POP"
INSTR_F18A_O = "RET"
INSTR_9995_VI = "MPYS" | "DIVS"
INSTR_9995_VIII = "LST" | "LWP"
INSTR_99000_VI = "BIND"
INSTR_99000_VIII = "BLSK"
INSTR_99000_I = "AM" | "SM"
INSTR_99000_IV = "TMB" | "TCMB" | "TSMB" | "SLAM" | "SRAM"

DIR_L = "DEF" | "END"
DIR_E = "EQU" | "WEQU" | "BSS" | "BES" | "DORG" | "XORG" | "BANK"
DIR_EO = "RORG" | "AORG"
DIR_ES = "DATA" | "BYTE"
DIR_EV = "SAVE"
DIR_RA = "REQU"  // register alias
DIR_T = "TEXT" | "STRI"
DIR_S = "TITL" | "IDT"
DIR_C = "COPY" | "BCOPY"
DIR_O = "EVEN" | "UNL" | "LIST" | "PAGE" | "DXOP"
DIR_X = "PSEG" | "PEND" | "CSEG" | "CEND" | "DSEG" | "DEND" | "LOAD" | "SREF"
DIR_F = "FLOA"
DIR_R = "REF"

PPDEFM = ".DEFM"
PPCMD = ".IFDEF" | ".IFNDEF" | ".IFEQ" | ".IFNE" | ".IFGT" | ".IFGE" | ".IFLT" | ".IFLE" | ".REPT" | ".PRINT" | ".ERROR"
PPCMD0 = ".ELSE" | ".ENDIF" | ".ENDR" | ".ENDM"
PPMAC = "."
PPPARM = "#" {DIGIT}+

LINE_COMMENT = "*" [^\r\n]*
PG_START = ";:"
PG_TERM = ALPHA+
PG_EQ = "="
PG_SEP = ","
PG_CYC = [Ss][+-] | [Dd][+-]
EOL_COMMENT = ";" [^\r\n]*

IDENT = ("!"+ | [A-Za-z_]) {ALPHA}*
INT = {DIGIT}+ | ">" {HEX}+ | ":" [01]+
REGISTER = [Rr] ([1-9] | 1[0-5])
REGISTER0 = [Rr] "0"  // PeteE's special rule :-)
OPMISC = [/%&|\^]

ALPHA = [^-+*/%&!~\^()#\"',: \t\r\n]
DIGIT = [0-9]
HEX = [0-9A-Fa-f]

QUOTE = "'"
TEXT = ([^'\r\n] | "''")+
FQUOTE = "\""
FNAME = [^\"\r\n]+

MOD_AUTO = [BbWw] "#"
MOD_LEN = [Ss] "#"
MOD_XBANK = [Xx] "#"

SPACE = " "
BLANK = {SPACE} | \t
WS = {BLANK}+
FIELDSEP = {BLANK}{BLANK}+ | \t
CRLF = \n | \r | \r\n

%state MNEMONIC MNEMONICO ARGUMENTS COMMENT PRAGMA TLIT FLIT PP

%%

{PG_START}            { yybegin(PRAGMA); return Xas99Types.PG_START; }
{EOL_COMMENT}         { return Xas99Types.COMMENT; }
{CRLF}                { yybegin(YYINITIAL); return Xas99Types.CRLF; }

<YYINITIAL> {
 {LINE_COMMENT}       { return Xas99Types.LCOMMENT; }
 ":"                  { return Xas99Types.OP_COLON; }
 {IDENT}              { return Xas99Types.IDENT; }
 {WS}                 { yybegin(MNEMONIC); return TokenType.WHITE_SPACE; }
}

<MNEMONIC> {
 {INSTR_I}            { return Xas99Types.INSTR_I; }
 {INSTR_II}           { return Xas99Types.INSTR_II; }
 {INSTR_III}          { return Xas99Types.INSTR_III; }
 {INSTR_IV}           { return Xas99Types.INSTR_IV; }
 {INSTR_V}            { return Xas99Types.INSTR_V; }
 {INSTR_VI}           { return Xas99Types.INSTR_VI; }
 {INSTR_VII}          { yybegin(MNEMONICO); return Xas99Types.INSTR_VII; }
 {INSTR_VIII}         { return Xas99Types.INSTR_VIII; }
 {INSTR_VIII_I}       { return Xas99Types.INSTR_VIII_I; }
 {INSTR_VIII_R}       { return Xas99Types.INSTR_VIII_R; }
 {INSTR_IX}           { return Xas99Types.INSTR_IX; }
 {INSTR_IX_X}         { return Xas99Types.INSTR_IX_X; }
 {INSTR_O}            { yybegin(MNEMONICO); return Xas99Types.INSTR_O; }
 {INSTR_9995_VI}      { return Xas99Types.INSTR_9995_VI; }
 {INSTR_9995_VIII}    { return Xas99Types.INSTR_9995_VIII; }
 {INSTR_99000_VI}     { return Xas99Types.INSTR_99000_VI; }
 {INSTR_99000_VIII}   { return Xas99Types.INSTR_99000_VIII; }
 {INSTR_99000_I}      { return Xas99Types.INSTR_99000_I; }
 {INSTR_99000_IV}     { return Xas99Types.INSTR_99000_IV; }
 {INSTR_F18A_IA}      { return Xas99Types.INSTR_F18A_IA; }
 {INSTR_F18A_VI}      { return Xas99Types.INSTR_F18A_VI; }
 {INSTR_F18A_O}       { yybegin(MNEMONICO); return Xas99Types.INSTR_F18A_O; }

 {DIR_L}              { return Xas99Types.DIR_L; }
 {DIR_E}              { return Xas99Types.DIR_E; }
 {DIR_EO}             { return Xas99Types.DIR_EO; }
 {DIR_ES}             { return Xas99Types.DIR_ES; }
 {DIR_EV}             { return Xas99Types.DIR_EV; }
 {DIR_RA}             { return Xas99Types.DIR_RA; }
 {DIR_T}              { return Xas99Types.DIR_T; }
 {DIR_S}              { return Xas99Types.DIR_S; }
 {DIR_C}              { return Xas99Types.DIR_C; }
 {DIR_F}              { return Xas99Types.DIR_F; }
 {DIR_R}              { return Xas99Types.DIR_R; }
 {DIR_O}              { yybegin(MNEMONICO); return Xas99Types.DIR_O; }
 {DIR_X}              { yybegin(MNEMONICO); return Xas99Types.DIR_X; }

 {PPCMD}              { yybegin(ARGUMENTS); return Xas99Types.PPCMD; }
 {PPCMD0}             { yybegin(MNEMONICO); return Xas99Types.PPCMD0; }
 {PPDEFM}             { yybegin(ARGUMENTS); return Xas99Types.PPDEFM; }
 {PPMAC}              { yybegin(PP); return Xas99Types.PPMAC; }

// {IDENT}              { yybegin(COMMENT); return Xas99Types.UNKNOWN; }
 {WS}                 { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE; }
}
<MNEMONICO> {
 {WS}                 { yybegin(COMMENT); return TokenType.WHITE_SPACE; }
}

<PP> {
  {IDENT}             { yybegin(ARGUMENTS); return Xas99Types.IDENT; }
}

<ARGUMENTS> {
 ","                  { return Xas99Types.OP_SEP; }
 "@"                  { return Xas99Types.OP_AT; }
 "*"                  { return Xas99Types.OP_AST; }
 "+"                  { return Xas99Types.OP_PLUS; }
 "-"                  { return Xas99Types.OP_MINUS; }
 "~"                  { return Xas99Types.OP_NOT; }
 "("                  { return Xas99Types.OP_LPAREN; }
 ")"                  { return Xas99Types.OP_RPAREN; }
 "$"                  { return Xas99Types.OP_LC; }
 {OPMISC}             { return Xas99Types.OP_MISC; }
 {REGISTER0}          { return Xas99Types.REGISTER0; }
 {REGISTER}           { return Xas99Types.REGISTER; }
 {IDENT}              { return Xas99Types.IDENT; }
 {INT}                { return Xas99Types.INT; }
 {QUOTE}              { yybegin(TLIT); return Xas99Types.OP_QUOTE; }
 {FQUOTE}             { yybegin(FLIT); return Xas99Types.OP_FQUOTE; }
 {MOD_AUTO}           { return Xas99Types.MOD_AUTO; }
 {MOD_LEN}            { return Xas99Types.MOD_LEN; }
 {MOD_XBANK}          { return Xas99Types.MOD_XBANK; }
 {PPPARM}             { return Xas99Types.PP_PARAM; }
 {FIELDSEP}           { yybegin(COMMENT); return TokenType.WHITE_SPACE; }
 {SPACE}              { return TokenType.WHITE_SPACE; }
}

<PRAGMA> {
 {PG_CYC}             { return Xas99Types.PG_CYC; }
 {PG_TERM}            { return Xas99Types.PG_TERM; }
 {PG_EQ}              { return Xas99Types.PG_EQ; }
 {PG_SEP}             { return Xas99Types.PG_SEP; }
 {WS}                 { return TokenType.WHITE_SPACE; }
}

<TLIT> {
 {QUOTE}              { yybegin(ARGUMENTS); return Xas99Types.OP_QUOTE; }
 {TEXT}               { return Xas99Types.TEXT; }
}

<FLIT> {
 {FQUOTE}             { yybegin(ARGUMENTS); return Xas99Types.OP_FQUOTE; }
 {FNAME}              { return Xas99Types.FNAME; }
}

<COMMENT> {
 [^\r\n]+             { yybegin(YYINITIAL); return Xas99Types.COMMENT; }
}

[^]                   { return TokenType.BAD_CHARACTER; }
