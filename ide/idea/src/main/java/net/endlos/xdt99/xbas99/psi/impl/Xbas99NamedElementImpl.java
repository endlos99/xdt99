package net.endlos.xdt99.xbas99.psi.impl;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import com.intellij.openapi.util.NlsSafe;
import net.endlos.xdt99.xbas99.psi.Xbas99NamedElement;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public abstract class Xbas99NamedElementImpl extends ASTWrapperPsiElement implements Xbas99NamedElement {
    public Xbas99NamedElementImpl(@NotNull ASTNode node) {
        super(node);
    }
}
