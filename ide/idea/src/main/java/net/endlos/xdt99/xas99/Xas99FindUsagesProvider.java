package net.endlos.xdt99.xas99;

import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99FindUsagesProvider implements FindUsagesProvider {

    @Override
    @Nullable
    public WordsScanner getWordsScanner() {
        return null;
    }

    @Override
    public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
        return psiElement instanceof PsiNamedElement;
    }

    @Override
    @Nullable
    public String getHelpId(@NotNull PsiElement psiElement) {
        return null;
    }

    @Override
    @NotNull
    public String getType(@NotNull PsiElement element) {
        if (element instanceof Xas99Labeldef) {
            if (element.getText().charAt(0) == '!')
                return "Assembly local label";
            else
                return "Assembly label";
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getDescriptiveName(@NotNull PsiElement element) {
        if (element instanceof Xas99Labeldef) {
            return ((Xas99Labeldef) element).getName();
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        if (element instanceof Xas99Labeldef) {
            return ((Xas99Labeldef) element).getName();  //TODO: return line?
        } else {
            return "";
        }
    }
}
