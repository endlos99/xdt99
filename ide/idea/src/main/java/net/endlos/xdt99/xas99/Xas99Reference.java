package net.endlos.xdt99.xas99;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99OpAlias;
import net.endlos.xdt99.xas99.psi.Xas99OpMacro;
import net.endlos.xdt99.xas99.psi.Xas99OpMacrodef;
import net.endlos.xdt99.xas99.psi.impl.Xas99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99Reference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String label;
    private final boolean isAlias, isMacro;
    private final int offset;
    private final int distance;

    public Xas99Reference(@NotNull PsiElement element, TextRange textRange) {
        super(element, textRange);
        label = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        isAlias = element instanceof Xas99OpAlias;
        isMacro = element instanceof Xas99OpMacro;
        offset = Xas99Util.findBeginningOfLine(element);
        distance = Xas99Util.getDistance(label, element);
    }

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        Project project = myElement.getProject();
        List<ResolveResult> results = new ArrayList<ResolveResult>();
        if (isMacro) {
            List<Xas99OpMacrodef> macros = Xas99Util.findMacros(project, label, false);
            for (Xas99OpMacrodef macro : macros) {
                results.add(new PsiElementResolveResult(macro));
            }
        } else {
            List<Xas99Labeldef> labels;
            if (isAlias) {
                labels = Xas99Util.findAliases(project, label, false);
            } else {
                labels = Xas99Util.findLabels(project, label, distance, myElement, offset, false);
            }
            for (Xas99Labeldef label : labels) {
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
        Xas99PsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
