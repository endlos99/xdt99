package net.endlos.xdt99.xas99.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiFileFactory;
import net.endlos.xdt99.xas99.Xas99FileType;

public class Xas99ElementFactory {
    public static Xas99Label createLabel(Project project, String name) {
        final Xas99File file = createFile(project, name);
        return (Xas99Label) file.getFirstChild();
    }

    public static Xas99File createFile(Project project, String text) {
        String name = "dummy.a99";
        return (Xas99File) PsiFileFactory.getInstance(project).
                createFileFromText(name, Xas99FileType.INSTANCE, text);
    }
}
