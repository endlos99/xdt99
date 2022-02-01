package net.endlos.xdt99.xbas99;

import com.intellij.codeInsight.completion.CompletionUtilCore;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xbas99.psi.Xbas99Linedef;
import net.endlos.xdt99.xbas99.psi.impl.Xbas99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xbas99LineReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String lineNumber;

    public Xbas99LineReference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        lineNumber = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset());
    }

    // highlighting occurrences

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        final List<Xbas99Linedef> linedefs = Xbas99Util.findLinedefs(myElement, lineNumber, false);
        for (Xbas99Linedef linedef : linedefs) {
            results.add(new PsiElementResolveResult(linedef));
        }
        return results.toArray(new ResolveResult[results.size()]);
    }

    @Nullable
    @Override
    public PsiElement resolve() {
        ResolveResult[] resolveResults = multiResolve(false);
        return resolveResults.length == 1 ? resolveResults[0].getElement() : null;
    }

    // code completion (makes no sense)

//    @Override
//    public Object @NotNull [] getVariants() {
//        return new LookupElement[0];
//    }

    @Override
    public PsiElement handleElementRename(@NotNull String newElementName) throws IncorrectOperationException {
        Xbas99PsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
