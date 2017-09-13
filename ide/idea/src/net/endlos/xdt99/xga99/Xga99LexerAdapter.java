package net.endlos.xdt99.xga99;

import com.intellij.lexer.FlexAdapter;

import java.io.Reader;

public class Xga99LexerAdapter extends FlexAdapter {
    public Xga99LexerAdapter() {
        super(new Xga99Lexer((Reader) null));
    }
}
