package net.endlos.xdt99.xbas99;

import com.intellij.lang.cacheBuilder.DefaultWordsScanner;
import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.lexer.FlexAdapter;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xbas99.psi.Xbas99Linedef;
import net.endlos.xdt99.xbas99.psi.Xbas99Nvar;
import net.endlos.xdt99.xbas99.psi.Xbas99Svar;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.io.Reader;

public class Xbas99FindUsagesProvider implements FindUsagesProvider {
    private static final DefaultWordsScanner WORDS_SCANNER =
            new DefaultWordsScanner(new FlexAdapter(new Xbas99Lexer((Reader) null)),
                    TokenSet.create(Xbas99Types.IDENT, Xbas99Types.SIDENT),
                    TokenSet.create(Xbas99Types.COMMENT),
                    TokenSet.EMPTY);

    @Nullable
    @Override
    public WordsScanner getWordsScanner() {
        return null; // disabled WORDS_SCANNER;
    }

    @Override
    public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
        return psiElement instanceof PsiNamedElement;
    }

    @Nullable
    @Override
    public String getHelpId(@NotNull PsiElement psiElement) {
        return null;
    }

    @NotNull
    @Override
    public String getType(@NotNull PsiElement element) {
        if (element instanceof Xbas99Linedef) {
            return "BASIC line number";
        } if (element instanceof Xbas99Nvar) {
            return "BASIC numerical variable";
        } if (element instanceof Xbas99Svar) {
            return "BASIC string variable";
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getDescriptiveName(@NotNull PsiElement element) {
        return getNodeText(element, true);
    }

    @NotNull
    @Override
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        if (element instanceof Xbas99Linedef) {
            return ((Xbas99Linedef) element).getName();
        } else if (element instanceof Xbas99Nvar) {
            return ((Xbas99Nvar) element).getName();
        } else if (element instanceof Xbas99Svar) {
            return ((Xbas99Svar) element).getName();
        } else {
            return "";
        }
    }
}