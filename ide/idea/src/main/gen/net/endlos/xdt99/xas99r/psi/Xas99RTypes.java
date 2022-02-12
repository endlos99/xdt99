// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99r.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xas99r.psi.impl.*;

public interface Xas99RTypes {

  IElementType ARGS_ADV_I = new Xas99RElementType("ARGS_ADV_I");
  IElementType ARGS_ADV_IA = new Xas99RElementType("ARGS_ADV_IA");
  IElementType ARGS_ADV_IV = new Xas99RElementType("ARGS_ADV_IV");
  IElementType ARGS_ADV_VI = new Xas99RElementType("ARGS_ADV_VI");
  IElementType ARGS_ADV_VIII = new Xas99RElementType("ARGS_ADV_VIII");
  IElementType ARGS_DIR_C = new Xas99RElementType("ARGS_DIR_C");
  IElementType ARGS_DIR_E = new Xas99RElementType("ARGS_DIR_E");
  IElementType ARGS_DIR_EO = new Xas99RElementType("ARGS_DIR_EO");
  IElementType ARGS_DIR_ES = new Xas99RElementType("ARGS_DIR_ES");
  IElementType ARGS_DIR_F = new Xas99RElementType("ARGS_DIR_F");
  IElementType ARGS_DIR_L = new Xas99RElementType("ARGS_DIR_L");
  IElementType ARGS_DIR_R = new Xas99RElementType("ARGS_DIR_R");
  IElementType ARGS_DIR_S = new Xas99RElementType("ARGS_DIR_S");
  IElementType ARGS_DIR_T = new Xas99RElementType("ARGS_DIR_T");
  IElementType ARGS_I = new Xas99RElementType("ARGS_I");
  IElementType ARGS_II = new Xas99RElementType("ARGS_II");
  IElementType ARGS_III = new Xas99RElementType("ARGS_III");
  IElementType ARGS_IV = new Xas99RElementType("ARGS_IV");
  IElementType ARGS_IX = new Xas99RElementType("ARGS_IX");
  IElementType ARGS_IX_X = new Xas99RElementType("ARGS_IX_X");
  IElementType ARGS_V = new Xas99RElementType("ARGS_V");
  IElementType ARGS_VI = new Xas99RElementType("ARGS_VI");
  IElementType ARGS_VIII = new Xas99RElementType("ARGS_VIII");
  IElementType ARGS_VIII_I = new Xas99RElementType("ARGS_VIII_I");
  IElementType ARGS_VIII_R = new Xas99RElementType("ARGS_VIII_R");
  IElementType DIRECTIVE = new Xas99RElementType("DIRECTIVE");
  IElementType DUMMY = new Xas99RElementType("DUMMY");
  IElementType INSTRUCTION = new Xas99RElementType("INSTRUCTION");
  IElementType LABELDEF = new Xas99RElementType("LABELDEF");
  IElementType LINECOMMENT = new Xas99RElementType("LINECOMMENT");
  IElementType OP_FILENAME = new Xas99RElementType("OP_FILENAME");
  IElementType OP_FLOAT = new Xas99RElementType("OP_FLOAT");
  IElementType OP_LABEL = new Xas99RElementType("OP_LABEL");
  IElementType OP_REGISTER = new Xas99RElementType("OP_REGISTER");
  IElementType OP_TEXT = new Xas99RElementType("OP_TEXT");
  IElementType PRAGMA = new Xas99RElementType("PRAGMA");
  IElementType PREPROCESSOR = new Xas99RElementType("PREPROCESSOR");
  IElementType UNKNOWN_MNEM = new Xas99RElementType("UNKNOWN_MNEM");

  IElementType COMMENT = new Xas99RTokenType("COMMENT");
  IElementType CRLF = new Xas99RTokenType("CRLF");
  IElementType DIGIT = new Xas99RTokenType("DIGIT");
  IElementType DIR_C = new Xas99RTokenType("DIR_C");
  IElementType DIR_E = new Xas99RTokenType("DIR_E");
  IElementType DIR_EO = new Xas99RTokenType("DIR_EO");
  IElementType DIR_ES = new Xas99RTokenType("DIR_ES");
  IElementType DIR_F = new Xas99RTokenType("DIR_F");
  IElementType DIR_L = new Xas99RTokenType("DIR_L");
  IElementType DIR_O = new Xas99RTokenType("DIR_O");
  IElementType DIR_R = new Xas99RTokenType("DIR_R");
  IElementType DIR_S = new Xas99RTokenType("DIR_S");
  IElementType DIR_T = new Xas99RTokenType("DIR_T");
  IElementType DIR_X = new Xas99RTokenType("DIR_X");
  IElementType FNAME = new Xas99RTokenType("FNAME");
  IElementType IDENT = new Xas99RTokenType("IDENT");
  IElementType INSTR_99000_I = new Xas99RTokenType("INSTR_99000_I");
  IElementType INSTR_99000_IV = new Xas99RTokenType("INSTR_99000_IV");
  IElementType INSTR_99000_VI = new Xas99RTokenType("INSTR_99000_VI");
  IElementType INSTR_99000_VIII = new Xas99RTokenType("INSTR_99000_VIII");
  IElementType INSTR_9995_VI = new Xas99RTokenType("INSTR_9995_VI");
  IElementType INSTR_9995_VIII = new Xas99RTokenType("INSTR_9995_VIII");
  IElementType INSTR_F18A_IA = new Xas99RTokenType("INSTR_F18A_IA");
  IElementType INSTR_F18A_O = new Xas99RTokenType("INSTR_F18A_O");
  IElementType INSTR_F18A_VI = new Xas99RTokenType("INSTR_F18A_VI");
  IElementType INSTR_I = new Xas99RTokenType("INSTR_I");
  IElementType INSTR_II = new Xas99RTokenType("INSTR_II");
  IElementType INSTR_III = new Xas99RTokenType("INSTR_III");
  IElementType INSTR_IV = new Xas99RTokenType("INSTR_IV");
  IElementType INSTR_IX = new Xas99RTokenType("INSTR_IX");
  IElementType INSTR_IX_X = new Xas99RTokenType("INSTR_IX_X");
  IElementType INSTR_O = new Xas99RTokenType("INSTR_O");
  IElementType INSTR_V = new Xas99RTokenType("INSTR_V");
  IElementType INSTR_VI = new Xas99RTokenType("INSTR_VI");
  IElementType INSTR_VII = new Xas99RTokenType("INSTR_VII");
  IElementType INSTR_VIII = new Xas99RTokenType("INSTR_VIII");
  IElementType INSTR_VIII_I = new Xas99RTokenType("INSTR_VIII_I");
  IElementType INSTR_VIII_R = new Xas99RTokenType("INSTR_VIII_R");
  IElementType INT = new Xas99RTokenType("INT");
  IElementType LCOMMENT = new Xas99RTokenType("LCOMMENT");
  IElementType LOCAL = new Xas99RTokenType("LOCAL");
  IElementType MOD_AUTO = new Xas99RTokenType("MOD_AUTO");
  IElementType MOD_LEN = new Xas99RTokenType("MOD_LEN");
  IElementType MOD_XBANK = new Xas99RTokenType("MOD_XBANK");
  IElementType OP_AST = new Xas99RTokenType("OP_AST");
  IElementType OP_AT = new Xas99RTokenType("OP_AT");
  IElementType OP_COLON = new Xas99RTokenType("OP_COLON");
  IElementType OP_FQUOTE = new Xas99RTokenType("OP_FQUOTE");
  IElementType OP_LC = new Xas99RTokenType("OP_LC");
  IElementType OP_LPAREN = new Xas99RTokenType("OP_LPAREN");
  IElementType OP_MINUS = new Xas99RTokenType("OP_MINUS");
  IElementType OP_MISC = new Xas99RTokenType("OP_MISC");
  IElementType OP_NOT = new Xas99RTokenType("OP_NOT");
  IElementType OP_PLUS = new Xas99RTokenType("OP_PLUS");
  IElementType OP_QUOTE = new Xas99RTokenType("OP_QUOTE");
  IElementType OP_RPAREN = new Xas99RTokenType("OP_RPAREN");
  IElementType OP_SEP = new Xas99RTokenType("OP_SEP");
  IElementType PG_CYC = new Xas99RTokenType("PG_CYC");
  IElementType PG_EQ = new Xas99RTokenType("PG_EQ");
  IElementType PG_SEP = new Xas99RTokenType("PG_SEP");
  IElementType PG_START = new Xas99RTokenType("PG_START");
  IElementType PG_TERM = new Xas99RTokenType("PG_TERM");
  IElementType PP_ARG = new Xas99RTokenType("PP_ARG");
  IElementType PP_PARAM = new Xas99RTokenType("PP_PARAM");
  IElementType PP_SEP = new Xas99RTokenType("PP_SEP");
  IElementType PREP = new Xas99RTokenType("PREP");
  IElementType REGISTER = new Xas99RTokenType("REGISTER");
  IElementType REGISTER0 = new Xas99RTokenType("REGISTER0");
  IElementType TEXT = new Xas99RTokenType("TEXT");
  IElementType UNKNOWN = new Xas99RTokenType("UNKNOWN");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == ARGS_ADV_I) {
        return new Xas99RArgsAdvIImpl(node);
      }
      else if (type == ARGS_ADV_IA) {
        return new Xas99RArgsAdvIaImpl(node);
      }
      else if (type == ARGS_ADV_IV) {
        return new Xas99RArgsAdvIVImpl(node);
      }
      else if (type == ARGS_ADV_VI) {
        return new Xas99RArgsAdvVIImpl(node);
      }
      else if (type == ARGS_ADV_VIII) {
        return new Xas99RArgsAdvVIIIImpl(node);
      }
      else if (type == ARGS_DIR_C) {
        return new Xas99RArgsDirCImpl(node);
      }
      else if (type == ARGS_DIR_E) {
        return new Xas99RArgsDirEImpl(node);
      }
      else if (type == ARGS_DIR_EO) {
        return new Xas99RArgsDirEOImpl(node);
      }
      else if (type == ARGS_DIR_ES) {
        return new Xas99RArgsDirESImpl(node);
      }
      else if (type == ARGS_DIR_F) {
        return new Xas99RArgsDirFImpl(node);
      }
      else if (type == ARGS_DIR_L) {
        return new Xas99RArgsDirLImpl(node);
      }
      else if (type == ARGS_DIR_R) {
        return new Xas99RArgsDirRImpl(node);
      }
      else if (type == ARGS_DIR_S) {
        return new Xas99RArgsDirSImpl(node);
      }
      else if (type == ARGS_DIR_T) {
        return new Xas99RArgsDirTImpl(node);
      }
      else if (type == ARGS_I) {
        return new Xas99RArgsIImpl(node);
      }
      else if (type == ARGS_II) {
        return new Xas99RArgsIIImpl(node);
      }
      else if (type == ARGS_III) {
        return new Xas99RArgsIIIImpl(node);
      }
      else if (type == ARGS_IV) {
        return new Xas99RArgsIVImpl(node);
      }
      else if (type == ARGS_IX) {
        return new Xas99RArgsIXImpl(node);
      }
      else if (type == ARGS_IX_X) {
        return new Xas99RArgsIXXImpl(node);
      }
      else if (type == ARGS_V) {
        return new Xas99RArgsVImpl(node);
      }
      else if (type == ARGS_VI) {
        return new Xas99RArgsVIImpl(node);
      }
      else if (type == ARGS_VIII) {
        return new Xas99RArgsVIIIImpl(node);
      }
      else if (type == ARGS_VIII_I) {
        return new Xas99RArgsVIIIIImpl(node);
      }
      else if (type == ARGS_VIII_R) {
        return new Xas99RArgsVIIIRImpl(node);
      }
      else if (type == DIRECTIVE) {
        return new Xas99RDirectiveImpl(node);
      }
      else if (type == DUMMY) {
        return new Xas99RDummyImpl(node);
      }
      else if (type == INSTRUCTION) {
        return new Xas99RInstructionImpl(node);
      }
      else if (type == LABELDEF) {
        return new Xas99RLabeldefImpl(node);
      }
      else if (type == LINECOMMENT) {
        return new Xas99RLinecommentImpl(node);
      }
      else if (type == OP_FILENAME) {
        return new Xas99ROpFilenameImpl(node);
      }
      else if (type == OP_FLOAT) {
        return new Xas99ROpFloatImpl(node);
      }
      else if (type == OP_LABEL) {
        return new Xas99ROpLabelImpl(node);
      }
      else if (type == OP_REGISTER) {
        return new Xas99ROpRegisterImpl(node);
      }
      else if (type == OP_TEXT) {
        return new Xas99ROpTextImpl(node);
      }
      else if (type == PRAGMA) {
        return new Xas99RPragmaImpl(node);
      }
      else if (type == PREPROCESSOR) {
        return new Xas99RPreprocessorImpl(node);
      }
      else if (type == UNKNOWN_MNEM) {
        return new Xas99RUnknownMnemImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
