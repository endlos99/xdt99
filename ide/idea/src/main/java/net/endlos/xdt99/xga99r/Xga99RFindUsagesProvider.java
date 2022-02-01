package net.endlos.xdt99.xga99r;

import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xga99RFindUsagesProvider implements FindUsagesProvider {
//    private static final DefaultWordsScanner WORDS_SCANNER =
//            new DefaultWordsScanner(new Xga99RLexerAdapter(),
//                    TokenSet.create(Xga99RTypes.IDENT),
//                    TokenSet.create(Xga99RTypes.COMMENT, Xga99RTypes.LCOMMENT),
//                    TokenSet.create(Xga99RTypes.TEXT));

    @Nullable
    @Override
    public WordsScanner getWordsScanner() {
        return null;  // not needed
    }

    @Override
    public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
        return psiElement instanceof PsiNamedElement;
    }

    @Nullable
    @Override
    public String getHelpId(@NotNull PsiElement psiElement) {
        return null;
    }

    @NotNull
    @Override
    public String getType(@NotNull PsiElement element) {
        if (element instanceof Xga99RLabeldef) {
            if (element.getText().charAt(0) == '!')
                return "GPL local label";
            else
                return "GPL label";
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getDescriptiveName(@NotNull PsiElement element) {
        if (element instanceof Xga99RLabeldef) {
            return ((Xga99RLabeldef) element).getName();
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        if (element instanceof Xga99RLabeldef) {
            return ((Xga99RLabeldef) element).getName();
        } else {
            return "";
        }
    }

}
