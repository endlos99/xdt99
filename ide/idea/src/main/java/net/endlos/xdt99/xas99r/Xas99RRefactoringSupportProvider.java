package net.endlos.xdt99.xas99r;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xas99r.psi.Xas99RLabeldef;
import net.endlos.xdt99.xas99r.psi.Xas99ROpAlias;
import net.endlos.xdt99.xas99r.psi.Xas99ROpLabel;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99RRefactoringSupportProvider extends RefactoringSupportProvider {

    @Override
    public boolean isMemberInplaceRenameAvailable(@NotNull PsiElement element, @Nullable PsiElement context) {
        return (element instanceof Xas99RLabeldef ||
                element instanceof Xas99ROpLabel ||
                element instanceof Xas99ROpAlias) &&
                element.getText().charAt(0) != '!';
    }

}
