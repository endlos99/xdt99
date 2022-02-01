package net.endlos.xdt99.xbas99;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xbas99FileType extends LanguageFileType {
    public static final Xbas99FileType INSTANCE = new Xbas99FileType();

    private Xbas99FileType() {
        super(Xbas99Language.INSTANCE);
    }

    @Override
    @NotNull
    public String getName() {
        return "Xbas99";
    }

    @Override
    @NotNull
    public String getDescription() {
        return "TI BASIC or TI Extended BASIC";
    }

    @Override
    @NotNull
    public String getDefaultExtension() {
        return "b99";
    }

    @Override
    @Nullable
    public Icon getIcon() {
        return Xbas99Icons.FILE;
    }

}
