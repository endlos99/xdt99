package net.endlos.xdt99.xga99;

import com.intellij.openapi.util.Condition;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import net.endlos.xdt99.xga99.psi.Xga99OpLabel;

public class Xga99VetoRenameCondition implements Condition<PsiElement> {
    public boolean value(final PsiElement element) {
        return (element instanceof Xga99Labeldef || element instanceof Xga99OpLabel) &&
                element.getText().charAt(0) == '!';
    }
}
