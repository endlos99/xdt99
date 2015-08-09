package net.endlos.xdt99.xas99;

import com.intellij.lexer.FlexAdapter;

import java.io.Reader;

public class Xas99LexerAdapter extends FlexAdapter {
    public Xas99LexerAdapter() {
        super(new Xas99Lexer((Reader) null));
    }
}
