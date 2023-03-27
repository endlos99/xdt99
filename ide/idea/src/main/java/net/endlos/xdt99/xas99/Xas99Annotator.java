package net.endlos.xdt99.xas99;

import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiWhiteSpace;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99.psi.*;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xas99Annotator implements Annotator {
    private final static TokenSet operators = TokenSet.create(Xas99Types.OP_SEP, Xas99Types.OP_PLUS,
            Xas99Types.OP_MINUS, Xas99Types.OP_AST, Xas99Types.OP_MISC);
    private static final String LOCAL_LABEL_PREFIX = "!";

    @Override
    public void annotate(@NotNull final PsiElement element, @NotNull AnnotationHolder holder) {
        if (element instanceof Xas99OpRegister) {
            if (element.getFirstChild() instanceof Xas99OpAlias) {
                // check if alias is defined
                String label = element.getText();
                if (label != null) {
                    TextRange labelRange = element.getTextRange();
                    List<Xas99Labeldef> labeldefs = Xas99Util.findAliases(element.getProject(), label, false);
                    if (labeldefs.isEmpty()) {
                        holder.newAnnotation(HighlightSeverity.ERROR, "Undefined register alias")
                                .range(labelRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
                        return;
                    }
                }
            }
            // register might be uncolored value or macro argument
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(element.getTextRange()).textAttributes(Xas99SyntaxHighlighter.REGISTER).create();
        } else if (element instanceof Xas99Labeldef) {
            Xas99Labeldef labeldef = (Xas99Labeldef) element;
            // duplicate symbols?
            if (!labeldef.getName().startsWith(LOCAL_LABEL_PREFIX)) {
                List<Xas99Labeldef> definitions = Xas99Util.findLabels(element.getProject(), labeldef.getName(),
                        0, element, 0, false);
                if (definitions.size() > 1) {
                    holder.newAnnotation(HighlightSeverity.ERROR, "Duplicate symbols")
                            .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
                    return;
                }
            }
            // is defined label used at all?
            if (Xas99Util.isAliasDefinition(labeldef)) {
                List<Xas99OpAlias> usages = Xas99Util.findAliasUsages(labeldef);
                if (usages.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Unused alias")
                            .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL)
                            .create();
                }
            } else {
                List<Xas99OpLabel> usages = Xas99Util.findLabelUsages(labeldef);
                if (usages.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Unused label")
                            .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL)
                            .create();
                }
            }
        } else if (element instanceof Xas99OpLabel) {
            // annotate label references
            if (element.getParent() instanceof Xas99OpRegister)
                return;  // actually an alias register
            String label = element.getText();
            if (label == null)
                return;
            TextRange labelRange = element.getTextRange();
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(labelRange).textAttributes(Xas99SyntaxHighlighter.IDENT).create();
            if (label.startsWith(LOCAL_LABEL_PREFIX)) {
                // bad local label (invalid target)?
                int distance = Xas99Util.getDistance(label, element);
                int offset = Xas99Util.findBeginningOfLine(element);
                List<Xas99Labeldef> targets = Xas99Util.findLabels(element.getProject(), label, distance, element,
                        offset,false);
                if (targets.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.WARNING, "Undefined target")
                            .range(labelRange).highlightType(ProblemHighlightType.WARNING).create();
                }
            } else {
                // undefined label?
                List<Xas99Labeldef> labeldefs = Xas99Util.findLabels(element.getProject(), label, 0,
                        null, 0, false);
                if (labeldefs.isEmpty()) {
                    holder.newAnnotation(HighlightSeverity.ERROR, "Undefined symbol")
                            .range(labelRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
                }
            }
        } else if (element instanceof Xas99OpMacrodef) {
            Xas99OpMacrodef macrodef = (Xas99OpMacrodef) element;
            // duplicate symbols?
            List<Xas99OpMacrodef> definitions = Xas99Util.findMacros(element.getProject(), macrodef.getName(),
                    false);
            if (definitions.size() > 1) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Duplicate macro")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.GENERIC_ERROR).create();
                return;
            }
            // is defined macro used at all?
            List<Xas99OpMacro> usages = Xas99Util.findMacroUsages(macrodef);
            if (usages.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.WARNING, "Unused macro")
                        .range(element.getTextRange()).highlightType(ProblemHighlightType.LIKE_UNUSED_SYMBOL)
                        .create();
            }
        } else if (element instanceof Xas99OpMacro) {
            // annotate macro references
            String macro = element.getText();
            if (macro == null)
                return;
            TextRange macroRange = element.getTextRange();
            holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(macroRange).textAttributes(Xas99SyntaxHighlighter.PREPROCESSOR).create();
            // undefined macro?
            List<Xas99OpMacrodef> macrodefs = Xas99Util.findMacros(element.getProject(), macro, false);
            if (macrodefs.isEmpty()) {
                holder.newAnnotation(HighlightSeverity.ERROR, "Undefined macro")
                        .range(macroRange).highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL).create();
            }
        } else if (Xas99CodeStyleSettings.XAS99_STRICT && element instanceof PsiWhiteSpace) {
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
