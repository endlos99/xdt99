package net.endlos.xdt99.xas99;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99OpLabel;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99RefactoringSupportProvider extends RefactoringSupportProvider {

    @Override
    public boolean isMemberInplaceRenameAvailable(@NotNull PsiElement element, @Nullable PsiElement context) {
        return (element instanceof Xas99Labeldef || element instanceof Xas99OpLabel) &&
                element.getText().charAt(0) != '!';
    }

}
