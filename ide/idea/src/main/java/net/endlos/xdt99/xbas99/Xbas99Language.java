package net.endlos.xdt99.xbas99;

import com.intellij.lang.Language;
import com.intellij.psi.tree.TokenSet;

public class Xbas99Language extends Language {
    public static final Xbas99Language INSTANCE = new Xbas99Language();

    private Xbas99Language() {
        super("Xbas99");
    }

}
