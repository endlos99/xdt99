package net.endlos.xdt99.xbas99.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
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
    private static final String lino_re = "\\d+";
    private static final String ident_re = "[A-Za-z0-9_@\\[\\]\\\\]+";
    private static final String sident_re = "[A-Za-z0-9_@\\[\\]\\\\]+\\$";
    private static final String blanks = "                                       ";

    @NotNull
    public static String getName(Xbas99Linedef element) {
        return getLabelName(element, Xbas99Types.LNUMBER);
    }

    @NotNull
    public static String getName(Xbas99Lino element) {
        return getLabelName(element, Xbas99Types.NUMBER);
    }

    @NotNull
    public static String getName(Xbas99NvarW element) {
        return getVarName(element, Xbas99Types.IDENT);
    }

    @NotNull
    public static String getName(Xbas99NvarR element) {
        return getVarName(element, Xbas99Types.IDENT);
    }

    @NotNull
    public static String getName(Xbas99NvarF element) {
        return getVarName(element, Xbas99Types.IDENT);
    }

    @NotNull
    public static String getName(Xbas99SvarW element) {
        return getVarName(element, Xbas99Types.SIDENT);
    }

    @NotNull
    public static String getName(Xbas99SvarR element) {
        return getVarName(element, Xbas99Types.SIDENT);
    }

    @NotNull
    public static String getName(Xbas99SvarF element) {
        return getVarName(element, Xbas99Types.SIDENT);
    }

    public static PsiElement setName(Xbas99Linedef element, String newName) {
        return setAnyName(element, newName, Xbas99Types.IDENT);
    }

    public static PsiElement setName(Xbas99Lino element, String newName) {
        return setAnyName(element, newName, Xbas99Types.IDENT);
    }

    public static PsiElement setName(Xbas99NvarW element, String newName) {
        return setAnyName(element, newName, Xbas99Types.IDENT);
    }

    public static PsiElement setName(Xbas99NvarR element, String newName) {
        return setAnyName(element, newName, Xbas99Types.IDENT);
    }

    public static PsiElement setName(Xbas99NvarF element, String newName) {
        return setAnyName(element, newName, Xbas99Types.IDENT);
    }

    public static PsiElement setName(Xbas99SvarW element, String newName) {
        return setAnyName(element, newName, Xbas99Types.SIDENT);
    }

    public static PsiElement setName(Xbas99SvarR element, String newName) {
        return setAnyName(element, newName, Xbas99Types.SIDENT);
    }

    public static PsiElement setName(Xbas99SvarF element, String newName) {
        return setAnyName(element, newName, Xbas99Types.SIDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99Linedef element) {
        return getAnyIdentifier(element, Xbas99Types.LNUMBER);
    }

    public static PsiElement getNameIdentifier(Xbas99Lino element) {
        return getAnyIdentifier(element, Xbas99Types.NUMBER);
    }

    public static PsiElement getNameIdentifier(Xbas99NvarW element) {
        return getAnyIdentifier(element, Xbas99Types.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99NvarR element) {
        return getAnyIdentifier(element, Xbas99Types.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99NvarF element) {
        return getAnyIdentifier(element, Xbas99Types.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99SvarW element) {
        return getAnyIdentifier(element, Xbas99Types.SIDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99SvarR element) {
        return getAnyIdentifier(element, Xbas99Types.SIDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99SvarF element) {
        return getAnyIdentifier(element, Xbas99Types.SIDENT);
    }

    public static PsiReference getReference(@NotNull Xbas99Lino element) {
        return new Xbas99LineReference(element, TextRange.from(0, element.getText().trim().length()));
    }

    public static PsiReference getReference(@NotNull Xbas99NvarW element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), false);
    }

    public static PsiReference getReference(@NotNull Xbas99NvarR element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), false);
    }

    public static PsiReference getReference(@NotNull Xbas99NvarF element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), false);
    }

    public static PsiReference getReference(@NotNull Xbas99SvarW element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), true);
    }

    public static PsiReference getReference(@NotNull Xbas99SvarR element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), true);
    }

    public static PsiReference getReference(@NotNull Xbas99SvarF element) {
        return new Xbas99VarReference(element, TextRange.from(0, element.getText().trim().length()), true);
    }

    public static ItemPresentation getPresentation(final Xbas99NamedElement element) {
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
                return Xbas99Icons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        if (myElement instanceof Xbas99Lino && newElementName.matches(lino_re)) {
            Xbas99Lino lino = (Xbas99Lino) myElement;
            lino.setName(newElementName);
        } else if (myElement instanceof Xbas99NvarW && newElementName.matches(ident_re)) {
            Xbas99NvarW nvar = (Xbas99NvarW) myElement;
            nvar.setName(newElementName);
        } else if (myElement instanceof Xbas99NvarR && newElementName.matches(ident_re)) {
            Xbas99NvarR nvar = (Xbas99NvarR) myElement;
            nvar.setName(newElementName);
        } else if (myElement instanceof Xbas99NvarF && newElementName.matches(ident_re)) {
            Xbas99NvarF nvar = (Xbas99NvarF) myElement;
            nvar.setName(newElementName);
        } else if (myElement instanceof Xbas99SvarW && newElementName.matches(sident_re)) {
            Xbas99SvarW svar = (Xbas99SvarW) myElement;
            svar.setName(newElementName);
        } else if (myElement instanceof Xbas99SvarR && newElementName.matches(sident_re)) {
            Xbas99SvarR svar = (Xbas99SvarR) myElement;
            svar.setName(newElementName);
        } else if (myElement instanceof Xbas99SvarF && newElementName.matches(sident_re)) {
            Xbas99SvarF svar = (Xbas99SvarF) myElement;
            svar.setName(newElementName);
        }
    }

    @NotNull
    private static String getLabelName(PsiElement element, IElementType type) {
        ASTNode keyNode = element.getNode().findChildByType(type);
        if (keyNode == null)
            return "";
        return keyNode.getText();
    }

    @NotNull
    private static String getVarName(PsiElement element, IElementType type) {
        ASTNode keyNode = element.getNode().findChildByType(type);
        if (keyNode == null)
            return "";
        String name = keyNode.getText();
        int arrayIndex = name.indexOf('(');  // not part of simple variable
        if (arrayIndex > 0)
            return name.substring(0, arrayIndex);
        return name;
    }

    private static Xbas99NamedElement setAnyName(Xbas99NamedElement element, String newName, IElementType type) {
        ASTNode identNode = element.getNode().findChildByType(type);
        if (identNode != null) {
            String oldName = element.getName();
            int padding = oldName.isEmpty() ? 0 : oldName.length() - oldName.trim().length();
            Xbas99NamedElement var = Xbas99ElementFactory.createThing(element, element.getProject(),
                    newName + blanks.substring(0, padding));
            if (var != null) {
                ASTNode newKeyNode = var.getFirstChild().getNode();
                element.getNode().replaceChild(identNode, newKeyNode);
            }
        }
        return element;
    }

    private static PsiElement getAnyIdentifier(PsiElement element, IElementType type) {
        ASTNode keyNode = element.getNode().findChildByType(type);
        if (keyNode != null) {
            return keyNode.getPsi();
        } else {
            return null;
        }
    }

}
