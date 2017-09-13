package net.endlos.xdt99.xga99.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import net.endlos.xdt99.xga99.Xga99FileType;
import net.endlos.xdt99.xga99.Xga99Language;
import net.endlos.xdt99.xga99.Xga99FileType;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class Xga99File extends PsiFileBase {
    public Xga99File(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, Xga99Language.INSTANCE);
    }

    @NotNull
    @Override
    public FileType getFileType() {
        return Xga99FileType.INSTANCE;
    }

    @Override
    public String toString() {
        return "GPL assembly file";
    }

    @Override
    public Icon getIcon(int flags) {
        return super.getIcon(flags);
    }
}
