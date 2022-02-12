package net.endlos.xdt99.xga99;

import com.intellij.codeInsight.completion.CompletionUtilCore;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xga99.psi.Xga99File;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import net.endlos.xdt99.xga99.psi.Xga99Types;
import net.endlos.xdt99.xga99.psi.impl.Xga99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xga99Reference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String label;
    private final int offset;
    private int distance;

    public Xga99Reference(@NotNull PsiElement element, TextRange textRange) {
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
        final List<Xga99Labeldef> labels = Xga99Util.findLabels(project, label, distance, myElement, offset, false);
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        for (Xga99Labeldef label : labels) {
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
        Xga99PsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

    private int findBeginningOfLine(PsiElement element) {
        while (element != null && !(element.getParent() instanceof Xga99File))
            element = element.getParent();
        while (element != null &&
                (element.getPrevSibling() == null ||
                        element.getPrevSibling().getNode().getElementType() != Xga99Types.CRLF))
            element = element.getPrevSibling();
        return element == null ? 0 : element.getTextOffset();
    }

    private boolean findLabelDirection(PsiElement element) {
        try {
            PsiElement prev = element.getParent().getParent().getPrevSibling();
            return prev.getNode().getElementType() == Xga99Types.OP_MINUS;
        } catch (NullPointerException e) {
            return false;
        }
    }
}
