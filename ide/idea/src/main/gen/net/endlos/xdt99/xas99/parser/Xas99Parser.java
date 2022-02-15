// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.parser;

import com.intellij.lang.PsiBuilder;
import com.intellij.lang.PsiBuilder.Marker;
import static net.endlos.xdt99.xas99.psi.Xas99Types.*;
import static com.intellij.lang.parser.GeneratedParserUtilBase.*;
import com.intellij.psi.tree.IElementType;
import com.intellij.lang.ASTNode;
import com.intellij.psi.tree.TokenSet;
import com.intellij.lang.PsiParser;
import com.intellij.lang.LightPsiParser;

@SuppressWarnings({"SimplifiableIfStatement", "UnusedAssignment"})
public class Xas99Parser implements PsiParser, LightPsiParser {

  public ASTNode parse(IElementType t, PsiBuilder b) {
    parseLight(t, b);
    return b.getTreeBuilt();
  }

  public void parseLight(IElementType t, PsiBuilder b) {
    boolean r;
    b = adapt_builder_(t, b, this, null);
    Marker m = enter_section_(b, 0, _COLLAPSE_, null);
    r = parse_root_(t, b);
    exit_section_(b, 0, m, t, r, true, TRUE_CONDITION);
  }

  protected boolean parse_root_(IElementType t, PsiBuilder b) {
    return parse_root_(t, b, 0);
  }

  static boolean parse_root_(IElementType t, PsiBuilder b, int l) {
    return xas99File(b, l + 1);
  }

  /* ********************************************************** */
  // opGA OP_SEP opGA
  public static boolean args_I(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_I")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_I, "<args i>");
    r = opGA(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opGA(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // expr
  public static boolean args_II(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_II")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_II, "<args ii>");
    r = expr(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opGA OP_SEP opRegister
  public static boolean args_III(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_III")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_III, "<args iii>");
    r = opGA(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opRegister(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opGA OP_SEP opValue
  public static boolean args_IV(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_IV")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_IV, "<args iv>");
    r = opGA(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opValue(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opGA OP_SEP opRegister
  public static boolean args_IX(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_IX")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_IX, "<args ix>");
    r = opGA(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opRegister(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opGA OP_SEP opValue
  public static boolean args_IX_X(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_IX_X")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_IX_X, "<args ix x>");
    r = opGA(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opValue(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opRegister OP_SEP (opValue | REGISTER0)
  public static boolean args_V(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_V")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_V, "<args v>");
    r = opRegister(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && args_V_2(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  // opValue | REGISTER0
  private static boolean args_V_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_V_2")) return false;
    boolean r;
    r = opValue(b, l + 1);
    if (!r) r = consumeToken(b, REGISTER0);
    return r;
  }

  /* ********************************************************** */
  // opGA
  public static boolean args_VI(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_VI")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_VI, "<args vi>");
    r = opGA(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opRegister OP_SEP opValue
  public static boolean args_VIII(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_VIII")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_VIII, "<args viii>");
    r = opRegister(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opValue(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opValue
  public static boolean args_VIII_I(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_VIII_I")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_VIII_I, "<args viii i>");
    r = opValue(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opRegister
  public static boolean args_VIII_R(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_VIII_R")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_VIII_R, "<args viii r>");
    r = opRegister(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // args_I
  public static boolean args_adv_I(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_adv_I")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_ADV_I, "<args adv i>");
    r = args_I(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // args_IV
  public static boolean args_adv_IV(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_adv_IV")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_ADV_IV, "<args adv iv>");
    r = args_IV(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opGA OP_SEP (opGA | opValue)
  public static boolean args_adv_Ia(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_adv_Ia")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_ADV_IA, "<args adv ia>");
    r = opGA(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && args_adv_Ia_2(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  // opGA | opValue
  private static boolean args_adv_Ia_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_adv_Ia_2")) return false;
    boolean r;
    r = opGA(b, l + 1);
    if (!r) r = opValue(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // args_VI
  public static boolean args_adv_VI(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_adv_VI")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_ADV_VI, "<args adv vi>");
    r = args_VI(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // args_VIII
  public static boolean args_adv_VIII(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_adv_VIII")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_ADV_VIII, "<args adv viii>");
    r = args_VIII(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opFilename
  public static boolean args_dir_C(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_C")) return false;
    if (!nextTokenIs(b, OP_FQUOTE)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = opFilename(b, l + 1);
    exit_section_(b, m, ARGS_DIR_C, r);
    return r;
  }

  /* ********************************************************** */
  // expr
  public static boolean args_dir_E(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_E")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_E, "<args dir e>");
    r = expr(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // expr?
  public static boolean args_dir_EO(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_EO")) return false;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_EO, "<args dir eo>");
    expr(b, l + 1);
    exit_section_(b, l, m, true, false, null);
    return true;
  }

  /* ********************************************************** */
  // expr (OP_SEP expr)*
  public static boolean args_dir_ES(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_ES")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_ES, "<args dir es>");
    r = expr(b, l + 1);
    r = r && args_dir_ES_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_SEP expr)*
  private static boolean args_dir_ES_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_ES_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!args_dir_ES_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "args_dir_ES_1", c)) break;
    }
    return true;
  }

  // OP_SEP expr
  private static boolean args_dir_ES_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_ES_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_SEP);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // opFloat
  public static boolean args_dir_F(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_F")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_F, "<args dir f>");
    r = opFloat(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // (opLabel (OP_SEP opLabel)*)?
  public static boolean args_dir_L(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_L")) return false;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_L, "<args dir l>");
    args_dir_L_0(b, l + 1);
    exit_section_(b, l, m, true, false, null);
    return true;
  }

  // opLabel (OP_SEP opLabel)*
  private static boolean args_dir_L_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_L_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = opLabel(b, l + 1);
    r = r && args_dir_L_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_SEP opLabel)*
  private static boolean args_dir_L_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_L_0_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!args_dir_L_0_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "args_dir_L_0_1", c)) break;
    }
    return true;
  }

  // OP_SEP opLabel
  private static boolean args_dir_L_0_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_L_0_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_SEP);
    r = r && opLabel(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // labeldef (OP_SEP labeldef)*
  public static boolean args_dir_R(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_R")) return false;
    if (!nextTokenIs(b, IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = labeldef(b, l + 1);
    r = r && args_dir_R_1(b, l + 1);
    exit_section_(b, m, ARGS_DIR_R, r);
    return r;
  }

  // (OP_SEP labeldef)*
  private static boolean args_dir_R_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_R_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!args_dir_R_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "args_dir_R_1", c)) break;
    }
    return true;
  }

  // OP_SEP labeldef
  private static boolean args_dir_R_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_R_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_SEP);
    r = r && labeldef(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // opText
  public static boolean args_dir_S(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_S")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_S, "<args dir s>");
    r = opText(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opText (OP_SEP opText)*
  public static boolean args_dir_T(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_T")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_T, "<args dir t>");
    r = opText(b, l + 1);
    r = r && args_dir_T_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_SEP opText)*
  private static boolean args_dir_T_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_T_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!args_dir_T_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "args_dir_T_1", c)) break;
    }
    return true;
  }

  // OP_SEP opText
  private static boolean args_dir_T_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_T_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_SEP);
    r = r && opText(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // opAddress | INT | (OP_QUOTE TEXT? OP_QUOTE) | MOD_LEN opLabel
  static boolean atom(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "atom")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<value>");
    r = opAddress(b, l + 1);
    if (!r) r = consumeToken(b, INT);
    if (!r) r = atom_2(b, l + 1);
    if (!r) r = atom_3(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_QUOTE TEXT? OP_QUOTE
  private static boolean atom_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "atom_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_QUOTE);
    r = r && atom_2_1(b, l + 1);
    r = r && consumeToken(b, OP_QUOTE);
    exit_section_(b, m, null, r);
    return r;
  }

  // TEXT?
  private static boolean atom_2_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "atom_2_1")) return false;
    consumeToken(b, TEXT);
    return true;
  }

  // MOD_LEN opLabel
  private static boolean atom_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "atom_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, MOD_LEN);
    r = r && opLabel(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // DIR_L args_dir_L |
  //     DIR_E args_dir_E |
  //     DIR_EO args_dir_EO |
  //     DIR_ES args_dir_ES |
  //     DIR_T args_dir_T |
  //     DIR_S args_dir_S |
  //     DIR_C args_dir_C |
  //     DIR_O |
  //     DIR_X |
  //     DIR_F args_dir_F |
  //     DIR_R args_dir_R
  public static boolean directive(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, DIRECTIVE, "<directive>");
    r = directive_0(b, l + 1);
    if (!r) r = directive_1(b, l + 1);
    if (!r) r = directive_2(b, l + 1);
    if (!r) r = directive_3(b, l + 1);
    if (!r) r = directive_4(b, l + 1);
    if (!r) r = directive_5(b, l + 1);
    if (!r) r = directive_6(b, l + 1);
    if (!r) r = consumeToken(b, DIR_O);
    if (!r) r = consumeToken(b, DIR_X);
    if (!r) r = directive_9(b, l + 1);
    if (!r) r = directive_10(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // DIR_L args_dir_L
  private static boolean directive_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_L);
    r = r && args_dir_L(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_E args_dir_E
  private static boolean directive_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_E);
    r = r && args_dir_E(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_EO args_dir_EO
  private static boolean directive_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_EO);
    r = r && args_dir_EO(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_ES args_dir_ES
  private static boolean directive_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_ES);
    r = r && args_dir_ES(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_T args_dir_T
  private static boolean directive_4(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_4")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_T);
    r = r && args_dir_T(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_S args_dir_S
  private static boolean directive_5(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_5")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_S);
    r = r && args_dir_S(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_C args_dir_C
  private static boolean directive_6(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_6")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_C);
    r = r && args_dir_C(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_F args_dir_F
  private static boolean directive_9(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_9")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_F);
    r = r && args_dir_F(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_R args_dir_R
  private static boolean directive_10(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_10")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_R);
    r = r && args_dir_R(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // COMMENT
  public static boolean dummy(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "dummy")) return false;
    if (!nextTokenIs(b, COMMENT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, COMMENT);
    exit_section_(b, m, DUMMY, r);
    return r;
  }

  /* ********************************************************** */
  // (OP_PLUS | OP_MINUS | OP_NOT) expr |
  //     term (xop expr)*
  static boolean expr(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "expr")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<expression>");
    r = expr_0(b, l + 1);
    if (!r) r = expr_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_PLUS | OP_MINUS | OP_NOT) expr
  private static boolean expr_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "expr_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = expr_0_0(b, l + 1);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_PLUS | OP_MINUS | OP_NOT
  private static boolean expr_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "expr_0_0")) return false;
    boolean r;
    r = consumeToken(b, OP_PLUS);
    if (!r) r = consumeToken(b, OP_MINUS);
    if (!r) r = consumeToken(b, OP_NOT);
    return r;
  }

  // term (xop expr)*
  private static boolean expr_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "expr_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = term(b, l + 1);
    r = r && expr_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (xop expr)*
  private static boolean expr_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "expr_1_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!expr_1_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "expr_1_1", c)) break;
    }
    return true;
  }

  // xop expr
  private static boolean expr_1_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "expr_1_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = xop(b, l + 1);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // INSTR_I args_I |
  //     INSTR_II args_II |
  //     INSTR_III args_III |
  //     INSTR_IV args_IV |
  //     INSTR_V args_V |
  //     INSTR_VI args_VI |
  //     INSTR_VII |
  //     INSTR_VIII args_VIII |
  //     INSTR_VIII_I args_VIII_I |
  //     INSTR_VIII_R args_VIII_R |
  //     INSTR_IX args_IX |
  //     INSTR_IX_X args_IX_X |
  //     INSTR_O |
  //     INSTR_9995_VI args_VI |
  //     INSTR_9995_VIII args_VIII_R |
  //     INSTR_99000_I args_adv_I |
  //     INSTR_99000_IV args_adv_IV |
  //     INSTR_99000_VI args_adv_VI |
  //     INSTR_99000_VIII args_adv_VIII |
  //     INSTR_F18A_IA args_adv_Ia |
  //     INSTR_F18A_VI args_adv_VI |
  //     INSTR_F18A_O
  public static boolean instruction(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, INSTRUCTION, "<instruction>");
    r = instruction_0(b, l + 1);
    if (!r) r = instruction_1(b, l + 1);
    if (!r) r = instruction_2(b, l + 1);
    if (!r) r = instruction_3(b, l + 1);
    if (!r) r = instruction_4(b, l + 1);
    if (!r) r = instruction_5(b, l + 1);
    if (!r) r = consumeToken(b, INSTR_VII);
    if (!r) r = instruction_7(b, l + 1);
    if (!r) r = instruction_8(b, l + 1);
    if (!r) r = instruction_9(b, l + 1);
    if (!r) r = instruction_10(b, l + 1);
    if (!r) r = instruction_11(b, l + 1);
    if (!r) r = consumeToken(b, INSTR_O);
    if (!r) r = instruction_13(b, l + 1);
    if (!r) r = instruction_14(b, l + 1);
    if (!r) r = instruction_15(b, l + 1);
    if (!r) r = instruction_16(b, l + 1);
    if (!r) r = instruction_17(b, l + 1);
    if (!r) r = instruction_18(b, l + 1);
    if (!r) r = instruction_19(b, l + 1);
    if (!r) r = instruction_20(b, l + 1);
    if (!r) r = consumeToken(b, INSTR_F18A_O);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // INSTR_I args_I
  private static boolean instruction_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_I);
    r = r && args_I(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_II args_II
  private static boolean instruction_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_II);
    r = r && args_II(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_III args_III
  private static boolean instruction_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_III);
    r = r && args_III(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_IV args_IV
  private static boolean instruction_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_IV);
    r = r && args_IV(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_V args_V
  private static boolean instruction_4(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_4")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_V);
    r = r && args_V(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_VI args_VI
  private static boolean instruction_5(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_5")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_VI);
    r = r && args_VI(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_VIII args_VIII
  private static boolean instruction_7(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_7")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_VIII);
    r = r && args_VIII(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_VIII_I args_VIII_I
  private static boolean instruction_8(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_8")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_VIII_I);
    r = r && args_VIII_I(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_VIII_R args_VIII_R
  private static boolean instruction_9(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_9")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_VIII_R);
    r = r && args_VIII_R(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_IX args_IX
  private static boolean instruction_10(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_10")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_IX);
    r = r && args_IX(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_IX_X args_IX_X
  private static boolean instruction_11(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_11")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_IX_X);
    r = r && args_IX_X(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_9995_VI args_VI
  private static boolean instruction_13(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_13")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_9995_VI);
    r = r && args_VI(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_9995_VIII args_VIII_R
  private static boolean instruction_14(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_14")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_9995_VIII);
    r = r && args_VIII_R(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_99000_I args_adv_I
  private static boolean instruction_15(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_15")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_99000_I);
    r = r && args_adv_I(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_99000_IV args_adv_IV
  private static boolean instruction_16(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_16")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_99000_IV);
    r = r && args_adv_IV(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_99000_VI args_adv_VI
  private static boolean instruction_17(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_17")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_99000_VI);
    r = r && args_adv_VI(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_99000_VIII args_adv_VIII
  private static boolean instruction_18(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_18")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_99000_VIII);
    r = r && args_adv_VIII(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F18A_IA args_adv_Ia
  private static boolean instruction_19(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_19")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F18A_IA);
    r = r && args_adv_Ia(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F18A_VI args_adv_VI
  private static boolean instruction_20(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_20")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F18A_VI);
    r = r && args_adv_VI(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // labeldef OP_COLON?
  static boolean label(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "label")) return false;
    if (!nextTokenIs(b, IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = labeldef(b, l + 1);
    r = r && label_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_COLON?
  private static boolean label_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "label_1")) return false;
    consumeToken(b, OP_COLON);
    return true;
  }

  /* ********************************************************** */
  // IDENT
  public static boolean labeldef(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "labeldef")) return false;
    if (!nextTokenIs(b, IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, IDENT);
    exit_section_(b, m, LABELDEF, r);
    return r;
  }

  /* ********************************************************** */
  // linecomment | label? statement? pragma?
  static boolean line(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = linecomment(b, l + 1);
    if (!r) r = line_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // label? statement? pragma?
  private static boolean line_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = line_1_0(b, l + 1);
    r = r && line_1_1(b, l + 1);
    r = r && line_1_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // label?
  private static boolean line_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line_1_0")) return false;
    label(b, l + 1);
    return true;
  }

  // statement?
  private static boolean line_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line_1_1")) return false;
    statement(b, l + 1);
    return true;
  }

  // pragma?
  private static boolean line_1_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line_1_2")) return false;
    pragma(b, l + 1);
    return true;
  }

  /* ********************************************************** */
  // LCOMMENT
  public static boolean linecomment(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "linecomment")) return false;
    if (!nextTokenIs(b, LCOMMENT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, LCOMMENT);
    exit_section_(b, m, LINECOMMENT, r);
    return r;
  }

  /* ********************************************************** */
  // MOD_XBANK? opLabel | OP_LC | LOCAL | PP_PARAM
  static boolean opAddress(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opAddress")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<address value>");
    r = opAddress_0(b, l + 1);
    if (!r) r = consumeToken(b, OP_LC);
    if (!r) r = consumeToken(b, LOCAL);
    if (!r) r = consumeToken(b, PP_PARAM);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // MOD_XBANK? opLabel
  private static boolean opAddress_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opAddress_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = opAddress_0_0(b, l + 1);
    r = r && opLabel(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // MOD_XBANK?
  private static boolean opAddress_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opAddress_0_0")) return false;
    consumeToken(b, MOD_XBANK);
    return true;
  }

  /* ********************************************************** */
  // OP_FQUOTE FNAME OP_FQUOTE
  public static boolean opFilename(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFilename")) return false;
    if (!nextTokenIs(b, OP_FQUOTE)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, OP_FQUOTE, FNAME, OP_FQUOTE);
    exit_section_(b, m, OP_FILENAME, r);
    return r;
  }

  /* ********************************************************** */
  // (OP_PLUS | OP_MINUS)? DIGIT* ("." DIGIT*)?
  public static boolean opFloat(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFloat")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, OP_FLOAT, "<op float>");
    r = opFloat_0(b, l + 1);
    r = r && opFloat_1(b, l + 1);
    r = r && opFloat_2(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_PLUS | OP_MINUS)?
  private static boolean opFloat_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFloat_0")) return false;
    opFloat_0_0(b, l + 1);
    return true;
  }

  // OP_PLUS | OP_MINUS
  private static boolean opFloat_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFloat_0_0")) return false;
    boolean r;
    r = consumeToken(b, OP_PLUS);
    if (!r) r = consumeToken(b, OP_MINUS);
    return r;
  }

  // DIGIT*
  private static boolean opFloat_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFloat_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!consumeToken(b, DIGIT)) break;
      if (!empty_element_parsed_guard_(b, "opFloat_1", c)) break;
    }
    return true;
  }

  // ("." DIGIT*)?
  private static boolean opFloat_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFloat_2")) return false;
    opFloat_2_0(b, l + 1);
    return true;
  }

  // "." DIGIT*
  private static boolean opFloat_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFloat_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, ".");
    r = r && opFloat_2_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIGIT*
  private static boolean opFloat_2_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opFloat_2_0_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!consumeToken(b, DIGIT)) break;
      if (!empty_element_parsed_guard_(b, "opFloat_2_0_1", c)) break;
    }
    return true;
  }

  /* ********************************************************** */
  // OP_AT OP_MINUS? sexpr (OP_LPAREN opRegister OP_RPAREN)? |
  //     opRegister |
  //     OP_AST opRegister OP_PLUS? |
  //     MOD_AUTO opValue
  static boolean opGA(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<general address>");
    r = opGA_0(b, l + 1);
    if (!r) r = opRegister(b, l + 1);
    if (!r) r = opGA_2(b, l + 1);
    if (!r) r = opGA_3(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_AT OP_MINUS? sexpr (OP_LPAREN opRegister OP_RPAREN)?
  private static boolean opGA_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_AT);
    r = r && opGA_0_1(b, l + 1);
    r = r && sexpr(b, l + 1);
    r = r && opGA_0_3(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_MINUS?
  private static boolean opGA_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA_0_1")) return false;
    consumeToken(b, OP_MINUS);
    return true;
  }

  // (OP_LPAREN opRegister OP_RPAREN)?
  private static boolean opGA_0_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA_0_3")) return false;
    opGA_0_3_0(b, l + 1);
    return true;
  }

  // OP_LPAREN opRegister OP_RPAREN
  private static boolean opGA_0_3_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA_0_3_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && opRegister(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_AST opRegister OP_PLUS?
  private static boolean opGA_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_AST);
    r = r && opRegister(b, l + 1);
    r = r && opGA_2_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_PLUS?
  private static boolean opGA_2_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA_2_2")) return false;
    consumeToken(b, OP_PLUS);
    return true;
  }

  // MOD_AUTO opValue
  private static boolean opGA_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGA_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, MOD_AUTO);
    r = r && opValue(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // IDENT | PP_PARAM
  public static boolean opLabel(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opLabel")) return false;
    if (!nextTokenIs(b, "<label>", IDENT, PP_PARAM)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, OP_LABEL, "<label>");
    r = consumeToken(b, IDENT);
    if (!r) r = consumeToken(b, PP_PARAM);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // REGISTER | REGISTER0 | INT | PP_PARAM | opLabel
  public static boolean opRegister(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opRegister")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, OP_REGISTER, "<register>");
    r = consumeToken(b, REGISTER);
    if (!r) r = consumeToken(b, REGISTER0);
    if (!r) r = consumeToken(b, INT);
    if (!r) r = consumeToken(b, PP_PARAM);
    if (!r) r = opLabel(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // OP_MINUS? (OP_QUOTE TEXT? OP_QUOTE | INT | PP_PARAM)
  public static boolean opText(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opText")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, OP_TEXT, "<text>");
    r = opText_0(b, l + 1);
    r = r && opText_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_MINUS?
  private static boolean opText_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opText_0")) return false;
    consumeToken(b, OP_MINUS);
    return true;
  }

  // OP_QUOTE TEXT? OP_QUOTE | INT | PP_PARAM
  private static boolean opText_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opText_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = opText_1_0(b, l + 1);
    if (!r) r = consumeToken(b, INT);
    if (!r) r = consumeToken(b, PP_PARAM);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_QUOTE TEXT? OP_QUOTE
  private static boolean opText_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opText_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_QUOTE);
    r = r && opText_1_0_1(b, l + 1);
    r = r && consumeToken(b, OP_QUOTE);
    exit_section_(b, m, null, r);
    return r;
  }

  // TEXT?
  private static boolean opText_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opText_1_0_1")) return false;
    consumeToken(b, TEXT);
    return true;
  }

  /* ********************************************************** */
  // expr
  static boolean opValue(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opValue")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<value>");
    r = expr(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // PG_START pragmaClause (PG_SEP pragmaClause)*
  public static boolean pragma(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "pragma")) return false;
    if (!nextTokenIs(b, PG_START)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, PG_START);
    r = r && pragmaClause(b, l + 1);
    r = r && pragma_2(b, l + 1);
    exit_section_(b, m, PRAGMA, r);
    return r;
  }

  // (PG_SEP pragmaClause)*
  private static boolean pragma_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "pragma_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!pragma_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "pragma_2", c)) break;
    }
    return true;
  }

  // PG_SEP pragmaClause
  private static boolean pragma_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "pragma_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, PG_SEP);
    r = r && pragmaClause(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // PG_TERM PG_EQ PG_TERM | PG_CYC+
  static boolean pragmaClause(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "pragmaClause")) return false;
    if (!nextTokenIs(b, "", PG_CYC, PG_TERM)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = parseTokens(b, 0, PG_TERM, PG_EQ, PG_TERM);
    if (!r) r = pragmaClause_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // PG_CYC+
  private static boolean pragmaClause_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "pragmaClause_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, PG_CYC);
    while (r) {
      int c = current_position_(b);
      if (!consumeToken(b, PG_CYC)) break;
      if (!empty_element_parsed_guard_(b, "pragmaClause_1", c)) break;
    }
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // PREP (PP_ARG | PP_SEP)*
  public static boolean preprocessor(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "preprocessor")) return false;
    if (!nextTokenIs(b, PREP)) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, PREPROCESSOR, null);
    r = consumeToken(b, PREP);
    p = r; // pin = 1
    r = r && preprocessor_1(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  // (PP_ARG | PP_SEP)*
  private static boolean preprocessor_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "preprocessor_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!preprocessor_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "preprocessor_1", c)) break;
    }
    return true;
  }

  // PP_ARG | PP_SEP
  private static boolean preprocessor_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "preprocessor_1_0")) return false;
    boolean r;
    r = consumeToken(b, PP_ARG);
    if (!r) r = consumeToken(b, PP_SEP);
    return r;
  }

  /* ********************************************************** */
  // (OP_PLUS | OP_MINUS | OP_NOT) sexpr |
  //     atom (xop sexpr)*
  static boolean sexpr(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<simple expressions>");
    r = sexpr_0(b, l + 1);
    if (!r) r = sexpr_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_PLUS | OP_MINUS | OP_NOT) sexpr
  private static boolean sexpr_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = sexpr_0_0(b, l + 1);
    r = r && sexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_PLUS | OP_MINUS | OP_NOT
  private static boolean sexpr_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr_0_0")) return false;
    boolean r;
    r = consumeToken(b, OP_PLUS);
    if (!r) r = consumeToken(b, OP_MINUS);
    if (!r) r = consumeToken(b, OP_NOT);
    return r;
  }

  // atom (xop sexpr)*
  private static boolean sexpr_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = atom(b, l + 1);
    r = r && sexpr_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (xop sexpr)*
  private static boolean sexpr_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr_1_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!sexpr_1_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "sexpr_1_1", c)) break;
    }
    return true;
  }

  // xop sexpr
  private static boolean sexpr_1_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr_1_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = xop(b, l + 1);
    r = r && sexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // directive | instruction | preprocessor | unknown_mnem
  static boolean statement(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_);
    r = directive(b, l + 1);
    if (!r) r = instruction(b, l + 1);
    if (!r) r = preprocessor(b, l + 1);
    if (!r) r = unknown_mnem(b, l + 1);
    exit_section_(b, l, m, r, false, Xas99Parser::statement_recover);
    return r;
  }

  /* ********************************************************** */
  // !CRLF
  static boolean statement_recover(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_recover")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NOT_);
    r = !consumeToken(b, CRLF);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // OP_LPAREN expr OP_RPAREN |
  //     atom
  static boolean term(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "term")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<term>");
    r = term_0(b, l + 1);
    if (!r) r = atom(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_LPAREN expr OP_RPAREN
  private static boolean term_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "term_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && expr(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // UNKNOWN
  public static boolean unknown_mnem(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "unknown_mnem")) return false;
    if (!nextTokenIs(b, UNKNOWN)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, UNKNOWN);
    exit_section_(b, m, UNKNOWN_MNEM, r);
    return r;
  }

  /* ********************************************************** */
  // (line CRLF)*
  static boolean xas99File(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xas99File")) return false;
    while (true) {
      int c = current_position_(b);
      if (!xas99File_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "xas99File", c)) break;
    }
    return true;
  }

  // line CRLF
  private static boolean xas99File_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xas99File_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = line(b, l + 1);
    r = r && consumeToken(b, CRLF);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // OP_PLUS | OP_MINUS | OP_AST | OP_MISC
  static boolean xop(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xop")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<operator>");
    r = consumeToken(b, OP_PLUS);
    if (!r) r = consumeToken(b, OP_MINUS);
    if (!r) r = consumeToken(b, OP_AST);
    if (!r) r = consumeToken(b, OP_MISC);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

}
