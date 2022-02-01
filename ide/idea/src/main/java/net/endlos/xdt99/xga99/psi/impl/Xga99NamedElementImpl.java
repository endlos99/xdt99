package net.endlos.xdt99.xga99.psi.impl;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xga99.psi.Xga99NamedElement;
import org.jetbrains.annotations.NotNull;

public abstract class Xga99NamedElementImpl extends ASTWrapperPsiElement implements Xga99NamedElement {

    public Xga99NamedElementImpl(@NotNull ASTNode node) {
        super(node);
    }

}
