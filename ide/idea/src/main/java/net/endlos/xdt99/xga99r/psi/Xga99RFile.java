package net.endlos.xdt99.xga99r.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import net.endlos.xdt99.xga99r.Xga99RFileType;
import net.endlos.xdt99.xga99r.Xga99RLanguage;
import org.jetbrains.annotations.NotNull;

public class Xga99RFile extends PsiFileBase {

    public Xga99RFile(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, Xga99RLanguage.INSTANCE);
    }

    @Override
    @NotNull
    public FileType getFileType() {
        return Xga99RFileType.INSTANCE;
    }

    @Override
    public String toString() {
        return "GPL assembly file";
    }

}
