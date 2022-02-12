package net.endlos.xdt99.xas99r;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.editor.markup.TextAttributes;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import com.intellij.ui.JBColor;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import org.jetbrains.annotations.NotNull;

import java.awt.*;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;
import static java.awt.Font.BOLD;

public class Xas99RSyntaxHighlighter extends SyntaxHighlighterBase {
    public static final TokenSet instructions = TokenSet.create(Xas99RTypes.INSTR_I, Xas99RTypes.INSTR_II,
            Xas99RTypes.INSTR_III, Xas99RTypes.INSTR_IV, Xas99RTypes.INSTR_V, Xas99RTypes.INSTR_VI, Xas99RTypes.INSTR_VII,
            Xas99RTypes.INSTR_VIII, Xas99RTypes.INSTR_VIII_I, Xas99RTypes.INSTR_VIII_R, Xas99RTypes.INSTR_IX,
            Xas99RTypes.INSTR_IX_X, Xas99RTypes.INSTR_O);
    public static final TokenSet extendedInstructions = TokenSet.create(Xas99RTypes.INSTR_F18A_IA,
            Xas99RTypes.INSTR_F18A_VI, Xas99RTypes.INSTR_F18A_O, Xas99RTypes.INSTR_9995_VI, Xas99RTypes.INSTR_9995_VIII,
            Xas99RTypes.INSTR_99000_I, Xas99RTypes.INSTR_99000_IV, Xas99RTypes.INSTR_99000_VI,
            Xas99RTypes.INSTR_99000_VIII);
    public static final TokenSet directives = TokenSet.create(Xas99RTypes.DIR_L, Xas99RTypes.DIR_E, Xas99RTypes.DIR_ES,
            Xas99RTypes.DIR_EO, Xas99RTypes.DIR_R, Xas99RTypes.DIR_T, Xas99RTypes.DIR_S, Xas99RTypes.DIR_O,
            Xas99RTypes.DIR_X);
    public static final TokenSet operators = TokenSet.create(Xas99RTypes.OP_AT, Xas99RTypes.OP_AST,
            Xas99RTypes.OP_PLUS, Xas99RTypes.OP_MINUS, Xas99RTypes.OP_NOT, Xas99RTypes.OP_LPAREN, Xas99RTypes.OP_RPAREN,
            Xas99RTypes.OP_MISC, Xas99RTypes.MOD_AUTO, Xas99RTypes.MOD_LEN, Xas99RTypes.MOD_XBANK);
    public static final TokenSet preprocessor = TokenSet.create(Xas99RTypes.PREP);  // could add PP_ARG

    public static final TextAttributesKey INSTRUCTION =
            createTextAttributesKey("XAS99_INSTR", DefaultLanguageHighlighterColors.KEYWORD);
//    public static final TextAttributesKey XINSTRUCTION = createTextAttributesKey("XAS99_XINSTR", DefaultLanguageHighlighterColors.INSTANCE_METHOD);
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

    public Xas99RSyntaxHighlighter() {
        // define derived style for foreign keywords
        TextAttributes myAttr = DefaultLanguageHighlighterColors.KEYWORD.getDefaultAttributes().clone();
        myAttr.setFontType(Font.ITALIC);
        XINSTRUCTION = createTextAttributesKey("XAS99_XINSTR", myAttr);
        XINSTRUCTION_KEYS = new TextAttributesKey[]{XINSTRUCTION};
    }

    @NotNull
    @Override
    public Lexer getHighlightingLexer() {
        return new Xas99RLexerAdapter();
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
        } else if (tokenType.equals(Xas99RTypes.IDENT) || tokenType.equals(Xas99RTypes.OP_LC) ||
                tokenType.equals(Xas99RTypes.LOCAL)) {
            return IDENT_KEYS;
        } else if (tokenType.equals(Xas99RTypes.INT)) {
            return VALUE_KEYS;
        } else if (tokenType.equals(Xas99RTypes.TEXT)) {
            return TEXT_KEYS;
        } else if (tokenType.equals(Xas99RTypes.REGISTER) || tokenType.equals(Xas99RTypes.REGISTER0)) {
            return REGISTER_KEYS;
        } else if (operators.contains(tokenType)) {
            return OPERATOR_KEYS;
        } else if (tokenType.equals(Xas99RTypes.OP_SEP) || tokenType.equals(Xas99RTypes.PP_SEP)) {
            return SEPARATOR_KEYS;
        } else if (tokenType.equals(Xas99RTypes.PRAGMA)) {
            return PRAGMA_KEYS;
        } else if (tokenType.equals(Xas99RTypes.COMMENT)) {
            return COMMENT_KEYS;
        } else if (tokenType.equals(Xas99RTypes.LCOMMENT)) {
            return LCOMMENT_KEYS;
        } else if (tokenType.equals(TokenType.BAD_CHARACTER)) {
            return BAD_CHAR_KEYS;
        } else {
            return EMPTY_KEYS;
        }
    }
}
