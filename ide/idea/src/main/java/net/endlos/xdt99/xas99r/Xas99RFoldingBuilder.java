package net.endlos.xdt99.xas99r;

import com.intellij.lang.ASTNode;
import com.intellij.lang.folding.FoldingBuilderEx;
import com.intellij.lang.folding.FoldingDescriptor;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.editor.FoldingGroup;
import com.intellij.openapi.project.DumbAware;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import net.endlos.xdt99.xas99r.psi.Xas99RLinecomment;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99RFoldingBuilder extends FoldingBuilderEx implements DumbAware {
    private static final String folderName = "Xas99RFolder";
    private static int foldId = 0;

    @Override
    public FoldingDescriptor @NotNull [] buildFoldRegions(@NotNull PsiElement root, @NotNull Document document, boolean quick) {
        List<FoldingDescriptor> descriptors = new ArrayList<FoldingDescriptor>();
        PsiElement element = getNextComment(root.getFirstChild());  // skip to first comment
        while (element != null) {
            PsiElement start = getNextNonComment(element);
            PsiElement end = getNextComment(start);  // might be null = end of file
            if (start != null) {
                TextRange range = getBlockRange(start, end);
                if (range != null) {
                    FoldingGroup group = FoldingGroup.newGroup(folderName + foldId++);
                    descriptors.add(new FoldingDescriptor(start.getNode(), range, group));
                }
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

    private PsiElement getNextComment(PsiElement element) {
        while (element != null && !(element instanceof Xas99RLinecomment)) {
            element = element.getNextSibling();
        }
        return element;
    }

    private PsiElement getNextNonComment(PsiElement element) {
        while (element instanceof Xas99RLinecomment) {
            element = element.getNextSibling().getNextSibling();  // COMMENT + CRLF
        }
        return element;
    }

    private TextRange getBlockRange(PsiElement from, PsiElement to) {
        int offset = from.getTextRange().getStartOffset();
        int size = 0;
        while (from != to) {
            PsiElement curr = from;
            from = from.getNextSibling();
            if (from != to || to == null)  // exclude last element before up to (CRLF)
                size += curr.getTextLength();
        }
        return size > 0 ? new TextRange(offset, offset + size) : null;
    }

}
