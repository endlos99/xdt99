package net.endlos.xdt99.xbas99.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFileFactory;
import net.endlos.xdt99.xbas99.Xbas99FileType;

public class Xbas99ElementFactory {
    public static Xbas99Linedef createLinedef(Project project, String name) {
        final Xbas99File file = createFile(project, name + " END\n");
        PsiElement linedef = file.getFirstChild();
        return linedef instanceof Xbas99Linedef ? (Xbas99Linedef) linedef : null;
    }

    public static Xbas99Lino createLino(Project project, String name) {
        final Xbas99File file = createFile(project, "1 GOTO " + name + "\n");
        PsiElement slist = file.getChildren()[2];
        PsiElement lino = slist.getFirstChild().getFirstChild().getLastChild();
        return lino instanceof Xbas99Lino ? (Xbas99Lino) lino : null;
    }

    public static Xbas99Nvar createNvar(Project project, String name) {
        final Xbas99File file = createFile(project, "1 " + name + "=1\n");
        PsiElement slist = file.getChildren()[2];
        PsiElement var = slist.getFirstChild().getFirstChild().getFirstChild();
        return var instanceof Xbas99Nvar ? (Xbas99Nvar) var : null;
    }

    public static Xbas99Svar createSvar(Project project, String name) {
        final Xbas99File file = createFile(project, "1 " + name + "=\"\"\n");
        PsiElement slist = file.getChildren()[2];
        PsiElement var = slist.getFirstChild().getFirstChild().getFirstChild();
        return var instanceof Xbas99Svar ? (Xbas99Svar) var : null;
    }

    public static Xbas99File createFile(Project project, String text) {
        String name = "dummy.b99";
        return (Xbas99File) PsiFileFactory.getInstance(project).
                createFileFromText(name, Xbas99FileType.INSTANCE, text);
    }

}
