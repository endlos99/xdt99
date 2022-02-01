package net.endlos.xdt99.xbas99;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xbas99.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xbas99RefactoringSupportProvider extends RefactoringSupportProvider {

    @Override
    public boolean isMemberInplaceRenameAvailable(@NotNull PsiElement element, @Nullable PsiElement context) {
        return element instanceof Xbas99Linedef ||
               element instanceof Xbas99Lino ||
               element instanceof Xbas99NvarW ||
               element instanceof Xbas99NvarR ||
               element instanceof Xbas99SvarW ||
               element instanceof Xbas99SvarR;
    }

}
