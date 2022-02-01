package net.endlos.xdt99.xas99r;

import com.intellij.codeInsight.editorActions.QuoteHandler;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.editor.highlighter.HighlighterIterator;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;

public class Xas99RQuoteHandler implements QuoteHandler {
    private static final TokenSet quoteTokens = TokenSet.create(Xas99RTypes.OP_QUOTE, Xas99RTypes.OP_FQUOTE);

    @Override
    public boolean isClosingQuote(HighlighterIterator iterator, int offset) {
        final IElementType token = iterator.getTokenType();
        if (!quoteTokens.contains(token))
            return false;
        final String part = getOperandPart(iterator, offset);
        char quote = token == Xas99RTypes.OP_QUOTE ? '\'' : '"';
        long occurrences = part.chars().filter(ch -> ch == quote).count();
        return occurrences % 2 == 0;
    }

    @Override
    public boolean isOpeningQuote(HighlighterIterator iterator, int offset) {
        final IElementType token = iterator.getTokenType();
        if (!quoteTokens.contains(token))
            return false;
        final String part = getOperandPart(iterator, offset);
        char quote = token == Xas99RTypes.OP_QUOTE ? '\'' : '"';
        long occurrences = part.chars().filter(ch -> ch == quote).count();
        return occurrences % 2 == 1;
    }

    @Override
    public boolean hasNonClosedLiteral(Editor editor, HighlighterIterator iterator, int offset) {
        final IElementType token = iterator.getTokenType();
        if (!quoteTokens.contains(token))
            return false;
        // check of only space follows, up to next ','
        String restOfLine = getRestOfLine(iterator, offset);  // excludes quote
        for (char ch : restOfLine.toCharArray()) {
            if (ch != ' ')
                return false;
        }
        return true;
    }

    @Override
    public boolean isInsideLiteral(HighlighterIterator iterator) {
        return false;  // when is this actually called?!
    }

    // return part of line between ',', within line
    private String getOperandPart(HighlighterIterator iterator, int offset) {
        final CharSequence chars = iterator.getDocument().getCharsSequence();
        final int endOfFile = chars.length();
        int beginningOfLine = offset - 1;
        int endOfLine = offset + 1;
        while (beginningOfLine > 0) {
            if (chars.charAt(beginningOfLine) == ',')
                break;
            if (chars.charAt(beginningOfLine - 1) == '\n')
                break;
            --beginningOfLine;
        }
        while (endOfLine < endOfFile) {
            final char ch = chars.charAt(endOfLine);
            if (ch == '\n' || ch == ',' || ch == ';')
                break;
            ++endOfLine;
        }
        return chars.subSequence(beginningOfLine + 1, endOfLine).toString();
    }

    // return to end of line (or beginning of comment), excludes offset char
    private String getRestOfLine(HighlighterIterator iterator, int offset) {
        final CharSequence chars = iterator.getDocument().getCharsSequence();
        final int endOfFile = chars.length();
        int endOfLine = offset + 1;
        while (endOfLine < endOfFile) {
            final char ch = chars.charAt(endOfLine);
            if (ch == '\n' || ch == ',' || ch == ';')
                break;
            ++endOfLine;
        }
        return chars.subSequence(offset + 1, endOfLine).toString();
    }

}
