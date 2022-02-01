package net.endlos.xdt99.xbas99l;

import com.intellij.codeInsight.completion.CompletionUtilCore;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xbas99l.psi.Xbas99LLabeldef;
import net.endlos.xdt99.xbas99l.psi.impl.Xbas99LPsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xbas99LLabelReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String label;

    public Xbas99LLabelReference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
    }

    // highlighting occurrences

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        List<ResolveResult> results = new ArrayList<>();
        final List<Xbas99LLabeldef> labeldefs = Xbas99LUtil.findLabeldefs(myElement, label, false);
        for (Xbas99LLabeldef labeldef : labeldefs) {
            results.add(new PsiElementResolveResult(labeldef));
        }
        return results.toArray(new ResolveResult[results.size()]);
    }

    @Nullable
    @Override
    public PsiElement resolve() {
        ResolveResult[] resolveResults = multiResolve(false);
        return resolveResults.length == 1 ? resolveResults[0].getElement() : null;
    }

    // code completion

    @Override
    public Object @NotNull [] getVariants() {
        String labelText = label;
        if (label.endsWith(dummy)) {
            labelText = label.substring(0, label.length() - dummy.length());
        }
        List<Xbas99LLabeldef> labeldefs = Xbas99LUtil.findLabeldefs(myElement, labelText, true);
        List<LookupElement> variants = new ArrayList<LookupElement>();
        for (final Xbas99LLabeldef labeldef : labeldefs) {
            if (!labeldef.getName().isEmpty() && labeldef.getName().length() > 0) {
                variants.add(LookupElementBuilder.create(labeldef)
                        .withIcon(Xbas99LIcons.FILE)
                        .withTypeText(labeldef.getContainingFile().getName())
                );
            }
        }
        return variants.toArray();
    }

    @Override
    public PsiElement handleElementRename(@NotNull String newElementName) throws IncorrectOperationException {
        Xbas99LPsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
