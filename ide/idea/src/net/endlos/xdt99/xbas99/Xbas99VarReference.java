package net.endlos.xdt99.xbas99;

import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xbas99.psi.Xbas99NamedElement;
import net.endlos.xdt99.xbas99.psi.Xbas99Nvar;
import net.endlos.xdt99.xbas99.psi.Xbas99Svar;
import net.endlos.xdt99.xbas99.psi.Xbas99Var;
import net.endlos.xdt99.xbas99.psi.impl.Xbas99PsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xbas99VarReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private String varName;
    private boolean isStringVar;

    public Xbas99VarReference(@NotNull PsiElement element, TextRange textRange, boolean forString) {
        super(element, textRange);
        varName = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset());
        isStringVar = forString;
    }

    @NotNull
    @Override
    public ResolveResult[] multiResolve(boolean incompleteCode) {
        final Xbas99NamedElement var = isStringVar ?
                Xbas99Util.findSvardef(myElement, varName) : Xbas99Util.findNvardef(myElement, varName);
        return var != null ?
                new ResolveResult[]{new PsiElementResolveResult(var)} : new ResolveResult[]{};
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
        List<LookupElement> variants = new ArrayList<LookupElement>();
        List<? extends Xbas99NamedElement> vars = isStringVar ?
                Xbas99Util.findSvardefs(myElement) : Xbas99Util.findNvardefs(myElement);
        for (final Xbas99NamedElement var : vars) {
            if (var.getName() != null && var.getName().length() > 0) {
                variants.add(LookupElementBuilder.create(var).
                                withIcon(Xbas99Icons.FILE).
                                withTypeText(var.getContainingFile().getName())
                );
            }
        }
        return variants.toArray();
    }

    @Override
    public PsiElement handleElementRename(String newElementName) throws IncorrectOperationException {
        Xbas99PsiImplUtil.rename(myElement, newElementName);
        return myElement;
    }

}
