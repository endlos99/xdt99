package net.endlos.xdt99.xas99r.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiFileFactory;
import net.endlos.xdt99.xas99r.Xas99RFileType;

public class Xas99RElementFactory {

    // can be used for macro as well, since we just want the IDENT node
    public static Xas99RLabeldef createLabel(Project project, String name) {
        final Xas99RFile file = createFile(project, name + "\n");
        return (Xas99RLabeldef) file.getFirstChild();
    }

    public static Xas99RFile createFile(Project project, String text) {
        String name = "dummy.a99";
        return (Xas99RFile) PsiFileFactory.getInstance(project).
                createFileFromText(name, Xas99RFileType.INSTANCE, text);
    }

}
