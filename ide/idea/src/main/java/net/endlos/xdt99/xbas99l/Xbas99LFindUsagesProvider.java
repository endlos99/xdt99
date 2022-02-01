package net.endlos.xdt99.xbas99l;

import com.intellij.lang.cacheBuilder.DefaultWordsScanner;
import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xbas99l.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xbas99LFindUsagesProvider implements FindUsagesProvider {

    @Override
    @Nullable
    public WordsScanner getWordsScanner() {
        return new DefaultWordsScanner(new Xbas99LLexerAdapter(),
                TokenSet.create(Xbas99LTypes.IDENT, Xbas99LTypes.SIDENT),  // identifiers
                TokenSet.create(Xbas99LTypes.COMMENT),  // comments
                TokenSet.create(Xbas99LTypes.QSTRING, Xbas99LTypes.NUMBER, Xbas99LTypes.FLOAT));  // literals
    }

    @Override
    public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
        return psiElement instanceof Xbas99LNamedElement;
    }

    @Override
    @Nullable
    public String getHelpId(@NotNull PsiElement psiElement) {
        return null;
    }

    @Override
    @NotNull
    public String getType(@NotNull PsiElement element) {
        if (element instanceof Xbas99LLabeldef || element instanceof Xbas99LLabelref) {
            return "BASIC label";
        }
        if (element instanceof Xbas99LNvarW || element instanceof Xbas99LNvarR) {
            return "BASIC numerical variable";
        }
        if (element instanceof Xbas99LSvarW || element instanceof Xbas99LSvarR) {
            return "BASIC string variable";
        }
        return "";
    }

    @Override
    @NotNull
    public String getDescriptiveName(@NotNull PsiElement element) {
        return getNodeText(element, true);
    }

    @Override
    @NotNull
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        if (element instanceof Xbas99LLabeldef) {
            return ((Xbas99LLabeldef) element).getName();
        }
        if (element instanceof Xbas99LLabelref) {
            return ((Xbas99LLabelref) element).getName();
        }
        if (element instanceof Xbas99LNvarW) {
            return ((Xbas99LNvarW) element).getName();
        }
        if (element instanceof Xbas99LNvarR) {
            return ((Xbas99LNvarR) element).getName();
        }
        if (element instanceof Xbas99LSvarW) {
            return ((Xbas99LSvarW) element).getName();
        }
        if (element instanceof Xbas99LSvarR) {
            return ((Xbas99LSvarR) element).getName();
        }
        return "";
    }

}