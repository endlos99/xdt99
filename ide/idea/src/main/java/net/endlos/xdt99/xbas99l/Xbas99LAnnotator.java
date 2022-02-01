package net.endlos.xdt99.xbas99l;

import com.intellij.application.options.CodeStyle;
import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.impl.source.tree.LeafPsiElement;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99l.psi.*;
import org.jetbrains.annotations.NotNull;

import java.util.List;

import static org.apache.commons.lang.ArrayUtils.contains;

public class Xbas99LAnnotator implements Annotator {
    private static final IElementType[] allXbTokens = {
            Xbas99LTypes.OP_SEP,
            Xbas99LTypes.W_ALL,
            Xbas99LTypes.W_AT,
            Xbas99LTypes.W_BEEP,
            Xbas99LTypes.W_ERASE,
            Xbas99LTypes.W_SIZE
    };

    @Override
    public void annotate(@NotNull final PsiElement element, @NotNull AnnotationHolder holder) {
        final Xbas99LCodeStyleSettings settings =
                CodeStyle.getCustomSettings(element.getContainingFile(), Xbas99LCodeStyleSettings.class);

        // color
        if (element instanceof Xbas99LNvarW) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99LSyntaxHighlighter.NVAR).create();
        } else if (element instanceof Xbas99LNvarR) {
            if (Xbas99LUtil.findFNvardef(element, ((Xbas99LNvarR) element).getName()).isEmpty()) {
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(element.getTextRange()).textAttributes(Xbas99LSyntaxHighlighter.NVAR).create();
            } else {
                // highlight function usages parsed as variables
                TextRange range = getFunNameRange(element);
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(range).textAttributes(Xbas99LSyntaxHighlighter.FUNCTION).create();
            }
        } else if (element instanceof Xbas99LSvarW) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99LSyntaxHighlighter.SVAR).create();
        } else if (element instanceof Xbas99LSvarR) {
            if (Xbas99LUtil.findFSvardef(element, ((Xbas99LSvarR) element).getName()).isEmpty()) {
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(element.getTextRange()).textAttributes(Xbas99LSyntaxHighlighter.SVAR).create();
            } else {
                // highlight function usages parsed as variables
                TextRange range = getFunNameRange(element);
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                        .range(range).textAttributes(Xbas99LSyntaxHighlighter.FUNCTION).create();
            }
        } else if (element instanceof Xbas99LLabelref) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99LSyntaxHighlighter.LABEL).create();
        } else if (element instanceof Xbas99LSubprog) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99LSyntaxHighlighter.SUBPROG).create();
        } else if (element instanceof Xbas99LNvarF || element instanceof Xbas99LSvarF) {
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xbas99LSyntaxHighlighter.FUNCTION).create();
        }

        // error check
        if (!Xbas99LCodeStyleSettings.XBAS99_EXTENDEDBASIC) {
            if (element instanceof Xbas99LStatementXb ||
                    (element instanceof LeafPsiElement &&
                            contains(allXbTokens, ((LeafPsiElement)element).getElementType())) ||
                    (element instanceof Xbas99LAThenElse &&
                            element.getFirstChild() instanceof Xbas99LSlist) ||
                    element instanceof Xbas99LBangComment) {
                holder.newAnnotation(HighlightSeverity.ERROR, "ExtBASIC only")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.ERROR).create();
            }
        }

        if (element instanceof Xbas99LLabeldef) {
            List<Xbas99LNamedElement> usages = Xbas99LUtil.findLabelUsages((Xbas99LLabeldef) element);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused label")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL).create();
            }
        } else if (element instanceof Xbas99LLabelref) {
            List<Xbas99LLabeldef> defs = Xbas99LUtil.findLabeldefs(element, ((Xbas99LLabelref) element).getName(),
                    false);
            if (defs.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Undefined label")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
            }
        } else if (element instanceof Xbas99LNvarW) {
            List<Xbas99LNamedElement> usages = Xbas99LUtil.findNvarUsages((Xbas99LNvarW) element);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL).create();
            }
        } else if (element instanceof Xbas99LSvarW) {
            List<Xbas99LNamedElement> usages = Xbas99LUtil.findSvarUsages((Xbas99LSvarW) element);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL).create();
            }
        }
        
        // information
        else if (element instanceof Xbas99LNvarR) {
            if (Xbas99LUtil.findBothNdef(element, ((Xbas99LNvarR) element).getName(), false).isEmpty())
                holder.newAnnotation(HighlightSeverity.WARNING, "Unassigned variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
        } else if (element instanceof Xbas99LSvarR) {
            if (Xbas99LUtil.findBothSdef(element, ((Xbas99LSvarR) element).getName(), false).isEmpty())
                holder.newAnnotation(HighlightSeverity.WARNING, "Unassigned variable")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
        }
    }

    private TextRange getFunNameRange(PsiElement element) {
        int newEndOffset = ((Xbas99LNamedElement) element).getName().length();
        int startOffset = element.getTextRange().getStartOffset();
        return TextRange.create(startOffset, startOffset + newEndOffset);
    }

}
