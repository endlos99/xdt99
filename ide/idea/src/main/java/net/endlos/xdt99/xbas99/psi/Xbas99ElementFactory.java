package net.endlos.xdt99.xbas99.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFileFactory;
import com.intellij.psi.util.PsiTreeUtil;
import net.endlos.xdt99.xbas99.Xbas99FileType;

public class Xbas99ElementFactory {

    public static Xbas99NamedElement createThing(Xbas99NamedElement element, Project project, String name) {
        if (element instanceof Xbas99NvarW)
            return createNvarW(project, name);
        else if (element instanceof Xbas99NvarR)
            return createNvarR(project, name);
        else if (element instanceof Xbas99NvarF)
            return createNvarF(project, name);
        else if (element instanceof Xbas99SvarW)
            return createSvarW(project, name);
        else if (element instanceof Xbas99SvarR)
            return createSvarR(project, name);
        else if (element instanceof Xbas99SvarF)
            return createSvarF(project, name);
        else
            return null;
    }

    public static Xbas99Linedef createLinedef(Project project, String name) {
        final Xbas99File file = createFile(project, name + " END\n");
        PsiElement linedef = file.getFirstChild();
        return linedef instanceof Xbas99Linedef ? (Xbas99Linedef) linedef : null;
    }

    public static Xbas99Lino createLino(Project project, String name) {
        final Xbas99File file = createFile(project, "1 GOTO " + name + "\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99Lino.class);
    }

    public static Xbas99NvarW createNvarW(Project project, String name) {
        final Xbas99File file = createFile(project, "1 " + name + "=1\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99NvarW.class);
    }

    public static Xbas99NvarR createNvarR(Project project, String name) {
        final Xbas99File file = createFile(project, "1 X=" + name + "\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99NvarR.class);
    }

    public static Xbas99NvarF createNvarF(Project project, String name) {
        final Xbas99File file = createFile(project, "1 DEF " + name + "=1\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99NvarF.class);
    }

    public static Xbas99SvarW createSvarW(Project project, String name) {
        final Xbas99File file = createFile(project, "1 " + name + "=\"\"\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99SvarW.class);
    }

    public static Xbas99SvarR createSvarR(Project project, String name) {
        final Xbas99File file = createFile(project, "1 X$=" + name + "\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99SvarR.class);
    }

    public static Xbas99SvarF createSvarF(Project project, String name) {
        final Xbas99File file = createFile(project, "1 DEF " + name + "=\"\"\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99SvarF.class);
    }

    public static Xbas99File createFile(Project project, String text) {
        String name = "dummy.b99";
        return (Xbas99File) PsiFileFactory.getInstance(project).
                createFileFromText(name, Xbas99FileType.INSTANCE, text);
    }

}
