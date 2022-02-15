package net.endlos.xdt99.xga99;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import net.endlos.xdt99.xga99.psi.impl.Xga99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xga99Reference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String label;
    private final int offset;
    private final int distance;

    public Xga99Reference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        offset = Xga99Util.findBeginningOfLine(element);
        distance = Xga99Util.getDistance(label, element);
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

}
