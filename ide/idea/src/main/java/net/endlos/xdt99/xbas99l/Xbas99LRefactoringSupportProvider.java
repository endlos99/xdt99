package net.endlos.xdt99.xbas99l;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xbas99l.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xbas99LRefactoringSupportProvider extends RefactoringSupportProvider {

    @Override
    public boolean isMemberInplaceRenameAvailable(@NotNull PsiElement element, @Nullable PsiElement context) {
        return element instanceof Xbas99LLabeldef ||
               element instanceof Xbas99LLabelref ||
               element instanceof Xbas99LNvarW ||
               element instanceof Xbas99LNvarR ||
               element instanceof Xbas99LSvarW ||
               element instanceof Xbas99LSvarR;
    }

}
