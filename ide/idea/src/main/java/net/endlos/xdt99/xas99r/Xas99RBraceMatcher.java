package net.endlos.xdt99.xas99r;

import com.intellij.codeInsight.highlighting.PairedBraceMatcherAdapter;
import com.intellij.lang.BracePair;
import com.intellij.lang.PairedBraceMatcher;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import org.jetbrains.annotations.NotNull;

public class Xas99RBraceMatcher extends PairedBraceMatcherAdapter {

    public Xas99RBraceMatcher() {
        super(new Xas99RPairedBraceMatcher(), Xas99RLanguage.INSTANCE);
    }

    private static class Xas99RPairedBraceMatcher implements PairedBraceMatcher {

        @Override
        public BracePair @NotNull [] getPairs() {
            return new BracePair[] {
                    new BracePair(Xas99RTypes.OP_LPAREN, Xas99RTypes.OP_RPAREN, false)
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
