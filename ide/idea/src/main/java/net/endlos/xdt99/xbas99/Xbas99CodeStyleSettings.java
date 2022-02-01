package net.endlos.xdt99.xbas99;

import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import net.endlos.xdt99.common.Xdt99CharCase;

public class Xbas99CodeStyleSettings extends CustomCodeStyleSettings {
    public static Xdt99CharCase XBAS99_CHAR_CASE = Xdt99CharCase.ASIS;  // 0=lower, 1=upper, 2=as-is
    public static boolean XBAS99_CASE_COMMENTS = false;
    public static boolean XBAS99_EXTENDEDBASIC = true;

    public Xbas99CodeStyleSettings(CodeStyleSettings settings) {
        super("Xbas99CodeStyleSettings", settings);
    }

}