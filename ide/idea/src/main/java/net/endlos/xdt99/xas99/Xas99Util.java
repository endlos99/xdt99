package net.endlos.xdt99.xas99;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiManager;
import com.intellij.psi.search.FileTypeIndex;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.psi.util.PsiTreeUtil;
import net.endlos.xdt99.common.IntWrapper;
import net.endlos.xdt99.xas99.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.*;

public class Xas99Util {
    private static final Character LOCAL_LABEL_PREFIX = '!';

    // find all symbol definitions in project
    public static List<Xas99Labeldef> findLabels(Project project, String ident, int distance, PsiElement element,
                                                 int offset, boolean partial) {
        String normalizedIdent = ident.toUpperCase();
        if (distance == 0) {
            // non-local label search
            List<Xas99Labeldef> result = null;
            Collection<VirtualFile> virtualFiles =
                    FileTypeIndex.getFiles(Xas99FileType.INSTANCE, GlobalSearchScope.allScope(project));
            for (VirtualFile virtualFile : virtualFiles) {
                Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
                if (file == null)
                    continue;
                Collection<Xas99Labeldef> labels = PsiTreeUtil.findChildrenOfType(file, Xas99Labeldef.class);
                for (Xas99Labeldef label : labels) {
                    String normalizedLabel = label.getText().toUpperCase();
                    if ((!partial && normalizedIdent.equals(normalizedLabel)) ||
                            (partial && normalizedLabel.startsWith(normalizedIdent))) {
                        if (result == null) {
                            result = new ArrayList<Xas99Labeldef>();
                        }
                        result.add(label);
                    }
                }
            }
            return result != null ? result : Collections.<Xas99Labeldef>emptyList();
        } else {
            // local label search
            PsiElement file = element;
            while (!(file instanceof Xas99File))
                file = file.getParent();
            final String name = normalizedIdent.substring(Math.abs(distance) - 1);  // label definition text to look for
            Xas99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xas99Labeldef.class);
            if (labels == null)
                return Collections.<Xas99Labeldef>emptyList();
            TreeMap<Integer, Xas99Labeldef> defs = new TreeMap<Integer, Xas99Labeldef>();
            for (Xas99Labeldef label : labels) {
                int pos = label.getTextOffset();
                if (name.equals(label.getText().toUpperCase()) &&
                        (distance > 0 && pos > offset || distance < 0 && pos < offset)) {
                    defs.put(distance > 0 ? pos : -pos, label);
                }
            }
            Map.Entry<Integer, Xas99Labeldef> e = defs.firstEntry();
            int count = Math.abs(distance);
            while (e != null && --count > 0)
                e = defs.higherEntry(e.getKey());
            if (e == null)
                return Collections.<Xas99Labeldef>emptyList();
            Xas99Labeldef[] result = {e.getValue()};
            return Arrays.asList(result);
        }
    }

    public static List<Xas99Labeldef> findLabels(Project project) {
        List<Xas99Labeldef> result = new ArrayList<Xas99Labeldef>();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xas99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xas99Labeldef> labels = PsiTreeUtil.findChildrenOfType(file, Xas99Labeldef.class);
            result.addAll(labels);
        }
        return result;
    }

    public static List<Xas99OpLabel> findLabelUsages(Xas99Labeldef label) {
        List<Xas99OpLabel> result = new ArrayList<>();
        Project project = label.getProject();
        String labelText = label.getName();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xas99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xas99OpLabel> usages = PsiTreeUtil.findChildrenOfType(file, Xas99OpLabel.class);
            for (Xas99OpLabel usage : usages) {
                if (labelText.equalsIgnoreCase(usage.getName()))
                    result.add(usage);
            }
        }
        return result;
    }

    @Nullable
    public static String getLabeldefText(@NotNull Xas99Labeldef element, IntWrapper lino) {
        // get line number:
        int lineNumber = 1;  // CRLF of element line is implicit
        for (PsiElement prev = element; prev != null; prev = prev.getPrevSibling()) {
            if (prev.getNode().getElementType() == Xas99Types.CRLF)
                ++lineNumber;
        }
        lino.set(lineNumber);  // wrapper for pass-by-reference

        // build text
        PsiDocumentManager psiDocumentManager = PsiDocumentManager.getInstance(element.getProject());
        Document document = psiDocumentManager.getDocument(element.getContainingFile());
        if (document == null)
            return null;
        int startOffset = element.getTextRange().getStartOffset();
        PsiElement e = element;
        int allowedCrLfsInARow = 1;
        for (;;) {
            e = e.getPrevSibling();
            if (e == null)
                break;
            if (e instanceof Xas99Linecomment) {
                startOffset = e.getTextOffset();
                allowedCrLfsInARow = 1;
            } else if (e.getNode().getElementType() == Xas99Types.CRLF) {
                if (allowedCrLfsInARow-- == 0)
                    break;
            } else
                break;
        }
        boolean colon = false;
        e = element;
        while (e != null) {
            if (e.getNode().getElementType() == Xas99Types.CRLF) {
                if (colon)
                    colon = false;  // if colon, include next line as well
                else
                    break;  // end of line(s)
            } else if (e.getNode().getElementType() == Xas99Types.OP_COLON) {
                colon = true;
            }
            e = e.getNextSibling();
        }
        if (e == null)
            return null;
        final int endOffset = e.getTextOffset();
        return document.getText(new TextRange(startOffset, endOffset));
    }

    public static int getDistance(String localLabel, PsiElement element) {
        int distance = 0;
        while (distance < localLabel.length() && localLabel.charAt(distance) == LOCAL_LABEL_PREFIX)
            ++distance;
        return isNegativeDirection(element) ? -distance : distance;
    }

    private static boolean isNegativeDirection(PsiElement element) {
        try {
            PsiElement prev = element.getParent().getParent().getPrevSibling();
            return prev.getNode().getElementType() == Xas99Types.OP_MINUS;
        } catch (NullPointerException e) {
            return false;
        }
    }

    public static int findBeginningOfLine(PsiElement element) {
        while (element != null && !(element.getParent() instanceof Xas99File))
            element = element.getParent();
        while (element != null &&
                (element.getPrevSibling() == null ||
                        element.getPrevSibling().getNode().getElementType() != Xas99Types.CRLF))
            element = element.getPrevSibling();
        return element == null ? 0 : element.getTextOffset();
    }

    // check if element tree is equivalent to positive local label (-!... is ignored):
    // expr -> op_address -> op_label -> ident with '!'
    public static boolean isLocalLabelExpr(PsiElement element) {
        if (!(element instanceof Xas99Expr))
            return false;
        element = element.getFirstChild();
        if (element.getNode().getElementType() != Xas99Types.OP_ADDRESS)
            return false;
        element = element.getFirstChild();
        if (element.getNode().getElementType() != Xas99Types.OP_LABEL)
            return false;
        if (((Xas99OpLabel) element).getName().charAt(0) != '!')
            return false;
        return true;
    }

}
