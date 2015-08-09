package net.endlos.xdt99.xbas99.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiReference;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99.Xbas99Icons;
import net.endlos.xdt99.xbas99.Xbas99LineReference;
import net.endlos.xdt99.xbas99.Xbas99VarReference;
import net.endlos.xdt99.xbas99.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xbas99PsiImplUtil {

    private static final String blanks = "                                       ";

    public static String getId(PsiElement element, IElementType type) {
        ASTNode keyNode = element.getNode().findChildByType(type);
        if (keyNode != null) {
            return keyNode.getText();
        } else {
            return null;
        }
    }

    public static String getName(Xbas99Linedef element) {
        return getId(element, Xbas99Types.LNUMBER);
    }

    public static String getName(Xbas99Lino element) {
        return getId(element, Xbas99Types.NUMBER);
    }

    public static String getName(Xbas99Nvar element) {
        return getId(element, Xbas99Types.IDENT);
    }

    public static String getName(Xbas99Svar element) {
        return getId(element, Xbas99Types.SIDENT);
    }

    public static PsiElement setName(Xbas99Linedef element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xbas99Types.LNUMBER);
        if (keyNode != null) {
            Xbas99Linedef linedef = Xbas99ElementFactory.createLinedef(element.getProject(), newName);
            if (linedef != null) {
                ASTNode newKeyNode = linedef.getFirstChild().getNode();
                element.getNode().replaceChild(keyNode, newKeyNode);
            }
        }
        return element;
    }

    public static PsiElement setName(Xbas99Lino element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xbas99Types.NUMBER);
        if (keyNode != null) {
            String oldName = element.getName();
            int padding = oldName != null ? oldName.length() - oldName.trim().length() : 0;
            Xbas99Lino lino = Xbas99ElementFactory.createLino(element.getProject(),
                    newName + blanks.substring(0, padding));
            if (lino != null) {
                ASTNode newKeyNode = lino.getFirstChild().getNode();
                element.getNode().replaceChild(keyNode, newKeyNode);
            }
        }
        return element;
    }

    public static PsiElement setName(Xbas99Nvar element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xbas99Types.IDENT);
        if (keyNode != null) {
            String oldName = element.getName();
            int padding = oldName != null ? oldName.length() - oldName.trim().length() : 0;
            Xbas99Nvar var = Xbas99ElementFactory.createNvar(element.getProject(),
                    newName + blanks.substring(0, padding));
            if (var != null) {
                ASTNode newKeyNode = var.getFirstChild().getNode();
                element.getNode().replaceChild(keyNode, newKeyNode);
            }
        }
        return element;
    }

    public static PsiElement setName(Xbas99Svar element, String newName) {
        ASTNode keyNode = element.getNode().findChildByType(Xbas99Types.SIDENT);
        if (keyNode != null) {
            String oldName = element.getName();
            int padding = oldName != null ? oldName.length() - oldName.trim().length() : 0;
            Xbas99Svar var = Xbas99ElementFactory.createSvar(element.getProject(),
                    newName + blanks.substring(0, padding));
            if (var != null) {
                ASTNode newKeyNode = var.getFirstChild().getNode();
                element.getNode().replaceChild(keyNode, newKeyNode);
            }
        }
        return element;
    }

    public static PsiElement getIdentifier(PsiElement element, IElementType type) {
        ASTNode keyNode = element.getNode().findChildByType(type);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

    public static PsiElement getNameIdentifier(Xbas99Linedef element) {
        return getIdentifier(element, Xbas99Types.LNUMBER);
    }

    public static PsiElement getNameIdentifier(Xbas99Lino element) {
        return getIdentifier(element, Xbas99Types.NUMBER);
    }

    public static PsiElement getNameIdentifier(Xbas99Nvar element) {
        return getIdentifier(element, Xbas99Types.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99Svar element) {
        return getIdentifier(element, Xbas99Types.SIDENT);
    }

    @Nullable
    public static PsiReference getReference(@NotNull Xbas99Lino element) {
        return new Xbas99LineReference(element, TextRange.from(0, element.getText().trim().length()));
    }

    @Nullable
    public static PsiReference getReference(@NotNull Xbas99Nvar element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), false);
    }

    @Nullable
    public static PsiReference getReference(@NotNull Xbas99Svar element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), true);
    }

    public static ItemPresentation getPresentation(final Xbas99NamedElement element) {
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
                return Xbas99Icons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        if (myElement instanceof Xbas99Lino &&
                newElementName.matches("\\d+")) {
            Xbas99Lino lino = (Xbas99Lino) myElement;
            lino.setName(newElementName);
        } else if (myElement instanceof Xbas99Nvar &&
                newElementName.matches("[A-Za-z0-9_@\\[\\]\\\\]+")) {
            Xbas99Nvar nvar = (Xbas99Nvar) myElement;
            nvar.setName(newElementName);
        } else if (myElement instanceof Xbas99Svar &&
                newElementName.matches("[A-Za-z0-9_@\\[\\]\\\\]+\\$")) {
            Xbas99Svar svar = (Xbas99Svar) myElement;
            svar.setName(newElementName);
        }
    }

}
