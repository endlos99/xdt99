package net.endlos.xdt99.xbas99l;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xbas99LFileType extends LanguageFileType {
    public static final Xbas99LFileType INSTANCE = new Xbas99LFileType();

    private Xbas99LFileType() {
        super(Xbas99LLanguage.INSTANCE);
    }

    @Override
    @NotNull
    public String getName() {
        return "Xbas99L";
    }

    @Override
    @NotNull
    public String getDescription() {
        return "TI BASIC or TI Extended BASIC (labels)";
    }

    @Override
    @NotNull
    public String getDefaultExtension() {
        return "b99";
    }

    @Override
    @Nullable
    public Icon getIcon() {
        return Xbas99LIcons.FILE;
    }

}
