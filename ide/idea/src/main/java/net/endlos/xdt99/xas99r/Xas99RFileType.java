package net.endlos.xdt99.xas99r;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class Xas99RFileType extends LanguageFileType {
    public static final Xas99RFileType INSTANCE = new Xas99RFileType();

    private Xas99RFileType() {
        super(Xas99RLanguage.INSTANCE);
    }

    @Override
    @NotNull
    public String getName() {
        return "Xas99R";
    }

    @Override
    @NotNull
    public String getDescription() {
        return "TMS 9900 assembly file (relaxed)";
    }

    @Override
    @NotNull
    public String getDefaultExtension() {
        return "a99";
    }

    @Override
    @Nullable
    public Icon getIcon() {
        return Xas99RIcons.FILE;
    }

}
