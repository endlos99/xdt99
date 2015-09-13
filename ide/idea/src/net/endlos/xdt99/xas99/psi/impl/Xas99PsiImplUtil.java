package net.endlos.xdt99.xas99.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiReference;
import net.endlos.xdt99.xas99.Xas99Icons;
import net.endlos.xdt99.xas99.Xas99Reference;
import net.endlos.xdt99.xas99.psi.Xas99ElementFactory;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99OpLabel;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xas99PsiImplUtil {

    public static String getName(Xas99Labeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static String getName(Xas99OpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static PsiElement setName(Xas99Labeldef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null && element.getText().charAt(0) != '!') {
            Xas99Labeldef label = Xas99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99OpLabel element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null && element.getText().charAt(0) != '!') {
            Xas99Labeldef label = Xas99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement getNameIdentifier(Xas99Labeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xas99OpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    @Nullable
    public static PsiReference getReference(@NotNull Xas99OpLabel element) {
        return new Xas99Reference(element, TextRange.from(0, element.getTextLength()));
    }

    public static ItemPresentation getPresentation(final Xas99Labeldef element) {
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
                return Xas99Icons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        // renaming/introduction of local label is prevented by Xas99NamesValidator;
        // change of local label to global label is prevented by Xas99RefactoringSupportProvider
        if (myElement instanceof Xas99Labeldef) {
            Xas99Labeldef label = (Xas99Labeldef) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xas99OpLabel &&
                myElement.getText().charAt(0) != '!') {
            Xas99OpLabel label = (Xas99OpLabel) myElement;
            label.setName(newElementName);
        }
    }

}
