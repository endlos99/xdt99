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

FUNN = "ABS" | "ASC" | "ATN" | "COS" | "EOF" | "EXP" | "INT" | "LEN" | "LOG" |
       "MAX" | "MIN" | "POS" | "REC" | "RND" | "SGN" | "SIN" | "SQR" | "TAB" |
       "TAN" | "VAL"
FUNS = "CHR" | "RPT" | "SEG" | "STR"
FUNC = "PI" | "RND"

IDENT = {ALPHA}({ALPHA}|{DIGIT})*
NUMBER = {DIGIT}{DIGIT}*
EXP = [Ee] "-"? {DIGIT}{DIGIT}*
FLOAT = {DIGIT}{DIGIT}* {EXP} | {DIGIT}* "." {DIGIT}* {EXP}?
QSTRING = "\"" ([^\"\r\n] | "\"\"")* "\""

ALPHA = [A-Za-z_@\[\]\\]
EOW = [^ \tA-Za-z_@\[\]\\]
DIGIT = [0-9]
ARITH = [+*/\^]

BLANK = " " | \t
WS = {BLANK}{BLANK}*
CHOMP = {BLANK}*
CRLF = \n | \r | \r\n
ANY = [^\r\n]
PART = [^,\r\n]

%state S
%state DATA
%state IMAGE
%state REM

%%

<YYINITIAL> {NUMBER}   { return Xbas99Types.LNUMBER; }
<YYINITIAL> {WS}       { yybegin(S); return Xbas99Types.WS; }

<S> "ACCEPT"{WS}       { return Xbas99Types.W_ACCEPT; }
<S> "ALL"{WS}          { return Xbas99Types.W_ALL; }
<S> "AND"{WS}          { return Xbas99Types.W_AND; }
<S> "APPEND"{WS}       { return Xbas99Types.W_APPEND; }
<S> "AT"{WS}           { return Xbas99Types.W_AT; }
<S> "BASE"{WS}         { return Xbas99Types.W_BASE; }
<S> "BEEP"{WS}         { return Xbas99Types.W_BEEP; }
<S> "BREAK"{WS}        { return Xbas99Types.W_BREAK; }
<S> "CALL"{WS}         { return Xbas99Types.W_CALL; }
<S> "CLOSE"{WS}        { return Xbas99Types.W_CLOSE; }
<S> "DATA"{WS}         { yybegin(DATA); return Xbas99Types.W_DATA; }
<S> "DEF"{WS}          { return Xbas99Types.W_DEF; }
<S> "DELETE"{WS}       { return Xbas99Types.W_DELETE; }
<S> "DIGIT"{WS}        { return Xbas99Types.W_DIGIT; }
<S> "DIM"{WS}          { return Xbas99Types.W_DIM; }
<S> "DISPLAY"{WS}      { return Xbas99Types.W_DISPLAY; }
<S> "ELSE"{WS}         { return Xbas99Types.W_ELSE; }
<S> "END"{WS}          { return Xbas99Types.W_END; }
<S> "ERASE"{WS}        { return Xbas99Types.W_ERASE; }
<S> "ERROR"{WS}        { return Xbas99Types.W_ERROR; }
<S> "FIXED"{WS}        { return Xbas99Types.W_FIXED; }
<S> "FOR"{WS}          { return Xbas99Types.W_FOR; }
<S> "GO"{WS}           { return Xbas99Types.W_GO; }
<S> "GOSUB"{WS}        { return Xbas99Types.W_GOSUB; }
<S> "GOTO"{WS}         { return Xbas99Types.W_GOTO; }
<S> "IF"{WS}           { return Xbas99Types.W_IF; }
<S> "IMAGE"{WS}        { yybegin(IMAGE); return Xbas99Types.W_IMAGE; }
<S> "INPUT"{WS}        { return Xbas99Types.W_INPUT; }
<S> "INTERNAL"{WS}     { return Xbas99Types.W_INTERNAL; }
<S> "LET"{WS}          { return Xbas99Types.W_LET; }
<S> "LINPUT"{WS}       { return Xbas99Types.W_LINPUT; }
<S> "NEXT"{WS}         { return Xbas99Types.W_NEXT; }
<S> "NOT"{WS}          { return Xbas99Types.W_NOT; }
<S> "NUMERIC"{WS}      { return Xbas99Types.W_NUMERIC; }
<S> "ON"{WS}           { return Xbas99Types.W_ON; }
<S> "OPEN"{WS}         { return Xbas99Types.W_OPEN; }
<S> "OPTION"{WS}       { return Xbas99Types.W_OPTION; }
<S> "OR"{WS}           { return Xbas99Types.W_OR; }
<S> "OUTPUT"{WS}       { return Xbas99Types.W_OUTPUT; }
<S> "PERMANENT"{WS}    { return Xbas99Types.W_PERMANENT; }
<S> "PRINT"{WS}        { return Xbas99Types.W_PRINT; }
<S> "RANDOMIZE"{WS}    { return Xbas99Types.W_RANDOMIZE; }
<S> "READ"{WS}         { return Xbas99Types.W_READ; }
<S> "RELATIVE"{WS}     { return Xbas99Types.W_RELATIVE; }
<S> "REM"{WS}          { yybegin(REM); return Xbas99Types.W_REM; }
<S> "RESTORE"{WS}      { return Xbas99Types.W_RESTORE; }
<S> "RETURN"{WS}       { return Xbas99Types.W_RETURN; }
<S> "RUN"{WS}          { return Xbas99Types.W_RUN; }
<S> "SEQUENTIAL"{WS}   { return Xbas99Types.W_SEQUENTIAL; }
<S> "SIZE"{WS}         { return Xbas99Types.W_SIZE; }
<S> "STEP"{WS}         { return Xbas99Types.W_STEP; }
<S> "STOP"{WS}         { return Xbas99Types.W_STOP; }
<S> "SUB"{WS}          { return Xbas99Types.W_SUB; }
<S> "SUBEND"{WS}       { return Xbas99Types.W_SUBEND; }
<S> "SUBEXIT"{WS}      { return Xbas99Types.W_SUBEXIT; }
<S> "THEN"{WS}         { return Xbas99Types.W_THEN; }
<S> "TO"{WS}           { return Xbas99Types.W_TO; }
<S> "TRACE"{WS}        { return Xbas99Types.W_TRACE; }
<S> "UALPHA"{WS}       { return Xbas99Types.W_UALPHA; }
<S> "UNBREAK"{WS}      { return Xbas99Types.W_UNBREAK; }
<S> "UNTRACE"{WS}      { return Xbas99Types.W_UNTRACE; }
<S> "UPDATE"{WS}       { return Xbas99Types.W_UPDATE; }
<S> "USING"{WS}        { return Xbas99Types.W_USING; }
<S> "VALIDATE"{WS}     { return Xbas99Types.W_VALIDATE; }
<S> "VARIABLE"{WS}     { return Xbas99Types.W_VARIABLE; }
<S> "WARNING"{WS}      { return Xbas99Types.W_WARNING; }
<S> "XOR"{WS}          { return Xbas99Types.W_XOR; }

<S> "ACCEPT"{EOW}      { yypushback(1); return Xbas99Types.W_ACCEPT; }
<S> "ALL"{EOW}         { yypushback(1); return Xbas99Types.W_ALL; }
<S> "AND"{EOW}         { yypushback(1); return Xbas99Types.W_AND; }
<S> "APPEND"{EOW}      { yypushback(1); return Xbas99Types.W_APPEND; }
<S> "AT"{EOW}          { yypushback(1); return Xbas99Types.W_AT; }
<S> "BASE"{EOW}        { yypushback(1); return Xbas99Types.W_BASE; }
<S> "BEEP"{EOW}        { yypushback(1); return Xbas99Types.W_BEEP; }
<S> "BREAK"{EOW}       { yypushback(1); return Xbas99Types.W_BREAK; }
<S> "CALL"{EOW}        { yypushback(1); return Xbas99Types.W_CALL; }
<S> "CLOSE"{EOW}       { yypushback(1); return Xbas99Types.W_CLOSE; }
<S> "DATA"{EOW}        { yypushback(1); yybegin(DATA); return Xbas99Types.W_DATA; }
<S> "DEF"{EOW}         { yypushback(1); return Xbas99Types.W_DEF; }
<S> "DELETE"{EOW}      { yypushback(1); return Xbas99Types.W_DELETE; }
<S> "DIGIT"{EOW}       { yypushback(1); return Xbas99Types.W_DIGIT; }
<S> "DIM"{EOW}         { yypushback(1); return Xbas99Types.W_DIM; }
<S> "DISPLAY"{EOW}     { yypushback(1); return Xbas99Types.W_DISPLAY; }
<S> "ELSE"{EOW}        { yypushback(1); return Xbas99Types.W_ELSE; }
<S> "END"{EOW}         { yypushback(1); return Xbas99Types.W_END; }
<S> "ERASE"{EOW}       { yypushback(1); return Xbas99Types.W_ERASE; }
<S> "ERROR"{EOW}       { yypushback(1); return Xbas99Types.W_ERROR; }
<S> "FIXED"{EOW}       { yypushback(1); return Xbas99Types.W_FIXED; }
<S> "FOR"{EOW}         { yypushback(1); return Xbas99Types.W_FOR; }
<S> "GO"{EOW}          { yypushback(1); return Xbas99Types.W_GO; }
<S> "GOSUB"{EOW}       { yypushback(1); return Xbas99Types.W_GOSUB; }
<S> "GOTO"{EOW}        { yypushback(1); return Xbas99Types.W_GOTO; }
<S> "IF"{EOW}          { yypushback(1); return Xbas99Types.W_IF; }
<S> "IMAGE"{EOW}       { yypushback(1); yybegin(IMAGE); return Xbas99Types.W_IMAGE; }
<S> "INPUT"{EOW}       { yypushback(1); return Xbas99Types.W_INPUT; }
<S> "INTERNAL"{EOW}    { yypushback(1); return Xbas99Types.W_INTERNAL; }
<S> "LET"{EOW}         { yypushback(1); return Xbas99Types.W_LET; }
<S> "LINPUT"{EOW}      { yypushback(1); return Xbas99Types.W_LINPUT; }
<S> "NEXT"{EOW}        { yypushback(1); return Xbas99Types.W_NEXT; }
<S> "NOT"{EOW}         { yypushback(1); return Xbas99Types.W_NOT; }
<S> "NUMERIC"{EOW}     { yypushback(1); return Xbas99Types.W_NUMERIC; }
<S> "ON"{EOW}          { yypushback(1); return Xbas99Types.W_ON; }
<S> "OPEN"{EOW}        { yypushback(1); return Xbas99Types.W_OPEN; }
<S> "OPTION"{EOW}      { yypushback(1); return Xbas99Types.W_OPTION; }
<S> "OR"{EOW}          { yypushback(1); return Xbas99Types.W_OR; }
<S> "OUTPUT"{EOW}      { yypushback(1); return Xbas99Types.W_OUTPUT; }
<S> "PERMANENT"{EOW}   { yypushback(1); return Xbas99Types.W_PERMANENT; }
<S> "PRINT"{EOW}       { yypushback(1); return Xbas99Types.W_PRINT; }
<S> "RANDOMIZE"{EOW}   { yypushback(1); return Xbas99Types.W_RANDOMIZE; }
<S> "READ"{EOW}        { yypushback(1); return Xbas99Types.W_READ; }
<S> "RELATIVE"{EOW}    { yypushback(1); return Xbas99Types.W_RELATIVE; }
<S> "REM"{EOW}         { yypushback(1); yybegin(REM); return Xbas99Types.W_REM; }
<S> "RESTORE"{EOW}     { yypushback(1); return Xbas99Types.W_RESTORE; }
<S> "RETURN"{EOW}      { yypushback(1); return Xbas99Types.W_RETURN; }
<S> "RUN"{EOW}         { yypushback(1); return Xbas99Types.W_RUN; }
<S> "SEQUENTIAL"{EOW}  { yypushback(1); return Xbas99Types.W_SEQUENTIAL; }
<S> "SIZE"{EOW}        { yypushback(1); return Xbas99Types.W_SIZE; }
<S> "STEP"{EOW}        { yypushback(1); return Xbas99Types.W_STEP; }
<S> "STOP"{EOW}        { yypushback(1); return Xbas99Types.W_STOP; }
<S> "SUB"{EOW}         { yypushback(1); return Xbas99Types.W_SUB; }
<S> "SUBEND"{EOW}      { yypushback(1); return Xbas99Types.W_SUBEND; }
<S> "SUBEXIT"{EOW}     { yypushback(1); return Xbas99Types.W_SUBEXIT; }
<S> "THEN"{EOW}        { yypushback(1); return Xbas99Types.W_THEN; }
<S> "TO"{EOW}          { yypushback(1); return Xbas99Types.W_TO; }
<S> "TRACE"{EOW}       { yypushback(1); return Xbas99Types.W_TRACE; }
<S> "UALPHA"{EOW}      { yypushback(1); return Xbas99Types.W_UALPHA; }
<S> "UNBREAK"{EOW}     { yypushback(1); return Xbas99Types.W_UNBREAK; }
<S> "UNTRACE"{EOW}     { yypushback(1); return Xbas99Types.W_UNTRACE; }
<S> "UPDATE"{EOW}      { yypushback(1); return Xbas99Types.W_UPDATE; }
<S> "USING"{EOW}       { yypushback(1); return Xbas99Types.W_USING; }
<S> "VALIDATE"{EOW}    { yypushback(1); return Xbas99Types.W_VALIDATE; }
<S> "VARIABLE"{EOW}    { yypushback(1); return Xbas99Types.W_VARIABLE; }
<S> "WARNING"{EOW}     { yypushback(1); return Xbas99Types.W_WARNING; }
<S> "XOR"{EOW}         { yypushback(1); return Xbas99Types.W_XOR; }

<S> {FUNN}{WS}         { return Xbas99Types.W_FUN_N; }
<S> {FUNS}"$"{WS}      { return Xbas99Types.W_FUN_S; }
<S> {FUNC}{WS}         { return Xbas99Types.W_FUN_C; }

<S> {IDENT}"$"{CHOMP}  { return Xbas99Types.SIDENT; }
<S> {IDENT}{CHOMP}     { return Xbas99Types.IDENT; }
<S> {NUMBER}{CHOMP}    { return Xbas99Types.NUMBER; }
<S> {FLOAT}{CHOMP}     { return Xbas99Types.FLOAT; }
<S> {QSTRING}{CHOMP}   { return Xbas99Types.QSTRING; }

<S> "::"{CHOMP}        { return Xbas99Types.OP_SEP; }
<S> ":"{CHOMP}         { return Xbas99Types.OP_COLON; }
<S> ","{CHOMP}         { return Xbas99Types.OP_COMMA; }
<S> ";"{CHOMP}         { return Xbas99Types.OP_SEMI; }
<S> "="{CHOMP}         { return Xbas99Types.OP_EQ; }
<S> "<"{CHOMP}         { return Xbas99Types.OP_LT; }
<S> ">"{CHOMP}         { return Xbas99Types.OP_GT; }
<S> "#"{CHOMP}         { return Xbas99Types.OP_HASH; }
<S> "("{CHOMP}         { return Xbas99Types.OP_LPAREN; }
<S> ")"{CHOMP}         { return Xbas99Types.OP_RPAREN; }
<S> "&"{CHOMP}         { return Xbas99Types.OP_AMP; }
<S> "-"{CHOMP}         { return Xbas99Types.OP_NEG; }
<S> {ARITH}{CHOMP}     { return Xbas99Types.OP_ARITH; }
<S> "!"                { yybegin(REM); return Xbas99Types.OP_EXCL; }

<DATA> ","             { return Xbas99Types.OP_COMMA; }
<DATA> {PART}*         { return Xbas99Types.A_DATA; }
<IMAGE> {ANY}*         { return Xbas99Types.A_IMAGE; }
<REM> {ANY}*           { return Xbas99Types.A_REM; }

{CRLF}                 { yybegin(YYINITIAL); return Xbas99Types.CRLF; }
//{WS}                 { return Xbas99Types.WS; }

.                      { return TokenType.BAD_CHARACTER; }
