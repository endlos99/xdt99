package net.endlos.xdt99.xbas99l;

import com.intellij.codeInsight.completion.CompletionUtilCore;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.util.IncorrectOperationException;
import net.endlos.xdt99.xbas99l.psi.Xbas99LNamedElement;
import net.endlos.xdt99.xbas99l.psi.impl.Xbas99LPsiImplUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xbas99LVarReference extends PsiReferenceBase<PsiElement> implements PsiPolyVariantReference {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String varName;
    private final boolean isStringVar;

    public Xbas99LVarReference(@NotNull PsiElement element, TextRange textRange, boolean forString) {
        super(element, textRange);
        varName = element.getText().substring(textRange.getStartOffset(), textRange.getEndOffset()).toUpperCase();
        isStringVar = forString;
    }

    // highlighting occurrences

    @Override
    public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
        List<ResolveResult> results = new ArrayList<>();
        final List<Xbas99LNamedElement> vars = isStringVar ?
                Xbas99LUtil.findSvardef(myElement, varName, false) :
                Xbas99LUtil.findNvardef(myElement, varName, false);
        for (Xbas99LNamedElement var : vars) {
            results.add(new PsiElementResolveResult(var));
        }
        return results.toArray(new ResolveResult[results.size()]);
    }

    @Override
    @Nullable
    public PsiElement resolve() {
        ResolveResult[] resolveResults = multiResolve(false);
        return resolveResults.length == 1 ? resolveResults[0].getElement() : null;
    }

    // code completion

    @Override
    public Object @NotNull [] getVariants() {
        boolean queryForString = false;
        String varText = varName;
        if (varText.endsWith("$")) {
            do {
                varText = varText.substring(0, varText.length() - 1);  // remove last char
            } while (varText.endsWith(" "));
            queryForString = true;
        }
        if (varText.endsWith(dummy)) {
            varText = varText.substring(0, varText.length() - dummy.length());
        }
        List<Xbas99LNamedElement> vars = isStringVar || queryForString ?
                Xbas99LUtil.findSvardef(myElement, varText, true) :
                Xbas99LUtil.findNvardef(myElement, varText, true);
        List<LookupElement> variants = new ArrayList<LookupElement>();
        for (final Xbas99LNamedElement var : vars) {
            if (!var.getName().isEmpty() && var.getName().length() > 0) {
                variants.add(LookupElementBuilder.create(var).
                                withIcon(Xbas99LIcons.FILE).
                                withTypeText(var.getContainingFile().getName())
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
