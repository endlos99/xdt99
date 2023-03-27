package net.endlos.xdt99.xas99.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiReference;
import net.endlos.xdt99.xas99.Xas99Icons;
import net.endlos.xdt99.xas99.Xas99Reference;
import net.endlos.xdt99.xas99.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xas99PsiImplUtil {

    public static String getName(Xas99Labeldef element) {
        return getIdentName(element);
    }

    public static String getName(Xas99OpLabel element) {
        return getIdentName(element);
    }

    public static String getName(Xas99OpAlias element) {
        return getIdentName(element);
    }

    public static String getName(Xas99OpMacrodef element) {
        return getIdentName(element);
    }

    public static String getName(Xas99OpMacro element) {
        return getIdentName(element);
    }

    public static PsiElement setName(Xas99Labeldef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            Xas99Labeldef label = Xas99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99OpLabel element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            Xas99Labeldef label = Xas99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99OpAlias element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            Xas99Labeldef label = Xas99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99OpMacrodef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            Xas99Labeldef label = Xas99ElementFactory.createLabel(element.getProject(), newName);
            ASTNode newKeyNode = label.getFirstChild().getNode();
            element.getNode().replaceChild(keyNode, newKeyNode);
        }
        return element;
    }

    public static PsiElement setName(Xas99OpMacro element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
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

    public static PsiElement getNameIdentifier(Xas99OpAlias element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xas99OpMacrodef element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xas99OpMacro element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiReference getReference(@NotNull Xas99OpLabel element) {
        return new Xas99Reference(element, TextRange.from(0, element.getTextLength()));
    }

    public static PsiReference getReference(@NotNull Xas99OpAlias element) {
        return new Xas99Reference(element, TextRange.from(0, element.getTextLength()));
    }

    public static PsiReference getReference(@NotNull Xas99OpMacro element) {
        return new Xas99Reference(element, TextRange.from(0, element.getTextLength()));
    }

    public static ItemPresentation getPresentation(final Xas99Labeldef element) {
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
                return Xas99Icons.FILE;
            }
        };
    }

    public static ItemPresentation getPresentation(final Xas99OpMacrodef element) {
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
                return Xas99Icons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        // editing local label is prevented by Xas99VetoRenameCondition;
        // introduction of local label is prevented by Xas99NamesValidator
        if (myElement instanceof Xas99Labeldef) {
            Xas99Labeldef label = (Xas99Labeldef) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xas99OpLabel) {
            Xas99OpLabel label = (Xas99OpLabel) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xas99OpAlias) {
            Xas99OpAlias alias = (Xas99OpAlias) myElement;
            alias.setName(newElementName);
        } else if (myElement instanceof Xas99OpMacrodef) {
            Xas99OpMacrodef macro = (Xas99OpMacrodef) myElement;
            macro.setName(newElementName);
        } else if (myElement instanceof Xas99OpMacro) {
            Xas99OpMacro macro = (Xas99OpMacro) myElement;
            macro.setName(newElementName);
        }
    }

    private static String getIdentName(PsiElement element) {
        ASTNode keyNode = element.getNode().findChildByType(Xas99Types.IDENT);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

}
