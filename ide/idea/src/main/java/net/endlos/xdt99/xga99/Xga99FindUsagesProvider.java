package net.endlos.xdt99.xga99;

import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xga99FindUsagesProvider implements FindUsagesProvider {

    @Nullable
    @Override
    public WordsScanner getWordsScanner() {
        return null;
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
        if (element instanceof Xga99Labeldef) {
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
        if (element instanceof Xga99Labeldef) {
            return ((Xga99Labeldef) element).getName();
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        if (element instanceof Xga99Labeldef) {
            return ((Xga99Labeldef) element).getName();
        } else {
            return "";
        }
    }

}
