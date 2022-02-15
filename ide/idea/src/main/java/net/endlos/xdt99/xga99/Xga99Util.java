package net.endlos.xdt99.xga99;

import com.intellij.openapi.editor.Document;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiDocumentManager;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiManager;
import com.intellij.psi.PsiWhiteSpace;
import com.intellij.psi.search.FileTypeIndex;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.psi.util.PsiTreeUtil;
import net.endlos.xdt99.common.IntWrapper;
import net.endlos.xdt99.xga99.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.*;

public class Xga99Util {
    private static final Character LOCAL_LABEL_PREFIX = '!';

    // find all symbol definitions in project
    public static List<Xga99Labeldef> findLabels(Project project, String ident, int distance, PsiElement element,
                                                 int offset, boolean partial) {
        String normalizedIdent = ident.toUpperCase();
        if (distance == 0) {
            // non-local label search
            List<Xga99Labeldef> result = null;
            Collection<VirtualFile> virtualFiles =
                    FileTypeIndex.getFiles(Xga99FileType.INSTANCE, GlobalSearchScope.allScope(project));
            for (VirtualFile virtualFile : virtualFiles) {
                Xga99File file = (Xga99File) PsiManager.getInstance(project).findFile(virtualFile);
                if (file == null)
                    continue;
                Collection<Xga99Labeldef> labels = PsiTreeUtil.findChildrenOfType(file, Xga99Labeldef.class);
                for (Xga99Labeldef label : labels) {
                    String normalizedLabel = label.getText().toUpperCase();
                    if ((!partial && normalizedIdent.equals(normalizedLabel)) ||
                            (partial && normalizedLabel.startsWith(normalizedIdent))) {
                        if (result == null) {
                            result = new ArrayList<Xga99Labeldef>();
                        }
                        result.add(label);
                    }
                }
            }
            return result != null ? result : Collections.<Xga99Labeldef>emptyList();
        } else {
            // local label search
            PsiElement file = element;
            while (!(file instanceof Xga99File))
                file = file.getParent();
            final String name = normalizedIdent.substring(Math.abs(distance) - 1);  // label definition text to look for
            Xga99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xga99Labeldef.class);
            if (labels == null)
                return Collections.<Xga99Labeldef>emptyList();
            TreeMap<Integer, Xga99Labeldef> defs = new TreeMap<Integer, Xga99Labeldef>();
            for (Xga99Labeldef label : labels) {
                int pos = label.getTextOffset();
                if (name.equals(label.getText().toUpperCase()) &&
                        (distance > 0 && pos > offset || distance < 0 && pos < offset)) {
                    defs.put(distance > 0 ? pos : -pos, label);
                }
            }
            Map.Entry<Integer, Xga99Labeldef> e = defs.firstEntry();
            int count = Math.abs(distance);
            while (e != null && --count > 0)
                e = defs.higherEntry(e.getKey());
            if (e == null)
                return Collections.<Xga99Labeldef>emptyList();
            Xga99Labeldef[] result = {e.getValue()};
            return Arrays.asList(result);
        }
    }

    public static List<Xga99Labeldef> findLabels(Project project) {
        List<Xga99Labeldef> result = new ArrayList<Xga99Labeldef>();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xga99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xga99File file = (Xga99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xga99Labeldef> labels = PsiTreeUtil.findChildrenOfType(file, Xga99Labeldef.class);
            result.addAll(labels);
        }
        return result;
    }

    public static List<Xga99OpLabel> findLabelUsages(Xga99Labeldef label) {
        List<Xga99OpLabel> result = new ArrayList<>();
        Project project = label.getProject();
        String labelText = label.getName();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xga99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xga99File file = (Xga99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xga99OpLabel> usages = PsiTreeUtil.findChildrenOfType(file, Xga99OpLabel.class);
            for (Xga99OpLabel usage : usages) {
                if (labelText.equalsIgnoreCase(usage.getName()))
                    result.add(usage);
            }
        }
        return result;
    }

    @Nullable
    public static String getLabeldefText(@NotNull Xga99Labeldef element, IntWrapper lino) {
        // get line number:
        int lineNumber = 1;  // CRLF of element line is implicit
        for (PsiElement prev = element; prev != null; prev = prev.getPrevSibling()) {
            if (prev.getNode().getElementType() == Xga99Types.CRLF)
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
            if (e instanceof Xga99Linecomment) {
                startOffset = e.getTextOffset();
                allowedCrLfsInARow = 1;
            } else if (e.getNode().getElementType() == Xga99Types.CRLF) {
                if (allowedCrLfsInARow-- == 0)
                    break;
            } else
                break;
        }
        boolean colon = false;
        e = element;
        while (e != null) {
            if (e.getNode().getElementType() == Xga99Types.CRLF) {
                if (colon)
                    colon = false;  // if colon, include next line as well
                else
                    break;  // end of line(s)
            } else if (e.getNode().getElementType() == Xga99Types.OP_COLON) {
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
        PsiElement prev = element.getPrevSibling();
        if (prev instanceof PsiWhiteSpace) {
            prev = prev.getPrevSibling();
        }
        if (prev == null)
            return false;
        return prev.getNode().getElementType() == Xga99Types.OP_MINUS;
    }

    public static int findBeginningOfLine(PsiElement element) {
        while (element != null && !(element.getParent() instanceof Xga99File))
            element = element.getParent();
        while (element != null &&
                (element.getPrevSibling() == null ||
                        element.getPrevSibling().getNode().getElementType() != Xga99Types.CRLF))
            element = element.getPrevSibling();
        return element == null ? 0 : element.getTextOffset();
    }

    // check if element tree is equivalent to positive local label (-!... is ignored):
    // expr -> op_address -> op_label -> ident with '!'
    public static boolean isLocalLabelExpr(PsiElement element) {
        return element instanceof Xga99OpLabel && ((Xga99OpLabel) element).getName().charAt(0) == '!';
    }

}
