package net.endlos.xdt99.xas99r.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiReference;
import net.endlos.xdt99.xas99r.psi.Xas99RLabeldef;
import net.endlos.xdt99.xas99r.psi.Xas99ROpLabel;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import net.endlos.xdt99.xas99r.Xas99RIcons;
import net.endlos.xdt99.xas99r.Xas99RReference;
import net.endlos.xdt99.xas99r.psi.Xas99RElementFactory;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xas99RPsiImplUtil {

    public static String getName(Xas99RLabeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static String getName(Xas99ROpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static PsiElement setName(Xas99RLabeldef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            Xas99RLabeldef label = Xas99RElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99ROpLabel element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            Xas99RLabeldef label = Xas99RElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement getNameIdentifier(Xas99RLabeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xas99ROpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiReference getReference(@NotNull Xas99ROpLabel element) {
        return new Xas99RReference(element, TextRange.from(0, element.getTextLength()));
    }

    public static ItemPresentation getPresentation(final Xas99RLabeldef element) {
        return new ItemPresentation() {
            @Override
            @Nullable
            public String getPresentableText() {
                return element.getName();
            }

            @Override
            @Nullable
            public String getLocationString() {
                PsiFile containingFile = element.getContainingFile();
                return containingFile == null ? null : containingFile.getName();
            }

            @Override
            public Icon getIcon(boolean unused) {
                return Xas99RIcons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        // editing local label is prevented by Xas99RVetoRenameCondition;
        // introduction of local label is prevented by Xas99RNamesValidator
        if (myElement instanceof Xas99RLabeldef) {
            Xas99RLabeldef label = (Xas99RLabeldef) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xas99ROpLabel) {
            Xas99ROpLabel label = (Xas99ROpLabel) myElement;
            label.setName(newElementName);
        }
    }

}
