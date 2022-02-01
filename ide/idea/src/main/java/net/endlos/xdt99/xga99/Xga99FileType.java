package net.endlos.xdt99.xga99;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xga99FileType extends LanguageFileType {
    public static final Xga99FileType INSTANCE = new Xga99FileType();

    private Xga99FileType() {
        super(Xga99Language.INSTANCE);
    }

    @NotNull
    @Override
    public String getName() {
        return "Xga99";
    }

    @NotNull
    @Override
    public String getDescription() {
        return "GPL assembly";
    }

    @NotNull
    @Override
    public String getDefaultExtension() {
        return "gpl";
    }

    @Nullable
    @Override
    public Icon getIcon() {
        return Xga99Icons.FILE;
    }

}