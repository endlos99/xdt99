package net.endlos.xdt99.xga99;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiManager;
import com.intellij.psi.search.FileTypeIndex;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.psi.util.PsiTreeUtil;
import com.intellij.util.indexing.FileBasedIndex;
import net.endlos.xdt99.xga99.psi.Xga99File;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;

import java.util.*;

public class Xga99Util {
    public static List<Xga99Labeldef> findLabels(Project project, PsiElement element, String ident, int offset, int distance) {
        if (distance == 0) {
            // global search
            List<Xga99Labeldef> result = null;
            Collection<VirtualFile> virtualFiles = FileBasedIndex.getInstance().getContainingFiles(FileTypeIndex.NAME, Xga99FileType.INSTANCE,
                    GlobalSearchScope.allScope(project));
            for (VirtualFile virtualFile : virtualFiles) {
                Xga99File file = (Xga99File) PsiManager.getInstance(project).findFile(virtualFile);
                if (file != null) {
                    Xga99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xga99Labeldef.class);
                    if (labels != null) {
                        for (Xga99Labeldef label : labels) {
                            if (ident.equals(label.getText().toUpperCase())) {
                                if (result == null) {
                                    result = new ArrayList<Xga99Labeldef>();
                                }
                                result.add(label);
                            }
                        }
                    }
                }
            }
            return result != null ? result : Collections.<Xga99Labeldef>emptyList();
        } else {
            // local search
            PsiElement file = element;
            while (!(file instanceof Xga99File))
                file = file.getParent();
            final String name = ident.substring(Math.abs(distance) - 1);  // label definition text to look for
            Xga99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(file, Xga99Labeldef.class);
            if (labels != null) {
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
                if (e != null) {
                    Xga99Labeldef[] result = {e.getValue()};
                    return Arrays.asList(result);
                }
            }
            return Collections.<Xga99Labeldef>emptyList();
        }
    }

    public static List<Xga99Labeldef> findLabels(Project project) {
        List<Xga99Labeldef> result = new ArrayList<Xga99Labeldef>();
        Collection<VirtualFile> virtualFiles = FileBasedIndex.getInstance().getContainingFiles(FileTypeIndex.NAME, Xga99FileType.INSTANCE,
                GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xga99File Xga99File = (Xga99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (Xga99File != null) {
                Xga99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(Xga99File, Xga99Labeldef.class);
                if (labels != null) {
                    Collections.addAll(result, labels);
                }
            }
        }
        return result;
    }
}
