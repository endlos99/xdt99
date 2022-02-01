package net.endlos.xdt99.xbas99l;

import com.intellij.codeInsight.highlighting.PairedBraceMatcherAdapter;
import com.intellij.lang.BracePair;
import com.intellij.lang.PairedBraceMatcher;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99l.psi.Xbas99LTypes;
import org.jetbrains.annotations.NotNull;

public class Xbas99LBraceMatcher extends PairedBraceMatcherAdapter {

    public Xbas99LBraceMatcher() {
        super(new Xbas99LPairedBraceMatcher(), Xbas99LLanguage.INSTANCE);
    }

    private static class Xbas99LPairedBraceMatcher implements PairedBraceMatcher {

        @Override
        public BracePair @NotNull [] getPairs() {
            return new BracePair[] {
                    new BracePair(Xbas99LTypes.OP_LPAREN, Xbas99LTypes.OP_RPAREN, false)
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
