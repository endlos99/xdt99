package net.endlos.xdt99.xas99r;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import com.intellij.psi.TokenType;

%%

%class Xas99RLexer
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
DIR_ES = "DATA" | "BYTE" | "SAVE"
DIR_RA = "REQU"  // register alias
DIR_R = "REQU"
DIR_T = "TEXT" | "STRI"
DIR_S = "TITL" | "IDT"
DIR_C = "COPY" | "BCOPY"
DIR_O = "EVEN" | "UNL" | "LIST" | "PAGE" | "DXOP"
DIR_X = "PSEG" | "PEND" | "CSEG" | "CEND" | "DSEG" | "DEND" | "LOAD" | "SREF"
DIR_F = "FLOA"
DIR_R = "REF"

PREPROC = "." [A-Za-z0-9]+
PP_ARG = [^, \t\r\n]+
PP_PARM = "#" {DIGIT}+

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
REGISTER0 = [Rr] "0"
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
SPACES = {SPACE}+
BLANK = {SPACE} | \t
WS = {BLANK}+
CRLF = \n | \r | \r\n

%state MNEMONIC MNEMONICO ARGUMENTS PREPROC PRAGMA TLIT FLIT

%%

{PG_START}             { yybegin(PRAGMA); return Xas99RTypes.PG_START; }
{EOL_COMMENT}          { return Xas99RTypes.COMMENT; }
{CRLF}                 { yybegin(YYINITIAL); return Xas99RTypes.CRLF; }

<YYINITIAL> {
 {LINE_COMMENT}        { return Xas99RTypes.LCOMMENT; }
 ":"                   { return Xas99RTypes.OP_COLON; }
 {IDENT}               { return Xas99RTypes.IDENT; }
 {WS}                  { yybegin(MNEMONIC); return TokenType.WHITE_SPACE; }
}

<MNEMONIC> {
 {INSTR_I}             { return Xas99RTypes.INSTR_I; }
 {INSTR_II}            { return Xas99RTypes.INSTR_II; }
 {INSTR_III}           { return Xas99RTypes.INSTR_III; }
 {INSTR_IV}            { return Xas99RTypes.INSTR_IV; }
 {INSTR_V}             { return Xas99RTypes.INSTR_V; }
 {INSTR_VI}            { return Xas99RTypes.INSTR_VI; }
 {INSTR_VII}           { yybegin(MNEMONICO); return Xas99RTypes.INSTR_VII; }
 {INSTR_VIII}          { return Xas99RTypes.INSTR_VIII; }
 {INSTR_VIII_I}        { return Xas99RTypes.INSTR_VIII_I; }
 {INSTR_VIII_R}        { return Xas99RTypes.INSTR_VIII_R; }
 {INSTR_IX}            { return Xas99RTypes.INSTR_IX; }
 {INSTR_IX_X}          { return Xas99RTypes.INSTR_IX_X; }
 {INSTR_O}             { yybegin(MNEMONICO); return Xas99RTypes.INSTR_O; }
 {INSTR_9995_VI}       { return Xas99RTypes.INSTR_9995_VI; }
 {INSTR_9995_VIII}     { return Xas99RTypes.INSTR_9995_VIII; }
 {INSTR_99000_VI}      { return Xas99RTypes.INSTR_99000_VI; }
 {INSTR_99000_VIII}    { return Xas99RTypes.INSTR_99000_VIII; }
 {INSTR_99000_I}       { return Xas99RTypes.INSTR_99000_I; }
 {INSTR_99000_IV}      { return Xas99RTypes.INSTR_99000_IV; }
 {INSTR_F18A_IA}       { return Xas99RTypes.INSTR_F18A_IA; }
 {INSTR_F18A_VI}       { return Xas99RTypes.INSTR_F18A_VI; }
 {INSTR_F18A_O}        { yybegin(MNEMONICO); return Xas99RTypes.INSTR_F18A_O; }

 {DIR_L}               { return Xas99RTypes.DIR_L; }
 {DIR_E}               { return Xas99RTypes.DIR_E; }
 {DIR_EO}              { return Xas99RTypes.DIR_EO; }
 {DIR_ES}              { return Xas99RTypes.DIR_ES; }
 {DIR_RA}              { return Xas99RTypes.DIR_RA; }
 {DIR_R}               { return Xas99RTypes.DIR_R; }
 {DIR_T}               { return Xas99RTypes.DIR_T; }
 {DIR_S}               { return Xas99RTypes.DIR_S; }
 {DIR_C}               { return Xas99RTypes.DIR_C; }
 {DIR_F}               { return Xas99RTypes.DIR_F; }
 {DIR_R}               { return Xas99RTypes.DIR_R; }
 {DIR_O}               { yybegin(MNEMONICO); return Xas99RTypes.DIR_O; }
 {DIR_X}               { yybegin(MNEMONICO); return Xas99RTypes.DIR_X; }

 {PREPROC}             { yybegin(PREPROC); return Xas99RTypes.PREP; }

// {IDENT}               { return Xas99RTypes.UNKNOWN; }
 {WS}                  { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE; }
}

<MNEMONICO> {
 {WS}                  { return TokenType.WHITE_SPACE; }
}

<ARGUMENTS> {
 ","                   { return Xas99RTypes.OP_SEP; }
 "@"                   { return Xas99RTypes.OP_AT; }
 "*"                   { return Xas99RTypes.OP_AST; }
 "+"                   { return Xas99RTypes.OP_PLUS; }
 "-"                   { return Xas99RTypes.OP_MINUS; }
 "~"                   { return Xas99RTypes.OP_NOT; }
 "("                   { return Xas99RTypes.OP_LPAREN; }
 ")"                   { return Xas99RTypes.OP_RPAREN; }
 "$"                   { return Xas99RTypes.OP_LC; }
 {OPMISC}              { return Xas99RTypes.OP_MISC; }
 {REGISTER}            { return Xas99RTypes.REGISTER; }
 {REGISTER0}           { return Xas99RTypes.REGISTER0; }
 {IDENT}               { return Xas99RTypes.IDENT; }
 {INT}                 { return Xas99RTypes.INT; }
 {QUOTE}               { yybegin(TLIT); return Xas99RTypes.OP_QUOTE; }
 {FQUOTE}              { yybegin(FLIT); return Xas99RTypes.OP_FQUOTE; }
 {MOD_AUTO}            { return Xas99RTypes.MOD_AUTO; }
 {MOD_LEN}             { return Xas99RTypes.MOD_LEN; }
 {MOD_XBANK}           { return Xas99RTypes.MOD_XBANK; }
 {PP_PARM}             { return Xas99RTypes.PP_PARAM; }
 {SPACES}              { return TokenType.WHITE_SPACE; }
}

<PREPROC> {
 ","                   { return Xas99RTypes.PP_SEP; }
 {PP_ARG}              { return Xas99RTypes.PP_ARG; }
 {SPACES}              { return TokenType.WHITE_SPACE; }
}

<PRAGMA> {
 {PG_CYC}              { return Xas99RTypes.PG_CYC; }
 {PG_TERM}             { return Xas99RTypes.PG_TERM; }
 {PG_EQ}               { return Xas99RTypes.PG_EQ; }
 {PG_SEP}              { return Xas99RTypes.PG_SEP; }
 {WS}                  { return TokenType.WHITE_SPACE; }
}

<TLIT> {
 {QUOTE}              { yybegin(ARGUMENTS); return Xas99RTypes.OP_QUOTE; }
 {TEXT}               { return Xas99RTypes.TEXT; }
}

<FLIT> {
 {FQUOTE}             { yybegin(ARGUMENTS); return Xas99RTypes.OP_FQUOTE; }
 {FNAME}              { return Xas99RTypes.FNAME; }
}

[^]                    { return TokenType.BAD_CHARACTER; }
