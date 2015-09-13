package net.endlos.xdt99.xas99;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;

public class Xas99RefactoringSupportProvider extends RefactoringSupportProvider {
    @Override
    public boolean isMemberInplaceRenameAvailable(PsiElement element, PsiElement context) {
        return element instanceof Xas99Labeldef &&
                element.getText().charAt(0) != '!';
    }
}
