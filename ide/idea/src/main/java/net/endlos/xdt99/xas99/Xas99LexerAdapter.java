package net.endlos.xdt99.xas99;

import com.intellij.lexer.FlexAdapter;

public class Xas99LexerAdapter extends FlexAdapter {

    public Xas99LexerAdapter() {
        super(new Xas99Lexer(null));
    }

}
