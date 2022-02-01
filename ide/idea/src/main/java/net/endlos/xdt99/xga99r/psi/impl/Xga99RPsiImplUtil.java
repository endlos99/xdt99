package net.endlos.xdt99.xga99r.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiReference;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import net.endlos.xdt99.xga99r.psi.Xga99ROpLabel;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import net.endlos.xdt99.xga99r.Xga99RReference;
import net.endlos.xdt99.xga99r.psi.Xga99RElementFactory;
import net.endlos.xdt99.xga99r.Xga99RIcons;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xga99RPsiImplUtil {

    public static String getName(Xga99RLabeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static String getName(Xga99ROpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static PsiElement setName(Xga99RLabeldef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99RTypes.IDENT);
        if (keyNode != null) {
            Xga99RLabeldef label = Xga99RElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xga99ROpLabel element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99RTypes.IDENT);
        if (keyNode != null) {
            Xga99RLabeldef label = Xga99RElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement getNameIdentifier(Xga99RLabeldef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xga99ROpLabel element) {
        ASTNode keyNode = element.getNode().findChildByType(Xga99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiReference getReference(@NotNull Xga99ROpLabel element) {
        return new Xga99RReference(element, TextRange.from(0, element.getTextLength()));
    }

    public static ItemPresentation getPresentation(final Xga99RLabeldef element) {
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
            @Nullable
            public Icon getIcon(boolean unused) {
                return Xga99RIcons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        // editing local label is prevented by Xga99RVetoRenameCondition;
        // introduction of local label is prevented by Xga99RNamesValidator
        if (myElement instanceof Xga99RLabeldef) {
            Xga99RLabeldef label = (Xga99RLabeldef) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xga99ROpLabel) {
            Xga99ROpLabel label = (Xga99ROpLabel) myElement;
            label.setName(newElementName);
        }
    }

}
