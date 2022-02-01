package net.endlos.xdt99.xga99;

import com.intellij.codeInsight.highlighting.PairedBraceMatcherAdapter;
import com.intellij.lang.BracePair;
import com.intellij.lang.PairedBraceMatcher;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xga99.psi.Xga99Types;
import org.jetbrains.annotations.NotNull;

public class Xga99BraceMatcher extends PairedBraceMatcherAdapter {

    public Xga99BraceMatcher() {
        super(new Xga99PairedBraceMatcher(), Xga99Language.INSTANCE);
    }

    private static class Xga99PairedBraceMatcher implements PairedBraceMatcher {

        @Override
        public BracePair @NotNull [] getPairs() {
            return new BracePair[] {
                    new BracePair(Xga99Types.OP_LPAREN, Xga99Types.OP_RPAREN, false)
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
