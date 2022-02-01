package net.endlos.xdt99.xas99r.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import net.endlos.xdt99.xas99r.Xas99RFileType;
import net.endlos.xdt99.xas99r.Xas99RLanguage;
import org.jetbrains.annotations.NotNull;

public class Xas99RFile extends PsiFileBase {

    public Xas99RFile(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, Xas99RLanguage.INSTANCE);
    }

    @Override
    @NotNull
    public FileType getFileType() {
        return Xas99RFileType.INSTANCE;
    }

    @Override
    public String toString() {
        return "TMS 9900 assembly file";
    }

}
