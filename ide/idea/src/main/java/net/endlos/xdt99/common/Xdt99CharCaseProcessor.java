package net.endlos.xdt99.common;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.*;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.tree.TokenSet;
import org.jetbrains.annotations.NotNull;

import java.util.Map;

public class Xdt99CharCaseProcessor extends PsiElementVisitor {
    private final PsiDocumentManager psiDocumentManager;
    private final Document document;
    private final Xdt99CharCase charCase;
    private final boolean includeComments;
    private final TokenSet literals;
    private final TokenSet comments;
    private TextRange rangeToReformat;

    public Xdt99CharCaseProcessor(@NotNull PsiDocumentManager psiDocumentManager,
                                  @NotNull Document document,
                                  @NotNull Xdt99CharCase charCase,
                                  boolean includeComments,
                                  @NotNull TokenSet literals,
                                  @NotNull TokenSet comments) {
        this.psiDocumentManager = psiDocumentManager;
        this.document = document;
        this.charCase = charCase;
        this.includeComments = includeComments;
        this.literals = literals;
        this.comments = comments;
    }

    public PsiElement process(PsiElement source) {
        if (charCase == Xdt99CharCase.ASIS)
            return source;
        psiDocumentManager.doPostponedOperationsAndUnblockDocument(document);
        this.rangeToReformat = source.getTextRange();
        source.accept(this);
        return source;
    }

    public TextRange processText(PsiFile source, TextRange rangeToReformat) {
        if (charCase == Xdt99CharCase.ASIS)
            return TextRange.EMPTY_RANGE;
        psiDocumentManager.doPostponedOperationsAndUnblockDocument(document);
        this.rangeToReformat = rangeToReformat;
        source.accept(this);
        return rangeToReformat;
    }

    @Override
    public void visitElement(PsiElement element) {
        if (element.getNode().getFirstChildNode() == null &&
                !literals.contains(element.getNode().getElementType()) &&
                (includeComments || !comments.contains(element.getNode().getElementType())))
        {
            applyCaseFormattingFor(element);
        } else {
            element.acceptChildren(this);
        }
    }

    private void applyCaseFormattingFor(PsiElement name) {
        if (rangeToReformat.contains(name.getTextRange())) {
            int offset = name.getTextRange().getStartOffset();
            int endOffset = name.getTextRange().getEndOffset();
            switch (charCase) {
                case LOWER:
                    String lower = name.getText().toLowerCase();
                    document.replaceString(offset, endOffset, lower);
                    break;
                case UPPER:
                    String upper = name.getText().toUpperCase();
                    document.replaceString(offset, endOffset, upper);
                    break;
            }
        }
    }

}
