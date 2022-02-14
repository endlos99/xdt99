package net.endlos.xdt99.xga99r;

import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import net.endlos.xdt99.xga99r.psi.Xga99ROpLabel;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xga99RAnnotator implements Annotator {
    private static final String LOCAL_LABEL_PREFIX = "!";

    @Override
    public void annotate(@NotNull final PsiElement element, @NotNull AnnotationHolder holder) {
        if (element instanceof Xga99RLabeldef) {
            Xga99RLabeldef labeldef = (Xga99RLabeldef) element;
            // duplicate symbols?
            List<Xga99RLabeldef> definitions = Xga99RUtil.findLabels(element.getProject(), labeldef.getName(), 0,
                    element, 0, false);
            if (definitions.size() > 1) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Duplicate symbols")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
                return;
            }
            // is defined label used at all?
            List<Xga99ROpLabel> usages = Xga99RUtil.findLabelUsages((Xga99RLabeldef) element);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused label")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL).create();
            }
        } else if (element instanceof Xga99ROpLabel) {
            // annotate label references
            String label = element.getText();
            if (label == null)
                return;
            TextRange labelRange = element.getTextRange();
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(labelRange).textAttributes(Xga99RSyntaxHighlighter.IDENT).create();
            if (label.startsWith(LOCAL_LABEL_PREFIX)) {
                // bad local label (invalid target)?
                int distance = Xga99RUtil.getDistance(label, element);
                int offset = Xga99RUtil.findBeginningOfLine(element);
                List<Xga99RLabeldef> targets = Xga99RUtil.findLabels(element.getProject(), label, distance, element, offset,
                        false);
                if (targets.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Undefined target")
                            .range(labelRange).highlightType(ProblemHighlightType.WARNING).create();
                }
            } else {
                // undefined label?
                List<Xga99RLabeldef> labeldefs = Xga99RUtil.findLabels(element.getProject(), label, 0, null, 0, false);
                if (labeldefs.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.ERROR, "Undefined symbol")
                            .range(labelRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
                }
            }
        }
    }

}
