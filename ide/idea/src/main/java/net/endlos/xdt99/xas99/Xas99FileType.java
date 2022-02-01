package net.endlos.xdt99.xas99;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xas99FileType extends LanguageFileType {
    public static final Xas99FileType INSTANCE = new Xas99FileType();

    private Xas99FileType() {
        super(Xas99Language.INSTANCE);
    }

    @Override
    @NotNull
    public String getName() {
        return "Xas99";
    }

    @Override
    @NotNull
    public String getDescription() {
        return "TMS 9900 assembly file";
    }

    @Override
    @NotNull
    public String getDefaultExtension() {
        return "a99";
    }

    @Override
    @Nullable
    public Icon getIcon() {
        return Xas99Icons.FILE;
    }

}
