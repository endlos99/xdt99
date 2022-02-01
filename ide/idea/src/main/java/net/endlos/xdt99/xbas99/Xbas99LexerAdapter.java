package net.endlos.xdt99.xbas99;

import com.intellij.lexer.FlexAdapter;

public class Xbas99LexerAdapter extends FlexAdapter {

    public Xbas99LexerAdapter() {
        super(new Xbas99Lexer(null));
    }

}
