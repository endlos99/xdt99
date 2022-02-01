package net.endlos.xdt99.xbas99;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.editor.markup.TextAttributes;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import com.intellij.ui.JBColor;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import org.jetbrains.annotations.NotNull;

import java.awt.*;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;
import static org.apache.commons.lang.ArrayUtils.contains;

public class Xbas99SyntaxHighlighter extends SyntaxHighlighterBase {
    public static final TextAttributesKey STATEMENT =
            createTextAttributesKey("XBAS99_STMT", DefaultLanguageHighlighterColors.KEYWORD);
    public static final TextAttributesKey FUNCTION =
            createTextAttributesKey("XBAS99_FUNC", DefaultLanguageHighlighterColors.DOC_COMMENT_MARKUP);
    public static final TextAttributesKey SUBPROG =
            createTextAttributesKey("XBAS99_SUB", DefaultLanguageHighlighterColors.INSTANCE_METHOD);
    public static final TextAttributesKey NVAR =  // handled by Annotator
            createTextAttributesKey("XBAS99_NVAR", DefaultLanguageHighlighterColors.GLOBAL_VARIABLE);
    public static final TextAttributesKey SVAR =  // handled by Annotator
            createTextAttributesKey("XBAS99_SVAR", DefaultLanguageHighlighterColors.LOCAL_VARIABLE);
    public static final TextAttributesKey VALUE =
            createTextAttributesKey("XBAS99_VALUE", DefaultLanguageHighlighterColors.NUMBER);
    public static final TextAttributesKey LINO =
            createTextAttributesKey("XBAS99_LINO", DefaultLanguageHighlighterColors.CONSTANT);
    public static final TextAttributesKey QSTRING =
            createTextAttributesKey("XBAS99_QSTR", DefaultLanguageHighlighterColors.STRING);
    public static final TextAttributesKey OPERATOR =
            createTextAttributesKey("XBAS99_OPER", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    public static final TextAttributesKey SEPARATOR =
            createTextAttributesKey("XBAS99_SEP", DefaultLanguageHighlighterColors.SEMICOLON);
    public static final TextAttributesKey COMMENT =
            createTextAttributesKey("XBAS99_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);

    static final TextAttributesKey BAD_CHARACTER = createTextAttributesKey("SIMPLE_BAD_CHARACTER",
            new TextAttributes(JBColor.RED, null, null, null, Font.BOLD));

    private static final TextAttributesKey[] BAD_CHAR_KEYS = new TextAttributesKey[]{BAD_CHARACTER};
    private static final TextAttributesKey[] STATEMENT_KEYS = new TextAttributesKey[]{STATEMENT};
    private static final TextAttributesKey[] FUNCTION_KEYS = new TextAttributesKey[]{FUNCTION};
    private static final TextAttributesKey[] VALUE_KEYS = new TextAttributesKey[]{VALUE};
    private static final TextAttributesKey[] LINO_KEYS = new TextAttributesKey[]{LINO};
    private static final TextAttributesKey[] QSTRING_KEYS = new TextAttributesKey[]{QSTRING};
    private static final TextAttributesKey[] OPERATOR_KEYS = new TextAttributesKey[]{OPERATOR};
    private static final TextAttributesKey[] SEPARATOR_KEYS = new TextAttributesKey[]{SEPARATOR};
    private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
    private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];

    private static final IElementType[] allStatementTokens = {
            Xbas99Types.W_ACCEPT,
            Xbas99Types.W_ALL,
            Xbas99Types.W_AND,
            Xbas99Types.W_APPEND,
            Xbas99Types.W_AT,
            Xbas99Types.W_BASE,
            Xbas99Types.W_BEEP,
            Xbas99Types.W_BREAK,
            Xbas99Types.W_CALL,
            Xbas99Types.W_CLOSE,
            Xbas99Types.W_DATA,
            Xbas99Types.W_DEF,
            Xbas99Types.W_DELETE,
            Xbas99Types.W_DIGIT,
            Xbas99Types.W_DIM,
            Xbas99Types.W_DISPLAY,
            Xbas99Types.W_ELSE,
            Xbas99Types.W_END,
            Xbas99Types.W_ERASE,
            Xbas99Types.W_ERROR,
            Xbas99Types.W_FIXED,
            Xbas99Types.W_FOR,
            Xbas99Types.W_GO,
            Xbas99Types.W_GOSUB,
            Xbas99Types.W_GOTO,
            Xbas99Types.W_IF,
            Xbas99Types.W_IMAGE,
            Xbas99Types.W_INPUT,
            Xbas99Types.W_INTERNAL,
            Xbas99Types.W_LET,
            Xbas99Types.W_LINPUT,
            Xbas99Types.W_NEXT,
            Xbas99Types.W_NOT,
            Xbas99Types.W_NUMERIC,
            Xbas99Types.W_ON,
            Xbas99Types.W_OPEN,
            Xbas99Types.W_OPTION,
            Xbas99Types.W_OR,
            Xbas99Types.W_OUTPUT,
            Xbas99Types.W_PERMANENT,
            Xbas99Types.W_PRINT,
            Xbas99Types.W_RANDOMIZE,
            Xbas99Types.W_READ,
            Xbas99Types.W_RELATIVE,
            Xbas99Types.W_RETURN,
            Xbas99Types.W_RUN,
            Xbas99Types.W_SEQUENTIAL,
            Xbas99Types.W_SIZE,
            Xbas99Types.W_STEP,
            Xbas99Types.W_STOP,
            Xbas99Types.W_SUB,
            Xbas99Types.W_SUBEND,
            Xbas99Types.W_SUBEXIT,
            Xbas99Types.W_THEN,
            Xbas99Types.W_TO,
            Xbas99Types.W_TRACE,
            Xbas99Types.W_UALPHA,
            Xbas99Types.W_UNBREAK,
            Xbas99Types.W_UNTRACE,
            Xbas99Types.W_UPDATE,
            Xbas99Types.W_USING,
            Xbas99Types.W_VALIDATE,
            Xbas99Types.W_VARIABLE,
            Xbas99Types.W_WARNING,
            Xbas99Types.W_XOR
    };
    private static final IElementType[] allFunctionTokens = {
            Xbas99Types.W_FUN_N,
            Xbas99Types.W_FUN_S,
            Xbas99Types.W_FUN_C
    };
    private static final IElementType[] allOperatorTokens = {
            Xbas99Types.OP_COLON,
            Xbas99Types.OP_COMMA,
            Xbas99Types.OP_SEMI,
            Xbas99Types.OP_EQ,
            Xbas99Types.OP_LT,
            Xbas99Types.OP_GT,
            Xbas99Types.OP_HASH,
            Xbas99Types.OP_LPAREN,
            Xbas99Types.OP_RPAREN,
            Xbas99Types.OP_AMP,
            Xbas99Types.OP_PLUS,
            Xbas99Types.OP_MINUS,
            Xbas99Types.OP_MUL,
            Xbas99Types.OP_DIV,
            Xbas99Types.OP_EXP
    };
    private static final IElementType[] allTextLikeTokens = {
            Xbas99Types.OP_QUOTE,
            Xbas99Types.QSTRING,
            Xbas99Types.A_DATA,
            Xbas99Types.A_IMAGE
    };

    @Override
    @NotNull
    public Lexer getHighlightingLexer() { return new Xbas99LexerAdapter(); }

    @Override
    public TextAttributesKey @NotNull [] getTokenHighlights(IElementType tokenType) {
        if (contains(allStatementTokens, tokenType)) {
            return STATEMENT_KEYS;
        } else if (contains(allFunctionTokens, tokenType)) {
            return FUNCTION_KEYS;
        } else if (tokenType.equals(Xbas99Types.NUMBER) ||
                tokenType.equals(Xbas99Types.FLOAT)) {
            return VALUE_KEYS;
        } else if (tokenType.equals(Xbas99Types.LNUMBER)) {
            return LINO_KEYS;
        } else if (contains(allTextLikeTokens, tokenType)) {
            return QSTRING_KEYS;
        } else if (contains(allOperatorTokens, tokenType)) {
            return OPERATOR_KEYS;
        } else if (tokenType.equals(Xbas99Types.OP_SEP)) {
            return SEPARATOR_KEYS;
        } else if (tokenType.equals(Xbas99Types.COMMENT) ||
                tokenType.equals(Xbas99Types.W_REM)) {
            return COMMENT_KEYS;
        } else if (tokenType.equals(TokenType.BAD_CHARACTER)) {
            return BAD_CHAR_KEYS;
        } else {
            return EMPTY_KEYS;
        }
    }

}
