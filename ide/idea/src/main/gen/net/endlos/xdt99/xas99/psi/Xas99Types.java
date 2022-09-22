// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xas99.psi.impl.*;

public interface Xas99Types {

  IElementType ALIAS_DEFINITION = new Xas99ElementType("ALIAS_DEFINITION");
  IElementType ARGS_ADV_I = new Xas99ElementType("ARGS_ADV_I");
  IElementType ARGS_ADV_IA = new Xas99ElementType("ARGS_ADV_IA");
  IElementType ARGS_ADV_IV = new Xas99ElementType("ARGS_ADV_IV");
  IElementType ARGS_ADV_VI = new Xas99ElementType("ARGS_ADV_VI");
  IElementType ARGS_ADV_VIII = new Xas99ElementType("ARGS_ADV_VIII");
  IElementType ARGS_DIR_C = new Xas99ElementType("ARGS_DIR_C");
  IElementType ARGS_DIR_E = new Xas99ElementType("ARGS_DIR_E");
  IElementType ARGS_DIR_EO = new Xas99ElementType("ARGS_DIR_EO");
  IElementType ARGS_DIR_ES = new Xas99ElementType("ARGS_DIR_ES");
  IElementType ARGS_DIR_EV = new Xas99ElementType("ARGS_DIR_EV");
  IElementType ARGS_DIR_F = new Xas99ElementType("ARGS_DIR_F");
  IElementType ARGS_DIR_L = new Xas99ElementType("ARGS_DIR_L");
  IElementType ARGS_DIR_R = new Xas99ElementType("ARGS_DIR_R");
  IElementType ARGS_DIR_S = new Xas99ElementType("ARGS_DIR_S");
  IElementType ARGS_DIR_T = new Xas99ElementType("ARGS_DIR_T");
  IElementType ARGS_I = new Xas99ElementType("ARGS_I");
  IElementType ARGS_II = new Xas99ElementType("ARGS_II");
  IElementType ARGS_III = new Xas99ElementType("ARGS_III");
  IElementType ARGS_IV = new Xas99ElementType("ARGS_IV");
  IElementType ARGS_IX = new Xas99ElementType("ARGS_IX");
  IElementType ARGS_IX_X = new Xas99ElementType("ARGS_IX_X");
  IElementType ARGS_V = new Xas99ElementType("ARGS_V");
  IElementType ARGS_VI = new Xas99ElementType("ARGS_VI");
  IElementType ARGS_VIII = new Xas99ElementType("ARGS_VIII");
  IElementType ARGS_VIII_I = new Xas99ElementType("ARGS_VIII_I");
  IElementType ARGS_VIII_R = new Xas99ElementType("ARGS_VIII_R");
  IElementType DIRECTIVE = new Xas99ElementType("DIRECTIVE");
  IElementType DUMMY = new Xas99ElementType("DUMMY");
  IElementType INSTRUCTION = new Xas99ElementType("INSTRUCTION");
  IElementType LABELDEF = new Xas99ElementType("LABELDEF");
  IElementType LINECOMMENT = new Xas99ElementType("LINECOMMENT");
  IElementType OP_ALIAS = new Xas99ElementType("OP_ALIAS");
  IElementType OP_FILENAME = new Xas99ElementType("OP_FILENAME");
  IElementType OP_FLOAT = new Xas99ElementType("OP_FLOAT");
  IElementType OP_LABEL = new Xas99ElementType("OP_LABEL");
  IElementType OP_REGISTER = new Xas99ElementType("OP_REGISTER");
  IElementType OP_TEXT = new Xas99ElementType("OP_TEXT");
  IElementType PRAGMA = new Xas99ElementType("PRAGMA");
  IElementType PREPROCESSOR = new Xas99ElementType("PREPROCESSOR");

  IElementType COMMENT = new Xas99TokenType("COMMENT");
  IElementType CRLF = new Xas99TokenType("CRLF");
  IElementType DIGIT = new Xas99TokenType("DIGIT");
  IElementType DIR_C = new Xas99TokenType("DIR_C");
  IElementType DIR_E = new Xas99TokenType("DIR_E");
  IElementType DIR_EO = new Xas99TokenType("DIR_EO");
  IElementType DIR_ES = new Xas99TokenType("DIR_ES");
  IElementType DIR_EV = new Xas99TokenType("DIR_EV");
  IElementType DIR_F = new Xas99TokenType("DIR_F");
  IElementType DIR_L = new Xas99TokenType("DIR_L");
  IElementType DIR_O = new Xas99TokenType("DIR_O");
  IElementType DIR_R = new Xas99TokenType("DIR_R");
  IElementType DIR_RA = new Xas99TokenType("DIR_RA");
  IElementType DIR_S = new Xas99TokenType("DIR_S");
  IElementType DIR_T = new Xas99TokenType("DIR_T");
  IElementType DIR_X = new Xas99TokenType("DIR_X");
  IElementType FNAME = new Xas99TokenType("FNAME");
  IElementType IDENT = new Xas99TokenType("IDENT");
  IElementType INSTR_99000_I = new Xas99TokenType("INSTR_99000_I");
  IElementType INSTR_99000_IV = new Xas99TokenType("INSTR_99000_IV");
  IElementType INSTR_99000_VI = new Xas99TokenType("INSTR_99000_VI");
  IElementType INSTR_99000_VIII = new Xas99TokenType("INSTR_99000_VIII");
  IElementType INSTR_9995_VI = new Xas99TokenType("INSTR_9995_VI");
  IElementType INSTR_9995_VIII = new Xas99TokenType("INSTR_9995_VIII");
  IElementType INSTR_F18A_IA = new Xas99TokenType("INSTR_F18A_IA");
  IElementType INSTR_F18A_O = new Xas99TokenType("INSTR_F18A_O");
  IElementType INSTR_F18A_VI = new Xas99TokenType("INSTR_F18A_VI");
  IElementType INSTR_I = new Xas99TokenType("INSTR_I");
  IElementType INSTR_II = new Xas99TokenType("INSTR_II");
  IElementType INSTR_III = new Xas99TokenType("INSTR_III");
  IElementType INSTR_IV = new Xas99TokenType("INSTR_IV");
  IElementType INSTR_IX = new Xas99TokenType("INSTR_IX");
  IElementType INSTR_IX_X = new Xas99TokenType("INSTR_IX_X");
  IElementType INSTR_O = new Xas99TokenType("INSTR_O");
  IElementType INSTR_V = new Xas99TokenType("INSTR_V");
  IElementType INSTR_VI = new Xas99TokenType("INSTR_VI");
  IElementType INSTR_VII = new Xas99TokenType("INSTR_VII");
  IElementType INSTR_VIII = new Xas99TokenType("INSTR_VIII");
  IElementType INSTR_VIII_I = new Xas99TokenType("INSTR_VIII_I");
  IElementType INSTR_VIII_R = new Xas99TokenType("INSTR_VIII_R");
  IElementType INT = new Xas99TokenType("INT");
  IElementType LCOMMENT = new Xas99TokenType("LCOMMENT");
  IElementType LOCAL = new Xas99TokenType("LOCAL");
  IElementType MOD_AUTO = new Xas99TokenType("MOD_AUTO");
  IElementType MOD_LEN = new Xas99TokenType("MOD_LEN");
  IElementType MOD_XBANK = new Xas99TokenType("MOD_XBANK");
  IElementType OP_AST = new Xas99TokenType("OP_AST");
  IElementType OP_AT = new Xas99TokenType("OP_AT");
  IElementType OP_COLON = new Xas99TokenType("OP_COLON");
  IElementType OP_FQUOTE = new Xas99TokenType("OP_FQUOTE");
  IElementType OP_LC = new Xas99TokenType("OP_LC");
  IElementType OP_LPAREN = new Xas99TokenType("OP_LPAREN");
  IElementType OP_MINUS = new Xas99TokenType("OP_MINUS");
  IElementType OP_MISC = new Xas99TokenType("OP_MISC");
  IElementType OP_NOT = new Xas99TokenType("OP_NOT");
  IElementType OP_PLUS = new Xas99TokenType("OP_PLUS");
  IElementType OP_QUOTE = new Xas99TokenType("OP_QUOTE");
  IElementType OP_RPAREN = new Xas99TokenType("OP_RPAREN");
  IElementType OP_SEP = new Xas99TokenType("OP_SEP");
  IElementType PG_CYC = new Xas99TokenType("PG_CYC");
  IElementType PG_EQ = new Xas99TokenType("PG_EQ");
  IElementType PG_SEP = new Xas99TokenType("PG_SEP");
  IElementType PG_START = new Xas99TokenType("PG_START");
  IElementType PG_TERM = new Xas99TokenType("PG_TERM");
  IElementType PP_ARG = new Xas99TokenType("PP_ARG");
  IElementType PP_PARAM = new Xas99TokenType("PP_PARAM");
  IElementType PP_SEP = new Xas99TokenType("PP_SEP");
  IElementType PREP = new Xas99TokenType("PREP");
  IElementType REGISTER = new Xas99TokenType("REGISTER");
  IElementType REGISTER0 = new Xas99TokenType("REGISTER0");
  IElementType TEXT = new Xas99TokenType("TEXT");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == ALIAS_DEFINITION) {
        return new Xas99AliasDefinitionImpl(node);
      }
      else if (type == ARGS_ADV_I) {
        return new Xas99ArgsAdvIImpl(node);
      }
      else if (type == ARGS_ADV_IA) {
        return new Xas99ArgsAdvIaImpl(node);
      }
      else if (type == ARGS_ADV_IV) {
        return new Xas99ArgsAdvIVImpl(node);
      }
      else if (type == ARGS_ADV_VI) {
        return new Xas99ArgsAdvVIImpl(node);
      }
      else if (type == ARGS_ADV_VIII) {
        return new Xas99ArgsAdvVIIIImpl(node);
      }
      else if (type == ARGS_DIR_C) {
        return new Xas99ArgsDirCImpl(node);
      }
      else if (type == ARGS_DIR_E) {
        return new Xas99ArgsDirEImpl(node);
      }
      else if (type == ARGS_DIR_EO) {
        return new Xas99ArgsDirEOImpl(node);
      }
      else if (type == ARGS_DIR_ES) {
        return new Xas99ArgsDirESImpl(node);
      }
      else if (type == ARGS_DIR_EV) {
        return new Xas99ArgsDirEVImpl(node);
      }
      else if (type == ARGS_DIR_F) {
        return new Xas99ArgsDirFImpl(node);
      }
      else if (type == ARGS_DIR_L) {
        return new Xas99ArgsDirLImpl(node);
      }
      else if (type == ARGS_DIR_R) {
        return new Xas99ArgsDirRImpl(node);
      }
      else if (type == ARGS_DIR_S) {
        return new Xas99ArgsDirSImpl(node);
      }
      else if (type == ARGS_DIR_T) {
        return new Xas99ArgsDirTImpl(node);
      }
      else if (type == ARGS_I) {
        return new Xas99ArgsIImpl(node);
      }
      else if (type == ARGS_II) {
        return new Xas99ArgsIIImpl(node);
      }
      else if (type == ARGS_III) {
        return new Xas99ArgsIIIImpl(node);
      }
      else if (type == ARGS_IV) {
        return new Xas99ArgsIVImpl(node);
      }
      else if (type == ARGS_IX) {
        return new Xas99ArgsIXImpl(node);
      }
      else if (type == ARGS_IX_X) {
        return new Xas99ArgsIXXImpl(node);
      }
      else if (type == ARGS_V) {
        return new Xas99ArgsVImpl(node);
      }
      else if (type == ARGS_VI) {
        return new Xas99ArgsVIImpl(node);
      }
      else if (type == ARGS_VIII) {
        return new Xas99ArgsVIIIImpl(node);
      }
      else if (type == ARGS_VIII_I) {
        return new Xas99ArgsVIIIIImpl(node);
      }
      else if (type == ARGS_VIII_R) {
        return new Xas99ArgsVIIIRImpl(node);
      }
      else if (type == DIRECTIVE) {
        return new Xas99DirectiveImpl(node);
      }
      else if (type == DUMMY) {
        return new Xas99DummyImpl(node);
      }
      else if (type == INSTRUCTION) {
        return new Xas99InstructionImpl(node);
      }
      else if (type == LABELDEF) {
        return new Xas99LabeldefImpl(node);
      }
      else if (type == LINECOMMENT) {
        return new Xas99LinecommentImpl(node);
      }
      else if (type == OP_ALIAS) {
        return new Xas99OpAliasImpl(node);
      }
      else if (type == OP_FILENAME) {
        return new Xas99OpFilenameImpl(node);
      }
      else if (type == OP_FLOAT) {
        return new Xas99OpFloatImpl(node);
      }
      else if (type == OP_LABEL) {
        return new Xas99OpLabelImpl(node);
      }
      else if (type == OP_REGISTER) {
        return new Xas99OpRegisterImpl(node);
      }
      else if (type == OP_TEXT) {
        return new Xas99OpTextImpl(node);
      }
      else if (type == PRAGMA) {
        return new Xas99PragmaImpl(node);
      }
      else if (type == PREPROCESSOR) {
        return new Xas99PreprocessorImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
