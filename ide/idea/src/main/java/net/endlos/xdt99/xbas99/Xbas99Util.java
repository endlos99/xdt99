package net.endlos.xdt99.xbas99;

import com.intellij.psi.PsiElement;
import com.intellij.psi.util.PsiTreeUtil;
import net.endlos.xdt99.xbas99.psi.*;

import java.util.*;

public class Xbas99Util {

    public static List<Xbas99Linedef> findLinedefs(PsiElement ref, String ident, boolean partial) {
        final List<Xbas99Linedef> nil = Collections.<Xbas99Linedef>emptyList();
        List<Xbas99Linedef> result = null;
        Xbas99File file = (Xbas99File) ref.getOriginalElement().getContainingFile();  // search only current file
        if (file == null)
            return nil;
        Collection<Xbas99Linedef> linedefs = PsiTreeUtil.findChildrenOfType(file, Xbas99Linedef.class);
        for (Xbas99Linedef linedef : linedefs) {
            String normalizedLinedef = linedef.getName().toUpperCase();
            if ((partial && normalizedLinedef.startsWith(ident)) ||  // ident already uppercased
                    (!partial && ident.equals(normalizedLinedef))) {
                if (result == null) {
                    result = new ArrayList<Xbas99Linedef>();
                }
                result.add(linedef);
                // could break here, since there should be only one!
            }
        }
        return result != null ? result : nil;
    }

    public static List<Xbas99NamedElement> findNvardef(PsiElement ref, String ident, boolean partial) {
        return findThings(ref, Xbas99NvarW.class, ident, partial, false);
    }

    public static List<Xbas99NamedElement> findBothNdef(PsiElement ref, String ident, boolean partial) {
        List<Xbas99NamedElement> result = findThings(ref, Xbas99NvarW.class, ident, partial, false);  // save time by
        List<Xbas99NamedElement> funs = findThings(ref, Xbas99NvarF.class, ident, partial, false);  // only getting one def
        result.addAll(funs);
        return result;
    }

    public static List<Xbas99NamedElement> findSvardef(PsiElement ref, String ident, boolean partial) {
        return findThings(ref, Xbas99SvarW.class, ident, partial, false);
    }

    public static List<Xbas99NamedElement> findBothSdef(PsiElement ref, String ident, boolean partial) {
        List<Xbas99NamedElement> result = findThings(ref, Xbas99SvarW.class, ident, partial, false);
        List<Xbas99NamedElement> funs = findThings(ref, Xbas99SvarF.class, ident, partial, false);
        result.addAll(funs);
        return result;
    }

    public static List<Xbas99NamedElement> findFNvardef(PsiElement ref, String ident) {
        return findThings(ref, Xbas99NvarF.class, ident, false, false);
    }

    public static List<Xbas99NamedElement> findFSvardef(PsiElement ref, String ident) {
        return findThings(ref, Xbas99SvarF.class, ident, false, false);
    }

    public static List<Xbas99NamedElement> findLinoUsages(Xbas99Lino ref) {
        return findThings(ref, Xbas99Linedef.class, ref.getName(), false, false);  // only used in Annotator
    }

    public static List<Xbas99NamedElement> findNvarUsages(Xbas99NvarW ref) {
        return findThings(ref, Xbas99NvarR.class, ref.getName(), false, false);  // only used in Annotator
    }

    public static List<Xbas99NamedElement> findSvarUsages(Xbas99SvarW ref) {
        return findThings(ref, Xbas99SvarR.class, ref.getName(), false, false);  // only used in Annotator
    }

    private static <T extends Xbas99NamedElement> List<Xbas99NamedElement>
            findThings(PsiElement ref, Class<T> clazz, String ident, boolean partial, boolean all) {
        String normalizedIdent = ident.toUpperCase();
        List<Xbas99NamedElement> result = new ArrayList<>();
        Xbas99File file = (Xbas99File) ref.getOriginalElement().getContainingFile();  // search only current file
        if (file == null)
            return result;
        Collection<Xbas99NamedElement> elems = PsiTreeUtil.findChildrenOfType(file, clazz);
        for (Xbas99NamedElement elem : elems) {
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
