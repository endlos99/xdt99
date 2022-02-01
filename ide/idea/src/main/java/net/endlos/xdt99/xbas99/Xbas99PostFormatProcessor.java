package net.endlos.xdt99.xbas99;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.impl.source.codeStyle.PostFormatProcessor;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.common.Xdt99CharCaseProcessor;
import net.endlos.xdt99.xbas99.psi.Xbas99ElementType;
import net.endlos.xdt99.xbas99.psi.Xbas99File;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import org.jetbrains.annotations.NotNull;

public class Xbas99PostFormatProcessor implements PostFormatProcessor {
    private final static TokenSet literals = TokenSet.create(Xbas99Types.QSTRING, Xbas99Types.CRLF);
    private final static TokenSet comments = TokenSet.create(Xbas99Types.COMMENT);

    @Override
    @NotNull
    public PsiElement processElement(@NotNull PsiElement source, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xbas99ElementType) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xbas99CodeStyleSettings.XBAS99_CHAR_CASE, Xbas99CodeStyleSettings.XBAS99_CASE_COMMENTS,
                        literals, comments)
                        .process(source);
        }
        return source;
    }

    @Override
    @NotNull
    public TextRange processText(@NotNull PsiFile source, @NotNull TextRange rangeToReformat, @NotNull CodeStyleSettings settings) {
        if (source instanceof Xbas99File) {
            PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(source.getProject());
            Document document = psiDocumentManager.getDocument(source.getContainingFile());
            if (document != null)
                return new Xdt99CharCaseProcessor(psiDocumentManager, document,
                        Xbas99CodeStyleSettings.XBAS99_CHAR_CASE, Xbas99CodeStyleSettings.XBAS99_CASE_COMMENTS,
                        literals, comments)
                        .processText(source, rangeToReformat);
        }
        return rangeToReformat;
    }

}
