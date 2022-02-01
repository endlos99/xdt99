// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xbas99l.psi.impl.*;

public interface Xbas99LTypes {

  IElementType A_THEN_ELSE = new Xbas99LElementType("A_THEN_ELSE");
  IElementType BANG_COMMENT = new Xbas99LElementType("BANG_COMMENT");
  IElementType DUMMY = new Xbas99LElementType("DUMMY");
  IElementType F_CONST = new Xbas99LElementType("F_CONST");
  IElementType F_NUM = new Xbas99LElementType("F_NUM");
  IElementType F_STR = new Xbas99LElementType("F_STR");
  IElementType LABELDEF = new Xbas99LElementType("LABELDEF");
  IElementType LABELREF = new Xbas99LElementType("LABELREF");
  IElementType NEXPRN = new Xbas99LElementType("NEXPRN");
  IElementType NVAR_F = new Xbas99LElementType("NVAR_F");
  IElementType NVAR_R = new Xbas99LElementType("NVAR_R");
  IElementType NVAR_W = new Xbas99LElementType("NVAR_W");
  IElementType PARAM = new Xbas99LElementType("PARAM");
  IElementType SEXPR = new Xbas99LElementType("SEXPR");
  IElementType SLIST = new Xbas99LElementType("SLIST");
  IElementType STATEMENT_BOTH = new Xbas99LElementType("STATEMENT_BOTH");
  IElementType STATEMENT_XB = new Xbas99LElementType("STATEMENT_XB");
  IElementType SUBPROG = new Xbas99LElementType("SUBPROG");
  IElementType SVAR_F = new Xbas99LElementType("SVAR_F");
  IElementType SVAR_R = new Xbas99LElementType("SVAR_R");
  IElementType SVAR_W = new Xbas99LElementType("SVAR_W");
  IElementType S_ACCEPT = new Xbas99LElementType("S_ACCEPT");
  IElementType S_BREAK = new Xbas99LElementType("S_BREAK");
  IElementType S_CALL = new Xbas99LElementType("S_CALL");
  IElementType S_CLOSE = new Xbas99LElementType("S_CLOSE");
  IElementType S_DATA = new Xbas99LElementType("S_DATA");
  IElementType S_DEF = new Xbas99LElementType("S_DEF");
  IElementType S_DELETE = new Xbas99LElementType("S_DELETE");
  IElementType S_DIM = new Xbas99LElementType("S_DIM");
  IElementType S_DISPLAY = new Xbas99LElementType("S_DISPLAY");
  IElementType S_END = new Xbas99LElementType("S_END");
  IElementType S_FOR = new Xbas99LElementType("S_FOR");
  IElementType S_GO = new Xbas99LElementType("S_GO");
  IElementType S_IF = new Xbas99LElementType("S_IF");
  IElementType S_IMAGE = new Xbas99LElementType("S_IMAGE");
  IElementType S_INPUT = new Xbas99LElementType("S_INPUT");
  IElementType S_LET = new Xbas99LElementType("S_LET");
  IElementType S_LINPUT = new Xbas99LElementType("S_LINPUT");
  IElementType S_NEXT = new Xbas99LElementType("S_NEXT");
  IElementType S_ON_COND = new Xbas99LElementType("S_ON_COND");
  IElementType S_ON_GO = new Xbas99LElementType("S_ON_GO");
  IElementType S_OPEN = new Xbas99LElementType("S_OPEN");
  IElementType S_OPTION = new Xbas99LElementType("S_OPTION");
  IElementType S_PRINT = new Xbas99LElementType("S_PRINT");
  IElementType S_RANDOMIZE = new Xbas99LElementType("S_RANDOMIZE");
  IElementType S_READ = new Xbas99LElementType("S_READ");
  IElementType S_REM = new Xbas99LElementType("S_REM");
  IElementType S_RESTORE = new Xbas99LElementType("S_RESTORE");
  IElementType S_RETURN = new Xbas99LElementType("S_RETURN");
  IElementType S_RUN = new Xbas99LElementType("S_RUN");
  IElementType S_STOP = new Xbas99LElementType("S_STOP");
  IElementType S_SUB = new Xbas99LElementType("S_SUB");
  IElementType S_SUBEND = new Xbas99LElementType("S_SUBEND");
  IElementType S_TRACE = new Xbas99LElementType("S_TRACE");

  IElementType A_DATA = new Xbas99LTokenType("A_DATA");
  IElementType A_IMAGE = new Xbas99LTokenType("A_IMAGE");
  IElementType COMMENT = new Xbas99LTokenType("COMMENT");
  IElementType CRLF = new Xbas99LTokenType("CRLF");
  IElementType FLOAT = new Xbas99LTokenType("FLOAT");
  IElementType IDENT = new Xbas99LTokenType("IDENT");
  IElementType LIDENT = new Xbas99LTokenType("LIDENT");
  IElementType NUMBER = new Xbas99LTokenType("NUMBER");
  IElementType OP_AMP = new Xbas99LTokenType("OP_AMP");
  IElementType OP_COLON = new Xbas99LTokenType("OP_COLON");
  IElementType OP_COMMA = new Xbas99LTokenType("OP_COMMA");
  IElementType OP_DIV = new Xbas99LTokenType("OP_DIV");
  IElementType OP_EQ = new Xbas99LTokenType("OP_EQ");
  IElementType OP_EXP = new Xbas99LTokenType("OP_EXP");
  IElementType OP_GT = new Xbas99LTokenType("OP_GT");
  IElementType OP_HASH = new Xbas99LTokenType("OP_HASH");
  IElementType OP_LPAREN = new Xbas99LTokenType("OP_LPAREN");
  IElementType OP_LT = new Xbas99LTokenType("OP_LT");
  IElementType OP_MINUS = new Xbas99LTokenType("OP_MINUS");
  IElementType OP_MUL = new Xbas99LTokenType("OP_MUL");
  IElementType OP_PLUS = new Xbas99LTokenType("OP_PLUS");
  IElementType OP_QUOTE = new Xbas99LTokenType("OP_QUOTE");
  IElementType OP_RPAREN = new Xbas99LTokenType("OP_RPAREN");
  IElementType OP_SEMI = new Xbas99LTokenType("OP_SEMI");
  IElementType OP_SEP = new Xbas99LTokenType("OP_SEP");
  IElementType OP_STR = new Xbas99LTokenType("OP_STR");
  IElementType QSTRING = new Xbas99LTokenType("QSTRING");
  IElementType SIDENT = new Xbas99LTokenType("SIDENT");
  IElementType W_ACCEPT = new Xbas99LTokenType("W_ACCEPT");
  IElementType W_ALL = new Xbas99LTokenType("W_ALL");
  IElementType W_AND = new Xbas99LTokenType("W_AND");
  IElementType W_APPEND = new Xbas99LTokenType("W_APPEND");
  IElementType W_AT = new Xbas99LTokenType("W_AT");
  IElementType W_BANG = new Xbas99LTokenType("W_BANG");
  IElementType W_BASE = new Xbas99LTokenType("W_BASE");
  IElementType W_BEEP = new Xbas99LTokenType("W_BEEP");
  IElementType W_BREAK = new Xbas99LTokenType("W_BREAK");
  IElementType W_CALL = new Xbas99LTokenType("W_CALL");
  IElementType W_CLOSE = new Xbas99LTokenType("W_CLOSE");
  IElementType W_DATA = new Xbas99LTokenType("W_DATA");
  IElementType W_DEF = new Xbas99LTokenType("W_DEF");
  IElementType W_DELETE = new Xbas99LTokenType("W_DELETE");
  IElementType W_DIGIT = new Xbas99LTokenType("W_DIGIT");
  IElementType W_DIM = new Xbas99LTokenType("W_DIM");
  IElementType W_DISPLAY = new Xbas99LTokenType("W_DISPLAY");
  IElementType W_ELSE = new Xbas99LTokenType("W_ELSE");
  IElementType W_END = new Xbas99LTokenType("W_END");
  IElementType W_ERASE = new Xbas99LTokenType("W_ERASE");
  IElementType W_ERROR = new Xbas99LTokenType("W_ERROR");
  IElementType W_FIXED = new Xbas99LTokenType("W_FIXED");
  IElementType W_FOR = new Xbas99LTokenType("W_FOR");
  IElementType W_FUN_C = new Xbas99LTokenType("W_FUN_C");
  IElementType W_FUN_N = new Xbas99LTokenType("W_FUN_N");
  IElementType W_FUN_S = new Xbas99LTokenType("W_FUN_S");
  IElementType W_GO = new Xbas99LTokenType("W_GO");
  IElementType W_GOSUB = new Xbas99LTokenType("W_GOSUB");
  IElementType W_GOTO = new Xbas99LTokenType("W_GOTO");
  IElementType W_IF = new Xbas99LTokenType("W_IF");
  IElementType W_IMAGE = new Xbas99LTokenType("W_IMAGE");
  IElementType W_INPUT = new Xbas99LTokenType("W_INPUT");
  IElementType W_INTERNAL = new Xbas99LTokenType("W_INTERNAL");
  IElementType W_LET = new Xbas99LTokenType("W_LET");
  IElementType W_LINPUT = new Xbas99LTokenType("W_LINPUT");
  IElementType W_NEXT = new Xbas99LTokenType("W_NEXT");
  IElementType W_NOT = new Xbas99LTokenType("W_NOT");
  IElementType W_NUMERIC = new Xbas99LTokenType("W_NUMERIC");
  IElementType W_ON = new Xbas99LTokenType("W_ON");
  IElementType W_OPEN = new Xbas99LTokenType("W_OPEN");
  IElementType W_OPTION = new Xbas99LTokenType("W_OPTION");
  IElementType W_OR = new Xbas99LTokenType("W_OR");
  IElementType W_OUTPUT = new Xbas99LTokenType("W_OUTPUT");
  IElementType W_PERMANENT = new Xbas99LTokenType("W_PERMANENT");
  IElementType W_PRINT = new Xbas99LTokenType("W_PRINT");
  IElementType W_RANDOMIZE = new Xbas99LTokenType("W_RANDOMIZE");
  IElementType W_READ = new Xbas99LTokenType("W_READ");
  IElementType W_REC = new Xbas99LTokenType("W_REC");
  IElementType W_RELATIVE = new Xbas99LTokenType("W_RELATIVE");
  IElementType W_REM = new Xbas99LTokenType("W_REM");
  IElementType W_RESTORE = new Xbas99LTokenType("W_RESTORE");
  IElementType W_RETURN = new Xbas99LTokenType("W_RETURN");
  IElementType W_RUN = new Xbas99LTokenType("W_RUN");
  IElementType W_SEQUENTIAL = new Xbas99LTokenType("W_SEQUENTIAL");
  IElementType W_SIZE = new Xbas99LTokenType("W_SIZE");
  IElementType W_STEP = new Xbas99LTokenType("W_STEP");
  IElementType W_STOP = new Xbas99LTokenType("W_STOP");
  IElementType W_SUB = new Xbas99LTokenType("W_SUB");
  IElementType W_SUBEND = new Xbas99LTokenType("W_SUBEND");
  IElementType W_SUBEXIT = new Xbas99LTokenType("W_SUBEXIT");
  IElementType W_THEN = new Xbas99LTokenType("W_THEN");
  IElementType W_TO = new Xbas99LTokenType("W_TO");
  IElementType W_TRACE = new Xbas99LTokenType("W_TRACE");
  IElementType W_UALPHA = new Xbas99LTokenType("W_UALPHA");
  IElementType W_UNBREAK = new Xbas99LTokenType("W_UNBREAK");
  IElementType W_UNTRACE = new Xbas99LTokenType("W_UNTRACE");
  IElementType W_UPDATE = new Xbas99LTokenType("W_UPDATE");
  IElementType W_USING = new Xbas99LTokenType("W_USING");
  IElementType W_VALIDATE = new Xbas99LTokenType("W_VALIDATE");
  IElementType W_VARIABLE = new Xbas99LTokenType("W_VARIABLE");
  IElementType W_WARNING = new Xbas99LTokenType("W_WARNING");
  IElementType W_XOR = new Xbas99LTokenType("W_XOR");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == A_THEN_ELSE) {
        return new Xbas99LAThenElseImpl(node);
      }
      else if (type == BANG_COMMENT) {
        return new Xbas99LBangCommentImpl(node);
      }
      else if (type == DUMMY) {
        return new Xbas99LDummyImpl(node);
      }
      else if (type == F_CONST) {
        return new Xbas99LFConstImpl(node);
      }
      else if (type == F_NUM) {
        return new Xbas99LFNumImpl(node);
      }
      else if (type == F_STR) {
        return new Xbas99LFStrImpl(node);
      }
      else if (type == LABELDEF) {
        return new Xbas99LLabeldefImpl(node);
      }
      else if (type == LABELREF) {
        return new Xbas99LLabelrefImpl(node);
      }
      else if (type == NEXPRN) {
        return new Xbas99LNexprnImpl(node);
      }
      else if (type == NVAR_F) {
        return new Xbas99LNvarFImpl(node);
      }
      else if (type == NVAR_R) {
        return new Xbas99LNvarRImpl(node);
      }
      else if (type == NVAR_W) {
        return new Xbas99LNvarWImpl(node);
      }
      else if (type == PARAM) {
        return new Xbas99LParamImpl(node);
      }
      else if (type == SEXPR) {
        return new Xbas99LSexprImpl(node);
      }
      else if (type == SLIST) {
        return new Xbas99LSlistImpl(node);
      }
      else if (type == STATEMENT_BOTH) {
        return new Xbas99LStatementBothImpl(node);
      }
      else if (type == STATEMENT_XB) {
        return new Xbas99LStatementXbImpl(node);
      }
      else if (type == SUBPROG) {
        return new Xbas99LSubprogImpl(node);
      }
      else if (type == SVAR_F) {
        return new Xbas99LSvarFImpl(node);
      }
      else if (type == SVAR_R) {
        return new Xbas99LSvarRImpl(node);
      }
      else if (type == SVAR_W) {
        return new Xbas99LSvarWImpl(node);
      }
      else if (type == S_ACCEPT) {
        return new Xbas99LSAcceptImpl(node);
      }
      else if (type == S_BREAK) {
        return new Xbas99LSBreakImpl(node);
      }
      else if (type == S_CALL) {
        return new Xbas99LSCallImpl(node);
      }
      else if (type == S_CLOSE) {
        return new Xbas99LSCloseImpl(node);
      }
      else if (type == S_DATA) {
        return new Xbas99LSDataImpl(node);
      }
      else if (type == S_DEF) {
        return new Xbas99LSDefImpl(node);
      }
      else if (type == S_DELETE) {
        return new Xbas99LSDeleteImpl(node);
      }
      else if (type == S_DIM) {
        return new Xbas99LSDimImpl(node);
      }
      else if (type == S_DISPLAY) {
        return new Xbas99LSDisplayImpl(node);
      }
      else if (type == S_END) {
        return new Xbas99LSEndImpl(node);
      }
      else if (type == S_FOR) {
        return new Xbas99LSForImpl(node);
      }
      else if (type == S_GO) {
        return new Xbas99LSGoImpl(node);
      }
      else if (type == S_IF) {
        return new Xbas99LSIfImpl(node);
      }
      else if (type == S_IMAGE) {
        return new Xbas99LSImageImpl(node);
      }
      else if (type == S_INPUT) {
        return new Xbas99LSInputImpl(node);
      }
      else if (type == S_LET) {
        return new Xbas99LSLetImpl(node);
      }
      else if (type == S_LINPUT) {
        return new Xbas99LSLinputImpl(node);
      }
      else if (type == S_NEXT) {
        return new Xbas99LSNextImpl(node);
      }
      else if (type == S_ON_COND) {
        return new Xbas99LSOnCondImpl(node);
      }
      else if (type == S_ON_GO) {
        return new Xbas99LSOnGoImpl(node);
      }
      else if (type == S_OPEN) {
        return new Xbas99LSOpenImpl(node);
      }
      else if (type == S_OPTION) {
        return new Xbas99LSOptionImpl(node);
      }
      else if (type == S_PRINT) {
        return new Xbas99LSPrintImpl(node);
      }
      else if (type == S_RANDOMIZE) {
        return new Xbas99LSRandomizeImpl(node);
      }
      else if (type == S_READ) {
        return new Xbas99LSReadImpl(node);
      }
      else if (type == S_REM) {
        return new Xbas99LSRemImpl(node);
      }
      else if (type == S_RESTORE) {
        return new Xbas99LSRestoreImpl(node);
      }
      else if (type == S_RETURN) {
        return new Xbas99LSReturnImpl(node);
      }
      else if (type == S_RUN) {
        return new Xbas99LSRunImpl(node);
      }
      else if (type == S_STOP) {
        return new Xbas99LSStopImpl(node);
      }
      else if (type == S_SUB) {
        return new Xbas99LSSubImpl(node);
      }
      else if (type == S_SUBEND) {
        return new Xbas99LSSubendImpl(node);
      }
      else if (type == S_TRACE) {
        return new Xbas99LSTraceImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
