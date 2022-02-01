package net.endlos.xdt99.xbas99l;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99l.psi.Xbas99LTypes;
import com.intellij.psi.TokenType;

%%

%class Xbas99LLexer
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

//{WS}          { return TokenType.WHITE_SPACE; }
{CRLF}          { yybegin(YYINITIAL); return Xbas99LTypes.CRLF; }

<YYINITIAL> {
 {WS}           { yybegin(STMT); return TokenType.WHITE_SPACE; }
 {IDENT}        { yybegin(STMT); return Xbas99LTypes.LIDENT; }
}

<STMT> {
 "ACCEPT"       { return Xbas99LTypes.W_ACCEPT; }
 "ALL"          { return Xbas99LTypes.W_ALL; }
 "AND"          { return Xbas99LTypes.W_AND; }
 "APPEND"       { return Xbas99LTypes.W_APPEND; }
 "AT"           { return Xbas99LTypes.W_AT; }
 "BASE"         { return Xbas99LTypes.W_BASE; }
 "BEEP"         { return Xbas99LTypes.W_BEEP; }
 "BREAK"        { return Xbas99LTypes.W_BREAK; }
 "CALL"         { return Xbas99LTypes.W_CALL; }
 "CLOSE"        { return Xbas99LTypes.W_CLOSE; }
 "DATA"         { yybegin(DATA); return Xbas99LTypes.W_DATA; }
 "DEF"          { return Xbas99LTypes.W_DEF; }
 "DELETE"       { return Xbas99LTypes.W_DELETE; }
 "DIGIT"        { return Xbas99LTypes.W_DIGIT; }
 "DIM"          { return Xbas99LTypes.W_DIM; }
 "DISPLAY"      { return Xbas99LTypes.W_DISPLAY; }
 "ELSE"         { return Xbas99LTypes.W_ELSE; }
 "END"          { return Xbas99LTypes.W_END; }
 "ERASE"        { return Xbas99LTypes.W_ERASE; }
 "ERROR"        { return Xbas99LTypes.W_ERROR; }
 "FIXED"        { return Xbas99LTypes.W_FIXED; }
 "FOR"          { return Xbas99LTypes.W_FOR; }
 "GO"           { return Xbas99LTypes.W_GO; }
 "GOSUB"        { return Xbas99LTypes.W_GOSUB; }
 "GOTO"         { return Xbas99LTypes.W_GOTO; }
 "IF"           { return Xbas99LTypes.W_IF; }
 "IMAGE"        { yybegin(IMAGE); return Xbas99LTypes.W_IMAGE; }
 "INPUT"        { return Xbas99LTypes.W_INPUT; }
 "INTERNAL"     { return Xbas99LTypes.W_INTERNAL; }
 "LET"          { return Xbas99LTypes.W_LET; }
 "LINPUT"       { return Xbas99LTypes.W_LINPUT; }
 "NEXT"         { return Xbas99LTypes.W_NEXT; }
 "NOT"          { return Xbas99LTypes.W_NOT; }
 "NUMERIC"      { return Xbas99LTypes.W_NUMERIC; }
 "ON"           { return Xbas99LTypes.W_ON; }
 "OPEN"         { return Xbas99LTypes.W_OPEN; }
 "OPTION"       { return Xbas99LTypes.W_OPTION; }
 "OR"           { return Xbas99LTypes.W_OR; }
 "OUTPUT"       { return Xbas99LTypes.W_OUTPUT; }
 "PERMANENT"    { return Xbas99LTypes.W_PERMANENT; }
 "PRINT"        { return Xbas99LTypes.W_PRINT; }
 "RANDOMIZE"    { return Xbas99LTypes.W_RANDOMIZE; }
 "READ"         { return Xbas99LTypes.W_READ; }
 "RELATIVE"     { return Xbas99LTypes.W_RELATIVE; }
 "REM"          { yybegin(REM); return Xbas99LTypes.W_REM; }
 "RESTORE"      { return Xbas99LTypes.W_RESTORE; }
 "RETURN"       { return Xbas99LTypes.W_RETURN; }
 "RUN"          { return Xbas99LTypes.W_RUN; }
 "SEQUENTIAL"   { return Xbas99LTypes.W_SEQUENTIAL; }
 "SIZE"         { return Xbas99LTypes.W_SIZE; }
 "STEP"         { return Xbas99LTypes.W_STEP; }
 "STOP"         { return Xbas99LTypes.W_STOP; }
 "SUB"          { return Xbas99LTypes.W_SUB; }
 "SUBEND"       { return Xbas99LTypes.W_SUBEND; }
 "SUBEXIT"      { return Xbas99LTypes.W_SUBEXIT; }
 "THEN"         { return Xbas99LTypes.W_THEN; }
 "TO"           { return Xbas99LTypes.W_TO; }
 "TRACE"        { return Xbas99LTypes.W_TRACE; }
 "UALPHA"       { return Xbas99LTypes.W_UALPHA; }
 "UNBREAK"      { return Xbas99LTypes.W_UNBREAK; }
 "UNTRACE"      { return Xbas99LTypes.W_UNTRACE; }
 "UPDATE"       { return Xbas99LTypes.W_UPDATE; }
 "USING"        { return Xbas99LTypes.W_USING; }
 "VALIDATE"     { return Xbas99LTypes.W_VALIDATE; }
 "VARIABLE"     { return Xbas99LTypes.W_VARIABLE; }
 "WARNING"      { return Xbas99LTypes.W_WARNING; }
 "XOR"          { return Xbas99LTypes.W_XOR; }

 {FUNS}"$"      { return Xbas99LTypes.W_FUN_S; }
 {FUNN}         { return Xbas99LTypes.W_FUN_N; }
 {FUNC}         { return Xbas99LTypes.W_FUN_C; }
 {IDENT}"$"     { return Xbas99LTypes.SIDENT; }
 {IDENT}        { return Xbas99LTypes.IDENT; }
 {NUMBER}       { return Xbas99LTypes.NUMBER; }
 {FLOAT}        { return Xbas99LTypes.FLOAT; }
 {QUOTE}        { yybegin(STRING); return Xbas99LTypes.OP_QUOTE; }

 "::"           { return Xbas99LTypes.OP_SEP; }
 ":"            { return Xbas99LTypes.OP_COLON; }
 ","            { return Xbas99LTypes.OP_COMMA; }
 ";"            { return Xbas99LTypes.OP_SEMI; }
 "="            { return Xbas99LTypes.OP_EQ; }
 "<"            { return Xbas99LTypes.OP_LT; }
 ">"            { return Xbas99LTypes.OP_GT; }
 "#"            { return Xbas99LTypes.OP_HASH; }
 "("            { return Xbas99LTypes.OP_LPAREN; }
 ")"            { return Xbas99LTypes.OP_RPAREN; }
 "&"            { return Xbas99LTypes.OP_AMP; }
 "*"            { return Xbas99LTypes.OP_MUL; }
 "/"            { return Xbas99LTypes.OP_DIV; }
 "+"            { return Xbas99LTypes.OP_PLUS; }
 "-"            { return Xbas99LTypes.OP_MINUS; }
 "^"            { return Xbas99LTypes.OP_EXP; }
 "!"            { yybegin(REM); return Xbas99LTypes.W_BANG; }
 "$"            { return Xbas99LTypes.OP_STR; }  // usually not returned, but needed for var$ code completion
 {WS}           { return TokenType.WHITE_SPACE; }
}

<DATA> {
 ","            { return Xbas99LTypes.OP_COMMA; }
 {PART}+        { return Xbas99LTypes.A_DATA; }
 {WS}           { return TokenType.WHITE_SPACE; }
}

<IMAGE> {
 {ANY}+         { return Xbas99LTypes.A_IMAGE; }
 {WS}           { return TokenType.WHITE_SPACE; }
}

<STRING> {
 {QUOTE}        { yybegin(STMT); return Xbas99LTypes.OP_QUOTE; }
 {QSTRING}      { return Xbas99LTypes.QSTRING; }
}

<REM> {
 {ANY}+         { return Xbas99LTypes.COMMENT; }
}

[^]             { return TokenType.BAD_CHARACTER; }
