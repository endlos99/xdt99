package net.endlos.xdt99.xga99r;

import com.intellij.codeInsight.highlighting.PairedBraceMatcherAdapter;
import com.intellij.lang.BracePair;
import com.intellij.lang.PairedBraceMatcher;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import org.jetbrains.annotations.NotNull;

public class Xga99RBraceMatcher extends PairedBraceMatcherAdapter {

    public Xga99RBraceMatcher() {
        super(new Xga99RPairedBraceMatcher(), Xga99RLanguage.INSTANCE);
    }

    private static class Xga99RPairedBraceMatcher implements PairedBraceMatcher {

        @Override
        public BracePair @NotNull [] getPairs() {
            return new BracePair[] {
                    new BracePair(Xga99RTypes.OP_LPAREN, Xga99RTypes.OP_RPAREN, false)
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
