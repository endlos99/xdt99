package net.endlos.xdt99.xga99r;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import net.endlos.xdt99.xga99r.psi.impl.Xga99RPsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xga99RReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String label;
    private final int offset;
    private final int distance;

    public Xga99RReference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        offset = Xga99RUtil.findBeginningOfLine(element);
        distance = Xga99RUtil.getDistance(label, element);
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
    public PsiElement handleElementRename(@NotNull String newElementName) throws IncorrectOperationException {
        Xga99RPsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
