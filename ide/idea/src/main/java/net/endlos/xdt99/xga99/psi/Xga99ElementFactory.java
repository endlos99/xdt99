package net.endlos.xdt99.xga99.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiFileFactory;
import net.endlos.xdt99.xga99.Xga99FileType;

public class Xga99ElementFactory {

    public static Xga99Labeldef createLabel(Project project, String name) {
        final Xga99File file = createFile(project, name + "\n");
        return (Xga99Labeldef) file.getFirstChild();
    }

    public static Xga99File createFile(Project project, String text) {
        String name = "dummy.gpl";
        return (Xga99File) PsiFileFactory.getInstance(project).
                createFileFromText(name, Xga99FileType.INSTANCE, text);
    }

}
