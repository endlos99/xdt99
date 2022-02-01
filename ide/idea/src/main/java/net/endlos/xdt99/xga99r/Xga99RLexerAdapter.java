package net.endlos.xdt99.xga99r;

import com.intellij.lexer.FlexAdapter;
import net.endlos.xdt99.xga99r.Xga99RLexer;

public class Xga99RLexerAdapter extends FlexAdapter {

    public Xga99RLexerAdapter() {
        super(new Xga99RLexer(null));
    }

}
