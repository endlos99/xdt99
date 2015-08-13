package net.endlos.xdt99.xas99;

import com.intellij.lexer.FlexAdapter;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.editor.markup.TextAttributes;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;

import java.awt.*;
import java.io.Reader;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;

public class Xas99SyntaxHighlighter extends SyntaxHighlighterBase {
    public static final TextAttributesKey INSTRUCTION = createTextAttributesKey("XAS99_INSTR", DefaultLanguageHighlighterColors.KEYWORD);
    public static final TextAttributesKey DIRECTIVE = createTextAttributesKey("XAS99_DIR", DefaultLanguageHighlighterColors.INSTANCE_FIELD);
    public static final TextAttributesKey PREPROCESSOR = createTextAttributesKey("XAS99_PREP", DefaultLanguageHighlighterColors.METADATA);
    public static final TextAttributesKey IDENT = createTextAttributesKey("XAS99_IDENT", DefaultLanguageHighlighterColors.IDENTIFIER);
    public static final TextAttributesKey VALUE = createTextAttributesKey("XAS99_VALUE", DefaultLanguageHighlighterColors.NUMBER);
    public static final TextAttributesKey TEXT = createTextAttributesKey("XAS99_TEXT", DefaultLanguageHighlighterColors.STRING);
    public static final TextAttributesKey REGISTER = createTextAttributesKey("XAS99_REG", DefaultLanguageHighlighterColors.CONSTANT);
    public static final TextAttributesKey OPERATOR = createTextAttributesKey("XAS99_OPER", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    public static final TextAttributesKey SEPARATOR = createTextAttributesKey("XAS99_SEP", DefaultLanguageHighlighterColors.COMMA);
    public static final TextAttributesKey COMMENT = createTextAttributesKey("XAS99_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);
    public static final TextAttributesKey LCOMMENT = createTextAttributesKey("XAS99_LCOMMENT", DefaultLanguageHighlighterColors.DOC_COMMENT);

    static final TextAttributesKey BAD_CHARACTER = createTextAttributesKey("SIMPLE_BAD_CHARACTER",
            new TextAttributes(Color.RED, null, null, null, Font.BOLD));

    private static final TextAttributesKey[] BAD_CHAR_KEYS = new TextAttributesKey[]{BAD_CHARACTER};
    private static final TextAttributesKey[] INSTRUCTION_KEYS = new TextAttributesKey[]{INSTRUCTION};
    private static final TextAttributesKey[] DIRECTIVE_KEYS = new TextAttributesKey[]{DIRECTIVE};
    private static final TextAttributesKey[] PREPROCESSOR_KEYS = new TextAttributesKey[]{PREPROCESSOR};
    private static final TextAttributesKey[] IDENT_KEYS = new TextAttributesKey[]{IDENT};
    private static final TextAttributesKey[] VALUE_KEYS = new TextAttributesKey[]{VALUE};
    private static final TextAttributesKey[] TEXT_KEYS = new TextAttributesKey[]{TEXT};
    private static final TextAttributesKey[] REGISTER_KEYS = new TextAttributesKey[]{REGISTER};
    private static final TextAttributesKey[] OPERATOR_KEYS = new TextAttributesKey[]{OPERATOR};
    private static final TextAttributesKey[] SEPARATOR_KEYS = new TextAttributesKey[]{SEPARATOR};
    private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
    private static final TextAttributesKey[] LCOMMENT_KEYS = new TextAttributesKey[]{LCOMMENT};
    private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];

    @NotNull
    @Override
    public Lexer getHighlightingLexer() { return new FlexAdapter(new Xas99Lexer((Reader) null)); }

    @NotNull
    @Override
    public TextAttributesKey[] getTokenHighlights(IElementType tokenType) {
        if (tokenType.equals(Xas99Types.INSTR_I) ||
                tokenType.equals(Xas99Types.INSTR_II) ||
                tokenType.equals(Xas99Types.INSTR_III) ||
                tokenType.equals(Xas99Types.INSTR_IV) ||
                tokenType.equals(Xas99Types.INSTR_V) ||
                tokenType.equals(Xas99Types.INSTR_VI) ||
                tokenType.equals(Xas99Types.INSTR_VII) ||
                tokenType.equals(Xas99Types.INSTR_VIII) ||
                tokenType.equals(Xas99Types.INSTR_VIII_I) ||
                tokenType.equals(Xas99Types.INSTR_VIII_R) ||
                tokenType.equals(Xas99Types.INSTR_IX) ||
                tokenType.equals(Xas99Types.INSTR_O)) {
            return INSTRUCTION_KEYS;
        } else if (tokenType.equals(Xas99Types.DIR_L) ||
                tokenType.equals(Xas99Types.DIR_E) ||
                tokenType.equals(Xas99Types.DIR_ES) ||
                tokenType.equals(Xas99Types.DIR_S) ||
                tokenType.equals(Xas99Types.DIR_O) ||
                tokenType.equals(Xas99Types.DIR_X)) {
            return DIRECTIVE_KEYS;
        } else if (tokenType.equals(Xas99Types.PREPROCESSOR)) {
            return PREPROCESSOR_KEYS;
        } else if (tokenType.equals(Xas99Types.IDENT)) {
            return IDENT_KEYS;
        } else if (tokenType.equals(Xas99Types.INT) ||
                tokenType.equals(Xas99Types.OP_LC)) {
            return VALUE_KEYS;
        } else if (tokenType.equals(Xas99Types.TEXT)) {
            return TEXT_KEYS;
        } else if (tokenType.equals(Xas99Types.REGISTER)) {
            return REGISTER_KEYS;
        } else if (tokenType.equals(Xas99Types.OP_AT) ||
                tokenType.equals(Xas99Types.OP_AST) ||
                tokenType.equals(Xas99Types.OP_PLUS) ||
                tokenType.equals(Xas99Types.OP_MINUS) ||
                tokenType.equals(Xas99Types.OP_NOT) ||
                tokenType.equals(Xas99Types.OP_LPAREN) ||
                tokenType.equals(Xas99Types.OP_RPAREN) ||
                tokenType.equals(Xas99Types.OP_MISC)) {
            return OPERATOR_KEYS;
        } else if (tokenType.equals(Xas99Types.OP_SEP)) {
            return SEPARATOR_KEYS;
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
