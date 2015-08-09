package net.endlos.xdt99.xas99.psi.impl;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xas99.psi.Xas99NamedElement;
import org.jetbrains.annotations.NotNull;

public abstract class Xas99NamedElementImpl extends ASTWrapperPsiElement implements Xas99NamedElement {
    public Xas99NamedElementImpl(@NotNull ASTNode node) {
        super(node);
    }
}
