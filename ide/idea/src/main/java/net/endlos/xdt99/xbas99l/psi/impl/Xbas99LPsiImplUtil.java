package net.endlos.xdt99.xbas99l.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiReference;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99l.Xbas99LLabelReference;
import net.endlos.xdt99.xbas99l.psi.*;
import net.endlos.xdt99.xbas99l.Xbas99LIcons;
import net.endlos.xdt99.xbas99l.Xbas99LVarReference;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xbas99LPsiImplUtil {
    private static final String label_re = "[A-Za-z0-9_]+";
    private static final String ident_re = "[A-Za-z0-9_@\\[\\]\\\\]+";
    private static final String sident_re = "[A-Za-z0-9_@\\[\\]\\\\]+\\$";
    private static final String blanks = "                                       ";

    @NotNull
    public static String getName(Xbas99LLabeldef element) {
        return getLabelName(element, Xbas99LTypes.LIDENT);
    }

    @NotNull
    public static String getName(Xbas99LLabelref element) {
        return getLabelName(element, Xbas99LTypes.IDENT);
    }

    @NotNull
    public static String getName(Xbas99LNvarW element) {
        return getVarName(element, Xbas99LTypes.IDENT);
    }

    @NotNull
    public static String getName(Xbas99LNvarR element) {
        return getVarName(element, Xbas99LTypes.IDENT);
    }

    @NotNull
    public static String getName(Xbas99LNvarF element) {
        return getVarName(element, Xbas99LTypes.IDENT);
    }

    @NotNull
    public static String getName(Xbas99LSvarW element) {
        return getVarName(element, Xbas99LTypes.SIDENT);
    }

    @NotNull
    public static String getName(Xbas99LSvarR element) {
        return getVarName(element, Xbas99LTypes.SIDENT);
    }

    @NotNull
    public static String getName(Xbas99LSvarF element) {
        return getVarName(element, Xbas99LTypes.SIDENT);
    }

    public static PsiElement setName(Xbas99LLabeldef element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.IDENT);
    }

    public static PsiElement setName(Xbas99LLabelref element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.IDENT);
    }

    public static PsiElement setName(Xbas99LNvarW element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.IDENT);
    }

    public static PsiElement setName(Xbas99LNvarR element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.IDENT);
    }

    public static PsiElement setName(Xbas99LNvarF element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.IDENT);
    }

    public static PsiElement setName(Xbas99LSvarW element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.SIDENT);
    }

    public static PsiElement setName(Xbas99LSvarR element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.SIDENT);
    }

    public static PsiElement setName(Xbas99LSvarF element, String newName) {
        return setAnyName(element, newName, Xbas99LTypes.SIDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LLabeldef element) {
        return getAnyIdentifier(element, Xbas99LTypes.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LLabelref element) {
        return getAnyIdentifier(element, Xbas99LTypes.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LNvarW element) {
        return getAnyIdentifier(element, Xbas99LTypes.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LNvarR element) {
        return getAnyIdentifier(element, Xbas99LTypes.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LNvarF element) {
        return getAnyIdentifier(element, Xbas99LTypes.IDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LSvarW element) {
        return getAnyIdentifier(element, Xbas99LTypes.SIDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LSvarR element) {
        return getAnyIdentifier(element, Xbas99LTypes.SIDENT);
    }

    public static PsiElement getNameIdentifier(Xbas99LSvarF element) {
        return getAnyIdentifier(element, Xbas99LTypes.SIDENT);
    }

    public static PsiReference getReference(@NotNull Xbas99LLabeldef element) {
        return new Xbas99LLabelReference(element, TextRange.from(0, element.getName().trim().length()));
    }

    public static PsiReference getReference(@NotNull Xbas99LLabelref element) {
        return new Xbas99LLabelReference(element, TextRange.from(0, element.getText().trim().length()));
    }

    public static PsiReference getReference(@NotNull Xbas99LNvarW element) {
        return new Xbas99LVarReference(element, TextRange.from(0, element.getText().trim().length()), false);
    }

    public static PsiReference getReference(@NotNull Xbas99LNvarR element) {
        return new Xbas99LVarReference(element, TextRange.from(0, element.getText().trim().length()), false);
    }

    public static PsiReference getReference(@NotNull Xbas99LNvarF element) {
        return new Xbas99LVarReference(element, TextRange.from(0, element.getText().trim().length()), false);
    }

    public static PsiReference getReference(@NotNull Xbas99LSvarW element) {
        return new Xbas99LVarReference(element, TextRange.from(0, element.getText().trim().length()), true);
    }

    public static PsiReference getReference(@NotNull Xbas99LSvarR element) {
        return new Xbas99LVarReference(element, TextRange.from(0, element.getText().trim().length()), true);
    }

    public static PsiReference getReference(@NotNull Xbas99LSvarF element) {
        return new Xbas99LVarReference(element, TextRange.from(0, element.getText().trim().length()), true);
    }

    public static ItemPresentation getPresentation(final Xbas99LNamedElement element) {
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
                return Xbas99LIcons.FILE;
            }
        };
    }

    public static void rename(PsiElement myElement, String newElementName) {
        if (myElement instanceof Xbas99LLabelref && newElementName.matches(label_re)) {
            Xbas99LLabelref label = (Xbas99LLabelref) myElement;
            label.setName(newElementName);
        } else if (myElement instanceof Xbas99LNvarW && newElementName.matches(ident_re)) {
            Xbas99LNvarW nvar = (Xbas99LNvarW) myElement;
            nvar.setName(newElementName);
        } else if (myElement instanceof Xbas99LNvarR && newElementName.matches(ident_re)) {
            Xbas99LNvarR nvar = (Xbas99LNvarR) myElement;
            nvar.setName(newElementName);
        } else if (myElement instanceof Xbas99LNvarF && newElementName.matches(ident_re)) {
            Xbas99LNvarF nvar = (Xbas99LNvarF) myElement;
            nvar.setName(newElementName);
        } else if (myElement instanceof Xbas99LSvarW && newElementName.matches(sident_re)) {
            Xbas99LSvarW svar = (Xbas99LSvarW) myElement;
            svar.setName(newElementName);
        } else if (myElement instanceof Xbas99LSvarR && newElementName.matches(sident_re)) {
            Xbas99LSvarR svar = (Xbas99LSvarR) myElement;
            svar.setName(newElementName);
        } else if (myElement instanceof Xbas99LSvarF && newElementName.matches(sident_re)) {
            Xbas99LSvarF svar = (Xbas99LSvarF) myElement;
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

    private static Xbas99LNamedElement setAnyName(Xbas99LNamedElement element, String newName, IElementType type) {
        ASTNode identNode = element.getNode().findChildByType(type);
        if (identNode != null) {
            String oldName = element.getName();
            int padding = oldName.isEmpty() ? 0 : oldName.length() - oldName.trim().length();
            Xbas99LNamedElement var = Xbas99LElementFactory.createThing(element, element.getProject(),
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
