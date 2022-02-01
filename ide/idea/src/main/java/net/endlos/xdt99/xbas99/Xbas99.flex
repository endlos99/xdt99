package net.endlos.xdt99.xbas99;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import com.intellij.psi.TokenType;

%%

%class Xbas99Lexer
%implements FlexLexer
%unicode
%function advance
%type IElementType
%eof{  return;
%eof}

%ignorecase

FUNN = "ABS" | "ASC" | "ATN" | "COS" | "EOF" | "EXP" | "INT" | "LEN" | "LOG" | "MAX" |
       "MIN" | "POS" | "REC" | "SGN" | "SIN" | "SQR" | "TAB" | "TAN" | "VAL"
FUNS = "CHR" | "RPT" | "SEG" | "STR"
FUNC = "PI" | "RND"

IDENT = {ALPHA}({ALPHA}|{DIGIT})*
NUMBER = {DIGIT}+
EXP = [Ee] "-"? {DIGIT}+
FLOAT = {DIGIT}+ {EXP} | {DIGIT}* "." {DIGIT}* {EXP}?

QUOTE = "\""
QSTRING = ([^\"\r\n] | "\"\"")+

ALPHA = [A-Za-z_@\[\]\\]
DIGIT = [0-9]

BLANK = " " | \t
CRLF = \n | \r | \r\n
WS = {BLANK}+
ANY = [^\r\n]
PART = [^,\r\n]

%state STMT DATA IMAGE REM STRING

%%

{WS}            { return TokenType.WHITE_SPACE; }
{CRLF}          { yybegin(YYINITIAL); return Xbas99Types.CRLF; }

<YYINITIAL> {
 {NUMBER}       { yybegin(STMT); return Xbas99Types.LNUMBER; }
}

<STMT> {
 "ACCEPT"       { return Xbas99Types.W_ACCEPT; }
 "ALL"          { return Xbas99Types.W_ALL; }
 "AND"          { return Xbas99Types.W_AND; }
 "APPEND"       { return Xbas99Types.W_APPEND; }
 "AT"           { return Xbas99Types.W_AT; }
 "BASE"         { return Xbas99Types.W_BASE; }
 "BEEP"         { return Xbas99Types.W_BEEP; }
 "BREAK"        { return Xbas99Types.W_BREAK; }
 "CALL"         { return Xbas99Types.W_CALL; }
 "CLOSE"        { return Xbas99Types.W_CLOSE; }
 "DATA"         { yybegin(DATA); return Xbas99Types.W_DATA; }
 "DEF"          { return Xbas99Types.W_DEF; }
 "DELETE"       { return Xbas99Types.W_DELETE; }
 "DIGIT"        { return Xbas99Types.W_DIGIT; }
 "DIM"          { return Xbas99Types.W_DIM; }
 "DISPLAY"      { return Xbas99Types.W_DISPLAY; }
 "ELSE"         { return Xbas99Types.W_ELSE; }
 "END"          { return Xbas99Types.W_END; }
 "ERASE"        { return Xbas99Types.W_ERASE; }
 "ERROR"        { return Xbas99Types.W_ERROR; }
 "FIXED"        { return Xbas99Types.W_FIXED; }
 "FOR"          { return Xbas99Types.W_FOR; }
 "GO"           { return Xbas99Types.W_GO; }
 "GOSUB"        { return Xbas99Types.W_GOSUB; }
 "GOTO"         { return Xbas99Types.W_GOTO; }
 "IF"           { return Xbas99Types.W_IF; }
 "IMAGE"        { yybegin(IMAGE); return Xbas99Types.W_IMAGE; }
 "INPUT"        { return Xbas99Types.W_INPUT; }
 "INTERNAL"     { return Xbas99Types.W_INTERNAL; }
 "LET"          { return Xbas99Types.W_LET; }
 "LINPUT"       { return Xbas99Types.W_LINPUT; }
 "NEXT"         { return Xbas99Types.W_NEXT; }
 "NOT"          { return Xbas99Types.W_NOT; }
 "NUMERIC"      { return Xbas99Types.W_NUMERIC; }
 "ON"           { return Xbas99Types.W_ON; }
 "OPEN"         { return Xbas99Types.W_OPEN; }
 "OPTION"       { return Xbas99Types.W_OPTION; }
 "OR"           { return Xbas99Types.W_OR; }
 "OUTPUT"       { return Xbas99Types.W_OUTPUT; }
 "PERMANENT"    { return Xbas99Types.W_PERMANENT; }
 "PRINT"        { return Xbas99Types.W_PRINT; }
 "RANDOMIZE"    { return Xbas99Types.W_RANDOMIZE; }
 "READ"         { return Xbas99Types.W_READ; }
 "RELATIVE"     { return Xbas99Types.W_RELATIVE; }
 "REM"          { yybegin(REM); return Xbas99Types.W_REM; }
 "RESTORE"      { return Xbas99Types.W_RESTORE; }
 "RETURN"       { return Xbas99Types.W_RETURN; }
 "RUN"          { return Xbas99Types.W_RUN; }
 "SEQUENTIAL"   { return Xbas99Types.W_SEQUENTIAL; }
 "SIZE"         { return Xbas99Types.W_SIZE; }
 "STEP"         { return Xbas99Types.W_STEP; }
 "STOP"         { return Xbas99Types.W_STOP; }
 "SUB"          { return Xbas99Types.W_SUB; }
 "SUBEND"       { return Xbas99Types.W_SUBEND; }
 "SUBEXIT"      { return Xbas99Types.W_SUBEXIT; }
 "THEN"         { return Xbas99Types.W_THEN; }
 "TO"           { return Xbas99Types.W_TO; }
 "TRACE"        { return Xbas99Types.W_TRACE; }
 "UALPHA"       { return Xbas99Types.W_UALPHA; }
 "UNBREAK"      { return Xbas99Types.W_UNBREAK; }
 "UNTRACE"      { return Xbas99Types.W_UNTRACE; }
 "UPDATE"       { return Xbas99Types.W_UPDATE; }
 "USING"        { return Xbas99Types.W_USING; }
 "VALIDATE"     { return Xbas99Types.W_VALIDATE; }
 "VARIABLE"     { return Xbas99Types.W_VARIABLE; }
 "WARNING"      { return Xbas99Types.W_WARNING; }
 "XOR"          { return Xbas99Types.W_XOR; }

 {FUNS}"$"      { return Xbas99Types.W_FUN_S; }
 {FUNN}         { return Xbas99Types.W_FUN_N; }
 {FUNC}         { return Xbas99Types.W_FUN_C; }
 {IDENT}"$"     { return Xbas99Types.SIDENT; }
 {IDENT}        { return Xbas99Types.IDENT; }
 {NUMBER}       { return Xbas99Types.NUMBER; }
 {FLOAT}        { return Xbas99Types.FLOAT; }
 {QUOTE}        { yybegin(STRING); return Xbas99Types.OP_QUOTE; }

 "::"           { return Xbas99Types.OP_SEP; }
 ":"            { return Xbas99Types.OP_COLON; }
 ","            { return Xbas99Types.OP_COMMA; }
 ";"            { return Xbas99Types.OP_SEMI; }
 "="            { return Xbas99Types.OP_EQ; }
 "<"            { return Xbas99Types.OP_LT; }
 ">"            { return Xbas99Types.OP_GT; }
 "#"            { return Xbas99Types.OP_HASH; }
 "("            { return Xbas99Types.OP_LPAREN; }
 ")"            { return Xbas99Types.OP_RPAREN; }
 "&"            { return Xbas99Types.OP_AMP; }
 "*"            { return Xbas99Types.OP_MUL; }
 "/"            { return Xbas99Types.OP_DIV; }
 "+"            { return Xbas99Types.OP_PLUS; }
 "-"            { return Xbas99Types.OP_MINUS; }
 "^"            { return Xbas99Types.OP_EXP; }
 "!"            { yybegin(REM); return Xbas99Types.W_BANG; }
 "$"            { return Xbas99Types.OP_STR; }  // usually not returned, but needed for var$ code completion
}

<STRING> {
 {QUOTE}        { yybegin(STMT); return Xbas99Types.OP_QUOTE; }
 {QSTRING}      { return Xbas99Types.QSTRING; }
}

<DATA> {
 ","            { return Xbas99Types.OP_COMMA; }
 {PART}+        { return Xbas99Types.A_DATA; }
}

<IMAGE> {
 {ANY}+         { return Xbas99Types.A_IMAGE; }
}

<REM> {
 {ANY}+         { return Xbas99Types.COMMENT; }
}

[^]             { return TokenType.BAD_CHARACTER; }
