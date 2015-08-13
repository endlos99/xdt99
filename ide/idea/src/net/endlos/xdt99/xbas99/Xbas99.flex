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
QSTRING = "\"" ([^\"\r\n] | "\"\"")* "\""

ALPHA = [A-Za-z_@\[\]\\]
DIGIT = [0-9]

BLANK = " " | \t
CRLF = \n | \r | \r\n
WS = {BLANK}+
ANY = [^\r\n]
PART = [^,\r\n]

%state STMT
%state DATA
%state IMAGE
%state REM

%%

{WS}                  { return TokenType.WHITE_SPACE; }
{CRLF}                { yybegin(YYINITIAL); return Xbas99Types.CRLF; }

<YYINITIAL> {NUMBER}  { yybegin(STMT); return Xbas99Types.LNUMBER; }

<STMT> "ACCEPT"       { return Xbas99Types.W_ACCEPT; }
<STMT> "ALL"          { return Xbas99Types.W_ALL; }
<STMT> "AND"          { return Xbas99Types.W_AND; }
<STMT> "APPEND"       { return Xbas99Types.W_APPEND; }
<STMT> "AT"           { return Xbas99Types.W_AT; }
<STMT> "BASE"         { return Xbas99Types.W_BASE; }
<STMT> "BEEP"         { return Xbas99Types.W_BEEP; }
<STMT> "BREAK"        { return Xbas99Types.W_BREAK; }
<STMT> "CALL"         { return Xbas99Types.W_CALL; }
<STMT> "CLOSE"        { return Xbas99Types.W_CLOSE; }
<STMT> "DATA"         { yybegin(DATA); return Xbas99Types.W_DATA; }
<STMT> "DEF"          { return Xbas99Types.W_DEF; }
<STMT> "DELETE"       { return Xbas99Types.W_DELETE; }
<STMT> "DIGIT"        { return Xbas99Types.W_DIGIT; }
<STMT> "DIM"          { return Xbas99Types.W_DIM; }
<STMT> "DISPLAY"      { return Xbas99Types.W_DISPLAY; }
<STMT> "ELSE"         { return Xbas99Types.W_ELSE; }
<STMT> "END"          { return Xbas99Types.W_END; }
<STMT> "ERASE"        { return Xbas99Types.W_ERASE; }
<STMT> "ERROR"        { return Xbas99Types.W_ERROR; }
<STMT> "FIXED"        { return Xbas99Types.W_FIXED; }
<STMT> "FOR"          { return Xbas99Types.W_FOR; }
<STMT> "GO"           { return Xbas99Types.W_GO; }
<STMT> "GOSUB"        { return Xbas99Types.W_GOSUB; }
<STMT> "GOTO"         { return Xbas99Types.W_GOTO; }
<STMT> "IF"           { return Xbas99Types.W_IF; }
<STMT> "IMAGE"        { yybegin(IMAGE); return Xbas99Types.W_IMAGE; }
<STMT> "INPUT"        { return Xbas99Types.W_INPUT; }
<STMT> "INTERNAL"     { return Xbas99Types.W_INTERNAL; }
<STMT> "LET"          { return Xbas99Types.W_LET; }
<STMT> "LINPUT"       { return Xbas99Types.W_LINPUT; }
<STMT> "NEXT"         { return Xbas99Types.W_NEXT; }
<STMT> "NOT"          { return Xbas99Types.W_NOT; }
<STMT> "NUMERIC"      { return Xbas99Types.W_NUMERIC; }
<STMT> "ON"           { return Xbas99Types.W_ON; }
<STMT> "OPEN"         { return Xbas99Types.W_OPEN; }
<STMT> "OPTION"       { return Xbas99Types.W_OPTION; }
<STMT> "OR"           { return Xbas99Types.W_OR; }
<STMT> "OUTPUT"       { return Xbas99Types.W_OUTPUT; }
<STMT> "PERMANENT"    { return Xbas99Types.W_PERMANENT; }
<STMT> "PRINT"        { return Xbas99Types.W_PRINT; }
<STMT> "RANDOMIZE"    { return Xbas99Types.W_RANDOMIZE; }
<STMT> "READ"         { return Xbas99Types.W_READ; }
<STMT> "RELATIVE"     { return Xbas99Types.W_RELATIVE; }
<STMT> "REM"          { yybegin(REM); return Xbas99Types.W_REM; }
<STMT> "RESTORE"      { return Xbas99Types.W_RESTORE; }
<STMT> "RETURN"       { return Xbas99Types.W_RETURN; }
<STMT> "RUN"          { return Xbas99Types.W_RUN; }
<STMT> "SEQUENTIAL"   { return Xbas99Types.W_SEQUENTIAL; }
<STMT> "SIZE"         { return Xbas99Types.W_SIZE; }
<STMT> "STEP"         { return Xbas99Types.W_STEP; }
<STMT> "STOP"         { return Xbas99Types.W_STOP; }
<STMT> "SUB"          { return Xbas99Types.W_SUB; }
<STMT> "SUBEND"       { return Xbas99Types.W_SUBEND; }
<STMT> "SUBEXIT"      { return Xbas99Types.W_SUBEXIT; }
<STMT> "THEN"         { return Xbas99Types.W_THEN; }
<STMT> "TO"           { return Xbas99Types.W_TO; }
<STMT> "TRACE"        { return Xbas99Types.W_TRACE; }
<STMT> "UALPHA"       { return Xbas99Types.W_UALPHA; }
<STMT> "UNBREAK"      { return Xbas99Types.W_UNBREAK; }
<STMT> "UNTRACE"      { return Xbas99Types.W_UNTRACE; }
<STMT> "UPDATE"       { return Xbas99Types.W_UPDATE; }
<STMT> "USING"        { return Xbas99Types.W_USING; }
<STMT> "VALIDATE"     { return Xbas99Types.W_VALIDATE; }
<STMT> "VARIABLE"     { return Xbas99Types.W_VARIABLE; }
<STMT> "WARNING"      { return Xbas99Types.W_WARNING; }
<STMT> "XOR"          { return Xbas99Types.W_XOR; }

<STMT> {FUNS}"$"      { return Xbas99Types.W_FUN_S; }
<STMT> {FUNN}         { return Xbas99Types.W_FUN_N; }
<STMT> {FUNC}         { return Xbas99Types.W_FUN_C; }
<STMT> {IDENT}"$"     { return Xbas99Types.SIDENT; }
<STMT> {IDENT}        { return Xbas99Types.IDENT; }
<STMT> {NUMBER}       { return Xbas99Types.NUMBER; }
<STMT> {FLOAT}        { return Xbas99Types.FLOAT; }
<STMT> {QSTRING}      { return Xbas99Types.QSTRING; }

<STMT> "::"           { return Xbas99Types.OP_SEP; }
<STMT> ":"            { return Xbas99Types.OP_COLON; }
<STMT> ","            { return Xbas99Types.OP_COMMA; }
<STMT> ";"            { return Xbas99Types.OP_SEMI; }
<STMT> "="            { return Xbas99Types.OP_EQ; }
<STMT> "<"            { return Xbas99Types.OP_LT; }
<STMT> ">"            { return Xbas99Types.OP_GT; }
<STMT> "#"            { return Xbas99Types.OP_HASH; }
<STMT> "("            { return Xbas99Types.OP_LPAREN; }
<STMT> ")"            { return Xbas99Types.OP_RPAREN; }
<STMT> "&"            { return Xbas99Types.OP_AMP; }
<STMT> "*"            { return Xbas99Types.OP_MUL; }
<STMT> "/"            { return Xbas99Types.OP_DIV; }
<STMT> "+"            { return Xbas99Types.OP_PLUS; }
<STMT> "-"            { return Xbas99Types.OP_MINUS; }
<STMT> "^"            { return Xbas99Types.OP_EXP; }
<STMT> "!" {ANY}*     { return Xbas99Types.COMMENT; }

<DATA> ","            { return Xbas99Types.OP_COMMA; }
<DATA> {PART}*        { return Xbas99Types.A_DATA; }
<IMAGE> {ANY}*        { return Xbas99Types.A_IMAGE; }

<REM> {ANY}*          { return Xbas99Types.COMMENT; }

.                     { return TokenType.BAD_CHARACTER; }
