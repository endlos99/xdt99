package net.endlos.xdt99.xas99r;

import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import net.endlos.xdt99.xas99r.psi.Xas99RLabeldef;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99RFindUsagesProvider implements FindUsagesProvider {
//    private static final DefaultWordsScanner WORDS_SCANNER =
//            new DefaultWordsScanner(new Xas99RLexerAdapter(),
//                    TokenSet.create(Xas99RTypes.IDENT),
//                    TokenSet.create(Xas99RTypes.COMMENT, Xas99RTypes.LCOMMENT),
//                    TokenSet.create(Xas99RTypes.TEXT));

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
        if (element instanceof Xas99RLabeldef) {
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
        if (element instanceof Xas99RLabeldef) {
            return ((Xas99RLabeldef) element).getName();
        } else {
            return "";
        }
    }

    @NotNull
    @Override
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        if (element instanceof Xas99RLabeldef) {
            return ((Xas99RLabeldef) element).getName();  //TODO: return line?
        } else {
            return "";
        }
    }
}
