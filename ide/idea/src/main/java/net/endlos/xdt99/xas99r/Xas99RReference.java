package net.endlos.xdt99.xas99r;

import com.intellij.codeInsight.completion.CompletionUtilCore;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xas99r.psi.Xas99RLabeldef;
import net.endlos.xdt99.xas99r.psi.impl.Xas99RPsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99RReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String label;
    private final int offset;
    private final int distance;

    public Xas99RReference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        offset = Xas99RUtil.findBeginningOfLine(element);
        distance = Xas99RUtil.getDistance(label, element);
    }

    // highlighting occurrences

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        Project project = myElement.getProject();
        final List<Xas99RLabeldef> labels = Xas99RUtil.findLabels(project, label, distance, myElement, offset, false);
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        for (Xas99RLabeldef label : labels) {
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

    @Override
    public PsiElement handleElementRename(@NotNull String newElementName) throws IncorrectOperationException {
        Xas99RPsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
