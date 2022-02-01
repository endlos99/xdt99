package net.endlos.xdt99.xas99r;

import com.intellij.lexer.FlexAdapter;
import net.endlos.xdt99.xas99r.Xas99RLexer;

public class Xas99RLexerAdapter extends FlexAdapter {

    public Xas99RLexerAdapter() {
        super(new Xas99RLexer(null));
    }

}
