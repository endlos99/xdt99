package net.endlos.xdt99.xbas99l;

import com.intellij.psi.PsiElement;
import com.intellij.psi.util.PsiTreeUtil;
import net.endlos.xdt99.xbas99l.psi.*;

import java.util.*;

public class Xbas99LUtil {

    public static List<Xbas99LLabeldef> findLabeldefs(PsiElement ref, String ident, boolean partial) {
        final List<Xbas99LLabeldef> nil = Collections.<Xbas99LLabeldef>emptyList();
        List<Xbas99LLabeldef> result = null;
        Xbas99LFile file = (Xbas99LFile) ref.getOriginalElement().getContainingFile();  // search only current file
        if (file == null)
            return nil;
        Collection<Xbas99LLabeldef> labels = PsiTreeUtil.findChildrenOfType(file, Xbas99LLabeldef.class);
        for (Xbas99LLabeldef label : labels) {
            String normalizedLabel = label.getName().toUpperCase();
            if ((partial && normalizedLabel.startsWith(ident)) ||  // ident already uppercased
                    (!partial && ident.equals(normalizedLabel))) {
                if (result == null) {
                    result = new ArrayList<Xbas99LLabeldef>();
                }
                result.add(label);
                // could break here, since there should be only one!
            }
        }
        return result != null ? result : nil;
    }

    public static List<Xbas99LNamedElement> findNvardef(PsiElement ref, String ident, boolean partial) {
        return findThings(ref, Xbas99LNvarW.class, ident, partial, false);
    }

    public static List<Xbas99LNamedElement> findBothNdef(PsiElement ref, String ident, boolean partial) {
        List<Xbas99LNamedElement> result = findThings(ref, Xbas99LNvarW.class, ident, partial, false);  // save time by
        List<Xbas99LNamedElement> funs = findThings(ref, Xbas99LNvarF.class, ident, partial, false);  // getting only one def
        result.addAll(funs);
        return result;
    }

    public static List<Xbas99LNamedElement> findSvardef(PsiElement ref, String ident, boolean partial) {
        return findThings(ref, Xbas99LSvarW.class, ident, partial, false);
    }

    public static List<Xbas99LNamedElement> findBothSdef(PsiElement ref, String ident, boolean partial) {
        List<Xbas99LNamedElement> result = findThings(ref, Xbas99LSvarW.class, ident, partial, false);
        List<Xbas99LNamedElement> funs = findThings(ref, Xbas99LSvarF.class, ident, partial, false);
        result.addAll(funs);
        return result;
    }

    public static List<Xbas99LNamedElement> findFNvardef(PsiElement ref, String ident) {
        return findThings(ref, Xbas99LNvarF.class, ident, false, false);
    }

    public static List<Xbas99LNamedElement> findFSvardef(PsiElement ref, String ident) {
        return findThings(ref, Xbas99LSvarF.class, ident, false, false);
    }

    public static List<Xbas99LNamedElement> findLabelUsages(Xbas99LLabeldef ref) {
        return findThings(ref, Xbas99LLabelref.class, ref.getName(), false, false);  // only used in Annotator
    }

    public static List<Xbas99LNamedElement> findNvarUsages(Xbas99LNvarW ref) {
        return findThings(ref, Xbas99LNvarR.class, ref.getName(), false, false);  // only used in Annotator
    }

    public static List<Xbas99LNamedElement> findSvarUsages(Xbas99LSvarW ref) {
        return findThings(ref, Xbas99LSvarR.class, ref.getName(), false, false);  // only used in Annotator
    }

    private static <T extends Xbas99LNamedElement> List<Xbas99LNamedElement>
            findThings(PsiElement ref, Class<T> clazz, String ident, boolean partial, boolean all) {
        String normalizedIdent = ident.toUpperCase();
        List<Xbas99LNamedElement> result = new ArrayList<>();
        Xbas99LFile file = (Xbas99LFile) ref.getOriginalElement().getContainingFile();  // search only current file
        if (file == null)
            return result;
        Collection<Xbas99LNamedElement> elems = PsiTreeUtil.findChildrenOfType(file, clazz);
        for (Xbas99LNamedElement elem : elems) {
            String normalizedElem = elem.getName().toUpperCase();
            if ((partial && normalizedElem.startsWith(normalizedIdent)) ||
                    (!partial && normalizedIdent.equals(normalizedElem))) {
                result.add(elem);
                if (!all)
                    break;
            }
        }
        return result;
    }

}
