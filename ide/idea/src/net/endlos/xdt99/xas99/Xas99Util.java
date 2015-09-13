package net.endlos.xdt99.xas99;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiManager;
import com.intellij.psi.search.FileTypeIndex;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.psi.util.PsiTreeUtil;
import com.intellij.util.indexing.FileBasedIndex;
import net.endlos.xdt99.xas99.psi.Xas99File;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;

import java.util.*;

public class Xas99Util {
    public static List<Xas99Labeldef> findLabels(Project project, PsiElement element, String ident, int offset, int distance) {
        if (distance == 0) {
            // global search
            List<Xas99Labeldef> result = null;
            Collection<VirtualFile> virtualFiles = FileBasedIndex.getInstance().getContainingFiles(FileTypeIndex.NAME, Xas99FileType.INSTANCE,
                    GlobalSearchScope.allScope(project));
            for (VirtualFile virtualFile : virtualFiles) {
                Xas99File file = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
                if (file != null) {
                    Xas99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xas99Labeldef.class);
                    if (labels != null) {
                        for (Xas99Labeldef label : labels) {
                            if (ident.equals(label.getText().toUpperCase())) {
                                if (result == null) {
                                    result = new ArrayList<Xas99Labeldef>();
                                }
                                result.add(label);
                            }
                        }
                    }
                }
            }
            return result != null ? result : Collections.<Xas99Labeldef>emptyList();
        } else {
            // local search
            PsiElement file = element;
            while (!(file instanceof Xas99File))
                file = file.getParent();
            final String name = ident.substring(Math.abs(distance) - 1);  // label definition text to look for
            Xas99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xas99Labeldef.class);
            if (labels != null) {
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
                if (e != null) {
                    Xas99Labeldef[] result = {e.getValue()};
                    return Arrays.asList(result);
                }
            }
            return Collections.<Xas99Labeldef>emptyList();
        }
    }

    public static List<Xas99Labeldef> findLabels(Project project) {
        List<Xas99Labeldef> result = new ArrayList<Xas99Labeldef>();
        Collection<VirtualFile> virtualFiles = FileBasedIndex.getInstance().getContainingFiles(FileTypeIndex.NAME, Xas99FileType.INSTANCE,
                GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File Xas99File = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (Xas99File != null) {
                Xas99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(Xas99File, Xas99Labeldef.class);
                if (labels != null) {
                    Collections.addAll(result, labels);
                }
            }
        }
        return result;
    }
}
