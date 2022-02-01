package net.endlos.xdt99.xas99;

import com.intellij.codeInsight.completion.CompletionUtilCore;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99File;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import net.endlos.xdt99.xas99.psi.impl.Xas99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99Reference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String label;
    private final int offset;
    private final int distance;

    public Xas99Reference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        offset = Xas99Util.findBeginningOfLine(element);
        distance = Xas99Util.getDistance(label, element);
    }

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        Project project = myElement.getProject();
        final List<Xas99Labeldef> labels = Xas99Util.findLabels(project, label, distance, myElement, offset, false);
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        for (Xas99Labeldef label : labels) {
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
    public Object @NotNull [] getVariants() {
        Project project = myElement.getProject();
        String labelText = label;
        if (label.endsWith(dummy)) {
            labelText = label.substring(0, label.length() - dummy.length());
        }
        List<Xas99Labeldef> labeldefs = Xas99Util.findLabels(project, labelText, distance, myElement, offset, true);
        List<LookupElement> variants = new ArrayList<LookupElement>();
        for (final Xas99Labeldef labeldef : labeldefs) {
            if (labeldef.getName() != null && labeldef.getName().length() > 0) {
                variants.add(LookupElementBuilder.create(labeldef).
                                withIcon(Xas99Icons.FILE).
                                withTypeText(labeldef.getContainingFile().getName())
                );
            }
        }
        return variants.toArray();
    }

    @Override
    public PsiElement handleElementRename(@NotNull String newElementName) throws IncorrectOperationException {
        Xas99PsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
