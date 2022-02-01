package net.endlos.xdt99.xbas99l;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.editor.markup.TextAttributes;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import com.intellij.ui.JBColor;
import net.endlos.xdt99.xbas99l.psi.Xbas99LTypes;
import org.jetbrains.annotations.NotNull;

import java.awt.*;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;
import static org.apache.commons.lang.ArrayUtils.contains;

public class Xbas99LSyntaxHighlighter extends SyntaxHighlighterBase {
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
    public static final TextAttributesKey LABEL =
            createTextAttributesKey("XBAS99_LABEL", DefaultLanguageHighlighterColors.CONSTANT);
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
    private static final TextAttributesKey[] LABEL_KEYS = new TextAttributesKey[]{LABEL};
    private static final TextAttributesKey[] QSTRING_KEYS = new TextAttributesKey[]{QSTRING};
    private static final TextAttributesKey[] OPERATOR_KEYS = new TextAttributesKey[]{OPERATOR};
    private static final TextAttributesKey[] SEPARATOR_KEYS = new TextAttributesKey[]{SEPARATOR};
    private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
    private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];

    private static final IElementType[] allStatementTokens = {
            Xbas99LTypes.W_ACCEPT,
            Xbas99LTypes.W_ALL,
            Xbas99LTypes.W_AND,
            Xbas99LTypes.W_APPEND,
            Xbas99LTypes.W_AT,
            Xbas99LTypes.W_BASE,
            Xbas99LTypes.W_BEEP,
            Xbas99LTypes.W_BREAK,
            Xbas99LTypes.W_CALL,
            Xbas99LTypes.W_CLOSE,
            Xbas99LTypes.W_DATA,
            Xbas99LTypes.W_DEF,
            Xbas99LTypes.W_DELETE,
            Xbas99LTypes.W_DIGIT,
            Xbas99LTypes.W_DIM,
            Xbas99LTypes.W_DISPLAY,
            Xbas99LTypes.W_ELSE,
            Xbas99LTypes.W_END,
            Xbas99LTypes.W_ERASE,
            Xbas99LTypes.W_ERROR,
            Xbas99LTypes.W_FIXED,
            Xbas99LTypes.W_FOR,
            Xbas99LTypes.W_GO,
            Xbas99LTypes.W_GOSUB,
            Xbas99LTypes.W_GOTO,
            Xbas99LTypes.W_IF,
            Xbas99LTypes.W_IMAGE,
            Xbas99LTypes.W_INPUT,
            Xbas99LTypes.W_INTERNAL,
            Xbas99LTypes.W_LET,
            Xbas99LTypes.W_LINPUT,
            Xbas99LTypes.W_NEXT,
            Xbas99LTypes.W_NOT,
            Xbas99LTypes.W_NUMERIC,
            Xbas99LTypes.W_ON,
            Xbas99LTypes.W_OPEN,
            Xbas99LTypes.W_OPTION,
            Xbas99LTypes.W_OR,
            Xbas99LTypes.W_OUTPUT,
            Xbas99LTypes.W_PERMANENT,
            Xbas99LTypes.W_PRINT,
            Xbas99LTypes.W_RANDOMIZE,
            Xbas99LTypes.W_READ,
            Xbas99LTypes.W_RELATIVE,
            Xbas99LTypes.W_RETURN,
            Xbas99LTypes.W_RUN,
            Xbas99LTypes.W_SEQUENTIAL,
            Xbas99LTypes.W_SIZE,
            Xbas99LTypes.W_STEP,
            Xbas99LTypes.W_STOP,
            Xbas99LTypes.W_SUB,
            Xbas99LTypes.W_SUBEND,
            Xbas99LTypes.W_SUBEXIT,
            Xbas99LTypes.W_THEN,
            Xbas99LTypes.W_TO,
            Xbas99LTypes.W_TRACE,
            Xbas99LTypes.W_UALPHA,
            Xbas99LTypes.W_UNBREAK,
            Xbas99LTypes.W_UNTRACE,
            Xbas99LTypes.W_UPDATE,
            Xbas99LTypes.W_USING,
            Xbas99LTypes.W_VALIDATE,
            Xbas99LTypes.W_VARIABLE,
            Xbas99LTypes.W_WARNING,
            Xbas99LTypes.W_XOR
    };
    private static final IElementType[] allFunctionTokens = {
            Xbas99LTypes.W_FUN_N,
            Xbas99LTypes.W_FUN_S,
            Xbas99LTypes.W_FUN_C
    };
    private static final IElementType[] allOperatorTokens = {
            Xbas99LTypes.OP_COLON,
            Xbas99LTypes.OP_COMMA,
            Xbas99LTypes.OP_SEMI,
            Xbas99LTypes.OP_EQ,
            Xbas99LTypes.OP_LT,
            Xbas99LTypes.OP_GT,
            Xbas99LTypes.OP_HASH,
            Xbas99LTypes.OP_LPAREN,
            Xbas99LTypes.OP_RPAREN,
            Xbas99LTypes.OP_AMP,
            Xbas99LTypes.OP_PLUS,
            Xbas99LTypes.OP_MINUS,
            Xbas99LTypes.OP_MUL,
            Xbas99LTypes.OP_DIV,
            Xbas99LTypes.OP_EXP
    };
    private static final IElementType[] allTextLikeTokens = {
            Xbas99LTypes.OP_QUOTE,
            Xbas99LTypes.QSTRING,
            Xbas99LTypes.A_DATA,
            Xbas99LTypes.A_IMAGE
    };

    @Override
    @NotNull
    public Lexer getHighlightingLexer() { return new Xbas99LLexerAdapter(); }

    @Override
    public TextAttributesKey @NotNull [] getTokenHighlights(IElementType tokenType) {
        if (contains(allStatementTokens, tokenType)) {
            return STATEMENT_KEYS;
        } else if (contains(allFunctionTokens, tokenType)) {
            return FUNCTION_KEYS;
        } else if (tokenType.equals(Xbas99LTypes.NUMBER) ||
                tokenType.equals(Xbas99LTypes.FLOAT)) {
            return VALUE_KEYS;
        } else if (tokenType.equals(Xbas99LTypes.LIDENT)) {
            return LABEL_KEYS;
        } else if (contains(allTextLikeTokens, tokenType)) {
            return QSTRING_KEYS;
        } else if (contains(allOperatorTokens, tokenType)) {
            return OPERATOR_KEYS;
        } else if (tokenType.equals(Xbas99LTypes.OP_SEP)) {
            return SEPARATOR_KEYS;
        } else if (tokenType.equals(Xbas99LTypes.COMMENT) ||
                tokenType.equals(Xbas99LTypes.W_REM)) {
            return COMMENT_KEYS;
        } else if (tokenType.equals(TokenType.BAD_CHARACTER)) {
            return BAD_CHAR_KEYS;
        } else {
            return EMPTY_KEYS;
        }
    }

}
