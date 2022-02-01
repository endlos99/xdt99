package net.endlos.xdt99.xbas99l.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import net.endlos.xdt99.xbas99l.Xbas99LFileType;
import net.endlos.xdt99.xbas99l.Xbas99LLanguage;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class Xbas99LFile extends PsiFileBase {
    public Xbas99LFile(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, Xbas99LLanguage.INSTANCE);
    }

    @NotNull
    @Override
    public FileType getFileType() {
        return Xbas99LFileType.INSTANCE;
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
