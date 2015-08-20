package net.endlos.xdt99.xas99;

import com.intellij.lang.ASTNode;
import com.intellij.lang.folding.FoldingBuilderEx;
import com.intellij.lang.folding.FoldingDescriptor;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xas99.psi.Xas99Linecomment;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.*;

public class Xas99FoldingBuilder extends FoldingBuilderEx {

    @NotNull
    @Override
    public FoldingDescriptor[] buildFoldRegions(@NotNull PsiElement root, @NotNull Document document, boolean quick) {
        List<FoldingDescriptor> descriptors = new ArrayList<FoldingDescriptor>();
        PsiElement element = getNextComment(root.getFirstChild());
        while (element != null) {
            PsiElement start = getNextNonComment(element);
            PsiElement end = getNextComment(start);
            if (start != null && end != null) {
                TextRange range = getBlockRange(start, end);
                if (range != null)
                    descriptors.add(new FoldingDescriptor(start.getNode(), range));
            }
            element = end;
        }
        return descriptors.toArray(new FoldingDescriptor[descriptors.size()]);
    }

    @Nullable
    @Override
    public String getPlaceholderText(@NotNull ASTNode node) {
        return " <...> ";
    }

    @Override
    public boolean isCollapsedByDefault(@NotNull ASTNode node) {
        return false;
    }

    protected PsiElement getNextComment(PsiElement element) {
        while (element != null && !(element instanceof Xas99Linecomment)) {
            element = element.getNextSibling();
        }
        return element;
    }

    protected PsiElement getNextNonComment(PsiElement element) {
        assert element instanceof Xas99Linecomment;
        while (element != null && element instanceof Xas99Linecomment) {
            element = element.getNextSibling().getNextSibling();  // COMMENT + CRLF
        }
        return element;
    }

    protected TextRange getBlockRange(PsiElement from, PsiElement upto) {
        int offset = from.getTextRange().getStartOffset(), size = 0;
        while (from != upto) {
            PsiElement curr = from;
            from = from.getNextSibling();
            if (from != upto || upto == null)  // exclude last element before upto (CRLF)
                size += curr.getTextLength();
        }
        return size > 0 ? new TextRange(offset, offset + size) : null;
    }
}
