package net.endlos.xdt99.xbas99;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiManager;
import com.intellij.psi.util.PsiTreeUtil;
import net.endlos.xdt99.xbas99.psi.*;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

public class Xbas99Util {
    public static List<Xbas99Linedef> findLinedefs(PsiElement ref, String ident) {
        List<Xbas99Linedef> result = null;
        Project project = ref.getProject();
        VirtualFile currentFile = ref.getOriginalElement().getContainingFile().getVirtualFile();
        Xbas99File Xbas99File = (Xbas99File) PsiManager.getInstance(project).findFile(currentFile);
        if (Xbas99File != null) {
            Xbas99Linedef[] elems = PsiTreeUtil.getChildrenOfType(Xbas99File, Xbas99Linedef.class);
            if (elems != null) {
                for (Xbas99Linedef elem : elems) {
                    if (ident.equals(elem.getName())) {
                        if (result == null) {
                            result = new ArrayList<Xbas99Linedef>();
                        }
                        result.add(elem);
                    }
                }
            }
        }
        return result != null ? result : Collections.<Xbas99Linedef>emptyList();
    }

    public static <T extends Xbas99NamedElement> T findSingleVar(PsiElement ref, String ident, Class<T> clazz) {
        Project project = ref.getProject();
        VirtualFile currentFile = ref.getOriginalElement().getContainingFile().getVirtualFile();
        Xbas99File Xbas99File = (Xbas99File) PsiManager.getInstance(project).findFile(currentFile);
        if (Xbas99File != null) {
            Collection<T> elems = PsiTreeUtil.findChildrenOfType(Xbas99File, clazz);
            for (T elem : elems) {
                if (ident.equals(elem.getName().toUpperCase())) {
                    return elem;
                }
            }
        }
        return null;
    }

    public static Xbas99Nvar findNvardef(PsiElement ref, String ident) {
        return findSingleVar(ref, ident.toUpperCase(), Xbas99Nvar.class);
    }

    public static Xbas99Svar findSvardef(PsiElement ref, String ident) {
        return findSingleVar(ref, ident.toUpperCase(), Xbas99Svar.class);
    }

    public static List<Xbas99Linedef> findLinedefs(PsiElement ref) {
        List<Xbas99Linedef> result = new ArrayList<Xbas99Linedef>();
        Project project = ref.getProject();
        VirtualFile currentFile = ref.getOriginalElement().getContainingFile().getVirtualFile();
        Xbas99File Xbas99File = (Xbas99File) PsiManager.getInstance(project).findFile(currentFile);
        if (Xbas99File != null) {
            Xbas99Linedef[] elems = PsiTreeUtil.getChildrenOfType(Xbas99File, Xbas99Linedef.class);
            if (elems != null) {
                Collections.addAll(result, elems);
            }
        }
        return result;
    }

    public static <T extends Xbas99NamedElement> List<T> findVars(PsiElement ref, Class<T> clazz) {
        List<T> result = new ArrayList<T>();
        Project project = ref.getProject();
        VirtualFile currentFile = ref.getOriginalElement().getContainingFile().getVirtualFile();
        Xbas99File Xbas99File = (Xbas99File) PsiManager.getInstance(project).findFile(currentFile);
        if (Xbas99File != null) {
            Collection<T> elems = PsiTreeUtil.findChildrenOfType(Xbas99File, clazz);
            if (elems.size() > 0) {
                result.addAll(elems);
            }
        }
        return result;
    }

    public static List<Xbas99Nvar> findNvardefs(PsiElement ref) {
        return findVars(ref, Xbas99Nvar.class);
    }

    public static List<Xbas99Svar> findSvardefs(PsiElement ref) {
        return findVars(ref, Xbas99Svar.class);
    }
}
