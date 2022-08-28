package net.endlos.xdt99.xas99;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.editor.markup.TextAttributes;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import com.intellij.ui.JBColor;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;

import java.awt.*;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;
import static java.awt.Font.*;

public class Xas99SyntaxHighlighter extends SyntaxHighlighterBase {
    public static final TokenSet instructions = TokenSet.create(Xas99Types.INSTR_I, Xas99Types.INSTR_II,
            Xas99Types.INSTR_III, Xas99Types.INSTR_IV, Xas99Types.INSTR_V, Xas99Types.INSTR_VI, Xas99Types.INSTR_VII,
            Xas99Types.INSTR_VIII, Xas99Types.INSTR_VIII_I, Xas99Types.INSTR_VIII_R, Xas99Types.INSTR_IX,
            Xas99Types.INSTR_IX_X, Xas99Types.INSTR_O);
    public static final TokenSet extendedInstructions = TokenSet.create(Xas99Types.INSTR_F18A_IA,
            Xas99Types.INSTR_F18A_VI, Xas99Types.INSTR_F18A_O, Xas99Types.INSTR_9995_VI, Xas99Types.INSTR_9995_VIII,
            Xas99Types.INSTR_99000_I, Xas99Types.INSTR_99000_IV, Xas99Types.INSTR_99000_VI,
            Xas99Types.INSTR_99000_VIII);
    public static final TokenSet directives = TokenSet.create(Xas99Types.DIR_L, Xas99Types.DIR_E, Xas99Types.DIR_ES,
            Xas99Types.DIR_EO, Xas99Types.DIR_RA, Xas99Types.DIR_R, Xas99Types.DIR_T, Xas99Types.DIR_S,
            Xas99Types.DIR_C, Xas99Types.DIR_O, Xas99Types.DIR_X);
    public static final TokenSet text = TokenSet.create(Xas99Types.OP_QUOTE, Xas99Types.TEXT, Xas99Types.OP_FQUOTE,
            Xas99Types.FNAME);
    public static final TokenSet operators = TokenSet.create(Xas99Types.OP_AT, Xas99Types.OP_AST,
            Xas99Types.OP_PLUS, Xas99Types.OP_MINUS, Xas99Types.OP_NOT, Xas99Types.OP_LPAREN, Xas99Types.OP_RPAREN,
            Xas99Types.OP_MISC, Xas99Types.MOD_AUTO, Xas99Types.MOD_LEN, Xas99Types.MOD_XBANK);
    public static final TokenSet preprocessor = TokenSet.create(Xas99Types.PREP);  // could add PP_ARG

    public static final TextAttributesKey INSTRUCTION =
            createTextAttributesKey("XAS99_INSTR", DefaultLanguageHighlighterColors.KEYWORD);
//    public static final TextAttributesKey XINSTRUCTION =
//         createTextAttributesKey("XAS99_XINSTR", DefaultLanguageHighlighterColors.INSTANCE_METHOD);
    public static final TextAttributesKey DIRECTIVE =
        createTextAttributesKey("XAS99_DIR", DefaultLanguageHighlighterColors.INSTANCE_FIELD);
    public static final TextAttributesKey PREPROCESSOR =
            createTextAttributesKey("XAS99_PREP", DefaultLanguageHighlighterColors.METADATA);
    public static final TextAttributesKey IDENT =
            createTextAttributesKey("XAS99_IDENT", DefaultLanguageHighlighterColors.IDENTIFIER);
    public static final TextAttributesKey VALUE =
            createTextAttributesKey("XAS99_VALUE", DefaultLanguageHighlighterColors.NUMBER);
    public static final TextAttributesKey TEXT =
            createTextAttributesKey("XAS99_TEXT", DefaultLanguageHighlighterColors.STRING);
    public static final TextAttributesKey REGISTER =
            createTextAttributesKey("XAS99_REG", DefaultLanguageHighlighterColors.CONSTANT);
    public static final TextAttributesKey OPERATOR =
            createTextAttributesKey("XAS99_OPER", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    public static final TextAttributesKey SEPARATOR =
            createTextAttributesKey("XAS99_SEP", DefaultLanguageHighlighterColors.COMMA);
    public static final TextAttributesKey PRAGMA =
            createTextAttributesKey("XAS99_PRAGMA", DefaultLanguageHighlighterColors.DOC_COMMENT_TAG);
    public static final TextAttributesKey COMMENT =
            createTextAttributesKey("XAS99_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);
    public static final TextAttributesKey LCOMMENT =
            createTextAttributesKey("XAS99_LCOMMENT", DefaultLanguageHighlighterColors.DOC_COMMENT);
    public static TextAttributesKey XINSTRUCTION;

    public static final TextAttributesKey BAD_CHARACTER = createTextAttributesKey("SIMPLE_BAD_CHARACTER",
            new TextAttributes(JBColor.RED, null, null, null, BOLD));

    private static final TextAttributesKey[] BAD_CHAR_KEYS = new TextAttributesKey[]{BAD_CHARACTER};
    private static final TextAttributesKey[] INSTRUCTION_KEYS = new TextAttributesKey[]{INSTRUCTION};
//    private static final TextAttributesKey[] XINSTRUCTION_KEYS = new TextAttributesKey[]{XINSTRUCTION};
    private static final TextAttributesKey[] DIRECTIVE_KEYS = new TextAttributesKey[]{DIRECTIVE};
    private static final TextAttributesKey[] PREPROCESSOR_KEYS = new TextAttributesKey[]{PREPROCESSOR};
    private static final TextAttributesKey[] IDENT_KEYS = new TextAttributesKey[]{IDENT};
    private static final TextAttributesKey[] VALUE_KEYS = new TextAttributesKey[]{VALUE};
    private static final TextAttributesKey[] TEXT_KEYS = new TextAttributesKey[]{TEXT};
    private static final TextAttributesKey[] REGISTER_KEYS = new TextAttributesKey[]{REGISTER};
    private static final TextAttributesKey[] OPERATOR_KEYS = new TextAttributesKey[]{OPERATOR};
    private static final TextAttributesKey[] SEPARATOR_KEYS = new TextAttributesKey[]{SEPARATOR};
    private static final TextAttributesKey[] PRAGMA_KEYS = new TextAttributesKey[]{PRAGMA};
    private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
    private static final TextAttributesKey[] LCOMMENT_KEYS = new TextAttributesKey[]{LCOMMENT};
    private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];
    private static TextAttributesKey[] XINSTRUCTION_KEYS;

    public Xas99SyntaxHighlighter() {
        // define derived style for foreign keywords
        TextAttributes myAttr = DefaultLanguageHighlighterColors.KEYWORD.getDefaultAttributes().clone();
        myAttr.setFontType(Font.ITALIC);
        XINSTRUCTION = createTextAttributesKey("XAS99_XINSTR", myAttr);
        XINSTRUCTION_KEYS = new TextAttributesKey[]{XINSTRUCTION};
    }

    @NotNull
    @Override
    public Lexer getHighlightingLexer() {
        return new Xas99LexerAdapter();
    }

    @NotNull
    @Override
    public TextAttributesKey @NotNull [] getTokenHighlights(IElementType tokenType) {
        if (instructions.contains(tokenType)) {
            return INSTRUCTION_KEYS;
        } else if (extendedInstructions.contains(tokenType)) {
            return XINSTRUCTION_KEYS;
        } else if (directives.contains(tokenType)) {
            return DIRECTIVE_KEYS;
        } else if (preprocessor.contains(tokenType)) {
            return PREPROCESSOR_KEYS;
        } else if (tokenType.equals(Xas99Types.OP_LC) || tokenType.equals(Xas99Types.LOCAL)) {
            return IDENT_KEYS;
        } else if (tokenType.equals(Xas99Types.INT)) {
            return VALUE_KEYS;
        } else if (text.contains(tokenType)) {
            return TEXT_KEYS;
        } else if (tokenType.equals(Xas99Types.REGISTER) || tokenType.equals(Xas99Types.REGISTER0)) {
            return REGISTER_KEYS;
        } else if (operators.contains(tokenType)) {
            return OPERATOR_KEYS;
        } else if (tokenType.equals(Xas99Types.OP_SEP) || tokenType.equals(Xas99Types.PP_SEP)) {
            return SEPARATOR_KEYS;
        } else if (tokenType.equals(Xas99Types.PRAGMA)) {
            return PRAGMA_KEYS;
        } else if (tokenType.equals(Xas99Types.COMMENT)) {
            return COMMENT_KEYS;
        } else if (tokenType.equals(Xas99Types.LCOMMENT)) {
            return LCOMMENT_KEYS;
        } else if (tokenType.equals(TokenType.BAD_CHARACTER)) {
            return BAD_CHAR_KEYS;
        } else {
            return EMPTY_KEYS;
        }
    }
}
