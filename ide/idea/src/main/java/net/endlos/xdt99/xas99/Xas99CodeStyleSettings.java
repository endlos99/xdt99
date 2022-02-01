package net.endlos.xdt99.xas99;

import com.intellij.application.options.CodeStyle;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import com.intellij.openapi.project.Project;
import net.endlos.xdt99.common.Xdt99CharCase;
import org.jetbrains.annotations.NotNull;

public class Xas99CodeStyleSettings extends CustomCodeStyleSettings {
    public static final int XAS99_INDENT = 7;
    public static Xdt99CharCase XAS99_CHAR_CASE = Xdt99CharCase.ASIS;
    public static boolean XAS99_CASE_COMMENTS = false;
    public static boolean XAS99_STRICT = false;
    public static int XAS99_MNEMONIC_TAB_STOP = XAS99_INDENT + 1;
    public static int XAS99_OPERANDS_TAB_STOP = 13;
    public static int XAS99_COMMENT_TAB_STOP = 40;
    public static boolean XAS99_INCR_IDENT = false;
    public static boolean XAS99_COLONLABELS = true;

    public Xas99CodeStyleSettings(CodeStyleSettings settings) {
        super("Xas99CodeStyleSettings", settings);
    }

    public static Xas99CodeStyleSettings getInstance(@NotNull final Project project) {
        return CodeStyle.getSettings(project).getCustomSettings(Xas99CodeStyleSettings.class);
    }

}
