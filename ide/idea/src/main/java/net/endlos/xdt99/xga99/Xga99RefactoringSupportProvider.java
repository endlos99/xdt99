package net.endlos.xdt99.xga99;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xga99.psi.Xga99OpLabel;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xga99RefactoringSupportProvider extends RefactoringSupportProvider {

    @Override
    public boolean isMemberInplaceRenameAvailable(@NotNull PsiElement element, @Nullable PsiElement context) {
        return (element instanceof Xga99Labeldef || element instanceof Xga99OpLabel) &&
                element.getText().charAt(0) != '!';
    }

}
