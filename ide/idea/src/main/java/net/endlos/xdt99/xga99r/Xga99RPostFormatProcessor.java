package net.endlos.xdt99.xga99r;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.impl.source.codeStyle.PostFormatProcessor;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.common.Xdt99CharCaseProcessor;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import net.endlos.xdt99.xga99r.psi.Xga99RElementType;
import net.endlos.xdt99.xga99r.psi.Xga99RFile;
import org.jetbrains.annotations.NotNull;

public class Xga99RPostFormatProcessor implements PostFormatProcessor {
    private final static TokenSet literals = TokenSet.create(Xga99RTypes.TEXT, Xga99RTypes.CRLF);
    private final static TokenSet comments = TokenSet.create(Xga99RTypes.COMMENT, Xga99RTypes.LCOMMENT);

    @Override
    @NotNull
    public PsiElement processElement(@NotNull PsiElement source, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xga99RElementType) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xga99RCodeStyleSettings.XGA99_CHAR_CASE, Xga99RCodeStyleSettings.XGA99_CASE_COMMENTS,
                        literals, comments)
                        .process(source);
        }
        return source;
    }

    @Override
    @NotNull
    public TextRange processText(@NotNull PsiFile source, @NotNull TextRange rangeToReformat, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xga99RFile) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xga99RCodeStyleSettings.XGA99_CHAR_CASE, Xga99RCodeStyleSettings.XGA99_CASE_COMMENTS,
                        literals, comments)
                        .processText(source, rangeToReformat);
        }
        return rangeToReformat;
    }

}
