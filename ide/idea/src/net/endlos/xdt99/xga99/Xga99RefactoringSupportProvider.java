package net.endlos.xdt99.xga99;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;

public class Xga99RefactoringSupportProvider extends RefactoringSupportProvider {
    @Override
    public boolean isMemberInplaceRenameAvailable(PsiElement element, PsiElement context) {
        return element instanceof Xga99Labeldef &&
                element.getText().charAt(0) != '!';
    }
}
