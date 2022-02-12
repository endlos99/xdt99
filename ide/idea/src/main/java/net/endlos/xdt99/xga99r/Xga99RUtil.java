package net.endlos.xdt99.xga99r;

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
import net.endlos.xdt99.xga99r.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.*;

public class Xga99RUtil {
    private static final Character LOCAL_LABEL_PREFIX = '!';

    // find all symbol definitions in project
    public static List<Xga99RLabeldef> findLabels(Project project, String ident, int distance, PsiElement element,
                                                 int offset, boolean partial) {
        String normalizedIdent = ident.toUpperCase();
        if (distance == 0) {
            // non-local label search
            List<Xga99RLabeldef> result = null;
            Collection<VirtualFile> virtualFiles =
                    FileTypeIndex.getFiles(Xga99RFileType.INSTANCE, GlobalSearchScope.allScope(project));
            for (VirtualFile virtualFile : virtualFiles) {
                Xga99RFile file = (Xga99RFile) PsiManager.getInstance(project).findFile(virtualFile);
                if (file == null)
                    continue;
                Xga99RLabeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xga99RLabeldef.class);
                if (labels == null)
                    continue;
                for (Xga99RLabeldef label : labels) {
                    String normalizedLabel = label.getText().toUpperCase();
                    if ((!partial && normalizedIdent.equals(normalizedLabel)) ||
                            (partial && normalizedLabel.startsWith(normalizedIdent))) {
                        if (result == null) {
                            result = new ArrayList<Xga99RLabeldef>();
                        }
                        result.add(label);
                    }
                }
            }
            return result != null ? result : Collections.<Xga99RLabeldef>emptyList();
        } else {
            // local label search
            PsiElement file = element;
            while (!(file instanceof Xga99RFile))
                file = file.getParent();
            final String name = normalizedIdent.substring(Math.abs(distance) - 1);  // label definition text to look for
            Xga99RLabeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xga99RLabeldef.class);
            if (labels == null)
                return Collections.<Xga99RLabeldef>emptyList();
            TreeMap<Integer, Xga99RLabeldef> defs = new TreeMap<Integer, Xga99RLabeldef>();
            for (Xga99RLabeldef label : labels) {
                int pos = label.getTextOffset();
                if (name.equals(label.getText().toUpperCase()) &&
                        (distance > 0 && pos > offset || distance < 0 && pos < offset)) {
                    defs.put(distance > 0 ? pos : -pos, label);
                }
            }
            Map.Entry<Integer, Xga99RLabeldef> e = defs.firstEntry();
            int count = Math.abs(distance);
            while (e != null && --count > 0)
                e = defs.higherEntry(e.getKey());
            if (e == null)
                return Collections.<Xga99RLabeldef>emptyList();
            Xga99RLabeldef[] result = {e.getValue()};
            return Arrays.asList(result);
        }
    }

    public static List<Xga99RLabeldef> findLabels(Project project) {
        List<Xga99RLabeldef> result = new ArrayList<Xga99RLabeldef>();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xga99RFileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xga99RFile file = (Xga99RFile) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Xga99RLabeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xga99RLabeldef.class);
            if (labels != null) {
                Collections.addAll(result, labels);
            }
        }
        return result;
    }

    public static List<Xga99ROpLabel> findLabelUsages(Xga99RLabeldef label) {
        List<Xga99ROpLabel> result = new ArrayList<>();
        Project project = label.getProject();
        String labelText = label.getName();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xga99RFileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xga99RFile file = (Xga99RFile) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xga99ROpLabel> usages = PsiTreeUtil.findChildrenOfType(file, Xga99ROpLabel.class);
            for (Xga99ROpLabel usage : usages) {
                if (labelText.equalsIgnoreCase(usage.getName()))
                    result.add(usage);
            }
        }
        return result;
    }

    @Nullable
    public static String getLabeldefText(@NotNull Xga99RLabeldef element, IntWrapper lino) {
        // get line number:
        int lineNumber = 1;  // CRLF of element line is implicit
        for (PsiElement prev = element; prev != null; prev = prev.getPrevSibling()) {
            if (prev.getNode().getElementType() == Xga99RTypes.CRLF)
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
            if (e instanceof Xga99RLinecomment) {
                startOffset = e.getTextOffset();
                allowedCrLfsInARow = 1;
            } else if (e.getNode().getElementType() == Xga99RTypes.CRLF) {
                if (allowedCrLfsInARow-- == 0)
                    break;
            } else
                break;
        }
        boolean colon = false;
        e = element;
        while (e != null) {
            if (e.getNode().getElementType() == Xga99RTypes.CRLF) {
                if (colon)
                    colon = false;  // if colon, include next line as well
                else
                    break;  // end of line(s)
            } else if (e.getNode().getElementType() == Xga99RTypes.OP_COLON) {
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
            return prev.getNode().getElementType() == Xga99RTypes.OP_MINUS;
        } catch (NullPointerException e) {
            return false;
        }
    }

    public static int findBeginningOfLine(PsiElement element) {
        while (element != null && !(element.getParent() instanceof Xga99RFile))
            element = element.getParent();
        while (element != null &&
                (element.getPrevSibling() == null ||
                        element.getPrevSibling().getNode().getElementType() != Xga99RTypes.CRLF))
            element = element.getPrevSibling();
        return element == null ? 0 : element.getTextOffset();
    }

    // check if element tree is equivalent to positive local label (-!... is ignored):
    // expr -> op_address -> op_label -> ident with '!'
    public static boolean isLocalLabelExpr(PsiElement element) {
        return element instanceof Xga99ROpLabel && ((Xga99ROpLabel) element).getName().charAt(0) == '!';    }

}
