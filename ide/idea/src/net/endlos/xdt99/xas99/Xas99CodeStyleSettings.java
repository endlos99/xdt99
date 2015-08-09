package net.endlos.xdt99.xas99;

import com.intellij.openapi.project.Project;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsManager;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;

public class Xas99CodeStyleSettings extends CustomCodeStyleSettings {
    public int XAS99_MNEMONIC_TAB_STOP = 8;
    public int XAS99_OPERANDS_TAB_STOP = 13;
    public int XAS99_COMMENT_TAB_STOP = 30;

    public Xas99CodeStyleSettings(CodeStyleSettings container) {
        super(Xas99Language.INSTANCE.getID(), container);
    }

    public static Xas99CodeStyleSettings getInstance(final Project project) {
        return CodeStyleSettingsManager.getSettings(project).getCustomSettings(Xas99CodeStyleSettings.class);
    }
}
