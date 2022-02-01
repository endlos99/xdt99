package net.endlos.xdt99.xga99r;

import com.intellij.lexer.FlexAdapter;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.editor.markup.TextAttributes;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import com.intellij.ui.JBColor;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import org.jetbrains.annotations.NotNull;

import java.awt.*;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;

public class Xga99RSyntaxHighlighter extends SyntaxHighlighterBase {
    public static final TokenSet instructions = TokenSet.create(Xga99RTypes.INSTR_I, Xga99RTypes.INSTR_II,
            Xga99RTypes.INSTR_III, Xga99RTypes.INSTR_V, Xga99RTypes.INSTR_VI, Xga99RTypes.INSTR_VIII,
            Xga99RTypes.INSTR_IX);
    public static final TokenSet fmtInstructions = TokenSet.create(Xga99RTypes.INSTR_X, Xga99RTypes.INSTR_F_I,
            Xga99RTypes.INSTR_F_II, Xga99RTypes.INSTR_F_III, Xga99RTypes.INSTR_F_IV, Xga99RTypes.INSTR_F_V,
            Xga99RTypes.INSTR_F_IX, Xga99RTypes.INSTR_F_X);
    public static final TokenSet directives = TokenSet.create(Xga99RTypes.DIR_L, Xga99RTypes.DIR_S, Xga99RTypes.DIR_M,
            Xga99RTypes.DIR_T, Xga99RTypes.DIR_C, Xga99RTypes.DIR_F);
    public static final TokenSet text = TokenSet.create(Xga99RTypes.OP_QUOTE, Xga99RTypes.TEXT, Xga99RTypes.OP_FQUOTE,
            Xga99RTypes.FNAME);
    public static final TokenSet operators = TokenSet.create(Xga99RTypes.OP_AT, Xga99RTypes.OP_AST,
            Xga99RTypes.OP_PLUS, Xga99RTypes.OP_MINUS, Xga99RTypes.OP_NOT, Xga99RTypes.OP_LPAREN, Xga99RTypes.OP_RPAREN,
            Xga99RTypes.OP_MISC);
    public static final TokenSet preprocessor = TokenSet.create(Xga99RTypes.PREP);  // could add PP_ARG

public static final TextAttributesKey INSTRUCTION =
        createTextAttributesKey("XGA99_INSTR", DefaultLanguageHighlighterColors.KEYWORD);
    public static final TextAttributesKey FINSTRUCTION =
            createTextAttributesKey("XGA99_FINSTR", DefaultLanguageHighlighterColors.KEYWORD);
    public static final TextAttributesKey DIRECTIVE =
            createTextAttributesKey("XGA99_DIR", DefaultLanguageHighlighterColors.INSTANCE_FIELD);
    public static final TextAttributesKey PREPROCESSOR =
            createTextAttributesKey("XGA99_PREP", DefaultLanguageHighlighterColors.METADATA);
    public static final TextAttributesKey IDENT =
            createTextAttributesKey("XGA99_IDENT", DefaultLanguageHighlighterColors.IDENTIFIER);
    public static final TextAttributesKey VALUE =
            createTextAttributesKey("XGA99_VALUE", DefaultLanguageHighlighterColors.NUMBER);
    public static final TextAttributesKey TEXT =
            createTextAttributesKey("XGA99_TEXT", DefaultLanguageHighlighterColors.STRING);
    public static final TextAttributesKey OPERATOR =
            createTextAttributesKey("XGA99_OPER", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    public static final TextAttributesKey SEPARATOR =
            createTextAttributesKey("XGA99_SEP", DefaultLanguageHighlighterColors.COMMA);
    public static final TextAttributesKey COMMENT =
            createTextAttributesKey("XGA99_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);
    public static final TextAttributesKey LCOMMENT =
            createTextAttributesKey("XGA99_LCOMMENT", DefaultLanguageHighlighterColors.DOC_COMMENT);
    // no key for IDENT etc., keep labels normal color

    static final TextAttributesKey BAD_CHARACTER = TextAttributesKey.createTextAttributesKey("SIMPLE_BAD_CHARACTER",
            new TextAttributes(JBColor.RED, null, null, null, Font.BOLD));

    private static final TextAttributesKey[] BAD_CHAR_KEYS = new TextAttributesKey[]{BAD_CHARACTER};
    private static final TextAttributesKey[] INSTRUCTION_KEYS = new TextAttributesKey[]{INSTRUCTION};
    private static final TextAttributesKey[] FINSTRUCTION_KEYS = new TextAttributesKey[]{FINSTRUCTION};
    private static final TextAttributesKey[] DIRECTIVE_KEYS = new TextAttributesKey[]{DIRECTIVE};
    private static final TextAttributesKey[] PREPROCESSOR_KEYS = new TextAttributesKey[]{PREPROCESSOR};
    private static final TextAttributesKey[] IDENT_KEYS = new TextAttributesKey[]{IDENT};
    private static final TextAttributesKey[] VALUE_KEYS = new TextAttributesKey[]{VALUE};
    private static final TextAttributesKey[] TEXT_KEYS = new TextAttributesKey[]{TEXT};
    private static final TextAttributesKey[] OPERATOR_KEYS = new TextAttributesKey[]{OPERATOR};
    private static final TextAttributesKey[] SEPARATOR_KEYS = new TextAttributesKey[]{SEPARATOR};
    private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
    private static final TextAttributesKey[] LCOMMENT_KEYS = new TextAttributesKey[]{LCOMMENT};
    private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];

    @NotNull
    @Override
    public Lexer getHighlightingLexer() { return new FlexAdapter(new Xga99RLexer(null)); }

    @Override
    public TextAttributesKey @NotNull [] getTokenHighlights(IElementType tokenType) {
        if (instructions.contains(tokenType)) {
            return INSTRUCTION_KEYS;
        } else if (fmtInstructions.contains(tokenType)) {
            return FINSTRUCTION_KEYS;
        } else if (directives.contains(tokenType)) {
            return DIRECTIVE_KEYS;
        } else if (preprocessor.contains(tokenType)) {
            return PREPROCESSOR_KEYS;
        } else if (tokenType.equals(Xga99RTypes.IDENT) ||
                tokenType.equals(Xga99RTypes.OP_LC) ||
                tokenType.equals(Xga99RTypes.LOCAL)) {
            return IDENT_KEYS;
        } else if (tokenType.equals(Xga99RTypes.INT)) {
            return VALUE_KEYS;
        } else if (text.contains(tokenType)) {
            return TEXT_KEYS;
        } else if (operators.contains(tokenType)) {
            return OPERATOR_KEYS;
        } else if (tokenType.equals(Xga99RTypes.OP_SEP) ||
                tokenType.equals(Xga99RTypes.PP_SEP)) {
            return SEPARATOR_KEYS;
        } else if (tokenType.equals(Xga99RTypes.COMMENT)) {
            return COMMENT_KEYS;
        } else if (tokenType.equals(Xga99RTypes.LCOMMENT)) {
            return LCOMMENT_KEYS;
        } else if (tokenType.equals(TokenType.BAD_CHARACTER)) {
            return BAD_CHAR_KEYS;
        } else {
            return EMPTY_KEYS;
        }
    }

}
