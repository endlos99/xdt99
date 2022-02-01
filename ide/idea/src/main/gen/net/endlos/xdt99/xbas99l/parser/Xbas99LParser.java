// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.parser;

import com.intellij.lang.PsiBuilder;
import com.intellij.lang.PsiBuilder.Marker;
import static net.endlos.xdt99.xbas99l.psi.Xbas99LTypes.*;
import static com.intellij.lang.parser.GeneratedParserUtilBase.*;
import com.intellij.psi.tree.IElementType;
import com.intellij.lang.ASTNode;
import com.intellij.psi.tree.TokenSet;
import com.intellij.lang.PsiParser;
import com.intellij.lang.LightPsiParser;

@SuppressWarnings({"SimplifiableIfStatement", "UnusedAssignment"})
public class Xbas99LParser implements PsiParser, LightPsiParser {

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
    return xbas99File(b, l + 1);
  }

  /* ********************************************************** */
  // W_AT OP_LPAREN nexpr OP_COMMA nexpr OP_RPAREN |
  //     W_VALIDATE OP_LPAREN a_validate (OP_COMMA a_validate)* OP_RPAREN |
  //     W_BEEP |
  //     W_ERASE W_ALL |
  //     W_SIZE OP_LPAREN nexpr OP_RPAREN
  static boolean a_accept(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_accept")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_accept_0(b, l + 1);
    if (!r) r = a_accept_1(b, l + 1);
    if (!r) r = consumeToken(b, W_BEEP);
    if (!r) r = parseTokens(b, 0, W_ERASE, W_ALL);
    if (!r) r = a_accept_4(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_AT OP_LPAREN nexpr OP_COMMA nexpr OP_RPAREN
  private static boolean a_accept_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_accept_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_AT, OP_LPAREN);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, OP_COMMA);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_VALIDATE OP_LPAREN a_validate (OP_COMMA a_validate)* OP_RPAREN
  private static boolean a_accept_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_accept_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_VALIDATE, OP_LPAREN);
    r = r && a_validate(b, l + 1);
    r = r && a_accept_1_3(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA a_validate)*
  private static boolean a_accept_1_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_accept_1_3")) return false;
    while (true) {
      int c = current_position_(b);
      if (!a_accept_1_3_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "a_accept_1_3", c)) break;
    }
    return true;
  }

  // OP_COMMA a_validate
  private static boolean a_accept_1_3_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_accept_1_3_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && a_validate(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_SIZE OP_LPAREN nexpr OP_RPAREN
  private static boolean a_accept_4(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_accept_4")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_SIZE, OP_LPAREN);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // OP_HASH? nexpr | sexpr
  static boolean a_call(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_call")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_call_0(b, l + 1);
    if (!r) r = sexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_HASH? nexpr
  private static boolean a_call_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_call_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_call_0_0(b, l + 1);
    r = r && nexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_HASH?
  private static boolean a_call_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_call_0_0")) return false;
    consumeToken(b, OP_HASH);
    return true;
  }

  /* ********************************************************** */
  // var_w
  static boolean a_dim(PsiBuilder b, int l) {
    return var_w(b, l + 1);
  }

  /* ********************************************************** */
  // W_AT OP_LPAREN nexpr OP_COMMA nexpr OP_RPAREN |
  //     W_BEEP |
  //     W_ERASE W_ALL |
  //     W_SIZE OP_LPAREN nexpr OP_RPAREN
  static boolean a_display(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_display")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_display_0(b, l + 1);
    if (!r) r = consumeToken(b, W_BEEP);
    if (!r) r = parseTokens(b, 0, W_ERASE, W_ALL);
    if (!r) r = a_display_3(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_AT OP_LPAREN nexpr OP_COMMA nexpr OP_RPAREN
  private static boolean a_display_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_display_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_AT, OP_LPAREN);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, OP_COMMA);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_SIZE OP_LPAREN nexpr OP_RPAREN
  private static boolean a_display_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_display_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_SIZE, OP_LPAREN);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_RELATIVE | W_SEQUENTIAL |
  //     W_DISPLAY | W_INTERNAL |
  //     W_INPUT | W_OUTPUT | W_APPEND | W_UPDATE |
  //     W_FIXED nexpr? | W_VARIABLE nexpr? |
  //     W_PERMANENT
  static boolean a_open(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_open")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_RELATIVE);
    if (!r) r = consumeToken(b, W_SEQUENTIAL);
    if (!r) r = consumeToken(b, W_DISPLAY);
    if (!r) r = consumeToken(b, W_INTERNAL);
    if (!r) r = consumeToken(b, W_INPUT);
    if (!r) r = consumeToken(b, W_OUTPUT);
    if (!r) r = consumeToken(b, W_APPEND);
    if (!r) r = consumeToken(b, W_UPDATE);
    if (!r) r = a_open_8(b, l + 1);
    if (!r) r = a_open_9(b, l + 1);
    if (!r) r = consumeToken(b, W_PERMANENT);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_FIXED nexpr?
  private static boolean a_open_8(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_open_8")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_FIXED);
    r = r && a_open_8_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // nexpr?
  private static boolean a_open_8_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_open_8_1")) return false;
    nexpr(b, l + 1);
    return true;
  }

  // W_VARIABLE nexpr?
  private static boolean a_open_9(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_open_9")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_VARIABLE);
    r = r && a_open_9_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // nexpr?
  private static boolean a_open_9_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_open_9_1")) return false;
    nexpr(b, l + 1);
    return true;
  }

  /* ********************************************************** */
  // (expr | OP_COMMA | OP_SEMI | OP_COLON)+
  static boolean a_print(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_print")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_print_0(b, l + 1);
    while (r) {
      int c = current_position_(b);
      if (!a_print_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "a_print", c)) break;
    }
    exit_section_(b, m, null, r);
    return r;
  }

  // expr | OP_COMMA | OP_SEMI | OP_COLON
  private static boolean a_print_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_print_0")) return false;
    boolean r;
    r = expr(b, l + 1);
    if (!r) r = consumeToken(b, OP_COMMA);
    if (!r) r = consumeToken(b, OP_SEMI);
    if (!r) r = consumeToken(b, OP_COLON);
    return r;
  }

  /* ********************************************************** */
  // labelref | slist
  public static boolean a_then_else(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_then_else")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, A_THEN_ELSE, "<a then else>");
    r = labelref(b, l + 1);
    if (!r) r = slist(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // W_USING (sexpr | labelref)?
  static boolean a_using(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_using")) return false;
    if (!nextTokenIs(b, W_USING)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_USING);
    r = r && a_using_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (sexpr | labelref)?
  private static boolean a_using_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_using_1")) return false;
    a_using_1_0(b, l + 1);
    return true;
  }

  // sexpr | labelref
  private static boolean a_using_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_using_1_0")) return false;
    boolean r;
    r = sexpr(b, l + 1);
    if (!r) r = labelref(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // W_UALPHA | W_DIGIT | W_NUMERIC | sexpr
  static boolean a_validate(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "a_validate")) return false;
    boolean r;
    r = consumeToken(b, W_UALPHA);
    if (!r) r = consumeToken(b, W_DIGIT);
    if (!r) r = consumeToken(b, W_NUMERIC);
    if (!r) r = sexpr(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // W_BANG
  public static boolean bang_comment(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "bang_comment")) return false;
    if (!nextTokenIs(b, W_BANG)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_BANG);
    exit_section_(b, m, BANG_COMMENT, r);
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
  // nexpr | sexpr
  static boolean expr(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "expr")) return false;
    boolean r;
    r = nexpr(b, l + 1);
    if (!r) r = sexpr(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // W_FUN_C
  public static boolean f_const(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "f_const")) return false;
    if (!nextTokenIs(b, "<numerical constant>", W_FUN_C)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, F_CONST, "<numerical constant>");
    r = consumeToken(b, W_FUN_C);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // W_FUN_N OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN
  public static boolean f_num(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "f_num")) return false;
    if (!nextTokenIs(b, "<numerical function>", W_FUN_N)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, F_NUM, "<numerical function>");
    r = consumeTokens(b, 0, W_FUN_N, OP_LPAREN);
    r = r && expr(b, l + 1);
    r = r && f_num_3(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_COMMA expr)*
  private static boolean f_num_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "f_num_3")) return false;
    while (true) {
      int c = current_position_(b);
      if (!f_num_3_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "f_num_3", c)) break;
    }
    return true;
  }

  // OP_COMMA expr
  private static boolean f_num_3_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "f_num_3_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_FUN_S OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN
  public static boolean f_str(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "f_str")) return false;
    if (!nextTokenIs(b, "<string function>", W_FUN_S)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, F_STR, "<string function>");
    r = consumeTokens(b, 0, W_FUN_S, OP_LPAREN);
    r = r && expr(b, l + 1);
    r = r && f_str_3(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_COMMA expr)*
  private static boolean f_str_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "f_str_3")) return false;
    while (true) {
      int c = current_position_(b);
      if (!f_str_3_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "f_str_3", c)) break;
    }
    return true;
  }

  // OP_COMMA expr
  private static boolean f_str_3_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "f_str_3_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // LIDENT OP_COLON
  public static boolean labeldef(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "labeldef")) return false;
    if (!nextTokenIs(b, "<label>", LIDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, LABELDEF, "<label>");
    r = consumeTokens(b, 0, LIDENT, OP_COLON);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // IDENT
  public static boolean labelref(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "labelref")) return false;
    if (!nextTokenIs(b, "<label>", IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, LABELREF, "<label>");
    r = consumeToken(b, IDENT);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // slist | labeldef
  static boolean line(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_);
    r = slist(b, l + 1);
    if (!r) r = labeldef(b, l + 1);
    exit_section_(b, l, m, r, false, Xbas99LParser::line_recover);
    return r;
  }

  /* ********************************************************** */
  // !CRLF
  static boolean line_recover(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "line_recover")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NOT_);
    r = !consumeToken(b, CRLF);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // (OP_LPAREN nexprn OP_RPAREN) |
  //     f_num | f_const | nvar_r | nvalue
  static boolean natom(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "natom")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<numerical term>");
    r = natom_0(b, l + 1);
    if (!r) r = f_num(b, l + 1);
    if (!r) r = f_const(b, l + 1);
    if (!r) r = nvar_r(b, l + 1);
    if (!r) r = nvalue(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_LPAREN nexprn OP_RPAREN
  private static boolean natom_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "natom_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && nexprn(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // (satom rop satom) |    // string comparison yields -1, 0, +1
  //     nexprn
  static boolean nexpr(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexpr")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = nexpr_0(b, l + 1);
    if (!r) r = nexprn(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // satom rop satom
  private static boolean nexpr_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexpr_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = satom(b, l + 1);
    r = r && rop(b, l + 1);
    r = r && satom(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // (W_NOT nexprn) |
  //     (OP_MINUS nexprn) |
  //     ((natom | ssimple) (nop nexprn)*)
  public static boolean nexprn(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexprn")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _COLLAPSE_, NEXPRN, "<numerical expression>");
    r = nexprn_0(b, l + 1);
    if (!r) r = nexprn_1(b, l + 1);
    if (!r) r = nexprn_2(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // W_NOT nexprn
  private static boolean nexprn_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexprn_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_NOT);
    r = r && nexprn(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_MINUS nexprn
  private static boolean nexprn_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexprn_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_MINUS);
    r = r && nexprn(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (natom | ssimple) (nop nexprn)*
  private static boolean nexprn_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexprn_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = nexprn_2_0(b, l + 1);
    r = r && nexprn_2_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // natom | ssimple
  private static boolean nexprn_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexprn_2_0")) return false;
    boolean r;
    r = natom(b, l + 1);
    if (!r) r = ssimple(b, l + 1);
    return r;
  }

  // (nop nexprn)*
  private static boolean nexprn_2_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexprn_2_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!nexprn_2_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "nexprn_2_1", c)) break;
    }
    return true;
  }

  // nop nexprn
  private static boolean nexprn_2_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nexprn_2_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = nop(b, l + 1);
    r = r && nexprn(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // OP_MUL | OP_DIV | OP_PLUS | OP_MINUS | OP_EXP |
  //     rop |
  //     W_AND | W_OR | W_XOR
  static boolean nop(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nop")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<numerical operator>");
    r = consumeToken(b, OP_MUL);
    if (!r) r = consumeToken(b, OP_DIV);
    if (!r) r = consumeToken(b, OP_PLUS);
    if (!r) r = consumeToken(b, OP_MINUS);
    if (!r) r = consumeToken(b, OP_EXP);
    if (!r) r = rop(b, l + 1);
    if (!r) r = consumeToken(b, W_AND);
    if (!r) r = consumeToken(b, W_OR);
    if (!r) r = consumeToken(b, W_XOR);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // NUMBER | FLOAT
  static boolean nvalue(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvalue")) return false;
    if (!nextTokenIs(b, "<numerical value>", FLOAT, NUMBER)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<numerical value>");
    r = consumeToken(b, NUMBER);
    if (!r) r = consumeToken(b, FLOAT);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // IDENT (OP_LPAREN var_w (OP_COMMA var_w)* OP_RPAREN)?
  public static boolean nvar_f(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_f")) return false;
    if (!nextTokenIs(b, "<numerical function>", IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, NVAR_F, "<numerical function>");
    r = consumeToken(b, IDENT);
    r = r && nvar_f_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_LPAREN var_w (OP_COMMA var_w)* OP_RPAREN)?
  private static boolean nvar_f_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_f_1")) return false;
    nvar_f_1_0(b, l + 1);
    return true;
  }

  // OP_LPAREN var_w (OP_COMMA var_w)* OP_RPAREN
  private static boolean nvar_f_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_f_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && var_w(b, l + 1);
    r = r && nvar_f_1_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA var_w)*
  private static boolean nvar_f_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_f_1_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!nvar_f_1_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "nvar_f_1_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA var_w
  private static boolean nvar_f_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_f_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // IDENT (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  public static boolean nvar_r(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_r")) return false;
    if (!nextTokenIs(b, "<numerical variable>", IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, NVAR_R, "<numerical variable>");
    r = consumeToken(b, IDENT);
    r = r && nvar_r_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  private static boolean nvar_r_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_r_1")) return false;
    nvar_r_1_0(b, l + 1);
    return true;
  }

  // OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN
  private static boolean nvar_r_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_r_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && expr(b, l + 1);
    r = r && nvar_r_1_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA expr)*
  private static boolean nvar_r_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_r_1_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!nvar_r_1_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "nvar_r_1_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA expr
  private static boolean nvar_r_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_r_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // IDENT (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  public static boolean nvar_w(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_w")) return false;
    if (!nextTokenIs(b, "<numerical variable>", IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, NVAR_W, "<numerical variable>");
    r = consumeToken(b, IDENT);
    r = r && nvar_w_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  private static boolean nvar_w_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_w_1")) return false;
    nvar_w_1_0(b, l + 1);
    return true;
  }

  // OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN
  private static boolean nvar_w_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_w_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && expr(b, l + 1);
    r = r && nvar_w_1_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA expr)*
  private static boolean nvar_w_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_w_1_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!nvar_w_1_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "nvar_w_1_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA expr
  private static boolean nvar_w_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "nvar_w_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // (IDENT | SIDENT) (OP_LPAREN OP_COMMA* OP_RPAREN)?
  public static boolean param(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "param")) return false;
    if (!nextTokenIs(b, "<function parameter>", IDENT, SIDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, PARAM, "<function parameter>");
    r = param_0(b, l + 1);
    r = r && param_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // IDENT | SIDENT
  private static boolean param_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "param_0")) return false;
    boolean r;
    r = consumeToken(b, IDENT);
    if (!r) r = consumeToken(b, SIDENT);
    return r;
  }

  // (OP_LPAREN OP_COMMA* OP_RPAREN)?
  private static boolean param_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "param_1")) return false;
    param_1_0(b, l + 1);
    return true;
  }

  // OP_LPAREN OP_COMMA* OP_RPAREN
  private static boolean param_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "param_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && param_1_0_1(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_COMMA*
  private static boolean param_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "param_1_0_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!consumeToken(b, OP_COMMA)) break;
      if (!empty_element_parsed_guard_(b, "param_1_0_1", c)) break;
    }
    return true;
  }

  /* ********************************************************** */
  // OP_EQ | OP_LT OP_GT | OP_LT OP_EQ? | OP_GT OP_EQ?
  static boolean rop(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "rop")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<relational operator>");
    r = consumeToken(b, OP_EQ);
    if (!r) r = parseTokens(b, 0, OP_LT, OP_GT);
    if (!r) r = rop_2(b, l + 1);
    if (!r) r = rop_3(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_LT OP_EQ?
  private static boolean rop_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "rop_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LT);
    r = r && rop_2_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_EQ?
  private static boolean rop_2_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "rop_2_1")) return false;
    consumeToken(b, OP_EQ);
    return true;
  }

  // OP_GT OP_EQ?
  private static boolean rop_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "rop_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_GT);
    r = r && rop_3_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_EQ?
  private static boolean rop_3_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "rop_3_1")) return false;
    consumeToken(b, OP_EQ);
    return true;
  }

  /* ********************************************************** */
  // W_ACCEPT (a_accept+ OP_COLON)? var_w
  public static boolean s_accept(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_accept")) return false;
    if (!nextTokenIs(b, W_ACCEPT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_ACCEPT);
    r = r && s_accept_1(b, l + 1);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, S_ACCEPT, r);
    return r;
  }

  // (a_accept+ OP_COLON)?
  private static boolean s_accept_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_accept_1")) return false;
    s_accept_1_0(b, l + 1);
    return true;
  }

  // a_accept+ OP_COLON
  private static boolean s_accept_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_accept_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_accept_1_0_0(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    exit_section_(b, m, null, r);
    return r;
  }

  // a_accept+
  private static boolean s_accept_1_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_accept_1_0_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_accept(b, l + 1);
    while (r) {
      int c = current_position_(b);
      if (!a_accept(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_accept_1_0_0", c)) break;
    }
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_BREAK (labelref (OP_COMMA labelref)*)? |
  //     W_UNBREAK (labelref (OP_COMMA labelref)*)?
  public static boolean s_break(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break")) return false;
    if (!nextTokenIs(b, "<s break>", W_BREAK, W_UNBREAK)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, S_BREAK, "<s break>");
    r = s_break_0(b, l + 1);
    if (!r) r = s_break_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // W_BREAK (labelref (OP_COMMA labelref)*)?
  private static boolean s_break_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_BREAK);
    r = r && s_break_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (labelref (OP_COMMA labelref)*)?
  private static boolean s_break_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_0_1")) return false;
    s_break_0_1_0(b, l + 1);
    return true;
  }

  // labelref (OP_COMMA labelref)*
  private static boolean s_break_0_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_0_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = labelref(b, l + 1);
    r = r && s_break_0_1_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA labelref)*
  private static boolean s_break_0_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_0_1_0_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_break_0_1_0_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_break_0_1_0_1", c)) break;
    }
    return true;
  }

  // OP_COMMA labelref
  private static boolean s_break_0_1_0_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_0_1_0_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && labelref(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_UNBREAK (labelref (OP_COMMA labelref)*)?
  private static boolean s_break_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_UNBREAK);
    r = r && s_break_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (labelref (OP_COMMA labelref)*)?
  private static boolean s_break_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_1_1")) return false;
    s_break_1_1_0(b, l + 1);
    return true;
  }

  // labelref (OP_COMMA labelref)*
  private static boolean s_break_1_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_1_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = labelref(b, l + 1);
    r = r && s_break_1_1_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA labelref)*
  private static boolean s_break_1_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_1_1_0_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_break_1_1_0_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_break_1_1_0_1", c)) break;
    }
    return true;
  }

  // OP_COMMA labelref
  private static boolean s_break_1_1_0_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_break_1_1_0_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && labelref(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_CALL subprog (OP_LPAREN (W_ALL | a_call) (OP_COMMA a_call)* OP_RPAREN)?
  public static boolean s_call(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_call")) return false;
    if (!nextTokenIs(b, W_CALL)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_CALL);
    r = r && subprog(b, l + 1);
    r = r && s_call_2(b, l + 1);
    exit_section_(b, m, S_CALL, r);
    return r;
  }

  // (OP_LPAREN (W_ALL | a_call) (OP_COMMA a_call)* OP_RPAREN)?
  private static boolean s_call_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_call_2")) return false;
    s_call_2_0(b, l + 1);
    return true;
  }

  // OP_LPAREN (W_ALL | a_call) (OP_COMMA a_call)* OP_RPAREN
  private static boolean s_call_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_call_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && s_call_2_0_1(b, l + 1);
    r = r && s_call_2_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_ALL | a_call
  private static boolean s_call_2_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_call_2_0_1")) return false;
    boolean r;
    r = consumeToken(b, W_ALL);
    if (!r) r = a_call(b, l + 1);
    return r;
  }

  // (OP_COMMA a_call)*
  private static boolean s_call_2_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_call_2_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_call_2_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_call_2_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA a_call
  private static boolean s_call_2_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_call_2_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && a_call(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_CLOSE OP_HASH nexpr (OP_COLON W_DELETE)?
  public static boolean s_close(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_close")) return false;
    if (!nextTokenIs(b, W_CLOSE)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_CLOSE, OP_HASH);
    r = r && nexpr(b, l + 1);
    r = r && s_close_3(b, l + 1);
    exit_section_(b, m, S_CLOSE, r);
    return r;
  }

  // (OP_COLON W_DELETE)?
  private static boolean s_close_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_close_3")) return false;
    s_close_3_0(b, l + 1);
    return true;
  }

  // OP_COLON W_DELETE
  private static boolean s_close_3_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_close_3_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, OP_COLON, W_DELETE);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_DATA A_DATA? (OP_COMMA A_DATA?)*
  public static boolean s_data(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_data")) return false;
    if (!nextTokenIs(b, W_DATA)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_DATA);
    r = r && s_data_1(b, l + 1);
    r = r && s_data_2(b, l + 1);
    exit_section_(b, m, S_DATA, r);
    return r;
  }

  // A_DATA?
  private static boolean s_data_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_data_1")) return false;
    consumeToken(b, A_DATA);
    return true;
  }

  // (OP_COMMA A_DATA?)*
  private static boolean s_data_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_data_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_data_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_data_2", c)) break;
    }
    return true;
  }

  // OP_COMMA A_DATA?
  private static boolean s_data_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_data_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && s_data_2_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // A_DATA?
  private static boolean s_data_2_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_data_2_0_1")) return false;
    consumeToken(b, A_DATA);
    return true;
  }

  /* ********************************************************** */
  // W_DEF ((nvar_f OP_EQ nexpr) |  // arguments covered by *var_* rules, includes constant case
  //            (svar_f OP_EQ sexpr))
  public static boolean s_def(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_def")) return false;
    if (!nextTokenIs(b, W_DEF)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_DEF);
    r = r && s_def_1(b, l + 1);
    exit_section_(b, m, S_DEF, r);
    return r;
  }

  // (nvar_f OP_EQ nexpr) |  // arguments covered by *var_* rules, includes constant case
  //            (svar_f OP_EQ sexpr)
  private static boolean s_def_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_def_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_def_1_0(b, l + 1);
    if (!r) r = s_def_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // nvar_f OP_EQ nexpr
  private static boolean s_def_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_def_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = nvar_f(b, l + 1);
    r = r && consumeToken(b, OP_EQ);
    r = r && nexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // svar_f OP_EQ sexpr
  private static boolean s_def_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_def_1_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = svar_f(b, l + 1);
    r = r && consumeToken(b, OP_EQ);
    r = r && sexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_DELETE sexpr
  public static boolean s_delete(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_delete")) return false;
    if (!nextTokenIs(b, W_DELETE)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_DELETE);
    r = r && sexpr(b, l + 1);
    exit_section_(b, m, S_DELETE, r);
    return r;
  }

  /* ********************************************************** */
  // W_DIM a_dim (OP_COMMA a_dim)*
  public static boolean s_dim(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_dim")) return false;
    if (!nextTokenIs(b, W_DIM)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_DIM);
    r = r && a_dim(b, l + 1);
    r = r && s_dim_2(b, l + 1);
    exit_section_(b, m, S_DIM, r);
    return r;
  }

  // (OP_COMMA a_dim)*
  private static boolean s_dim_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_dim_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_dim_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_dim_2", c)) break;
    }
    return true;
  }

  // OP_COMMA a_dim
  private static boolean s_dim_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_dim_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && a_dim(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_DISPLAY
  //     (a_display+ (OP_COLON a_using)? (OP_COLON a_print)? |
  //      a_using (OP_COLON a_print)? |
  //      a_print)?
  public static boolean s_display(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display")) return false;
    if (!nextTokenIs(b, W_DISPLAY)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_DISPLAY);
    r = r && s_display_1(b, l + 1);
    exit_section_(b, m, S_DISPLAY, r);
    return r;
  }

  // (a_display+ (OP_COLON a_using)? (OP_COLON a_print)? |
  //      a_using (OP_COLON a_print)? |
  //      a_print)?
  private static boolean s_display_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1")) return false;
    s_display_1_0(b, l + 1);
    return true;
  }

  // a_display+ (OP_COLON a_using)? (OP_COLON a_print)? |
  //      a_using (OP_COLON a_print)? |
  //      a_print
  private static boolean s_display_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_display_1_0_0(b, l + 1);
    if (!r) r = s_display_1_0_1(b, l + 1);
    if (!r) r = a_print(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // a_display+ (OP_COLON a_using)? (OP_COLON a_print)?
  private static boolean s_display_1_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_display_1_0_0_0(b, l + 1);
    r = r && s_display_1_0_0_1(b, l + 1);
    r = r && s_display_1_0_0_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // a_display+
  private static boolean s_display_1_0_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_0_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_display(b, l + 1);
    while (r) {
      int c = current_position_(b);
      if (!a_display(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_display_1_0_0_0", c)) break;
    }
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COLON a_using)?
  private static boolean s_display_1_0_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_0_1")) return false;
    s_display_1_0_0_1_0(b, l + 1);
    return true;
  }

  // OP_COLON a_using
  private static boolean s_display_1_0_0_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_0_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COLON);
    r = r && a_using(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COLON a_print)?
  private static boolean s_display_1_0_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_0_2")) return false;
    s_display_1_0_0_2_0(b, l + 1);
    return true;
  }

  // OP_COLON a_print
  private static boolean s_display_1_0_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COLON);
    r = r && a_print(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // a_using (OP_COLON a_print)?
  private static boolean s_display_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_using(b, l + 1);
    r = r && s_display_1_0_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COLON a_print)?
  private static boolean s_display_1_0_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_1_1")) return false;
    s_display_1_0_1_1_0(b, l + 1);
    return true;
  }

  // OP_COLON a_print
  private static boolean s_display_1_0_1_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_display_1_0_1_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COLON);
    r = r && a_print(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_END
  public static boolean s_end(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_end")) return false;
    if (!nextTokenIs(b, W_END)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_END);
    exit_section_(b, m, S_END, r);
    return r;
  }

  /* ********************************************************** */
  // W_FOR nvar_w OP_EQ nexpr W_TO nexpr (W_STEP nexpr)?
  public static boolean s_for(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_for")) return false;
    if (!nextTokenIs(b, W_FOR)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_FOR);
    r = r && nvar_w(b, l + 1);
    r = r && consumeToken(b, OP_EQ);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, W_TO);
    r = r && nexpr(b, l + 1);
    r = r && s_for_6(b, l + 1);
    exit_section_(b, m, S_FOR, r);
    return r;
  }

  // (W_STEP nexpr)?
  private static boolean s_for_6(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_for_6")) return false;
    s_for_6_0(b, l + 1);
    return true;
  }

  // W_STEP nexpr
  private static boolean s_for_6_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_for_6_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_STEP);
    r = r && nexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // (W_GOTO | W_GO W_TO | W_GOSUB | W_GO W_SUB) labelref
  public static boolean s_go(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_go")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, S_GO, "<s go>");
    r = s_go_0(b, l + 1);
    r = r && labelref(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // W_GOTO | W_GO W_TO | W_GOSUB | W_GO W_SUB
  private static boolean s_go_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_go_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_GOTO);
    if (!r) r = parseTokens(b, 0, W_GO, W_TO);
    if (!r) r = consumeToken(b, W_GOSUB);
    if (!r) r = parseTokens(b, 0, W_GO, W_SUB);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_IF nexpr W_THEN a_then_else (W_ELSE a_then_else)?
  public static boolean s_if(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_if")) return false;
    if (!nextTokenIs(b, W_IF)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_IF);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, W_THEN);
    r = r && a_then_else(b, l + 1);
    r = r && s_if_4(b, l + 1);
    exit_section_(b, m, S_IF, r);
    return r;
  }

  // (W_ELSE a_then_else)?
  private static boolean s_if_4(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_if_4")) return false;
    s_if_4_0(b, l + 1);
    return true;
  }

  // W_ELSE a_then_else
  private static boolean s_if_4_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_if_4_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_ELSE);
    r = r && a_then_else(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_IMAGE A_IMAGE?
  public static boolean s_image(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_image")) return false;
    if (!nextTokenIs(b, W_IMAGE)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_IMAGE);
    r = r && s_image_1(b, l + 1);
    exit_section_(b, m, S_IMAGE, r);
    return r;
  }

  // A_IMAGE?
  private static boolean s_image_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_image_1")) return false;
    consumeToken(b, A_IMAGE);
    return true;
  }

  /* ********************************************************** */
  // W_INPUT
  //     ((sexpr OP_COLON)? var_w (OP_COMMA var_w)* |
  //       OP_HASH nvalue (W_REC nexpr)? OP_COLON var_w (OP_COMMA var_w)* OP_COMMA?)
  public static boolean s_input(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input")) return false;
    if (!nextTokenIs(b, W_INPUT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_INPUT);
    r = r && s_input_1(b, l + 1);
    exit_section_(b, m, S_INPUT, r);
    return r;
  }

  // (sexpr OP_COLON)? var_w (OP_COMMA var_w)* |
  //       OP_HASH nvalue (W_REC nexpr)? OP_COLON var_w (OP_COMMA var_w)* OP_COMMA?
  private static boolean s_input_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_input_1_0(b, l + 1);
    if (!r) r = s_input_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (sexpr OP_COLON)? var_w (OP_COMMA var_w)*
  private static boolean s_input_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_input_1_0_0(b, l + 1);
    r = r && var_w(b, l + 1);
    r = r && s_input_1_0_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (sexpr OP_COLON)?
  private static boolean s_input_1_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_0_0")) return false;
    s_input_1_0_0_0(b, l + 1);
    return true;
  }

  // sexpr OP_COLON
  private static boolean s_input_1_0_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_0_0_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = sexpr(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA var_w)*
  private static boolean s_input_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_input_1_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_input_1_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA var_w
  private static boolean s_input_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_HASH nvalue (W_REC nexpr)? OP_COLON var_w (OP_COMMA var_w)* OP_COMMA?
  private static boolean s_input_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_HASH);
    r = r && nvalue(b, l + 1);
    r = r && s_input_1_1_2(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    r = r && var_w(b, l + 1);
    r = r && s_input_1_1_5(b, l + 1);
    r = r && s_input_1_1_6(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (W_REC nexpr)?
  private static boolean s_input_1_1_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_1_2")) return false;
    s_input_1_1_2_0(b, l + 1);
    return true;
  }

  // W_REC nexpr
  private static boolean s_input_1_1_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_1_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_REC);
    r = r && nexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA var_w)*
  private static boolean s_input_1_1_5(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_1_5")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_input_1_1_5_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_input_1_1_5", c)) break;
    }
    return true;
  }

  // OP_COMMA var_w
  private static boolean s_input_1_1_5_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_1_5_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_COMMA?
  private static boolean s_input_1_1_6(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_input_1_1_6")) return false;
    consumeToken(b, OP_COMMA);
    return true;
  }

  /* ********************************************************** */
  // W_LET?
  //     (nvar_w (OP_COMMA nvar_w)* (OP_EQ nexpr)? |
  //      svar_w (OP_COMMA svar_w)* (OP_EQ sexpr)?)
  public static boolean s_let(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, S_LET, "<s let>");
    r = s_let_0(b, l + 1);
    r = r && s_let_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // W_LET?
  private static boolean s_let_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_0")) return false;
    consumeToken(b, W_LET);
    return true;
  }

  // nvar_w (OP_COMMA nvar_w)* (OP_EQ nexpr)? |
  //      svar_w (OP_COMMA svar_w)* (OP_EQ sexpr)?
  private static boolean s_let_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_let_1_0(b, l + 1);
    if (!r) r = s_let_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // nvar_w (OP_COMMA nvar_w)* (OP_EQ nexpr)?
  private static boolean s_let_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = nvar_w(b, l + 1);
    r = r && s_let_1_0_1(b, l + 1);
    r = r && s_let_1_0_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA nvar_w)*
  private static boolean s_let_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_0_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_let_1_0_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_let_1_0_1", c)) break;
    }
    return true;
  }

  // OP_COMMA nvar_w
  private static boolean s_let_1_0_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_0_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && nvar_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_EQ nexpr)?
  private static boolean s_let_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_0_2")) return false;
    s_let_1_0_2_0(b, l + 1);
    return true;
  }

  // OP_EQ nexpr
  private static boolean s_let_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_EQ);
    r = r && nexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // svar_w (OP_COMMA svar_w)* (OP_EQ sexpr)?
  private static boolean s_let_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = svar_w(b, l + 1);
    r = r && s_let_1_1_1(b, l + 1);
    r = r && s_let_1_1_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA svar_w)*
  private static boolean s_let_1_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_1_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_let_1_1_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_let_1_1_1", c)) break;
    }
    return true;
  }

  // OP_COMMA svar_w
  private static boolean s_let_1_1_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_1_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && svar_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_EQ sexpr)?
  private static boolean s_let_1_1_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_1_2")) return false;
    s_let_1_1_2_0(b, l + 1);
    return true;
  }

  // OP_EQ sexpr
  private static boolean s_let_1_1_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_let_1_1_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_EQ);
    r = r && sexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_LINPUT
  //     ((sexpr OP_COLON)? var_w |
  //      OP_HASH nvalue (W_REC nexpr)? OP_COLON var_w)
  public static boolean s_linput(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput")) return false;
    if (!nextTokenIs(b, W_LINPUT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_LINPUT);
    r = r && s_linput_1(b, l + 1);
    exit_section_(b, m, S_LINPUT, r);
    return r;
  }

  // (sexpr OP_COLON)? var_w |
  //      OP_HASH nvalue (W_REC nexpr)? OP_COLON var_w
  private static boolean s_linput_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_linput_1_0(b, l + 1);
    if (!r) r = s_linput_1_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (sexpr OP_COLON)? var_w
  private static boolean s_linput_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_linput_1_0_0(b, l + 1);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (sexpr OP_COLON)?
  private static boolean s_linput_1_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput_1_0_0")) return false;
    s_linput_1_0_0_0(b, l + 1);
    return true;
  }

  // sexpr OP_COLON
  private static boolean s_linput_1_0_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput_1_0_0_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = sexpr(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_HASH nvalue (W_REC nexpr)? OP_COLON var_w
  private static boolean s_linput_1_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput_1_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_HASH);
    r = r && nvalue(b, l + 1);
    r = r && s_linput_1_1_2(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // (W_REC nexpr)?
  private static boolean s_linput_1_1_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput_1_1_2")) return false;
    s_linput_1_1_2_0(b, l + 1);
    return true;
  }

  // W_REC nexpr
  private static boolean s_linput_1_1_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_linput_1_1_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_REC);
    r = r && nexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_NEXT nvar_r
  public static boolean s_next(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_next")) return false;
    if (!nextTokenIs(b, W_NEXT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_NEXT);
    r = r && nvar_r(b, l + 1);
    exit_section_(b, m, S_NEXT, r);
    return r;
  }

  /* ********************************************************** */
  // W_ON W_BREAK (W_STOP | W_NEXT) |
  //     W_ON W_ERROR (W_STOP | labelref) |
  //     W_ON W_WARNING (W_PRINT | W_STOP | W_NEXT)
  public static boolean s_on_cond(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_cond")) return false;
    if (!nextTokenIs(b, W_ON)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_on_cond_0(b, l + 1);
    if (!r) r = s_on_cond_1(b, l + 1);
    if (!r) r = s_on_cond_2(b, l + 1);
    exit_section_(b, m, S_ON_COND, r);
    return r;
  }

  // W_ON W_BREAK (W_STOP | W_NEXT)
  private static boolean s_on_cond_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_cond_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_ON, W_BREAK);
    r = r && s_on_cond_0_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_STOP | W_NEXT
  private static boolean s_on_cond_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_cond_0_2")) return false;
    boolean r;
    r = consumeToken(b, W_STOP);
    if (!r) r = consumeToken(b, W_NEXT);
    return r;
  }

  // W_ON W_ERROR (W_STOP | labelref)
  private static boolean s_on_cond_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_cond_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_ON, W_ERROR);
    r = r && s_on_cond_1_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_STOP | labelref
  private static boolean s_on_cond_1_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_cond_1_2")) return false;
    boolean r;
    r = consumeToken(b, W_STOP);
    if (!r) r = labelref(b, l + 1);
    return r;
  }

  // W_ON W_WARNING (W_PRINT | W_STOP | W_NEXT)
  private static boolean s_on_cond_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_cond_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_ON, W_WARNING);
    r = r && s_on_cond_2_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // W_PRINT | W_STOP | W_NEXT
  private static boolean s_on_cond_2_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_cond_2_2")) return false;
    boolean r;
    r = consumeToken(b, W_PRINT);
    if (!r) r = consumeToken(b, W_STOP);
    if (!r) r = consumeToken(b, W_NEXT);
    return r;
  }

  /* ********************************************************** */
  // W_ON nexpr (W_GOTO | W_GO W_TO | W_GOSUB | W_GO W_SUB) labelref (OP_COMMA labelref)*
  public static boolean s_on_go(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_go")) return false;
    if (!nextTokenIs(b, W_ON)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_ON);
    r = r && nexpr(b, l + 1);
    r = r && s_on_go_2(b, l + 1);
    r = r && labelref(b, l + 1);
    r = r && s_on_go_4(b, l + 1);
    exit_section_(b, m, S_ON_GO, r);
    return r;
  }

  // W_GOTO | W_GO W_TO | W_GOSUB | W_GO W_SUB
  private static boolean s_on_go_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_go_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_GOTO);
    if (!r) r = parseTokens(b, 0, W_GO, W_TO);
    if (!r) r = consumeToken(b, W_GOSUB);
    if (!r) r = parseTokens(b, 0, W_GO, W_SUB);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA labelref)*
  private static boolean s_on_go_4(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_go_4")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_on_go_4_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_on_go_4", c)) break;
    }
    return true;
  }

  // OP_COMMA labelref
  private static boolean s_on_go_4_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_on_go_4_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && labelref(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_OPEN OP_HASH nexpr OP_COLON sexpr (OP_COMMA a_open)*
  public static boolean s_open(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_open")) return false;
    if (!nextTokenIs(b, W_OPEN)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_OPEN, OP_HASH);
    r = r && nexpr(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    r = r && sexpr(b, l + 1);
    r = r && s_open_5(b, l + 1);
    exit_section_(b, m, S_OPEN, r);
    return r;
  }

  // (OP_COMMA a_open)*
  private static boolean s_open_5(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_open_5")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_open_5_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_open_5", c)) break;
    }
    return true;
  }

  // OP_COMMA a_open
  private static boolean s_open_5_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_open_5_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && a_open(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_OPTION W_BASE nvalue
  public static boolean s_option(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_option")) return false;
    if (!nextTokenIs(b, W_OPTION)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, W_OPTION, W_BASE);
    r = r && nvalue(b, l + 1);
    exit_section_(b, m, S_OPTION, r);
    return r;
  }

  /* ********************************************************** */
  // W_PRINT
  //     (OP_HASH nexpr (OP_COMMA W_REC nexpr (OP_COMMA a_using))? OP_COLON |
  //      a_using OP_COLON)?
  //      a_print?
  public static boolean s_print(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print")) return false;
    if (!nextTokenIs(b, W_PRINT)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_PRINT);
    r = r && s_print_1(b, l + 1);
    r = r && s_print_2(b, l + 1);
    exit_section_(b, m, S_PRINT, r);
    return r;
  }

  // (OP_HASH nexpr (OP_COMMA W_REC nexpr (OP_COMMA a_using))? OP_COLON |
  //      a_using OP_COLON)?
  private static boolean s_print_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_1")) return false;
    s_print_1_0(b, l + 1);
    return true;
  }

  // OP_HASH nexpr (OP_COMMA W_REC nexpr (OP_COMMA a_using))? OP_COLON |
  //      a_using OP_COLON
  private static boolean s_print_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = s_print_1_0_0(b, l + 1);
    if (!r) r = s_print_1_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_HASH nexpr (OP_COMMA W_REC nexpr (OP_COMMA a_using))? OP_COLON
  private static boolean s_print_1_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_1_0_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_HASH);
    r = r && nexpr(b, l + 1);
    r = r && s_print_1_0_0_2(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA W_REC nexpr (OP_COMMA a_using))?
  private static boolean s_print_1_0_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_1_0_0_2")) return false;
    s_print_1_0_0_2_0(b, l + 1);
    return true;
  }

  // OP_COMMA W_REC nexpr (OP_COMMA a_using)
  private static boolean s_print_1_0_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_1_0_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, OP_COMMA, W_REC);
    r = r && nexpr(b, l + 1);
    r = r && s_print_1_0_0_2_0_3(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_COMMA a_using
  private static boolean s_print_1_0_0_2_0_3(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_1_0_0_2_0_3")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && a_using(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // a_using OP_COLON
  private static boolean s_print_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_1_0_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = a_using(b, l + 1);
    r = r && consumeToken(b, OP_COLON);
    exit_section_(b, m, null, r);
    return r;
  }

  // a_print?
  private static boolean s_print_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_print_2")) return false;
    a_print(b, l + 1);
    return true;
  }

  /* ********************************************************** */
  // W_RANDOMIZE nexpr?
  public static boolean s_randomize(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_randomize")) return false;
    if (!nextTokenIs(b, W_RANDOMIZE)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_RANDOMIZE);
    r = r && s_randomize_1(b, l + 1);
    exit_section_(b, m, S_RANDOMIZE, r);
    return r;
  }

  // nexpr?
  private static boolean s_randomize_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_randomize_1")) return false;
    nexpr(b, l + 1);
    return true;
  }

  /* ********************************************************** */
  // W_READ var_w (OP_COMMA var_w)*
  public static boolean s_read(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_read")) return false;
    if (!nextTokenIs(b, W_READ)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_READ);
    r = r && var_w(b, l + 1);
    r = r && s_read_2(b, l + 1);
    exit_section_(b, m, S_READ, r);
    return r;
  }

  // (OP_COMMA var_w)*
  private static boolean s_read_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_read_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_read_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_read_2", c)) break;
    }
    return true;
  }

  // OP_COMMA var_w
  private static boolean s_read_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_read_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_REM
  public static boolean s_rem(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_rem")) return false;
    if (!nextTokenIs(b, W_REM)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_REM);
    exit_section_(b, m, S_REM, r);
    return r;
  }

  /* ********************************************************** */
  // W_RESTORE (labelref | OP_HASH nexpr (OP_COMMA W_REC nexpr))?
  public static boolean s_restore(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_restore")) return false;
    if (!nextTokenIs(b, W_RESTORE)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_RESTORE);
    r = r && s_restore_1(b, l + 1);
    exit_section_(b, m, S_RESTORE, r);
    return r;
  }

  // (labelref | OP_HASH nexpr (OP_COMMA W_REC nexpr))?
  private static boolean s_restore_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_restore_1")) return false;
    s_restore_1_0(b, l + 1);
    return true;
  }

  // labelref | OP_HASH nexpr (OP_COMMA W_REC nexpr)
  private static boolean s_restore_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_restore_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = labelref(b, l + 1);
    if (!r) r = s_restore_1_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_HASH nexpr (OP_COMMA W_REC nexpr)
  private static boolean s_restore_1_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_restore_1_0_1")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_HASH);
    r = r && nexpr(b, l + 1);
    r = r && s_restore_1_0_1_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // OP_COMMA W_REC nexpr
  private static boolean s_restore_1_0_1_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_restore_1_0_1_2")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeTokens(b, 0, OP_COMMA, W_REC);
    r = r && nexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_RETURN (W_NEXT | labelref)?
  public static boolean s_return(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_return")) return false;
    if (!nextTokenIs(b, W_RETURN)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_RETURN);
    r = r && s_return_1(b, l + 1);
    exit_section_(b, m, S_RETURN, r);
    return r;
  }

  // (W_NEXT | labelref)?
  private static boolean s_return_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_return_1")) return false;
    s_return_1_0(b, l + 1);
    return true;
  }

  // W_NEXT | labelref
  private static boolean s_return_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_return_1_0")) return false;
    boolean r;
    r = consumeToken(b, W_NEXT);
    if (!r) r = labelref(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // W_RUN (sexpr | labelref)?
  public static boolean s_run(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_run")) return false;
    if (!nextTokenIs(b, W_RUN)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_RUN);
    r = r && s_run_1(b, l + 1);
    exit_section_(b, m, S_RUN, r);
    return r;
  }

  // (sexpr | labelref)?
  private static boolean s_run_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_run_1")) return false;
    s_run_1_0(b, l + 1);
    return true;
  }

  // sexpr | labelref
  private static boolean s_run_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_run_1_0")) return false;
    boolean r;
    r = sexpr(b, l + 1);
    if (!r) r = labelref(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // W_STOP
  public static boolean s_stop(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_stop")) return false;
    if (!nextTokenIs(b, W_STOP)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_STOP);
    exit_section_(b, m, S_STOP, r);
    return r;
  }

  /* ********************************************************** */
  // W_SUB subprog (OP_LPAREN param (OP_COMMA param)* OP_RPAREN)?
  public static boolean s_sub(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_sub")) return false;
    if (!nextTokenIs(b, W_SUB)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, W_SUB);
    r = r && subprog(b, l + 1);
    r = r && s_sub_2(b, l + 1);
    exit_section_(b, m, S_SUB, r);
    return r;
  }

  // (OP_LPAREN param (OP_COMMA param)* OP_RPAREN)?
  private static boolean s_sub_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_sub_2")) return false;
    s_sub_2_0(b, l + 1);
    return true;
  }

  // OP_LPAREN param (OP_COMMA param)* OP_RPAREN
  private static boolean s_sub_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_sub_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && param(b, l + 1);
    r = r && s_sub_2_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA param)*
  private static boolean s_sub_2_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_sub_2_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!s_sub_2_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "s_sub_2_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA param
  private static boolean s_sub_2_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_sub_2_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && param(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // W_SUBEND |
  //     W_SUBEXIT
  public static boolean s_subend(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_subend")) return false;
    if (!nextTokenIs(b, "<s subend>", W_SUBEND, W_SUBEXIT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, S_SUBEND, "<s subend>");
    r = consumeToken(b, W_SUBEND);
    if (!r) r = consumeToken(b, W_SUBEXIT);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // W_TRACE |
  //     W_UNTRACE
  public static boolean s_trace(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "s_trace")) return false;
    if (!nextTokenIs(b, "<s trace>", W_TRACE, W_UNTRACE)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, S_TRACE, "<s trace>");
    r = consumeToken(b, W_TRACE);
    if (!r) r = consumeToken(b, W_UNTRACE);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // (OP_LPAREN sexpr OP_RPAREN) |
  //     f_str | svar_r | svalue
  static boolean satom(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "satom")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<string term>");
    r = satom_0(b, l + 1);
    if (!r) r = f_str(b, l + 1);
    if (!r) r = svar_r(b, l + 1);
    if (!r) r = svalue(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // OP_LPAREN sexpr OP_RPAREN
  private static boolean satom_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "satom_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && sexpr(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // satom (sop sexpr)*
  public static boolean sexpr(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _COLLAPSE_, SEXPR, "<string expression>");
    r = satom(b, l + 1);
    r = r && sexpr_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (sop sexpr)*
  private static boolean sexpr_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!sexpr_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "sexpr_1", c)) break;
    }
    return true;
  }

  // sop sexpr
  private static boolean sexpr_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sexpr_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = sop(b, l + 1);
    r = r && sexpr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // statement (OP_SEP statement)*
  public static boolean slist(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "slist")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, SLIST, "<statement list>");
    r = statement(b, l + 1);
    r = r && slist_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_SEP statement)*
  private static boolean slist_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "slist_1")) return false;
    while (true) {
      int c = current_position_(b);
      if (!slist_1_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "slist_1", c)) break;
    }
    return true;
  }

  // OP_SEP statement
  private static boolean slist_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "slist_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_SEP);
    r = r && statement(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // !OP_SEP
  static boolean slist_recover(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "slist_recover")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NOT_);
    r = !consumeToken(b, OP_SEP);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // OP_AMP
  static boolean sop(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "sop")) return false;
    if (!nextTokenIs(b, "<string operator>", OP_AMP)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<string operator>");
    r = consumeToken(b, OP_AMP);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // OP_LPAREN satom rop satom OP_RPAREN
  static boolean ssimple(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "ssimple")) return false;
    if (!nextTokenIs(b, OP_LPAREN)) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && satom(b, l + 1);
    r = r && rop(b, l + 1);
    r = r && satom(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // statement_xb | statement_both
  static boolean statement(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement")) return false;
    boolean r;
    r = statement_xb(b, l + 1);
    if (!r) r = statement_both(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // (s_break |  // includes unbreak
  //      s_call |
  //      s_close |
  //      s_data |
  //      s_def |
  //      s_delete |
  //      s_dim |
  //      s_display |  // TI-BASIC: similar to print, XB: AT(), SIZE, ...
  //      s_end |
  //      s_for |
  //      s_go |
  //      s_if |  // TI-BASIC: only labels, no statements
  //      s_image |
  //      s_input |
  //      s_next |
  //      s_on_go |
  //      s_open |
  //      s_option |
  //      s_print |
  //      s_randomize |
  //      s_read |
  //      s_rem |
  //      s_restore |
  //      s_return |
  //      s_stop |
  //      s_trace |  // includes untrace
  //      s_let)  // keep this as last rule
  //      bang_comment?
  public static boolean statement_both(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_both")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, STATEMENT_BOTH, "<statement both>");
    r = statement_both_0(b, l + 1);
    r = r && statement_both_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // s_break |  // includes unbreak
  //      s_call |
  //      s_close |
  //      s_data |
  //      s_def |
  //      s_delete |
  //      s_dim |
  //      s_display |  // TI-BASIC: similar to print, XB: AT(), SIZE, ...
  //      s_end |
  //      s_for |
  //      s_go |
  //      s_if |  // TI-BASIC: only labels, no statements
  //      s_image |
  //      s_input |
  //      s_next |
  //      s_on_go |
  //      s_open |
  //      s_option |
  //      s_print |
  //      s_randomize |
  //      s_read |
  //      s_rem |
  //      s_restore |
  //      s_return |
  //      s_stop |
  //      s_trace |  // includes untrace
  //      s_let
  private static boolean statement_both_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_both_0")) return false;
    boolean r;
    r = s_break(b, l + 1);
    if (!r) r = s_call(b, l + 1);
    if (!r) r = s_close(b, l + 1);
    if (!r) r = s_data(b, l + 1);
    if (!r) r = s_def(b, l + 1);
    if (!r) r = s_delete(b, l + 1);
    if (!r) r = s_dim(b, l + 1);
    if (!r) r = s_display(b, l + 1);
    if (!r) r = s_end(b, l + 1);
    if (!r) r = s_for(b, l + 1);
    if (!r) r = s_go(b, l + 1);
    if (!r) r = s_if(b, l + 1);
    if (!r) r = s_image(b, l + 1);
    if (!r) r = s_input(b, l + 1);
    if (!r) r = s_next(b, l + 1);
    if (!r) r = s_on_go(b, l + 1);
    if (!r) r = s_open(b, l + 1);
    if (!r) r = s_option(b, l + 1);
    if (!r) r = s_print(b, l + 1);
    if (!r) r = s_randomize(b, l + 1);
    if (!r) r = s_read(b, l + 1);
    if (!r) r = s_rem(b, l + 1);
    if (!r) r = s_restore(b, l + 1);
    if (!r) r = s_return(b, l + 1);
    if (!r) r = s_stop(b, l + 1);
    if (!r) r = s_trace(b, l + 1);
    if (!r) r = s_let(b, l + 1);
    return r;
  }

  // bang_comment?
  private static boolean statement_both_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_both_1")) return false;
    bang_comment(b, l + 1);
    return true;
  }

  /* ********************************************************** */
  // (s_accept |  // xb only
  //      s_linput |  // XB only
  //      s_on_cond |  // XB only
  //      s_run |  // xb only
  //      s_sub |  // xb only
  //      s_subend)  // xb only
  //      bang_comment? |
  //     bang_comment
  public static boolean statement_xb(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_xb")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, STATEMENT_XB, "<statement xb>");
    r = statement_xb_0(b, l + 1);
    if (!r) r = bang_comment(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (s_accept |  // xb only
  //      s_linput |  // XB only
  //      s_on_cond |  // XB only
  //      s_run |  // xb only
  //      s_sub |  // xb only
  //      s_subend)  // xb only
  //      bang_comment?
  private static boolean statement_xb_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_xb_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = statement_xb_0_0(b, l + 1);
    r = r && statement_xb_0_1(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // s_accept |  // xb only
  //      s_linput |  // XB only
  //      s_on_cond |  // XB only
  //      s_run |  // xb only
  //      s_sub |  // xb only
  //      s_subend
  private static boolean statement_xb_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_xb_0_0")) return false;
    boolean r;
    r = s_accept(b, l + 1);
    if (!r) r = s_linput(b, l + 1);
    if (!r) r = s_on_cond(b, l + 1);
    if (!r) r = s_run(b, l + 1);
    if (!r) r = s_sub(b, l + 1);
    if (!r) r = s_subend(b, l + 1);
    return r;
  }

  // bang_comment?
  private static boolean statement_xb_0_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "statement_xb_0_1")) return false;
    bang_comment(b, l + 1);
    return true;
  }

  /* ********************************************************** */
  // IDENT
  public static boolean subprog(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "subprog")) return false;
    if (!nextTokenIs(b, "<subprogram name>", IDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, SUBPROG, "<subprogram name>");
    r = consumeToken(b, IDENT);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  /* ********************************************************** */
  // OP_QUOTE QSTRING? OP_QUOTE
  static boolean svalue(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svalue")) return false;
    if (!nextTokenIs(b, "<string literal>", OP_QUOTE)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, null, "<string literal>");
    r = consumeToken(b, OP_QUOTE);
    r = r && svalue_1(b, l + 1);
    r = r && consumeToken(b, OP_QUOTE);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // QSTRING?
  private static boolean svalue_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svalue_1")) return false;
    consumeToken(b, QSTRING);
    return true;
  }

  /* ********************************************************** */
  // SIDENT (OP_LPAREN var_w (OP_COMMA var_w)* OP_RPAREN)?
  public static boolean svar_f(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_f")) return false;
    if (!nextTokenIs(b, "<string function>", SIDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, SVAR_F, "<string function>");
    r = consumeToken(b, SIDENT);
    r = r && svar_f_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_LPAREN var_w (OP_COMMA var_w)* OP_RPAREN)?
  private static boolean svar_f_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_f_1")) return false;
    svar_f_1_0(b, l + 1);
    return true;
  }

  // OP_LPAREN var_w (OP_COMMA var_w)* OP_RPAREN
  private static boolean svar_f_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_f_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && var_w(b, l + 1);
    r = r && svar_f_1_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA var_w)*
  private static boolean svar_f_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_f_1_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!svar_f_1_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "svar_f_1_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA var_w
  private static boolean svar_f_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_f_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && var_w(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // (SIDENT | IDENT OP_STR) (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  public static boolean svar_r(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_r")) return false;
    if (!nextTokenIs(b, "<string variable>", IDENT, SIDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _COLLAPSE_, SVAR_R, "<string variable>");
    r = svar_r_0(b, l + 1);
    r = r && svar_r_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // SIDENT | IDENT OP_STR
  private static boolean svar_r_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_r_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, SIDENT);
    if (!r) r = parseTokens(b, 0, IDENT, OP_STR);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  private static boolean svar_r_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_r_1")) return false;
    svar_r_1_0(b, l + 1);
    return true;
  }

  // OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN
  private static boolean svar_r_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_r_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && expr(b, l + 1);
    r = r && svar_r_1_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA expr)*
  private static boolean svar_r_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_r_1_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!svar_r_1_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "svar_r_1_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA expr
  private static boolean svar_r_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_r_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // SIDENT (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  public static boolean svar_w(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_w")) return false;
    if (!nextTokenIs(b, "<string variable>", SIDENT)) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, SVAR_W, "<string variable>");
    r = consumeToken(b, SIDENT);
    r = r && svar_w_1(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // (OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN)?
  private static boolean svar_w_1(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_w_1")) return false;
    svar_w_1_0(b, l + 1);
    return true;
  }

  // OP_LPAREN expr (OP_COMMA expr)* OP_RPAREN
  private static boolean svar_w_1_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_w_1_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_LPAREN);
    r = r && expr(b, l + 1);
    r = r && svar_w_1_0_2(b, l + 1);
    r = r && consumeToken(b, OP_RPAREN);
    exit_section_(b, m, null, r);
    return r;
  }

  // (OP_COMMA expr)*
  private static boolean svar_w_1_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_w_1_0_2")) return false;
    while (true) {
      int c = current_position_(b);
      if (!svar_w_1_0_2_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "svar_w_1_0_2", c)) break;
    }
    return true;
  }

  // OP_COMMA expr
  private static boolean svar_w_1_0_2_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "svar_w_1_0_2_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = consumeToken(b, OP_COMMA);
    r = r && expr(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // nvar_w | svar_w
  static boolean var_w(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "var_w")) return false;
    if (!nextTokenIs(b, "", IDENT, SIDENT)) return false;
    boolean r;
    r = nvar_w(b, l + 1);
    if (!r) r = svar_w(b, l + 1);
    return r;
  }

  /* ********************************************************** */
  // (line? CRLF)*
  static boolean xbas99File(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xbas99File")) return false;
    while (true) {
      int c = current_position_(b);
      if (!xbas99File_0(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "xbas99File", c)) break;
    }
    return true;
  }

  // line? CRLF
  private static boolean xbas99File_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xbas99File_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = xbas99File_0_0(b, l + 1);
    r = r && consumeToken(b, CRLF);
    exit_section_(b, m, null, r);
    return r;
  }

  // line?
  private static boolean xbas99File_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "xbas99File_0_0")) return false;
    line(b, l + 1);
    return true;
  }

}
