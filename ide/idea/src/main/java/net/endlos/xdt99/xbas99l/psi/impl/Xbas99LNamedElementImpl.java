package net.endlos.xdt99.xbas99l.psi.impl;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import net.endlos.xdt99.xbas99l.psi.Xbas99LNamedElement;
import org.jetbrains.annotations.NotNull;

public abstract class Xbas99LNamedElementImpl extends ASTWrapperPsiElement implements Xbas99LNamedElement {
    public Xbas99LNamedElementImpl(@NotNull ASTNode node) {
        super(node);
    }
}
