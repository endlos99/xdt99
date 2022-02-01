package net.endlos.xdt99.xas99r.psi.impl;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xas99r.psi.Xas99RNamedElement;
import org.jetbrains.annotations.NotNull;

public abstract class Xas99RNamedElementImpl extends ASTWrapperPsiElement implements Xas99RNamedElement {

    public Xas99RNamedElementImpl(@NotNull ASTNode node) {
        super(node);
    }

}
