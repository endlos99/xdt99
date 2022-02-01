package net.endlos.xdt99.xbas99.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import net.endlos.xdt99.xbas99.Xbas99Language;
import net.endlos.xdt99.xbas99.Xbas99FileType;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class Xbas99File extends PsiFileBase {
    public Xbas99File(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, Xbas99Language.INSTANCE);
    }

    @NotNull
    @Override
    public FileType getFileType() {
        return Xbas99FileType.INSTANCE;
    }

    @Override
    public String toString() {
        return "TI Extended BASIC file";
    }

    @Override
    public Icon getIcon(int flags) {
        return super.getIcon(flags);
    }
}
