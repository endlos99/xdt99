// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xga99.psi.impl.*;

public interface Xga99Types {

  IElementType ARGS_DIR_C = new Xga99ElementType("ARGS_DIR_C");
  IElementType ARGS_DIR_F = new Xga99ElementType("ARGS_DIR_F");
  IElementType ARGS_DIR_N = new Xga99ElementType("ARGS_DIR_N");
  IElementType ARGS_DIR_S = new Xga99ElementType("ARGS_DIR_S");
  IElementType ARGS_DIR_T = new Xga99ElementType("ARGS_DIR_T");
  IElementType ARGS_F_I = new Xga99ElementType("ARGS_F_I");
  IElementType ARGS_F_II = new Xga99ElementType("ARGS_F_II");
  IElementType ARGS_F_III = new Xga99ElementType("ARGS_F_III");
  IElementType ARGS_F_IV = new Xga99ElementType("ARGS_F_IV");
  IElementType ARGS_F_IX = new Xga99ElementType("ARGS_F_IX");
  IElementType ARGS_F_V = new Xga99ElementType("ARGS_F_V");
  IElementType ARGS_F_X = new Xga99ElementType("ARGS_F_X");
  IElementType ARGS_I = new Xga99ElementType("ARGS_I");
  IElementType ARGS_II = new Xga99ElementType("ARGS_II");
  IElementType ARGS_III = new Xga99ElementType("ARGS_III");
  IElementType ARGS_IX = new Xga99ElementType("ARGS_IX");
  IElementType ARGS_VI = new Xga99ElementType("ARGS_VI");
  IElementType ARGS_VII = new Xga99ElementType("ARGS_VII");
  IElementType ARGS_VIII = new Xga99ElementType("ARGS_VIII");
  IElementType DIRECTIVE = new Xga99ElementType("DIRECTIVE");
  IElementType DUMMY = new Xga99ElementType("DUMMY");
  IElementType EXPR = new Xga99ElementType("EXPR");
  IElementType INSTRUCTION = new Xga99ElementType("INSTRUCTION");
  IElementType LABELDEF = new Xga99ElementType("LABELDEF");
  IElementType LINECOMMENT = new Xga99ElementType("LINECOMMENT");
  IElementType OP_ADDRESS = new Xga99ElementType("OP_ADDRESS");
  IElementType OP_FILENAME = new Xga99ElementType("OP_FILENAME");
  IElementType OP_FLOAT = new Xga99ElementType("OP_FLOAT");
  IElementType OP_GD = new Xga99ElementType("OP_GD");
  IElementType OP_GS = new Xga99ElementType("OP_GS");
  IElementType OP_INDEX = new Xga99ElementType("OP_INDEX");
  IElementType OP_LABEL = new Xga99ElementType("OP_LABEL");
  IElementType OP_MD = new Xga99ElementType("OP_MD");
  IElementType OP_MS = new Xga99ElementType("OP_MS");
  IElementType OP_TEXT = new Xga99ElementType("OP_TEXT");
  IElementType OP_VALUE = new Xga99ElementType("OP_VALUE");
  IElementType PREPROCESSOR = new Xga99ElementType("PREPROCESSOR");
  IElementType SEXPR = new Xga99ElementType("SEXPR");
  IElementType UNKNOWN_MNEM = new Xga99ElementType("UNKNOWN_MNEM");

  IElementType COMMENT = new Xga99TokenType("COMMENT");
  IElementType CRLF = new Xga99TokenType("CRLF");
  IElementType DIGIT = new Xga99TokenType("DIGIT");
  IElementType DIR_C = new Xga99TokenType("DIR_C");
  IElementType DIR_F = new Xga99TokenType("DIR_F");
  IElementType DIR_L = new Xga99TokenType("DIR_L");
  IElementType DIR_M = new Xga99TokenType("DIR_M");
  IElementType DIR_S = new Xga99TokenType("DIR_S");
  IElementType DIR_T = new Xga99TokenType("DIR_T");
  IElementType FNAME = new Xga99TokenType("FNAME");
  IElementType GADDR = new Xga99TokenType("GADDR");
  IElementType IDENT = new Xga99TokenType("IDENT");
  IElementType INSTR_F_I = new Xga99TokenType("INSTR_F_I");
  IElementType INSTR_F_II = new Xga99TokenType("INSTR_F_II");
  IElementType INSTR_F_III = new Xga99TokenType("INSTR_F_III");
  IElementType INSTR_F_IV = new Xga99TokenType("INSTR_F_IV");
  IElementType INSTR_F_IX = new Xga99TokenType("INSTR_F_IX");
  IElementType INSTR_F_V = new Xga99TokenType("INSTR_F_V");
  IElementType INSTR_F_X = new Xga99TokenType("INSTR_F_X");
  IElementType INSTR_I = new Xga99TokenType("INSTR_I");
  IElementType INSTR_II = new Xga99TokenType("INSTR_II");
  IElementType INSTR_III = new Xga99TokenType("INSTR_III");
  IElementType INSTR_IX = new Xga99TokenType("INSTR_IX");
  IElementType INSTR_V = new Xga99TokenType("INSTR_V");
  IElementType INSTR_VI = new Xga99TokenType("INSTR_VI");
  IElementType INSTR_VII = new Xga99TokenType("INSTR_VII");
  IElementType INSTR_VIII = new Xga99TokenType("INSTR_VIII");
  IElementType INSTR_X = new Xga99TokenType("INSTR_X");
  IElementType INT = new Xga99TokenType("INT");
  IElementType LCOMMENT = new Xga99TokenType("LCOMMENT");
  IElementType LOCAL = new Xga99TokenType("LOCAL");
  IElementType OP_AST = new Xga99TokenType("OP_AST");
  IElementType OP_AT = new Xga99TokenType("OP_AT");
  IElementType OP_COLON = new Xga99TokenType("OP_COLON");
  IElementType OP_FQUOTE = new Xga99TokenType("OP_FQUOTE");
  IElementType OP_LC = new Xga99TokenType("OP_LC");
  IElementType OP_LPAREN = new Xga99TokenType("OP_LPAREN");
  IElementType OP_MINUS = new Xga99TokenType("OP_MINUS");
  IElementType OP_MISC = new Xga99TokenType("OP_MISC");
  IElementType OP_NOT = new Xga99TokenType("OP_NOT");
  IElementType OP_PLUS = new Xga99TokenType("OP_PLUS");
  IElementType OP_QUOTE = new Xga99TokenType("OP_QUOTE");
  IElementType OP_RPAREN = new Xga99TokenType("OP_RPAREN");
  IElementType OP_SEP = new Xga99TokenType("OP_SEP");
  IElementType PP_ARG = new Xga99TokenType("PP_ARG");
  IElementType PP_PARAM = new Xga99TokenType("PP_PARAM");
  IElementType PP_SEP = new Xga99TokenType("PP_SEP");
  IElementType PREP = new Xga99TokenType("PREP");
  IElementType TEXT = new Xga99TokenType("TEXT");
  IElementType UNKNOWN = new Xga99TokenType("UNKNOWN");
  IElementType VADDR = new Xga99TokenType("VADDR");
  IElementType VINDR = new Xga99TokenType("VINDR");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == ARGS_DIR_C) {
        return new Xga99ArgsDirCImpl(node);
      }
      else if (type == ARGS_DIR_F) {
        return new Xga99ArgsDirFImpl(node);
      }
      else if (type == ARGS_DIR_N) {
        return new Xga99ArgsDirNImpl(node);
      }
      else if (type == ARGS_DIR_S) {
        return new Xga99ArgsDirSImpl(node);
      }
      else if (type == ARGS_DIR_T) {
        return new Xga99ArgsDirTImpl(node);
      }
      else if (type == ARGS_F_I) {
        return new Xga99ArgsFIImpl(node);
      }
      else if (type == ARGS_F_II) {
        return new Xga99ArgsFIIImpl(node);
      }
      else if (type == ARGS_F_III) {
        return new Xga99ArgsFIIIImpl(node);
      }
      else if (type == ARGS_F_IV) {
        return new Xga99ArgsFIVImpl(node);
      }
      else if (type == ARGS_F_IX) {
        return new Xga99ArgsFIXImpl(node);
      }
      else if (type == ARGS_F_V) {
        return new Xga99ArgsFVImpl(node);
      }
      else if (type == ARGS_F_X) {
        return new Xga99ArgsFXImpl(node);
      }
      else if (type == ARGS_I) {
        return new Xga99ArgsIImpl(node);
      }
      else if (type == ARGS_II) {
        return new Xga99ArgsIIImpl(node);
      }
      else if (type == ARGS_III) {
        return new Xga99ArgsIIIImpl(node);
      }
      else if (type == ARGS_IX) {
        return new Xga99ArgsIXImpl(node);
      }
      else if (type == ARGS_VI) {
        return new Xga99ArgsVIImpl(node);
      }
      else if (type == ARGS_VII) {
        return new Xga99ArgsVIIImpl(node);
      }
      else if (type == ARGS_VIII) {
        return new Xga99ArgsVIIIImpl(node);
      }
      else if (type == DIRECTIVE) {
        return new Xga99DirectiveImpl(node);
      }
      else if (type == DUMMY) {
        return new Xga99DummyImpl(node);
      }
      else if (type == EXPR) {
        return new Xga99ExprImpl(node);
      }
      else if (type == INSTRUCTION) {
        return new Xga99InstructionImpl(node);
      }
      else if (type == LABELDEF) {
        return new Xga99LabeldefImpl(node);
      }
      else if (type == LINECOMMENT) {
        return new Xga99LinecommentImpl(node);
      }
      else if (type == OP_ADDRESS) {
        return new Xga99OpAddressImpl(node);
      }
      else if (type == OP_FILENAME) {
        return new Xga99OpFilenameImpl(node);
      }
      else if (type == OP_FLOAT) {
        return new Xga99OpFloatImpl(node);
      }
      else if (type == OP_GD) {
        return new Xga99OpGdImpl(node);
      }
      else if (type == OP_GS) {
        return new Xga99OpGsImpl(node);
      }
      else if (type == OP_INDEX) {
        return new Xga99OpIndexImpl(node);
      }
      else if (type == OP_LABEL) {
        return new Xga99OpLabelImpl(node);
      }
      else if (type == OP_MD) {
        return new Xga99OpMdImpl(node);
      }
      else if (type == OP_MS) {
        return new Xga99OpMsImpl(node);
      }
      else if (type == OP_TEXT) {
        return new Xga99OpTextImpl(node);
      }
      else if (type == OP_VALUE) {
        return new Xga99OpValueImpl(node);
      }
      else if (type == PREPROCESSOR) {
        return new Xga99PreprocessorImpl(node);
      }
      else if (type == SEXPR) {
        return new Xga99SexprImpl(node);
      }
      else if (type == UNKNOWN_MNEM) {
        return new Xga99UnknownMnemImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
