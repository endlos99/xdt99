package net.endlos.xdt99.xbas99;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xbas99.psi.Xbas99Linedef;
import net.endlos.xdt99.xbas99.psi.Xbas99Nvar;
import net.endlos.xdt99.xbas99.psi.Xbas99Svar;

public class Xbas99RefactoringSupportProvider extends RefactoringSupportProvider {
    @Override
    public boolean isMemberInplaceRenameAvailable(PsiElement element, PsiElement context) {
        return element instanceof Xbas99Linedef ||
                element instanceof Xbas99Nvar ||
                element instanceof Xbas99Svar;
    }
}
