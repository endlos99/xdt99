// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99r.parser;

import com.intellij.lang.PsiBuilder;
import com.intellij.lang.PsiBuilder.Marker;
import static net.endlos.xdt99.xga99r.psi.Xga99RTypes.*;
import static com.intellij.lang.parser.GeneratedParserUtilBase.*;
import com.intellij.psi.tree.IElementType;
import com.intellij.lang.ASTNode;
import com.intellij.psi.tree.TokenSet;
import com.intellij.lang.PsiParser;
import com.intellij.lang.LightPsiParser;

@SuppressWarnings({"SimplifiableIfStatement", "UnusedAssignment"})
public class Xga99RParser implements PsiParser, LightPsiParser {

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
    return xga99File(b, l + 1);
  }

  /* ********************************************************** */
  // opValue
  public static boolean args_F_I(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_F_I")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_F_I, "<args f i>");
    r = opValue(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opValue | opGs
  public static boolean args_F_II(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_F_II")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_F_II, "<args f ii>");
    r = opValue(b, l + 1);
    if (!r) r = opGs(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opValue OP_SEP opValue
  public static boolean args_F_III(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_F_III")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_F_III, "<args f iii>");
    r = opValue(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opValue(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opText
  public static boolean args_F_IV(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_F_IV")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_F_IV, "<args f iv>");
    r = opText(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opValue OP_SEP opGs
  public static boolean args_F_IX(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_F_IX")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_F_IX, "<args f ix>");
    r = opValue(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opGs(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opValue
  public static boolean args_F_V(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_F_V")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_F_V, "<args f v>");
    r = opValue(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opAddress?
  public static boolean args_F_X(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_F_X")) return false;
    Marker m = enter_section_(b, l, _NONE_, ARGS_F_X, "<args f x>");
    opAddress(b, l + 1);
    exit_section_(b, l, m, true, false, null);
    return true;
  }

  /* ********************************************************** */
  // opGs OP_SEP opGd
  public static boolean args_I(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_I")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_I, "<args i>");
    r = opGs(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && opGd(b, l + 1);
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  /* ********************************************************** */
  // opValue
  public static boolean args_II(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_II")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_II, "<args ii>");
    r = opValue(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opAddress
  public static boolean args_III(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_III")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_III, "<args iii>");
    r = opAddress(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // (opGs | opValue) OP_SEP opMs OP_SEP opMd
  public static boolean args_IX(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_IX")) return false;
    boolean r, p;
    Marker m = enter_section_(b, l, _NONE_, ARGS_IX, "<args ix>");
    r = args_IX_0(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    p = r; // pin = OP_SEP
    r = r && report_error_(b, opMs(b, l + 1));
    r = p && report_error_(b, consumeToken(b, OP_SEP)) && r;
    r = p && opMd(b, l + 1) && r;
    exit_section_(b, l, m, r, p, null);
    return r || p;
  }

  // opGs | opValue
  private static boolean args_IX_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_IX_0")) return false;
    boolean r;
    r = opGs(b, l + 1);
    if (!r) r = opValue(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // opGd
  public static boolean args_VI(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_VI")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_VI, "<args vi>");
    r = opGd(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opValue?
  public static boolean args_VII(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_VII")) return false;
    Marker m = enter_section_(b, l, _NONE_, ARGS_VII, "<args vii>");
    opValue(b, l + 1);
    exit_section_(b, l, m, true, false, null);
    return true;
  }

  /* ********************************************************** */
  // opValue OP_SEP opGs
  public static boolean args_VIII(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_VIII")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_VIII, "<args viii>");
    r = opValue(b, l + 1);
    r = r && consumeToken(b, OP_SEP);
    r = r && opGs(b, l + 1);
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
  // expr (OP_SEP expr)*
  public static boolean args_dir_N(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_N")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_N, "<args dir n>");
    r = expr(b, l + 1);
    r = r && args_dir_N_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_SEP expr)*
  private static boolean args_dir_N_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_N_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!args_dir_N_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "args_dir_N_1", c)) break;
    }
    return true;
  }

  // OP_SEP expr
  private static boolean args_dir_N_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_N_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_SEP);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // opValue
  public static boolean args_dir_S(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "args_dir_S")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, ARGS_DIR_S, "<args dir s>");
    r = opValue(b, l + 1);
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
  // opLabel | INT | OP_QUOTE TEXT? OP_QUOTE
  static boolean atom(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "atom")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<value>");
    r = opLabel(b, l + 1);
    if (!r) r = consumeToken(b, INT);
    if (!r) r = atom_2(b, l + 1);
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

  /* ********************************************************** */
  // DIR_L |
  //     DIR_S args_dir_S |
  //     DIR_M args_dir_N |
  //     DIR_T args_dir_T |
  //     DIR_C args_dir_C |
  //     DIR_F args_dir_F
  public static boolean directive(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, DIRECTIVE, "<directive>");
    r = consumeToken(b, DIR_L);
    if (!r) r = directive_1(b, l + 1);
    if (!r) r = directive_2(b, l + 1);
    if (!r) r = directive_3(b, l + 1);
    if (!r) r = directive_4(b, l + 1);
    if (!r) r = directive_5(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // DIR_S args_dir_S
  private static boolean directive_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_S);
    r = r && args_dir_S(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_M args_dir_N
  private static boolean directive_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_M);
    r = r && args_dir_N(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_T args_dir_T
  private static boolean directive_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_T);
    r = r && args_dir_T(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_C args_dir_C
  private static boolean directive_4(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_4")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_C);
    r = r && args_dir_C(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // DIR_F args_dir_F
  private static boolean directive_5(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "directive_5")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, DIR_F);
    r = r && args_dir_F(b, l + 1);
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
  //     INSTR_V |
  //     INSTR_VI args_VI |
  //     INSTR_VII args_VII |
  //     INSTR_VIII args_VIII |
  //     INSTR_IX args_IX |
  //     INSTR_X |
  //     INSTR_F_I args_F_I |
  //     INSTR_F_II args_F_II |
  //     INSTR_F_III args_F_III |
  //     INSTR_F_IV args_F_IV |
  //     INSTR_F_V args_F_V |
  //     INSTR_F_IX args_F_IX |
  //     INSTR_F_X args_F_X
  public static boolean instruction(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, INSTRUCTION, "<instruction>");
    r = instruction_0(b, l + 1);
    if (!r) r = instruction_1(b, l + 1);
    if (!r) r = instruction_2(b, l + 1);
    if (!r) r = consumeToken(b, INSTR_V);
    if (!r) r = instruction_4(b, l + 1);
    if (!r) r = instruction_5(b, l + 1);
    if (!r) r = instruction_6(b, l + 1);
    if (!r) r = instruction_7(b, l + 1);
    if (!r) r = consumeToken(b, INSTR_X);
    if (!r) r = instruction_9(b, l + 1);
    if (!r) r = instruction_10(b, l + 1);
    if (!r) r = instruction_11(b, l + 1);
    if (!r) r = instruction_12(b, l + 1);
    if (!r) r = instruction_13(b, l + 1);
    if (!r) r = instruction_14(b, l + 1);
    if (!r) r = instruction_15(b, l + 1);
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

  // INSTR_VI args_VI
  private static boolean instruction_4(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_4")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_VI);
    r = r && args_VI(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_VII args_VII
  private static boolean instruction_5(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_5")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_VII);
    r = r && args_VII(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_VIII args_VIII
  private static boolean instruction_6(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_6")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_VIII);
    r = r && args_VIII(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_IX args_IX
  private static boolean instruction_7(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_7")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_IX);
    r = r && args_IX(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F_I args_F_I
  private static boolean instruction_9(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_9")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F_I);
    r = r && args_F_I(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F_II args_F_II
  private static boolean instruction_10(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_10")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F_II);
    r = r && args_F_II(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F_III args_F_III
  private static boolean instruction_11(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_11")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F_III);
    r = r && args_F_III(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F_IV args_F_IV
  private static boolean instruction_12(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_12")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F_IV);
    r = r && args_F_IV(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F_V args_F_V
  private static boolean instruction_13(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_13")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F_V);
    r = r && args_F_V(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F_IX args_F_IX
  private static boolean instruction_14(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_14")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F_IX);
    r = r && args_F_IX(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // INSTR_F_X args_F_X
  private static boolean instruction_15(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "instruction_15")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, INSTR_F_X);
    r = r && args_F_X(b, l + 1);
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
  // linecomment | label? statement?
  static boolean line(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = linecomment(b, l + 1);
    if (!r) r = line_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // label? statement?
  private static boolean line_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = line_1_0(b, l + 1);
    r = r && line_1_1(b, l + 1);
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
  // expr
  static boolean opAddress(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opAddress")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<address value>");
    r = expr(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
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
  // (VADDR | VINDR | OP_AT | OP_AST) OP_MINUS? sexpr opIndex?
  static boolean opGd(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGd")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<general destination address>");
    r = opGd_0(b, l + 1);
    r = r && opGd_1(b, l + 1);
    r = r && sexpr(b, l + 1);
    r = r && opGd_3(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // VADDR | VINDR | OP_AT | OP_AST
  private static boolean opGd_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGd_0")) return false;
    boolean r;
    r = consumeToken(b, VADDR);
    if (!r) r = consumeToken(b, VINDR);
    if (!r) r = consumeToken(b, OP_AT);
    if (!r) r = consumeToken(b, OP_AST);
    return r;
  }

  // OP_MINUS?
  private static boolean opGd_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGd_1")) return false;
    consumeToken(b, OP_MINUS);
    return true;
  }

  // opIndex?
  private static boolean opGd_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGd_3")) return false;
    opIndex(b, l + 1);
    return true;
  }

  /* ********************************************************** */
  // opGd | opValue
  static boolean opGs(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opGs")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<general source address>");
    r = opGd(b, l + 1);
    if (!r) r = opValue(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // OP_LPAREN OP_AT? opValue OP_RPAREN
  static boolean opIndex(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opIndex")) return false;
    if (!nextTokenIs(b, "<index>", OP_LPAREN)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<index>");
    r = consumeToken(b, OP_LPAREN);
    r = r && opIndex_1(b, l + 1);
    r = r && opValue(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_AT?
  private static boolean opIndex_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opIndex_1")) return false;
    consumeToken(b, OP_AT);
    return true;
  }

  /* ********************************************************** */
  // IDENT | LOCAL | OP_LC | PP_PARAM
  public static boolean opLabel(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opLabel")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, OP_LABEL, "<label>");
    r = consumeToken(b, IDENT);
    if (!r) r = consumeToken(b, LOCAL);
    if (!r) r = consumeToken(b, OP_LC);
    if (!r) r = consumeToken(b, PP_PARAM);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // opMs | PP_PARAM
  static boolean opMd(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opMd")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<MOVE destination address>");
    r = opMs(b, l + 1);
    if (!r) r = consumeToken(b, PP_PARAM);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // (GADDR | VADDR | VINDR | OP_AT | OP_AST) OP_MINUS? sexpr opIndex?
  static boolean opMs(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opMs")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<MOVE source address>");
    r = opMs_0(b, l + 1);
    r = r && opMs_1(b, l + 1);
    r = r && sexpr(b, l + 1);
    r = r && opMs_3(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // GADDR | VADDR | VINDR | OP_AT | OP_AST
  private static boolean opMs_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opMs_0")) return false;
    boolean r;
    r = consumeToken(b, GADDR);
    if (!r) r = consumeToken(b, VADDR);
    if (!r) r = consumeToken(b, VINDR);
    if (!r) r = consumeToken(b, OP_AT);
    if (!r) r = consumeToken(b, OP_AST);
    return r;
  }

  // OP_MINUS?
  private static boolean opMs_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opMs_1")) return false;
    consumeToken(b, OP_MINUS);
    return true;
  }

  // opIndex?
  private static boolean opMs_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "opMs_3")) return false;
    opIndex(b, l + 1);
    return true;
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
    exit_section_(b, l, m, r, false, Xga99RParser::statement_recover);
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
  static boolean xga99File(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xga99File")) return false;
    while (true) {
      int c = current_position_(b);
      if (!xga99File_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "xga99File", c)) break;
    }
    return true;
  }

  // line CRLF
  private static boolean xga99File_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xga99File_0")) return false;
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
