package net.endlos.xdt99.xbas99;

import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.impl.source.tree.LeafPsiElement;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99.psi.*;
import org.jetbrains.annotations.NotNull;

import java.util.List;

import static org.apache.commons.lang.ArrayUtils.contains;

public class Xbas99Annotator implements Annotator {
    private static final IElementType[] allXbTokens = {
            Xbas99Types.OP_SEP,
            Xbas99Types.W_ALL,
            Xbas99Types.W_AT,
            Xbas99Types.W_BEEP,
            Xbas99Types.W_ERASE,
            Xbas99Types.W_SIZE
    };

    @Override
    public void annotate(@NotNull final PsiElement element, @NotNull AnnotationHolder holder) {
        // color
        if (element instanceof Xbas99NvarW) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99SyntaxHighlighter.NVAR).create();
        } else if (element instanceof Xbas99NvarR) {
            if (Xbas99Util.findFNvardef(element, ((Xbas99NvarR) element).getName()).isEmpty()) {
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(element.getTextRange()).textAttributes(Xbas99SyntaxHighlighter.NVAR).create();
            } else {
                // highlight function usages parsed as variables
                TextRange range = getFunNameRange(element);
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(range).textAttributes(Xbas99SyntaxHighlighter.FUNCTION).create();
            }
        } else if (element instanceof Xbas99SvarW) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99SyntaxHighlighter.SVAR).create();
        } else if (element instanceof Xbas99SvarR) {
            if (Xbas99Util.findFSvardef(element, ((Xbas99SvarR) element).getName()).isEmpty()) {
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(element.getTextRange()).textAttributes(Xbas99SyntaxHighlighter.SVAR).create();
            } else {
                // highlight function usages parsed as variables
                TextRange range = getFunNameRange(element);
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(range).textAttributes(Xbas99SyntaxHighlighter.FUNCTION).create();
            }
        } else if (element instanceof Xbas99Lino) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99SyntaxHighlighter.LINO).create();
        } else if (element instanceof Xbas99Subprog) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99SyntaxHighlighter.SUBPROG).create();
        } else if (element instanceof Xbas99NvarF || element instanceof Xbas99SvarF) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99SyntaxHighlighter.FUNCTION).create();
        }

        // error check
        if (!Xbas99CodeStyleSettings.XBAS99_EXTENDEDBASIC) {
            if (element instanceof Xbas99StatementXb ||
                    (element instanceof LeafPsiElement &&
                            contains(allXbTokens, ((LeafPsiElement)element).getElementType())) ||
                    (element instanceof Xbas99AThenElse &&
                            element.getFirstChild() instanceof Xbas99Slist) ||
                    element instanceof Xbas99BangComment) {
                holder.newAnnotation(HighlightSeverity.ERROR, "ExtBASIC only")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.ERROR).create();
            }
        }
        if (element instanceof Xbas99Lino) {
            List<Xbas99NamedElement> usages = Xbas99Util.findLinoUsages((Xbas99Lino) element);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Bad line number")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
            }
        } else if (element instanceof Xbas99NvarW) {
            List<Xbas99NamedElement> usages = Xbas99Util.findNvarUsages((Xbas99NvarW) element);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL).create();
            }
        } else if (element instanceof Xbas99SvarW) {
            List<Xbas99NamedElement> usages = Xbas99Util.findSvarUsages((Xbas99SvarW) element);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL).create();
            }
        }

        // information
        if (element instanceof Xbas99NvarR) {
            if (Xbas99Util.findBothNdef(element, ((Xbas99NvarR)element).getName(), false).isEmpty())
                holder.newAnnotation(HighlightSeverity.WARNING, "Unassigned variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
        } else if (element instanceof Xbas99SvarR) {
            if (Xbas99Util.findBothSdef(element, ((Xbas99SvarR)element).getName(), false).isEmpty())
                holder.newAnnotation(HighlightSeverity.WARNING, "Unassigned variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
        }
    }

    private TextRange getFunNameRange(PsiElement element) {
        int newEndOffset = ((Xbas99NamedElement) element).getName().length();
        int startOffset = element.getTextRange().getStartOffset();
        return TextRange.create(startOffset, startOffset + newEndOffset);
    }

}
