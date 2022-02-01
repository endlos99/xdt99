package net.endlos.xdt99.xga99r;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xga99RFileType extends LanguageFileType {
    public static final Xga99RFileType INSTANCE = new Xga99RFileType();

    private Xga99RFileType() {
        super(Xga99RLanguage.INSTANCE);
    }

    @NotNull
    @Override
    public String getName() {
        return "Xga99R";
    }

    @NotNull
    @Override
    public String getDescription() {
        return "GPL assembly (relaxed)";
    }

    @NotNull
    @Override
    public String getDefaultExtension() {
        return "gpl";
    }

    @Nullable
    @Override
    public Icon getIcon() {
        return Xga99RIcons.FILE;
    }

}