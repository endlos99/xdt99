package net.endlos.xdt99.xbas99;

import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.refactoring.rename.BindablePsiReference;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xbas99.psi.Xbas99Linedef;
import net.endlos.xdt99.xbas99.psi.impl.Xbas99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xbas99LineReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private String lineNumber;

    public Xbas99LineReference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        lineNumber = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset());
    }

    @NotNull
    @Override
    public ResolveResult[] multiResolve(boolean incompleteCode) {
        final List<Xbas99Linedef> linedefs = Xbas99Util.findLinedefs(myElement, lineNumber);
        List<ResolveResult> results = new ArrayList<ResolveResult>();
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

    @NotNull
    @Override
    public Object[] getVariants() {
        List<Xbas99Linedef> linedefs = Xbas99Util.findLinedefs(myElement);
        List<LookupElement> variants = new ArrayList<LookupElement>();
        for (final Xbas99Linedef linedef : linedefs) {
            if (linedef.getName() != null && linedef.getName().length() > 0) {
                variants.add(LookupElementBuilder.create(linedef).
                                withIcon(Xbas99Icons.FILE).
                                withTypeText(linedef.getContainingFile().getName())
                );
            }
        }
        return variants.toArray();
    }

    @Override
    public PsiElement handleElementRename(String newElementName) throws IncorrectOperationException {
        Xbas99PsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
