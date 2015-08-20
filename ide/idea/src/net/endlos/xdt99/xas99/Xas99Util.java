package net.endlos.xdt99.xas99;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiManager;
import com.intellij.psi.search.FileTypeIndex;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.psi.util.PsiTreeUtil;
import com.intellij.util.indexing.FileBasedIndex;
import net.endlos.xdt99.xas99.psi.Xas99File;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

public class Xas99Util {
    public static List<Xas99Labeldef> findLabels(Project project, String ident) {
        String upper = ident.toUpperCase();
        List<Xas99Labeldef> result = null;
        Collection<VirtualFile> virtualFiles = FileBasedIndex.getInstance().getContainingFiles(FileTypeIndex.NAME, Xas99FileType.INSTANCE,
                GlobalSearchScope.allScope(project));
        for (VirtualFile virtualFile : virtualFiles) {
            Xas99File Xas99File = (Xas99File) PsiManager.getInstance(project).findFile(virtualFile);
            if (Xas99File != null) {
                Xas99Labeldef[] labels = PsiTreeUtil.getChildrenOfType(Xas99File, Xas99Labeldef.class);
                if (labels != null) {
                    for (Xas99Labeldef label : labels) {
                        if (upper.equals(label.getText().toUpperCase())) {
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
