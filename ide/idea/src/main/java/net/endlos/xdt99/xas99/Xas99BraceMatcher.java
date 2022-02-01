package net.endlos.xdt99.xas99;

import com.intellij.codeInsight.highlighting.PairedBraceMatcherAdapter;
import com.intellij.lang.BracePair;
import com.intellij.lang.PairedBraceMatcher;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;

public class Xas99BraceMatcher extends PairedBraceMatcherAdapter {

    public Xas99BraceMatcher() {
        super(new Xas99PairedBraceMatcher(), Xas99Language.INSTANCE);
    }

    private static class Xas99PairedBraceMatcher implements PairedBraceMatcher {

        @Override
        public BracePair @NotNull [] getPairs() {
            return new BracePair[] {
                    new BracePair(Xas99Types.OP_LPAREN, Xas99Types.OP_RPAREN, false)
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
