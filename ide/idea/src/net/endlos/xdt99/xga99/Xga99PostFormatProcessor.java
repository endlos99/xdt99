package net.endlos.xdt99.xga99;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.impl.source.codeStyle.PostFormatProcessor;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xga99.psi.*;
import org.jetbrains.annotations.NotNull;

public class Xga99PostFormatProcessor implements PostFormatProcessor {
    private final static TokenSet unmodified = TokenSet.create(Xga99Types.COMMENT, Xga99Types.LCOMMENT,
            Xga99Types.TEXT, Xga99Types.CRLF);

    @Override
    public PsiElement processElement(@NotNull PsiElement source, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xga99ElementType) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xga99CharCaseProcessor(settings, psiDocumentManager, document).process(source);
            else
                return null;
        }
        return source;
    }

    @Override
    public TextRange processText(@NotNull PsiFile source, @NotNull TextRange rangeToReformat, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xga99File) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xga99CharCaseProcessor(settings, psiDocumentManager, document).processText(source, rangeToReformat);
            else
                return null;
        }
        return rangeToReformat;
    }

    private class Xga99CharCaseProcessor extends PsiElementVisitor {
        private final PsiDocumentManager psiDocumentManager;
        private final Document document;
        private final int charCase;
        private TextRange rangeToReformat;

        public Xga99CharCaseProcessor(@NotNull CodeStyleSettings settings, @NotNull PsiDocumentManager psiDocumentManager,
                                      @NotNull Document document) {
            this.psiDocumentManager = psiDocumentManager;
            this.document = document;
            this.charCase = settings.getCustomSettings(Xga99CodeStyleSettings.class).XGA99_CHAR_CASE;
        }

        public PsiElement process(PsiElement source) {
            psiDocumentManager.doPostponedOperationsAndUnblockDocument(document);
            this.rangeToReformat = source.getTextRange();
            source.accept(this);
            return source;
        }

        public TextRange processText(PsiFile source, TextRange rangeToReformat) {
            psiDocumentManager.doPostponedOperationsAndUnblockDocument(document);
            this.rangeToReformat = rangeToReformat;
            source.accept(this);
            return rangeToReformat;
        }

        @Override
        public void visitElement(PsiElement element) {
            if (element.getNode().getFirstChildNode() == null &&
                    !unmodified.contains(element.getNode().getElementType()))
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
                    case 0:
                        String lower = name.getText().toLowerCase();
                        document.replaceString(offset, endOffset, lower);
                        break;
                    case 1:
                        String upper = name.getText().toUpperCase();
                        document.replaceString(offset, endOffset, upper);
                        break;
                }
            }
        }
    }
}
