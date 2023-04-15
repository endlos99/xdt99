package net.endlos.xdt99.xga99r;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import com.intellij.psi.TokenType;

%%

%class Xga99RLexer
%implements FlexLexer
%unicode
%function advance
%type IElementType
%eof{  return;
%eof}

%{
  private int fmtLevel = 0;
%}

%ignorecase

INSTR_I = "ADD" | "DADD" | "AND" | "DAND" | "CGE" | "DCGE" | "CEQ" | "DCEQ" | "CGT" | "DCGT" | "CH" | "DCH" |
          "CHE" | "DCHE" | "CLOG" | "DCLOG" | "COINC" | "EX" | "DEX" | "DIV" | "DDIV" | "MUL" | "DMUL" |
          "OR" | "DOR" | "SLL" | "DSLL" | "SRA" | "DSRA" | "SRC" | "DSRC" | "SRL" | "DSRL" | "ST" | "DST" |
          "SUB" | "DSUB" | "SWGR" | "DSWGR" | "XOR" | "DXOR"
INSTR_II = "ALL" | "BACK" | "PARSE" | "XML"
INSTR_III = "B" | "BR" | "BS" | "CALL"
INSTR_V =  "CARRY" | "CONT" | "EXEC" | "EXIT" | "GT" | "H" | "OVF" | "RTGR" | "RTN" | "RTNB" | "RTNC" | "SCAN"
INSTR_VI = "ABS" | "DABS" | "CASE" | "DCASE" | "CLR" | "DCLR" | "CZ" | "DCZ" | "DEC" | "DDEC" | "DECT" | "DDECT" |
           "FETCH" | "INC" | "DINC" | "INCT" | "DINCT" | "INV" | "DINV" | "NEG" | "DNEG" | "PUSH"
INSTR_VII = "RAND"  // special case of INSTR_II
INSTR_VIII = "I/O"
INSTR_IX = "MOVE"
INSTR_X = "FMT"

INSTR_F_I = "COL" | "COL+" | "ROW" | "ROW+"
INSTR_F_II = "BIAS"
INSTR_F_III = "HCHAR" | "VCHAR"
INSTR_F_IV = "HTEXT" | "VTEXT"
INSTR_F_V = "FOR"
INSTR_F_IX = "HMOVE"
INSTR_F_X = "FEND"

DIR_L = "END"
DIR_S = "AORG" | "BSS" | "EQU" | "GROM"
DIR_M = "BYTE" | "DATA"
DIR_T = "TEXT" | "STRI" | "TITLE"
DIR_C = "COPY" | "BCOPY"
DIR_F = "FLOAT"

PPDEFM = ".DEFM"
PPCMD = ".IFDEF" | ".IFNDEF" | ".IFEQ" | ".IFNE" | ".IFGT" | ".IFGE" | ".IFLT" | ".IFLE" | ".REPT" | ".PRINT" | ".ERROR"
PPCMD0 = ".ELSE" | ".ENDIF" | ".ENDR" | ".ENDM"
PPMAC = "."
PPPARM = "$" {DIGIT}+

LINE_COMMENT = "*" [^\r\n]*
EOL_COMMENT = ";" [^\r\n]*

IDENT = ("!"+ | [A-Za-z_]) {ALPHA}*
INT = {DIGIT}+ | ">" {HEX}+ | ":" [01]+
OPMISC = [/%&|\^]
VREG = "#" {DIGIT}

ALPHA = [^-+*/%&|~\^()#@\"',: \t\r\n]
DIGIT = [0-9]
HEX = [0-9A-Fa-f]

QUOTE = "'"
TEXT = ([^'\r\n] | "''")+
FQUOTE = "\""
FNAME = [^\"\r\n]+

SPACE = " "
SPACES = {SPACE}+
BLANK = {SPACE} | \t
WS = {BLANK}+
CRLF = \n | \r | \r\n

GADDR = "G@" | "g@"
VADDR = "V@" | "v@"
VINDR = "V*" | "v*"

%state MNEMONIC FMNEMONIC MNEMONICO ARGUMENTS PP TLIT FLIT

%%

{EOL_COMMENT}          { return Xga99RTypes.COMMENT; }
{CRLF}                 { yybegin(YYINITIAL); return Xga99RTypes.CRLF; }

<YYINITIAL> {
 {LINE_COMMENT}        { return Xga99RTypes.LCOMMENT; }
 ":"                   { return Xga99RTypes.OP_COLON; }
 {IDENT}               { return Xga99RTypes.IDENT; }
 {WS}                  { if (fmtLevel > 0) yybegin(FMNEMONIC); else yybegin(MNEMONIC);
                         return TokenType.WHITE_SPACE; }
}

<MNEMONIC> {
 {INSTR_I}             { return Xga99RTypes.INSTR_I; }
 {INSTR_II}            { return Xga99RTypes.INSTR_II; }
 {INSTR_III}           { return Xga99RTypes.INSTR_III; }
 {INSTR_V}             { yybegin(MNEMONICO); return Xga99RTypes.INSTR_V; }
 {INSTR_VI}            { return Xga99RTypes.INSTR_VI; }
 {INSTR_VII}           { return Xga99RTypes.INSTR_VII; }
                       // optional argument for RAND, see note for FEND below
 {INSTR_VIII}          { return Xga99RTypes.INSTR_VIII; }
 {INSTR_IX}            { return Xga99RTypes.INSTR_IX; }
 {INSTR_X}             { fmtLevel = 1; yybegin(MNEMONICO); return Xga99RTypes.INSTR_X; }

 {DIR_L}               { return Xga99RTypes.DIR_L; }
 {DIR_S}               { return Xga99RTypes.DIR_S; }
 {DIR_M}               { return Xga99RTypes.DIR_M; }
 {DIR_T}               { return Xga99RTypes.DIR_T; }
 {DIR_C}               { return Xga99RTypes.DIR_C; }
 {DIR_F}               { return Xga99RTypes.DIR_F; }

 {PPCMD}               { yybegin(ARGUMENTS); return Xga99RTypes.PPCMD; }
 {PPCMD0}              { yybegin(MNEMONICO); return Xga99RTypes.PPCMD0; }
 {PPDEFM}              { yybegin(ARGUMENTS); return Xga99RTypes.PPDEFM; }
 {PPMAC}               { yybegin(PP); return Xga99RTypes.PPMAC; }

 {IDENT}               { return Xga99RTypes.UNKNOWN; }
 {WS}                  { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE; }
}

<FMNEMONIC> {
 {INSTR_F_I}           { return Xga99RTypes.INSTR_F_I; }
 {INSTR_F_II}          { return Xga99RTypes.INSTR_F_II; }
 {INSTR_F_III}         { return Xga99RTypes.INSTR_F_III; }
 {INSTR_F_IV}          { return Xga99RTypes.INSTR_F_IV; }
 {INSTR_F_V}           { fmtLevel += 1; return Xga99RTypes.INSTR_F_V; }
 {INSTR_F_IX}          { return Xga99RTypes.INSTR_F_IX; }
 {INSTR_F_X}           { fmtLevel -= 1; return Xga99RTypes.INSTR_F_X; }
                       // NOTE: FEND may have an argument, so we cannot use FMNEMONICO,
                       //       and thus comments may not work here.
 {PPCMD}               { yybegin(ARGUMENTS); return Xga99RTypes.PPCMD; }
 {PPDEFM}              { yybegin(ARGUMENTS); return Xga99RTypes.PPDEFM; }
 {PPMAC}               { yybegin(PP); return Xga99RTypes.PPMAC; }

 {IDENT}               { return Xga99RTypes.UNKNOWN; }
 {WS}                  { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE; }
}

<MNEMONICO> {
 {WS}                  { return TokenType.WHITE_SPACE; }
}

<PP> {
  {IDENT}              { yybegin(ARGUMENTS); return Xga99RTypes.IDENT; }
}

<ARGUMENTS> {
 ","                   { return Xga99RTypes.OP_SEP; }
 "@"                   { return Xga99RTypes.OP_AT; }
 "*"                   { return Xga99RTypes.OP_AST; }
 "+"                   { return Xga99RTypes.OP_PLUS; }
 "-"                   { return Xga99RTypes.OP_MINUS; }
 "~"                   { return Xga99RTypes.OP_NOT; }
 "("                   { return Xga99RTypes.OP_LPAREN; }
 ")"                   { return Xga99RTypes.OP_RPAREN; }
 "$"                   { return Xga99RTypes.OP_LC; }
 {OPMISC}              { return Xga99RTypes.OP_MISC; }
 {GADDR}               { return Xga99RTypes.GADDR; }
 {VADDR}               { return Xga99RTypes.VADDR; }
 {VINDR}               { return Xga99RTypes.VINDR; }
 {IDENT}               { return Xga99RTypes.IDENT; }
 {INT}                 { return Xga99RTypes.INT; }
 {VREG}                { return Xga99RTypes.VREG; }
 {QUOTE}               { yybegin(TLIT); return Xga99RTypes.OP_QUOTE; }
 {FQUOTE}              { yybegin(FLIT); return Xga99RTypes.OP_FQUOTE; }
 {PPPARM}              { return Xga99RTypes.PP_PARAM; }
 {SPACES}              { return TokenType.WHITE_SPACE; }
}

<TLIT> {
 {QUOTE}              { yybegin(ARGUMENTS); return Xga99RTypes.OP_QUOTE; }
 {TEXT}               { return Xga99RTypes.TEXT; }
}

<FLIT> {
 {FQUOTE}             { yybegin(ARGUMENTS); return Xga99RTypes.OP_FQUOTE; }
 {FNAME}              { return Xga99RTypes.FNAME; }
}

[^]                    { return TokenType.BAD_CHARACTER; }
