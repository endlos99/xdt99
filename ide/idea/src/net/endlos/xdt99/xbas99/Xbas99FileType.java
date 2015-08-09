package net.endlos.xdt99.xbas99;

import com.intellij.openapi.fileTypes.LanguageFileType;
import net.endlos.xdt99.xbas99.Xbas99Icons;
import net.endlos.xdt99.xbas99.Xbas99Language;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xbas99FileType extends LanguageFileType {
    public static final Xbas99FileType INSTANCE = new Xbas99FileType();

    private Xbas99FileType() {
        super(Xbas99Language.INSTANCE);
    }

    @NotNull
    @Override
    public String getName() {
        return "xbas99";
    }

    @NotNull
    @Override
    public String getDescription() {
        return "TI BASIC or TI Extended BASIC";
    }

    @NotNull
    @Override
    public String getDefaultExtension() {
        return "b99";
    }

    @Nullable
    @Override
    public Icon getIcon() {
        return Xbas99Icons.FILE;
    }
}
