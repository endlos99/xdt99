package net.endlos.xdt99.xga99;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xga99.psi.Xga99Types;
import com.intellij.psi.TokenType;

%%

%class Xga99Lexer
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

DIR_S = "AORG" | "BSS" | "EQU" | "GROM"
DIR_M = "BYTE" | "DATA" | "TEXT"

PREP = "." [A-Za-z0-9]+

LINE_COMMENT = "*" [^\r\n]*
EOL_COMMENT = ";" [^\r\n]*

IDENT = ("!"+ | [A-Za-z_]) {ALPHA}*
INT = {DIGIT}+ | ">" {HEX}+ | ":" [01]+
TEXT = "'" ([^'\r\n] | "''")* "'" | "\"" [^\"\r\n]* "\""
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

GADDR = "G@"
VADDR = "V@"
VINDR = "V*"

%state MNEMONIC FMNEMONIC MNEMONICO ARGUMENTS COMMENT PREPROC

%%

{EOL_COMMENT}          { return Xga99Types.COMMENT; }
{CRLF}                 { yybegin(YYINITIAL); return Xga99Types.CRLF; }

<YYINITIAL> {
 {LINE_COMMENT}        { return Xga99Types.LCOMMENT; }
 ":"                   { return Xga99Types.OP_COLON; }
 {IDENT}               { return Xga99Types.IDENT; }
 {WS}                  { if (fmtLevel > 0) yybegin(FMNEMONIC); else yybegin(MNEMONIC);
                         return TokenType.WHITE_SPACE; }
}

<MNEMONIC> {
 {INSTR_I}             { return Xga99Types.INSTR_I; }
 {INSTR_II}            { return Xga99Types.INSTR_II; }
 {INSTR_III}           { return Xga99Types.INSTR_III; }
 {INSTR_V}             { yybegin(MNEMONICO); return Xga99Types.INSTR_V; }
 {INSTR_VI}            { return Xga99Types.INSTR_VI; }
 {INSTR_VII}           { return Xga99Types.INSTR_VII; }
                       // optional argument for RAND, see note for FEND below
 {INSTR_VIII}          { return Xga99Types.INSTR_VIII; }
 {INSTR_IX}            { return Xga99Types.INSTR_IX; }
 {INSTR_X}             { fmtLevel = 1; yybegin(MNEMONICO); return Xga99Types.INSTR_X; }

 {DIR_S}               { return Xga99Types.DIR_S; }
 {DIR_M}               { return Xga99Types.DIR_M; }
 {PREP}                { yybegin(PREPROC); return Xga99Types.PREP; }
 {IDENT}               { yybegin(COMMENT); return Xga99Types.UNKNOWN; }
 {WS}                  { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE; }
}

<FMNEMONIC> {
 {INSTR_F_I}           { return Xga99Types.INSTR_F_I; }
 {INSTR_F_II}          { return Xga99Types.INSTR_F_II; }
 {INSTR_F_III}         { return Xga99Types.INSTR_F_III; }
 {INSTR_F_IV}          { return Xga99Types.INSTR_F_IV; }
 {INSTR_F_V}           { fmtLevel += 1; return Xga99Types.INSTR_F_V; }
 {INSTR_F_IX}          { return Xga99Types.INSTR_F_IX; }
 {INSTR_F_X}           { fmtLevel -= 1; return Xga99Types.INSTR_F_X; }
                       // NOTE: FEND may have an argument, so we cannot use FMNEMONICO,
                       //       and thus comments may not work here.
 {PREP}                { yybegin(PREPROC); return Xga99Types.PREP; }
 {IDENT}               { yybegin(COMMENT); return Xga99Types.UNKNOWN; }
 {WS}                  { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE; }
}

<MNEMONICO> {
 {WS}                  { yybegin(COMMENT); return TokenType.WHITE_SPACE; }
}

<ARGUMENTS> {
 ","                   { return Xga99Types.OP_SEP; }
 "@"                   { return Xga99Types.OP_AT; }
 "*"                   { return Xga99Types.OP_AST; }
 "+"                   { return Xga99Types.OP_PLUS; }
 "-"                   { return Xga99Types.OP_MINUS; }
 "~"                   { return Xga99Types.OP_NOT; }
 "("                   { return Xga99Types.OP_LPAREN; }
 ")"                   { return Xga99Types.OP_RPAREN; }
 "$"                   { return Xga99Types.OP_LC; }
 {OPMISC}              { return Xga99Types.OP_MISC; }
 {GADDR}               { return Xga99Types.GADDR; }
 {VADDR}               { return Xga99Types.VADDR; }
 {VINDR}               { return Xga99Types.VINDR; }
 {IDENT}               { return Xga99Types.IDENT; }
 {INT}                 { return Xga99Types.INT; }
 {TEXT}                { return Xga99Types.TEXT; }
 {PPPARM}              { return Xga99Types.PP_PARAM; }
 {FIELDSEP}            { yybegin(COMMENT); return TokenType.WHITE_SPACE; }
 {SPACE}               { return TokenType.WHITE_SPACE; }
}

<PREPROC> {
 ","                   { return Xga99Types.PP_SEP; }
 {PPARG}               { return Xga99Types.PP_ARG; }
 {FIELDSEP}            { yybegin(COMMENT); return TokenType.WHITE_SPACE; }
 {SPACE}               { return TokenType.WHITE_SPACE; }
}

<COMMENT> {
 [^\r\n]+              { yybegin(YYINITIAL); return Xga99Types.COMMENT; }
}

[^]                    { return TokenType.BAD_CHARACTER; }
