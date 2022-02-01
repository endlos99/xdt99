package net.endlos.xdt99.xbas99;

import com.intellij.codeInsight.highlighting.PairedBraceMatcherAdapter;
import com.intellij.lang.BracePair;
import com.intellij.lang.PairedBraceMatcher;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import org.jetbrains.annotations.NotNull;

public class Xbas99BraceMatcher extends PairedBraceMatcherAdapter {

    public Xbas99BraceMatcher() {
        super(new Xbas99PairedBraceMatcher(), Xbas99Language.INSTANCE);
    }

    private static class Xbas99PairedBraceMatcher implements PairedBraceMatcher {

        @Override
        public BracePair @NotNull [] getPairs() {
            return new BracePair[] {
                    new BracePair(Xbas99Types.OP_LPAREN, Xbas99Types.OP_RPAREN, false)
            };
        }

        @Override
        public boolean isPairedBracesAllowedBeforeType(@NotNull IElementType lbraceType, IElementType type) {
            return true;
        }

        @Override
        public int getCodeConstructStart(PsiFile file, int openingBraceOffset) {
            return openingBraceOffset;
        }
    }

}
