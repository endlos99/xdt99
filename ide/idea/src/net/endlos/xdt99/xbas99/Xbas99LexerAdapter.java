package net.endlos.xdt99.xbas99;

import com.intellij.lexer.FlexAdapter;
import net.endlos.xdt99.xbas99.Xbas99Lexer;

import java.io.Reader;

public class Xbas99LexerAdapter extends FlexAdapter {
    public Xbas99LexerAdapter() {
        super(new Xbas99Lexer((Reader) null));
    }
}
