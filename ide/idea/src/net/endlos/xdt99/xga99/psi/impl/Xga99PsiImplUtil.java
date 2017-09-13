package net.endlos.xdt99.xga99.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiReference;
import net.endlos.xdt99.xga99.Xga99Icons;
import net.endlos.xdt99.xga99.Xga99Reference;
import net.endlos.xdt99.xga99.psi.Xga99ElementFactory;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import net.endlos.xdt99.xga99.psi.Xga99OpLabel;
import net.endlos.xdt99.xga99.psi.Xga99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xga99PsiImplUtil {

    public static String getName(Xga99Labeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static String getName(Xga99OpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static PsiElement setName(Xga99Labeldef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99Types.IDENT);
        if (keyNode != null) {
            Xga99Labeldef label = Xga99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xga99OpLabel element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99Types.IDENT);
        if (keyNode != null) {
            Xga99Labeldef label = Xga99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement getNameIdentifier(Xga99Labeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xga99OpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    @Nullable
    public static PsiReference getReference(@NotNull Xga99OpLabel element) {
        return new Xga99Reference(element, TextRange.from(0, element.getTextLength()));
    }

    public static ItemPresentation getPresentation(final Xga99Labeldef element) {
        return new ItemPresentation() {
            @Nullable
            @Override
            public String getPresentableText() {
                return element.getName();
            }

            @Nullable
            @Override
            public String getLocationString() {
                return element.getContainingFile().getName();
            }

            @Nullable
            @Override
            public Icon getIcon(boolean unused) {
                return Xga99Icons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        // editing local label is prevented by Xga99VetoRenameCondition;
        // introduction of local label is prevented by Xga99NamesValidator
        if (myElement instanceof Xga99Labeldef) {
            Xga99Labeldef label = (Xga99Labeldef) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xga99OpLabel) {
            Xga99OpLabel label = (Xga99OpLabel) myElement;
            label.setName(newElementName);
        }
    }

}
