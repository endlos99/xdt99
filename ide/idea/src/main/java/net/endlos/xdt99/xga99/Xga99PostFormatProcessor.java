package net.endlos.xdt99.xga99;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.impl.source.codeStyle.PostFormatProcessor;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.common.Xdt99CharCaseProcessor;
import net.endlos.xdt99.xga99.psi.*;
import org.jetbrains.annotations.NotNull;

public class Xga99PostFormatProcessor implements PostFormatProcessor {
    private final static TokenSet literals = TokenSet.create(Xga99Types.TEXT, Xga99Types.CRLF);
    private final static TokenSet comments = TokenSet.create(Xga99Types.COMMENT, Xga99Types.LCOMMENT);

    @Override
    @NotNull
    public PsiElement processElement(@NotNull PsiElement source, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xga99ElementType) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xga99CodeStyleSettings.XGA99_CHAR_CASE, Xga99CodeStyleSettings.XGA99_CASE_COMMENTS,
                        literals, comments)
                        .process(source);
        }
        return source;
    }

    @Override
    @NotNull
    public TextRange processText(@NotNull PsiFile source, @NotNull TextRange rangeToReformat, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xga99File) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xga99CodeStyleSettings.XGA99_CHAR_CASE, Xga99CodeStyleSettings.XGA99_CASE_COMMENTS,
                        literals, comments)
                        .processText(source, rangeToReformat);
        }
        return rangeToReformat;
    }

}
