package net.endlos.xdt99.xbas99;

import com.intellij.lang.cacheBuilder.DefaultWordsScanner;
import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xbas99.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xbas99FindUsagesProvider implements FindUsagesProvider {

    @Override
    @Nullable
    public WordsScanner getWordsScanner() {
        return new DefaultWordsScanner(new Xbas99LexerAdapter(),
                TokenSet.create(Xbas99Types.IDENT, Xbas99Types.SIDENT),  // identifiers
                TokenSet.create(Xbas99Types.COMMENT),  // comments
                TokenSet.create(Xbas99Types.QSTRING, Xbas99Types.NUMBER, Xbas99Types.FLOAT));  // literals
    }

    @Override
    public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
        return psiElement instanceof Xbas99NamedElement;
    }

    @Override
    @Nullable
    public String getHelpId(@NotNull PsiElement psiElement) {
        return null;
    }

    @Override
    @NotNull
    public String getType(@NotNull PsiElement element) {
        if (element instanceof Xbas99Linedef || element instanceof Xbas99Lino) {
            return "BASIC line number";
        }
        if (element instanceof Xbas99NvarW || element instanceof Xbas99NvarR) {
            return "BASIC numerical variable";
        }
        if (element instanceof Xbas99SvarW || element instanceof Xbas99SvarR) {
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
        if (element instanceof Xbas99Linedef) {
            return ((Xbas99Linedef) element).getName();
        }
        if (element instanceof Xbas99Lino) {
            return ((Xbas99Lino) element).getName();
        }
        if (element instanceof Xbas99NvarW) {
            return ((Xbas99NvarW) element).getName();
        }
        if (element instanceof Xbas99NvarR) {
            return ((Xbas99NvarR) element).getName();
        }
        if (element instanceof Xbas99SvarW) {
            return ((Xbas99SvarW) element).getName();
        }
        if (element instanceof Xbas99SvarR) {
            return ((Xbas99SvarR) element).getName();
        }
        return "";
    }

}