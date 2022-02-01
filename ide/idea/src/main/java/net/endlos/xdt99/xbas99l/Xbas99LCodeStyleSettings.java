package net.endlos.xdt99.xbas99l;

import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import net.endlos.xdt99.common.Xdt99CharCase;

public class Xbas99LCodeStyleSettings extends CustomCodeStyleSettings {
    public static Xdt99CharCase XBAS99_CHAR_CASE = Xdt99CharCase.ASIS;
    public static boolean XBAS99_CASE_COMMENTS = false;
    public static int XBAS99_INDENT = 1;
    public static boolean XBAS99_EXTENDEDBASIC = true;

    public Xbas99LCodeStyleSettings(CodeStyleSettings settings) {
        super("Xbas99LCodeStyleSettings", settings);
    }

}