package net.endlos.xdt99.xas99;

import com.intellij.lang.cacheBuilder.DefaultWordsScanner;
import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99FindUsagesProvider implements FindUsagesProvider {
//    private static final DefaultWordsScanner WORDS_SCANNER =
//            new DefaultWordsScanner(new Xas99LexerAdapter(),
//                    TokenSet.create(Xas99Types.IDENT),
//                    TokenSet.create(Xas99Types.COMMENT, Xas99Types.LCOMMENT),
//                    TokenSet.create(Xas99Types.TEXT));

    @Override
    @Nullable
    public WordsScanner getWordsScanner() {
        return null;  // not needed
    }

    @Override
    public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
        return psiElement instanceof PsiNamedElement;
    }

    @Override
    @Nullable
    public String getHelpId(@NotNull PsiElement psiElement) {
        return null;
    }

    @Override
    @NotNull
    public String getType(@NotNull PsiElement element) {
        if (element instanceof Xas99Labeldef) {
            if (element.getText().charAt(0) == '!')
                return "Assembly local label";
            else
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
            return ((Xas99Labeldef) element).getName();  //TODO: return line?
        } else {
            return "";
        }
    }
}
