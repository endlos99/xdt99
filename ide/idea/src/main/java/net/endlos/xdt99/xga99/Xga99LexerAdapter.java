package net.endlos.xdt99.xga99;

import com.intellij.lexer.FlexAdapter;

public class Xga99LexerAdapter extends FlexAdapter {

    public Xga99LexerAdapter() {
        super(new Xga99Lexer(null));
    }

}
