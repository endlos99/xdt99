package net.endlos.xdt99.xas99;

import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xas99.psi.Xas99Label;
import net.endlos.xdt99.xas99.psi.impl.Xas99PsiImplUtil;
import net.endlos.xdt99.xbas99.psi.impl.Xbas99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99Reference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private String label;

    public Xas99Reference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset());
    }

    @NotNull
    @Override
    public ResolveResult[] multiResolve(boolean incompleteCode) {
        Project project = myElement.getProject();
        final List<Xas99Label> labels = Xas99Util.findLabels(project, label);
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        for (Xas99Label label : labels) {
            results.add(new PsiElementResolveResult(label));
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
        Project project = myElement.getProject();
        List<Xas99Label> labels = Xas99Util.findLabels(project);
        List<LookupElement> variants = new ArrayList<LookupElement>();
        for (final Xas99Label label : labels) {
            if (label.getName() != null && label.getName().length() > 0) {
                variants.add(LookupElementBuilder.create(label).
                                withIcon(Xas99Icons.FILE).
                                withTypeText(label.getContainingFile().getName())
                );
            }
        }
        return variants.toArray();
    }

    @Override
    public PsiElement handleElementRename(String newElementName) throws IncorrectOperationException {
        Xas99PsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }
}
