package net.endlos.xdt99.xbas99l.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFileFactory;
import com.intellij.psi.util.PsiTreeUtil;
import net.endlos.xdt99.xbas99l.Xbas99LFileType;

public class Xbas99LElementFactory {

    public static Xbas99LNamedElement createThing(Xbas99LNamedElement element, Project project, String name) {
        if (element instanceof Xbas99LNvarW)
            return createNvarW(project, name);
        else if (element instanceof Xbas99LNvarR)
            return createNvarR(project, name);
        else if (element instanceof Xbas99LNvarF)
            return createNvarF(project, name);
        else if (element instanceof Xbas99LSvarW)
            return createSvarW(project, name);
        else if (element instanceof Xbas99LSvarR)
            return createSvarR(project, name);
        else if (element instanceof Xbas99LSvarF)
            return createSvarF(project, name);
        else
            return null;
    }

    public static Xbas99LLabeldef createLabeldef(Project project, String name) {
        final Xbas99LFile file = createFile(project, name + ":\n");
        PsiElement labeldef = file.getFirstChild();
        return labeldef instanceof Xbas99LLabeldef ? (Xbas99LLabeldef) labeldef : null;
    }

    public static Xbas99LLabelref createLabelref(Project project, String name) {
        final Xbas99LFile file = createFile(project, " GOTO " + name + "\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99LLabelref.class);
    }

    public static Xbas99LNvarW createNvarW(Project project, String name) {
        final Xbas99LFile file = createFile(project, " " + name + "=1\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99LNvarW.class);
    }

    public static Xbas99LNvarR createNvarR(Project project, String name) {
        final Xbas99LFile file = createFile(project, " X=" + name + "\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99LNvarR.class);
    }

    public static Xbas99LNvarF createNvarF(Project project, String name) {
        final Xbas99LFile file = createFile(project, " DEF " + name + "=1\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99LNvarF.class);
    }

    public static Xbas99LSvarW createSvarW(Project project, String name) {
        final Xbas99LFile file = createFile(project, " " + name + "=\"\"\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99LSvarW.class);
    }

    public static Xbas99LSvarR createSvarR(Project project, String name) {
        final Xbas99LFile file = createFile(project, " X$=" + name + "\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99LSvarR.class);
    }

    public static Xbas99LSvarF createSvarF(Project project, String name) {
        final Xbas99LFile file = createFile(project, " DEF " + name + "=\"\"\n");
        return PsiTreeUtil.findChildOfType(file, Xbas99LSvarF.class);
    }

    public static Xbas99LFile createFile(Project project, String text) {
        String name = "dummy.b99";
        return (Xbas99LFile) PsiFileFactory.getInstance(project).
                createFileFromText(name, Xbas99LFileType.INSTANCE, text);
    }

}
