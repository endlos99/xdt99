package net.endlos.xdt99.xas99;

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
            boolean getLocalLabels = normalizedIdent.startsWith("!");
            // NOTE: filtering by local prefix is only relevant for partial servers made by code completion!
            return findAll(project, normalizedIdent, partial, false, getLocalLabels);
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

    // find register aliases
    public static List<Xas99Labeldef> findAliases(Project project, String ident, boolean partial) {
        String normalizedIdent = ident.toUpperCase();
        return findAll(project, normalizedIdent, partial, true, false);
    }

    // find all macros
    public static List<Xas99OpMacrodef> findMacros(Project project, String ident, boolean partial) {
        List<Xas99OpMacrodef> result = new ArrayList<>();
        String normalizedIdent = ident.toUpperCase();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xas99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xas99OpMacrodef> macros = PsiTreeUtil.findChildrenOfType(file, Xas99OpMacrodef.class);
            for (Xas99OpMacrodef macro : macros) {
                String normalizedMacro = macro.getText().toUpperCase();
                if ((!partial && normalizedIdent.equals(normalizedMacro)) ||
                        (partial && normalizedMacro.startsWith(normalizedIdent))) {
                    result.add(macro);
                }
            }
        }
        return result;
    }

    // get both labels and aliases
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

    // find label usages for Annotator
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

    // find alias usages for Annotator
    public static List<Xas99OpAlias> findAliasUsages(Xas99Labeldef label) {
        List<Xas99OpAlias> result = new ArrayList<>();
        Project project = label.getProject();
        String labelText = label.getName();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xas99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xas99OpAlias> usages = PsiTreeUtil.findChildrenOfType(file, Xas99OpAlias.class);
            for (Xas99OpAlias usage : usages) {
                if (labelText.equalsIgnoreCase(usage.getName()))
                    result.add(usage);
            }
        }
        return result;
    }

    // find macro usages for Annotator
    public static List<Xas99OpMacro> findMacroUsages(Xas99OpMacrodef macro) {
        List<Xas99OpMacro> result = new ArrayList<>();
        Project project = macro.getProject();
        String macroText = macro.getName();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xas99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xas99OpMacro> usages = PsiTreeUtil.findChildrenOfType(file, Xas99OpMacro.class);
            for (Xas99OpMacro usage : usages) {
                if (macroText.equalsIgnoreCase(usage.getName()))
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
        PsiElement prev = element.getPrevSibling();
        if (prev instanceof PsiWhiteSpace) {
            prev = prev.getPrevSibling();
        }
        if (prev == null)
            return false;
        return prev.getNode().getElementType() == Xas99Types.OP_MINUS;
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
        return element instanceof Xas99OpLabel && ((Xas99OpLabel) element).getName().charAt(0) == '!';
    }

    private static List<Xas99Labeldef> findAll(Project project, String ident, boolean partial, boolean getAliases,
                                               boolean localLabels) {
        List<Xas99Labeldef> result = new ArrayList<>();
        Collection<VirtualFile> virtualFiles =
                FileTypeIndex.getFiles(Xas99FileType.INSTANCE, GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (file == null)
                continue;
            Collection<Xas99Labeldef> labels = PsiTreeUtil.findChildrenOfType(file, Xas99Labeldef.class);
            for (Xas99Labeldef label : labels) {
                if (isAliasDefinition(label) == getAliases) {
                    String normalizedLabel = label.getText().toUpperCase();
                    if ((normalizedLabel.charAt(0) == LOCAL_LABEL_PREFIX) == localLabels) {
                        if ((!partial && ident.equals(normalizedLabel)) ||
                                (partial && normalizedLabel.startsWith(ident))) {
                            result.add(label);
                        }
                    }
                }
            }
        }
        return result;
    }

    public static boolean isAliasDefinition(PsiElement element) {
        try {
            element = element.getNextSibling();
            if (element.getNode().getElementType() == Xas99Types.OP_COLON)
                element = element.getNextSibling().getNextSibling().getNextSibling();
            else
                element = element.getNextSibling();
            return element instanceof Xas99AliasDefinition;
        } catch (NullPointerException x) {
            return false;
        }
    }

}
