package net.endlos.xdt99.xga99r;

import com.intellij.codeInsight.completion.CompletionUtilCore;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import net.endlos.xdt99.xga99r.psi.Xga99RFile;
import net.endlos.xdt99.xga99r.psi.impl.Xga99RPsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xga99RReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String label;
    private final int offset;
    private int distance;

    public Xga99RReference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        offset = findBeginningOfLine(element);
        for (distance = 0; distance < label.length() && label.charAt(distance) == '!'; ++distance) {}
        if (findLabelDirection(element))
            distance = -distance;
    }

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        Project project = myElement.getProject();
        final List<Xga99RLabeldef> labels = Xga99RUtil.findLabels(project, label, distance, myElement, offset, false);
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        for (Xga99RLabeldef label : labels) {
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
        List<Xga99RLabeldef> labeldefs = Xga99RUtil.findLabels(project, labelText, distance, myElement, offset, true);
        List<LookupElement> variants = new ArrayList<LookupElement>();
        for (final Xga99RLabeldef labeldef : labeldefs) {
            if (labeldef.getName() != null && labeldef.getName().length() > 0) {
                variants.add(LookupElementBuilder.create(labeldef).
                                withIcon(Xga99RIcons.FILE).
                                withTypeText(labeldef.getContainingFile().getName())
                );
            }
        }
        return variants.toArray();
    }

    @Override
    public PsiElement handleElementRename(@NotNull String newElementName) throws IncorrectOperationException {
        Xga99RPsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

    private int findBeginningOfLine(PsiElement element) {
        while (element != null && !(element.getParent() instanceof Xga99RFile))
            element = element.getParent();
        while (element != null &&
                (element.getPrevSibling() == null ||
                        element.getPrevSibling().getNode().getElementType() != Xga99RTypes.CRLF))
            element = element.getPrevSibling();
        return element == null ? 0 : element.getTextOffset();
    }

    private boolean findLabelDirection(PsiElement element) {
        try {
            PsiElement prev = element.getParent().getParent().getPrevSibling();
            return prev.getNode().getElementType() == Xga99RTypes.OP_MINUS;
        } catch (NullPointerException e) {
            return false;
        }
    }
}
