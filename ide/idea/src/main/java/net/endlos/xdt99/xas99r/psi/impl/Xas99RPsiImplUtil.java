package net.endlos.xdt99.xas99r.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiReference;
import net.endlos.xdt99.xas99r.psi.*;
import net.endlos.xdt99.xas99r.Xas99RIcons;
import net.endlos.xdt99.xas99r.Xas99RReference;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xas99RPsiImplUtil {

    public static String getName(Xas99RLabeldef element) {
        return getIdentName(element);
    }

    public static String getName(Xas99ROpLabel element) {
        return getIdentName(element);
    }

    public static String getName(Xas99ROpAlias element) {
        return getIdentName(element);
    }

    public static String getName(Xas99ROpMacrodef element) {
        return getIdentName(element);
    }

    public static String getName(Xas99ROpMacro element) {
        return getIdentName(element);
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

    public static PsiElement setName(Xas99ROpAlias element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            Xas99RLabeldef label = Xas99RElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99ROpMacrodef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            Xas99RLabeldef label = Xas99RElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99ROpMacro element, String newName) {
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

    public static PsiElement getNameIdentifier(Xas99ROpAlias element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xas99ROpMacrodef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xas99ROpMacro element) {
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

    public static PsiReference getReference(@NotNull Xas99ROpAlias element) {
        return new Xas99RReference(element, TextRange.from(0, element.getTextLength()));
    }

    public static PsiReference getReference(@NotNull Xas99ROpMacro element) {
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

    public static ItemPresentation getPresentation(final Xas99ROpMacrodef element) {
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
        } else if (myElement instanceof Xas99ROpAlias) {
            Xas99ROpAlias label = (Xas99ROpAlias) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xas99ROpMacrodef) {
            Xas99ROpMacrodef macro = (Xas99ROpMacrodef) myElement;
            macro.setName(newElementName);
        } else if (myElement instanceof Xas99ROpMacro) {
            Xas99ROpMacro macro = (Xas99ROpMacro) myElement;
            macro.setName(newElementName);
        }
    }

    private static String getIdentName(PsiElement element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99RTypes.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

}
