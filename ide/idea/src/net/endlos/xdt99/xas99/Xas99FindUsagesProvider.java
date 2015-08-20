package net.endlos.xdt99.xas99;

import com.intellij.lang.cacheBuilder.DefaultWordsScanner;
import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.lexer.FlexAdapter;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.io.Reader;

public class Xas99FindUsagesProvider implements FindUsagesProvider {
    private static final DefaultWordsScanner WORDS_SCANNER =
            new DefaultWordsScanner(new FlexAdapter(new Xas99Lexer((Reader) null)),
                    TokenSet.create(Xas99Types.LABELDEF), TokenSet.create(Xas99Types.COMMENT), TokenSet.EMPTY); //TODO

    @Nullable
    @Override
    public WordsScanner getWordsScanner() {
        return WORDS_SCANNER;
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
        if (element instanceof Xas99Labeldef) {
            return "Assembly label";
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getDescriptiveName(@NotNull PsiElement element) {
        if (element instanceof Xas99Labeldef) {
            return ((Xas99Labeldef) element).getName();
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        if (element instanceof Xas99Labeldef) {
            return ((Xas99Labeldef) element).getName();
        } else {
            return "";
        }
    }
}