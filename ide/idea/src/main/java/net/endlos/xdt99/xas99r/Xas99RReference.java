package net.endlos.xdt99.xas99r;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xas99r.psi.Xas99RLabeldef;
import net.endlos.xdt99.xas99r.psi.Xas99ROpAlias;
import net.endlos.xdt99.xas99r.psi.Xas99ROpMacro;
import net.endlos.xdt99.xas99r.psi.Xas99ROpMacrodef;
import net.endlos.xdt99.xas99r.psi.impl.Xas99RPsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99RReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String label;
    private final boolean isAlias, isMacro;
    private final int offset;
    private final int distance;

    public Xas99RReference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        isAlias = element instanceof Xas99ROpAlias;
        isMacro = element instanceof Xas99ROpMacro;
        offset = Xas99RUtil.findBeginningOfLine(element);
        distance = Xas99RUtil.getDistance(label, element);
    }

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        Project project = myElement.getProject();
        if (isMacro) {
            final List<Xas99ROpMacrodef> macros;
            macros = Xas99RUtil.findMacros(project, label, false);
            for (Xas99ROpMacrodef macro : macros) {
                results.add(new PsiElementResolveResult(macro));
            }
        } else {
            final List<Xas99RLabeldef> labels;
            if (isAlias) {
                labels = Xas99RUtil.findAliases(project, label, false);
            } else {
                labels = Xas99RUtil.findLabels(project, label, distance, myElement, offset, false);
            }
            for (Xas99RLabeldef label : labels) {
                results.add(new PsiElementResolveResult(label));
            }
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
