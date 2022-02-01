package net.endlos.xdt99.xbas99l;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.impl.source.codeStyle.PostFormatProcessor;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.common.Xdt99CharCaseProcessor;
import net.endlos.xdt99.xbas99l.psi.Xbas99LElementType;
import net.endlos.xdt99.xbas99l.psi.Xbas99LFile;
import net.endlos.xdt99.xbas99l.psi.Xbas99LTypes;
import org.jetbrains.annotations.NotNull;

public class Xbas99LPostFormatProcessor implements PostFormatProcessor {
    private final static TokenSet literals = TokenSet.create(Xbas99LTypes.QSTRING, Xbas99LTypes.CRLF);
    private final static TokenSet comments = TokenSet.create(Xbas99LTypes.COMMENT);

    @Override
    @NotNull
    public PsiElement processElement(@NotNull PsiElement source, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xbas99LElementType) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xbas99LCodeStyleSettings.XBAS99_CHAR_CASE, Xbas99LCodeStyleSettings.XBAS99_CASE_COMMENTS,
                        literals, comments)
                        .process(source);
        }
        return source;
    }

    @Override
    @NotNull
    public TextRange processText(@NotNull PsiFile source, @NotNull TextRange rangeToReformat, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xbas99LFile) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xbas99LCodeStyleSettings.XBAS99_CHAR_CASE, Xbas99LCodeStyleSettings.XBAS99_CASE_COMMENTS,
                        literals, comments)
                        .processText(source, rangeToReformat);
        }
        return rangeToReformat;
    }

}
