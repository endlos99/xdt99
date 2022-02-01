package net.endlos.xdt99.xga99;

import com.intellij.openapi.project.Project;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsManager;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import net.endlos.xdt99.common.Xdt99CharCase;

public class Xga99CodeStyleSettings extends CustomCodeStyleSettings {
    public static final int XGA99_INDENT = 7;
    public static Xdt99CharCase XGA99_CHAR_CASE = Xdt99CharCase.ASIS;
    public static boolean XGA99_CASE_COMMENTS = false;
    public static int XGA99_MNEMONIC_TAB_STOP = XGA99_INDENT + 1;
    public static int XGA99_OPERANDS_TAB_STOP = 14;
    public static int XGA99_COMMENT_TAB_STOP = 40;
    public static boolean XGA99_INCR_INDENT = false;
    public static boolean XGA99_STRICT = true;

    public Xga99CodeStyleSettings(CodeStyleSettings container) {
        super(Xga99Language.INSTANCE.getID(), container);
    }

    public static Xga99CodeStyleSettings getInstance(final Project project) {
        return CodeStyleSettingsManager.getSettings(project).getCustomSettings(Xga99CodeStyleSettings.class);
    }

}
