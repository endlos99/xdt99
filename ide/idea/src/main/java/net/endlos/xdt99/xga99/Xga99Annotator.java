package net.endlos.xdt99.xga99;

import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiWhiteSpace;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import net.endlos.xdt99.xga99.psi.Xga99OpLabel;
import net.endlos.xdt99.xga99.psi.Xga99Types;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xga99Annotator implements Annotator {
    private final static TokenSet operators = TokenSet.create(Xga99Types.OP_SEP, Xga99Types.OP_PLUS,
            Xga99Types.OP_MINUS, Xga99Types.OP_AST, Xga99Types.OP_MISC);
    private static final String LOCAL_LABEL_PREFIX = "!";

    @Override
    public void annotate(@NotNull final PsiElement element, @NotNull AnnotationHolder holder) {
        if (element instanceof Xga99Labeldef) {
            Xga99Labeldef labeldef = (Xga99Labeldef) element;
            // duplicate symbols?
            List<Xga99Labeldef> definitions = Xga99Util.findLabels(element.getProject(), labeldef.getName(), 0,
                    element, 0, false);
            if (definitions.size() > 1) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Duplicate symbols")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
                return;
            }
            // is defined label used at all?
            List<Xga99OpLabel> usages = Xga99Util.findLabelUsages(labeldef);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused label")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL).create();
            }
        } else if (element instanceof Xga99OpLabel) {
            // annotate label references
            String label = element.getText();
            if (label == null)
                return;
            TextRange labelRange = element.getTextRange();
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(labelRange).textAttributes(Xga99SyntaxHighlighter.IDENT).create();
            if (label.startsWith(LOCAL_LABEL_PREFIX)) {
                // bad local label (invalid target)?
                int distance = Xga99Util.getDistance(label, element);
                int offset = Xga99Util.findBeginningOfLine(element);
                List<Xga99Labeldef> targets = Xga99Util.findLabels(element.getProject(), label, distance, element, offset,
                        false);
                if (targets.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Undefined target")
                            .range(labelRange).highlightType(ProblemHighlightType.WARNING).create();
                }
            } else {
                // undefined label?
                List<Xga99Labeldef> labeldefs = Xga99Util.findLabels(element.getProject(), label, 0, null, 0, false);
                if (labeldefs.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.ERROR, "Undefined symbol")
                            .range(labelRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
                }
            }
        } else if (Xga99CodeStyleSettings.XGA99_STRICT && element instanceof PsiWhiteSpace) {
            // no space after ',' in strict mode
            PsiElement e = element.getPrevSibling();
            if (e != null && operators.contains(e.getNode().getElementType())) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Erroneous space in strict mode")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
                return;  // no need to check other side as well
            }
            e = element.getNextSibling();
            if (e != null && operators.contains(e.getNode().getElementType())) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Erroneous space in strict mode")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
            }
        }
    }

}
