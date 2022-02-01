package net.endlos.xdt99.xas99r;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.TokenType;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.impl.source.codeStyle.PostFormatProcessor;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.common.Xdt99CharCaseProcessor;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import net.endlos.xdt99.xas99r.psi.Xas99RElementType;
import net.endlos.xdt99.xas99r.psi.Xas99RFile;
import org.jetbrains.annotations.NotNull;

public class Xas99RPostFormatProcessor implements PostFormatProcessor {
    private final static TokenSet literals = TokenSet.create(Xas99RTypes.TEXT, Xas99RTypes.CRLF, TokenType.WHITE_SPACE);
    private final static TokenSet comments = TokenSet.create(Xas99RTypes.COMMENT, Xas99RTypes.LCOMMENT);

    @Override
    @NotNull
    public PsiElement processElement(@NotNull PsiElement source, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xas99RElementType) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xas99RCodeStyleSettings.XAS99_CHAR_CASE, Xas99RCodeStyleSettings.XAS99_CASE_COMMENTS,
                        literals, comments)
                        .process(source);
        }
        return source;
    }

    @Override
    @NotNull
    public TextRange processText(@NotNull PsiFile source, @NotNull TextRange rangeToReformat, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xas99RFile) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xas99RCodeStyleSettings.XAS99_CHAR_CASE, Xas99RCodeStyleSettings.XAS99_CASE_COMMENTS,
                        literals, comments)
                        .processText(source, rangeToReformat);
        }
        return rangeToReformat;
    }

}
