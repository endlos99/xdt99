package net.endlos.xdt99.xas99;

import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xas99.psi.Xas99File;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import net.endlos.xdt99.xas99.psi.impl.Xas99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99Reference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private String label;
    private int offset;
    private int distance;

    public Xas99Reference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        offset = findBeginningOfLine(element);
        for (distance = 0; distance < label.length() && label.charAt(distance) == '!'; ++distance) {}
        if (findLabelDirection(element))
            distance = -distance;
    }

    @NotNull
    @Override
    public ResolveResult[] multiResolve(boolean incompleteCode) {
        Project project = myElement.getProject();
        final List<Xas99Labeldef> labels = Xas99Util.findLabels(project, myElement, label, offset, distance);
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

    @NotNull
    @Override
    public Object[] getVariants() {
        Project project = myElement.getProject();
        List<Xas99Labeldef> labels = Xas99Util.findLabels(project);
        List<LookupElement> variants = new ArrayList<LookupElement>();
        for (final Xas99Labeldef label : labels) {
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

    private int findBeginningOfLine(PsiElement element) {
        while (element != null && !(element.getParent() instanceof Xas99File))
            element = element.getParent();
        while (element != null && element.getPrevSibling().getNode().getElementType() != Xas99Types.CRLF)
            element = element.getPrevSibling();
        return element == null ? 0 : element.getTextOffset();
    }

    private boolean findLabelDirection(PsiElement element) {
        try {
            PsiElement prev = element.getParent().getParent().getPrevSibling();
            return prev.getNode().getElementType() == Xas99Types.OP_MINUS;
        } catch (NullPointerException e) {
            return false;
        }
    }
}
