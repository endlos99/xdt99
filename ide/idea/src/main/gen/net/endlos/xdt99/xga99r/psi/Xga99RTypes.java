// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99r.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xga99r.psi.impl.*;

public interface Xga99RTypes {

  IElementType ARGS_DIR_C = new Xga99RElementType("ARGS_DIR_C");
  IElementType ARGS_DIR_F = new Xga99RElementType("ARGS_DIR_F");
  IElementType ARGS_DIR_N = new Xga99RElementType("ARGS_DIR_N");
  IElementType ARGS_DIR_S = new Xga99RElementType("ARGS_DIR_S");
  IElementType ARGS_DIR_T = new Xga99RElementType("ARGS_DIR_T");
  IElementType ARGS_F_I = new Xga99RElementType("ARGS_F_I");
  IElementType ARGS_F_II = new Xga99RElementType("ARGS_F_II");
  IElementType ARGS_F_III = new Xga99RElementType("ARGS_F_III");
  IElementType ARGS_F_IV = new Xga99RElementType("ARGS_F_IV");
  IElementType ARGS_F_IX = new Xga99RElementType("ARGS_F_IX");
  IElementType ARGS_F_V = new Xga99RElementType("ARGS_F_V");
  IElementType ARGS_F_X = new Xga99RElementType("ARGS_F_X");
  IElementType ARGS_I = new Xga99RElementType("ARGS_I");
  IElementType ARGS_II = new Xga99RElementType("ARGS_II");
  IElementType ARGS_III = new Xga99RElementType("ARGS_III");
  IElementType ARGS_IX = new Xga99RElementType("ARGS_IX");
  IElementType ARGS_VI = new Xga99RElementType("ARGS_VI");
  IElementType ARGS_VII = new Xga99RElementType("ARGS_VII");
  IElementType ARGS_VIII = new Xga99RElementType("ARGS_VIII");
  IElementType DIRECTIVE = new Xga99RElementType("DIRECTIVE");
  IElementType DUMMY = new Xga99RElementType("DUMMY");
  IElementType INSTRUCTION = new Xga99RElementType("INSTRUCTION");
  IElementType LABELDEF = new Xga99RElementType("LABELDEF");
  IElementType LINECOMMENT = new Xga99RElementType("LINECOMMENT");
  IElementType OP_FILENAME = new Xga99RElementType("OP_FILENAME");
  IElementType OP_FLOAT = new Xga99RElementType("OP_FLOAT");
  IElementType OP_LABEL = new Xga99RElementType("OP_LABEL");
  IElementType OP_TEXT = new Xga99RElementType("OP_TEXT");
  IElementType PREPROCESSOR = new Xga99RElementType("PREPROCESSOR");
  IElementType UNKNOWN_MNEM = new Xga99RElementType("UNKNOWN_MNEM");

  IElementType COMMENT = new Xga99RTokenType("COMMENT");
  IElementType CRLF = new Xga99RTokenType("CRLF");
  IElementType DIGIT = new Xga99RTokenType("DIGIT");
  IElementType DIR_C = new Xga99RTokenType("DIR_C");
  IElementType DIR_F = new Xga99RTokenType("DIR_F");
  IElementType DIR_L = new Xga99RTokenType("DIR_L");
  IElementType DIR_M = new Xga99RTokenType("DIR_M");
  IElementType DIR_S = new Xga99RTokenType("DIR_S");
  IElementType DIR_T = new Xga99RTokenType("DIR_T");
  IElementType FNAME = new Xga99RTokenType("FNAME");
  IElementType GADDR = new Xga99RTokenType("GADDR");
  IElementType IDENT = new Xga99RTokenType("IDENT");
  IElementType INSTR_F_I = new Xga99RTokenType("INSTR_F_I");
  IElementType INSTR_F_II = new Xga99RTokenType("INSTR_F_II");
  IElementType INSTR_F_III = new Xga99RTokenType("INSTR_F_III");
  IElementType INSTR_F_IV = new Xga99RTokenType("INSTR_F_IV");
  IElementType INSTR_F_IX = new Xga99RTokenType("INSTR_F_IX");
  IElementType INSTR_F_V = new Xga99RTokenType("INSTR_F_V");
  IElementType INSTR_F_X = new Xga99RTokenType("INSTR_F_X");
  IElementType INSTR_I = new Xga99RTokenType("INSTR_I");
  IElementType INSTR_II = new Xga99RTokenType("INSTR_II");
  IElementType INSTR_III = new Xga99RTokenType("INSTR_III");
  IElementType INSTR_IX = new Xga99RTokenType("INSTR_IX");
  IElementType INSTR_V = new Xga99RTokenType("INSTR_V");
  IElementType INSTR_VI = new Xga99RTokenType("INSTR_VI");
  IElementType INSTR_VII = new Xga99RTokenType("INSTR_VII");
  IElementType INSTR_VIII = new Xga99RTokenType("INSTR_VIII");
  IElementType INSTR_X = new Xga99RTokenType("INSTR_X");
  IElementType INT = new Xga99RTokenType("INT");
  IElementType LCOMMENT = new Xga99RTokenType("LCOMMENT");
  IElementType LOCAL = new Xga99RTokenType("LOCAL");
  IElementType OP_AST = new Xga99RTokenType("OP_AST");
  IElementType OP_AT = new Xga99RTokenType("OP_AT");
  IElementType OP_COLON = new Xga99RTokenType("OP_COLON");
  IElementType OP_FQUOTE = new Xga99RTokenType("OP_FQUOTE");
  IElementType OP_LC = new Xga99RTokenType("OP_LC");
  IElementType OP_LPAREN = new Xga99RTokenType("OP_LPAREN");
  IElementType OP_MINUS = new Xga99RTokenType("OP_MINUS");
  IElementType OP_MISC = new Xga99RTokenType("OP_MISC");
  IElementType OP_NOT = new Xga99RTokenType("OP_NOT");
  IElementType OP_PLUS = new Xga99RTokenType("OP_PLUS");
  IElementType OP_QUOTE = new Xga99RTokenType("OP_QUOTE");
  IElementType OP_RPAREN = new Xga99RTokenType("OP_RPAREN");
  IElementType OP_SEP = new Xga99RTokenType("OP_SEP");
  IElementType PP_ARG = new Xga99RTokenType("PP_ARG");
  IElementType PP_PARAM = new Xga99RTokenType("PP_PARAM");
  IElementType PP_SEP = new Xga99RTokenType("PP_SEP");
  IElementType PREP = new Xga99RTokenType("PREP");
  IElementType TEXT = new Xga99RTokenType("TEXT");
  IElementType UNKNOWN = new Xga99RTokenType("UNKNOWN");
  IElementType VADDR = new Xga99RTokenType("VADDR");
  IElementType VINDR = new Xga99RTokenType("VINDR");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == ARGS_DIR_C) {
        return new Xga99RArgsDirCImpl(node);
      }
      else if (type == ARGS_DIR_F) {
        return new Xga99RArgsDirFImpl(node);
      }
      else if (type == ARGS_DIR_N) {
        return new Xga99RArgsDirNImpl(node);
      }
      else if (type == ARGS_DIR_S) {
        return new Xga99RArgsDirSImpl(node);
      }
      else if (type == ARGS_DIR_T) {
        return new Xga99RArgsDirTImpl(node);
      }
      else if (type == ARGS_F_I) {
        return new Xga99RArgsFIImpl(node);
      }
      else if (type == ARGS_F_II) {
        return new Xga99RArgsFIIImpl(node);
      }
      else if (type == ARGS_F_III) {
        return new Xga99RArgsFIIIImpl(node);
      }
      else if (type == ARGS_F_IV) {
        return new Xga99RArgsFIVImpl(node);
      }
      else if (type == ARGS_F_IX) {
        return new Xga99RArgsFIXImpl(node);
      }
      else if (type == ARGS_F_V) {
        return new Xga99RArgsFVImpl(node);
      }
      else if (type == ARGS_F_X) {
        return new Xga99RArgsFXImpl(node);
      }
      else if (type == ARGS_I) {
        return new Xga99RArgsIImpl(node);
      }
      else if (type == ARGS_II) {
        return new Xga99RArgsIIImpl(node);
      }
      else if (type == ARGS_III) {
        return new Xga99RArgsIIIImpl(node);
      }
      else if (type == ARGS_IX) {
        return new Xga99RArgsIXImpl(node);
      }
      else if (type == ARGS_VI) {
        return new Xga99RArgsVIImpl(node);
      }
      else if (type == ARGS_VII) {
        return new Xga99RArgsVIIImpl(node);
      }
      else if (type == ARGS_VIII) {
        return new Xga99RArgsVIIIImpl(node);
      }
      else if (type == DIRECTIVE) {
        return new Xga99RDirectiveImpl(node);
      }
      else if (type == DUMMY) {
        return new Xga99RDummyImpl(node);
      }
      else if (type == INSTRUCTION) {
        return new Xga99RInstructionImpl(node);
      }
      else if (type == LABELDEF) {
        return new Xga99RLabeldefImpl(node);
      }
      else if (type == LINECOMMENT) {
        return new Xga99RLinecommentImpl(node);
      }
      else if (type == OP_FILENAME) {
        return new Xga99ROpFilenameImpl(node);
      }
      else if (type == OP_FLOAT) {
        return new Xga99ROpFloatImpl(node);
      }
      else if (type == OP_LABEL) {
        return new Xga99ROpLabelImpl(node);
      }
      else if (type == OP_TEXT) {
        return new Xga99ROpTextImpl(node);
      }
      else if (type == PREPROCESSOR) {
        return new Xga99RPreprocessorImpl(node);
      }
      else if (type == UNKNOWN_MNEM) {
        return new Xga99RUnknownMnemImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
