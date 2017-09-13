package net.endlos.xdt99.xga99;

import com.intellij.openapi.project.Project;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsManager;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;

public class Xga99CodeStyleSettings extends CustomCodeStyleSettings {
    public static final int XGA99_INDENT = 7;
    public int XGA99_MNEMONIC_TAB_STOP = XGA99_INDENT + 1;
    public int XGA99_OPERANDS_TAB_STOP = 14;
    public int XGA99_COMMENT_TAB_STOP = 40;
    public int XGA99_CHAR_CASE = 0;  // 0=lower, 1=upper, 2=as-is
    public boolean XGA99_INCR_INDENT = false;
    public boolean XGA99_RELAXED = true;
    public boolean XGA99_COLONLABELS = true;

    public Xga99CodeStyleSettings(CodeStyleSettings container) {
        super(Xga99Language.INSTANCE.getID(), container);
    }

    public static Xga99CodeStyleSettings getInstance(final Project project) {
        return CodeStyleSettingsManager.getSettings(project).getCustomSettings(Xga99CodeStyleSettings.class);
    }
}
