package net.endlos.xdt99.xbas99l;

import com.intellij.lexer.FlexAdapter;

public class Xbas99LLexerAdapter extends FlexAdapter {

    public Xbas99LLexerAdapter() {
        super(new Xbas99LLexer(null));
    }

}
