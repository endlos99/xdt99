package net.endlos.xdt99.xas99.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import net.endlos.xdt99.xas99.Xas99FileType;
import net.endlos.xdt99.xas99.Xas99Language;
import net.endlos.xdt99.xas99.Xas99FileType;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class Xas99File extends PsiFileBase {
    public Xas99File(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, Xas99Language.INSTANCE);
    }

    @NotNull
    @Override
    public FileType getFileType() {
        return Xas99FileType.INSTANCE;
    }

    @Override
    public String toString() {
        return "TMS 9900 assembly file";
    }

    @Override
    public Icon getIcon(int flags) {
        return super.getIcon(flags);
    }
}
