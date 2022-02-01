package net.endlos.xdt99.xga99r.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiFileFactory;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import net.endlos.xdt99.xga99r.Xga99RFileType;

public class Xga99RElementFactory {

    public static Xga99RLabeldef createLabel(Project project, String name) {
        final Xga99RFile file = createFile(project, name + "\n");
        return (Xga99RLabeldef) file.getFirstChild();
    }

    public static Xga99RFile createFile(Project project, String text) {
        String name = "dummy.gpl";
        return (Xga99RFile) PsiFileFactory.getInstance(project).
                createFileFromText(name, Xga99RFileType.INSTANCE, text);
    }

}
