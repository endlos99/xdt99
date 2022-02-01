package net.endlos.xdt99.xga99r.psi.impl;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xga99r.psi.Xga99RNamedElement;
import org.jetbrains.annotations.NotNull;

public abstract class Xga99RNamedElementImpl extends ASTWrapperPsiElement implements Xga99RNamedElement {

    public Xga99RNamedElementImpl(@NotNull ASTNode node) {
        super(node);
    }

}
