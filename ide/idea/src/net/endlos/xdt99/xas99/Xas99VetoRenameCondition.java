package net.endlos.xdt99.xas99;

import com.intellij.openapi.util.Condition;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99OpLabel;

public class Xas99VetoRenameCondition implements Condition<PsiElement> {
    public boolean value(final PsiElement element) {
        return (element instanceof Xas99Labeldef || element instanceof Xas99OpLabel) &&
                element.getText().charAt(0) == '!';
    }
}
