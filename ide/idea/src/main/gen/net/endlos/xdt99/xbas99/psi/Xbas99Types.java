// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xbas99.psi.impl.*;

public interface Xbas99Types {

  IElementType A_THEN_ELSE = new Xbas99ElementType("A_THEN_ELSE");
  IElementType BANG_COMMENT = new Xbas99ElementType("BANG_COMMENT");
  IElementType DUMMY = new Xbas99ElementType("DUMMY");
  IElementType F_CONST = new Xbas99ElementType("F_CONST");
  IElementType F_NUM = new Xbas99ElementType("F_NUM");
  IElementType F_STR = new Xbas99ElementType("F_STR");
  IElementType LINEDEF = new Xbas99ElementType("LINEDEF");
  IElementType LINO = new Xbas99ElementType("LINO");
  IElementType NEXPRN = new Xbas99ElementType("NEXPRN");
  IElementType NVAR_F = new Xbas99ElementType("NVAR_F");
  IElementType NVAR_R = new Xbas99ElementType("NVAR_R");
  IElementType NVAR_W = new Xbas99ElementType("NVAR_W");
  IElementType PARAM = new Xbas99ElementType("PARAM");
  IElementType SEXPR = new Xbas99ElementType("SEXPR");
  IElementType SLIST = new Xbas99ElementType("SLIST");
  IElementType STATEMENT_BOTH = new Xbas99ElementType("STATEMENT_BOTH");
  IElementType STATEMENT_XB = new Xbas99ElementType("STATEMENT_XB");
  IElementType SUBPROG = new Xbas99ElementType("SUBPROG");
  IElementType SVAR_F = new Xbas99ElementType("SVAR_F");
  IElementType SVAR_R = new Xbas99ElementType("SVAR_R");
  IElementType SVAR_W = new Xbas99ElementType("SVAR_W");
  IElementType S_ACCEPT = new Xbas99ElementType("S_ACCEPT");
  IElementType S_BREAK = new Xbas99ElementType("S_BREAK");
  IElementType S_CALL = new Xbas99ElementType("S_CALL");
  IElementType S_CLOSE = new Xbas99ElementType("S_CLOSE");
  IElementType S_DATA = new Xbas99ElementType("S_DATA");
  IElementType S_DEF = new Xbas99ElementType("S_DEF");
  IElementType S_DELETE = new Xbas99ElementType("S_DELETE");
  IElementType S_DIM = new Xbas99ElementType("S_DIM");
  IElementType S_DISPLAY = new Xbas99ElementType("S_DISPLAY");
  IElementType S_END = new Xbas99ElementType("S_END");
  IElementType S_FOR = new Xbas99ElementType("S_FOR");
  IElementType S_GO = new Xbas99ElementType("S_GO");
  IElementType S_IF = new Xbas99ElementType("S_IF");
  IElementType S_IMAGE = new Xbas99ElementType("S_IMAGE");
  IElementType S_INPUT = new Xbas99ElementType("S_INPUT");
  IElementType S_LET = new Xbas99ElementType("S_LET");
  IElementType S_LINPUT = new Xbas99ElementType("S_LINPUT");
  IElementType S_NEXT = new Xbas99ElementType("S_NEXT");
  IElementType S_ON_COND = new Xbas99ElementType("S_ON_COND");
  IElementType S_ON_GO = new Xbas99ElementType("S_ON_GO");
  IElementType S_OPEN = new Xbas99ElementType("S_OPEN");
  IElementType S_OPTION = new Xbas99ElementType("S_OPTION");
  IElementType S_PRINT = new Xbas99ElementType("S_PRINT");
  IElementType S_RANDOMIZE = new Xbas99ElementType("S_RANDOMIZE");
  IElementType S_READ = new Xbas99ElementType("S_READ");
  IElementType S_REM = new Xbas99ElementType("S_REM");
  IElementType S_RESTORE = new Xbas99ElementType("S_RESTORE");
  IElementType S_RETURN = new Xbas99ElementType("S_RETURN");
  IElementType S_RUN = new Xbas99ElementType("S_RUN");
  IElementType S_STOP = new Xbas99ElementType("S_STOP");
  IElementType S_SUB = new Xbas99ElementType("S_SUB");
  IElementType S_SUBEND = new Xbas99ElementType("S_SUBEND");
  IElementType S_TRACE = new Xbas99ElementType("S_TRACE");

  IElementType A_DATA = new Xbas99TokenType("A_DATA");
  IElementType A_IMAGE = new Xbas99TokenType("A_IMAGE");
  IElementType COMMENT = new Xbas99TokenType("COMMENT");
  IElementType CRLF = new Xbas99TokenType("CRLF");
  IElementType FLOAT = new Xbas99TokenType("FLOAT");
  IElementType IDENT = new Xbas99TokenType("IDENT");
  IElementType LNUMBER = new Xbas99TokenType("LNUMBER");
  IElementType NUMBER = new Xbas99TokenType("NUMBER");
  IElementType OP_AMP = new Xbas99TokenType("OP_AMP");
  IElementType OP_COLON = new Xbas99TokenType("OP_COLON");
  IElementType OP_COMMA = new Xbas99TokenType("OP_COMMA");
  IElementType OP_DIV = new Xbas99TokenType("OP_DIV");
  IElementType OP_EQ = new Xbas99TokenType("OP_EQ");
  IElementType OP_EXP = new Xbas99TokenType("OP_EXP");
  IElementType OP_GT = new Xbas99TokenType("OP_GT");
  IElementType OP_HASH = new Xbas99TokenType("OP_HASH");
  IElementType OP_LPAREN = new Xbas99TokenType("OP_LPAREN");
  IElementType OP_LT = new Xbas99TokenType("OP_LT");
  IElementType OP_MINUS = new Xbas99TokenType("OP_MINUS");
  IElementType OP_MUL = new Xbas99TokenType("OP_MUL");
  IElementType OP_PLUS = new Xbas99TokenType("OP_PLUS");
  IElementType OP_QUOTE = new Xbas99TokenType("OP_QUOTE");
  IElementType OP_RPAREN = new Xbas99TokenType("OP_RPAREN");
  IElementType OP_SEMI = new Xbas99TokenType("OP_SEMI");
  IElementType OP_SEP = new Xbas99TokenType("OP_SEP");
  IElementType OP_STR = new Xbas99TokenType("OP_STR");
  IElementType QSTRING = new Xbas99TokenType("QSTRING");
  IElementType SIDENT = new Xbas99TokenType("SIDENT");
  IElementType W_ACCEPT = new Xbas99TokenType("W_ACCEPT");
  IElementType W_ALL = new Xbas99TokenType("W_ALL");
  IElementType W_AND = new Xbas99TokenType("W_AND");
  IElementType W_APPEND = new Xbas99TokenType("W_APPEND");
  IElementType W_AT = new Xbas99TokenType("W_AT");
  IElementType W_BANG = new Xbas99TokenType("W_BANG");
  IElementType W_BASE = new Xbas99TokenType("W_BASE");
  IElementType W_BEEP = new Xbas99TokenType("W_BEEP");
  IElementType W_BREAK = new Xbas99TokenType("W_BREAK");
  IElementType W_CALL = new Xbas99TokenType("W_CALL");
  IElementType W_CLOSE = new Xbas99TokenType("W_CLOSE");
  IElementType W_DATA = new Xbas99TokenType("W_DATA");
  IElementType W_DEF = new Xbas99TokenType("W_DEF");
  IElementType W_DELETE = new Xbas99TokenType("W_DELETE");
  IElementType W_DIGIT = new Xbas99TokenType("W_DIGIT");
  IElementType W_DIM = new Xbas99TokenType("W_DIM");
  IElementType W_DISPLAY = new Xbas99TokenType("W_DISPLAY");
  IElementType W_ELSE = new Xbas99TokenType("W_ELSE");
  IElementType W_END = new Xbas99TokenType("W_END");
  IElementType W_ERASE = new Xbas99TokenType("W_ERASE");
  IElementType W_ERROR = new Xbas99TokenType("W_ERROR");
  IElementType W_FIXED = new Xbas99TokenType("W_FIXED");
  IElementType W_FOR = new Xbas99TokenType("W_FOR");
  IElementType W_FUN_C = new Xbas99TokenType("W_FUN_C");
  IElementType W_FUN_N = new Xbas99TokenType("W_FUN_N");
  IElementType W_FUN_S = new Xbas99TokenType("W_FUN_S");
  IElementType W_GO = new Xbas99TokenType("W_GO");
  IElementType W_GOSUB = new Xbas99TokenType("W_GOSUB");
  IElementType W_GOTO = new Xbas99TokenType("W_GOTO");
  IElementType W_IF = new Xbas99TokenType("W_IF");
  IElementType W_IMAGE = new Xbas99TokenType("W_IMAGE");
  IElementType W_INPUT = new Xbas99TokenType("W_INPUT");
  IElementType W_INTERNAL = new Xbas99TokenType("W_INTERNAL");
  IElementType W_LET = new Xbas99TokenType("W_LET");
  IElementType W_LINPUT = new Xbas99TokenType("W_LINPUT");
  IElementType W_NEXT = new Xbas99TokenType("W_NEXT");
  IElementType W_NOT = new Xbas99TokenType("W_NOT");
  IElementType W_NUMERIC = new Xbas99TokenType("W_NUMERIC");
  IElementType W_ON = new Xbas99TokenType("W_ON");
  IElementType W_OPEN = new Xbas99TokenType("W_OPEN");
  IElementType W_OPTION = new Xbas99TokenType("W_OPTION");
  IElementType W_OR = new Xbas99TokenType("W_OR");
  IElementType W_OUTPUT = new Xbas99TokenType("W_OUTPUT");
  IElementType W_PERMANENT = new Xbas99TokenType("W_PERMANENT");
  IElementType W_PRINT = new Xbas99TokenType("W_PRINT");
  IElementType W_RANDOMIZE = new Xbas99TokenType("W_RANDOMIZE");
  IElementType W_READ = new Xbas99TokenType("W_READ");
  IElementType W_REC = new Xbas99TokenType("W_REC");
  IElementType W_RELATIVE = new Xbas99TokenType("W_RELATIVE");
  IElementType W_REM = new Xbas99TokenType("W_REM");
  IElementType W_RESTORE = new Xbas99TokenType("W_RESTORE");
  IElementType W_RETURN = new Xbas99TokenType("W_RETURN");
  IElementType W_RUN = new Xbas99TokenType("W_RUN");
  IElementType W_SEQUENTIAL = new Xbas99TokenType("W_SEQUENTIAL");
  IElementType W_SIZE = new Xbas99TokenType("W_SIZE");
  IElementType W_STEP = new Xbas99TokenType("W_STEP");
  IElementType W_STOP = new Xbas99TokenType("W_STOP");
  IElementType W_SUB = new Xbas99TokenType("W_SUB");
  IElementType W_SUBEND = new Xbas99TokenType("W_SUBEND");
  IElementType W_SUBEXIT = new Xbas99TokenType("W_SUBEXIT");
  IElementType W_THEN = new Xbas99TokenType("W_THEN");
  IElementType W_TO = new Xbas99TokenType("W_TO");
  IElementType W_TRACE = new Xbas99TokenType("W_TRACE");
  IElementType W_UALPHA = new Xbas99TokenType("W_UALPHA");
  IElementType W_UNBREAK = new Xbas99TokenType("W_UNBREAK");
  IElementType W_UNTRACE = new Xbas99TokenType("W_UNTRACE");
  IElementType W_UPDATE = new Xbas99TokenType("W_UPDATE");
  IElementType W_USING = new Xbas99TokenType("W_USING");
  IElementType W_VALIDATE = new Xbas99TokenType("W_VALIDATE");
  IElementType W_VARIABLE = new Xbas99TokenType("W_VARIABLE");
  IElementType W_WARNING = new Xbas99TokenType("W_WARNING");
  IElementType W_XOR = new Xbas99TokenType("W_XOR");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == A_THEN_ELSE) {
        return new Xbas99AThenElseImpl(node);
      }
      else if (type == BANG_COMMENT) {
        return new Xbas99BangCommentImpl(node);
      }
      else if (type == DUMMY) {
        return new Xbas99DummyImpl(node);
      }
      else if (type == F_CONST) {
        return new Xbas99FConstImpl(node);
      }
      else if (type == F_NUM) {
        return new Xbas99FNumImpl(node);
      }
      else if (type == F_STR) {
        return new Xbas99FStrImpl(node);
      }
      else if (type == LINEDEF) {
        return new Xbas99LinedefImpl(node);
      }
      else if (type == LINO) {
        return new Xbas99LinoImpl(node);
      }
      else if (type == NEXPRN) {
        return new Xbas99NexprnImpl(node);
      }
      else if (type == NVAR_F) {
        return new Xbas99NvarFImpl(node);
      }
      else if (type == NVAR_R) {
        return new Xbas99NvarRImpl(node);
      }
      else if (type == NVAR_W) {
        return new Xbas99NvarWImpl(node);
      }
      else if (type == PARAM) {
        return new Xbas99ParamImpl(node);
      }
      else if (type == SEXPR) {
        return new Xbas99SexprImpl(node);
      }
      else if (type == SLIST) {
        return new Xbas99SlistImpl(node);
      }
      else if (type == STATEMENT_BOTH) {
        return new Xbas99StatementBothImpl(node);
      }
      else if (type == STATEMENT_XB) {
        return new Xbas99StatementXbImpl(node);
      }
      else if (type == SUBPROG) {
        return new Xbas99SubprogImpl(node);
      }
      else if (type == SVAR_F) {
        return new Xbas99SvarFImpl(node);
      }
      else if (type == SVAR_R) {
        return new Xbas99SvarRImpl(node);
      }
      else if (type == SVAR_W) {
        return new Xbas99SvarWImpl(node);
      }
      else if (type == S_ACCEPT) {
        return new Xbas99SAcceptImpl(node);
      }
      else if (type == S_BREAK) {
        return new Xbas99SBreakImpl(node);
      }
      else if (type == S_CALL) {
        return new Xbas99SCallImpl(node);
      }
      else if (type == S_CLOSE) {
        return new Xbas99SCloseImpl(node);
      }
      else if (type == S_DATA) {
        return new Xbas99SDataImpl(node);
      }
      else if (type == S_DEF) {
        return new Xbas99SDefImpl(node);
      }
      else if (type == S_DELETE) {
        return new Xbas99SDeleteImpl(node);
      }
      else if (type == S_DIM) {
        return new Xbas99SDimImpl(node);
      }
      else if (type == S_DISPLAY) {
        return new Xbas99SDisplayImpl(node);
      }
      else if (type == S_END) {
        return new Xbas99SEndImpl(node);
      }
      else if (type == S_FOR) {
        return new Xbas99SForImpl(node);
      }
      else if (type == S_GO) {
        return new Xbas99SGoImpl(node);
      }
      else if (type == S_IF) {
        return new Xbas99SIfImpl(node);
      }
      else if (type == S_IMAGE) {
        return new Xbas99SImageImpl(node);
      }
      else if (type == S_INPUT) {
        return new Xbas99SInputImpl(node);
      }
      else if (type == S_LET) {
        return new Xbas99SLetImpl(node);
      }
      else if (type == S_LINPUT) {
        return new Xbas99SLinputImpl(node);
      }
      else if (type == S_NEXT) {
        return new Xbas99SNextImpl(node);
      }
      else if (type == S_ON_COND) {
        return new Xbas99SOnCondImpl(node);
      }
      else if (type == S_ON_GO) {
        return new Xbas99SOnGoImpl(node);
      }
      else if (type == S_OPEN) {
        return new Xbas99SOpenImpl(node);
      }
      else if (type == S_OPTION) {
        return new Xbas99SOptionImpl(node);
      }
      else if (type == S_PRINT) {
        return new Xbas99SPrintImpl(node);
      }
      else if (type == S_RANDOMIZE) {
        return new Xbas99SRandomizeImpl(node);
      }
      else if (type == S_READ) {
        return new Xbas99SReadImpl(node);
      }
      else if (type == S_REM) {
        return new Xbas99SRemImpl(node);
      }
      else if (type == S_RESTORE) {
        return new Xbas99SRestoreImpl(node);
      }
      else if (type == S_RETURN) {
        return new Xbas99SReturnImpl(node);
      }
      else if (type == S_RUN) {
        return new Xbas99SRunImpl(node);
      }
      else if (type == S_STOP) {
        return new Xbas99SStopImpl(node);
      }
      else if (type == S_SUB) {
        return new Xbas99SSubImpl(node);
      }
      else if (type == S_SUBEND) {
        return new Xbas99SSubendImpl(node);
      }
      else if (type == S_TRACE) {
        return new Xbas99STraceImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
