package net.endlos.xdt99.xas99r;

import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xas99r.psi.*;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xas99RAnnotator implements Annotator {
    private static final String LOCAL_LABEL_PREFIX = "!";

    @Override
    public void annotate(@NotNull final PsiElement element, @NotNull AnnotationHolder holder) {
        if (element instanceof Xas99ROpRegister) {
            if (element.getFirstChild() instanceof Xas99ROpAlias) {
                // check if alias is defined
                String label = element.getText();
                if (label != null) {
                    TextRange labelRange = element.getTextRange();
                    List<Xas99RLabeldef> labeldefs = Xas99RUtil.findAliases(element.getProject(), label, false);
                    if (labeldefs.isEmpty()) {
                        holder.newAnnotation(HighlightSeverity.ERROR, "Undefined register alias")
                                .range(labelRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
                        return;
                    }
                }
            }
            // register might be uncolored value or macro argument
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xas99RSyntaxHighlighter.REGISTER).create();
        } else if (element instanceof Xas99RLabeldef) {
            Xas99RLabeldef labeldef = (Xas99RLabeldef) element;
            // duplicate symbols?
            if (!labeldef.getName().startsWith(LOCAL_LABEL_PREFIX)) {
                List<Xas99RLabeldef> definitions = Xas99RUtil.findLabels(element.getProject(), labeldef.getName(),
                        0, element, 0, false);
                if (definitions.size() > 1) {
                    holder.newAnnotation(HighlightSeverity.ERROR, "Duplicate symbols")
                            .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
                    return;
                }
            }
            // is defined label used at all?
            if (Xas99RUtil.isAliasDefinition(labeldef)) {
                List<Xas99ROpAlias> usages = Xas99RUtil.findAliasUsages(labeldef);
                if (usages.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Unused alias")
                            .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL)
                            .create();
                }
            } else {
                List<Xas99ROpLabel> usages = Xas99RUtil.findLabelUsages(labeldef);
                if (usages.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Unused label")
                            .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL)
                            .create();
                }
            }
        } else if (element instanceof Xas99ROpLabel) {
            // annotate label references
            String label = element.getText();
            if (label == null)
                return;
            TextRange labelRange = element.getTextRange();
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(labelRange).textAttributes(Xas99RSyntaxHighlighter.IDENT).create();
            if (label.startsWith(LOCAL_LABEL_PREFIX)) {
                // bad local label (invalid target)?
                int distance = Xas99RUtil.getDistance(label, element);
                int offset = Xas99RUtil.findBeginningOfLine(element);
                List<Xas99RLabeldef> targets = Xas99RUtil.findLabels(element.getProject(), label, distance, element,
                        offset, false);
                if (targets.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Undefined target")
                            .range(labelRange).highlightType(ProblemHighlightType.WARNING).create();
                }
            } else {
                // undefined label?
                List<Xas99RLabeldef> labeldefs = Xas99RUtil.findLabels(element.getProject(), label, 0,
                        null, 0, false);
                if (labeldefs.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.ERROR, "Undefined symbol")
                            .range(labelRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
                }
            }
        } else if (element instanceof Xas99ROpMacrodef) {
            Xas99ROpMacrodef macrodef = (Xas99ROpMacrodef) element;
            // duplicate symbols?
            List<Xas99ROpMacrodef> definitions = Xas99RUtil.findMacros(element.getProject(), macrodef.getName(),
                    false);
            if (definitions.size() > 1) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Duplicate macro")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
                return;
            }
            // is defined macro used at all?
            List<Xas99ROpMacro> usages = Xas99RUtil.findMacroUsages(macrodef);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused macro")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL)
                        .create();
            }
        } else if (element instanceof Xas99ROpMacro) {
            // annotate macro references
            String macro = element.getText();
            if (macro == null)
                return;
            TextRange macroRange = element.getTextRange();
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(macroRange).textAttributes(Xas99RSyntaxHighlighter.PREPROCESSOR).create();
            // undefined macro?
            List<Xas99ROpMacrodef> macrodefs = Xas99RUtil.findMacros(element.getProject(), macro, false);
            if (macrodefs.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Undefined macro")
                        .range(macroRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
            }
        }
    }

}
