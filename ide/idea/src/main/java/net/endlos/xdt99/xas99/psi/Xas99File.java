package net.endlos.xdt99.xas99.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import net.endlos.xdt99.xas99.Xas99FileType;
import net.endlos.xdt99.xas99.Xas99Language;
import org.jetbrains.annotations.NotNull;

public class Xas99File extends PsiFileBase {

    public Xas99File(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, Xas99Language.INSTANCE);
    }

    @Override
    @NotNull
    public FileType getFileType() {
        return Xas99FileType.INSTANCE;
    }

    @Override
    public String toString() {
        return "TMS 9900 assembly file";
    }

}
