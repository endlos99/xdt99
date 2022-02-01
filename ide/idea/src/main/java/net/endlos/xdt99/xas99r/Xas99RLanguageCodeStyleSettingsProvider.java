package net.endlos.xdt99.xas99r;

import com.intellij.lang.Language;
import com.intellij.psi.codeStyle.CodeStyleSettingsCustomizable;
import com.intellij.psi.codeStyle.LanguageCodeStyleSettingsProvider;
import org.jetbrains.annotations.NotNull;

public class Xas99RLanguageCodeStyleSettingsProvider extends LanguageCodeStyleSettingsProvider {
    private static final String[] SYNTAX_DESCRS = new String[]{"Strict", "Normal", "Relaxed"};
    private static final int[] SYNTAX_VALUES = new int[]{0, 1, 2};

    @NotNull
    @Override
    public Language getLanguage() {
        return Xas99RLanguage.INSTANCE;
    }

    //TODO
    @Override
    public void customizeSettings(@NotNull CodeStyleSettingsCustomizable consumer, @NotNull SettingsType settingsType) {
        consumer.showCustomOption(Xas99RCodeStyleSettings.class, "XAS99_STRICT", "Strict mode",
                "Syntax Style");
        consumer.showCustomOption(Xas99RCodeStyleSettings.class, "XAS99_RELAXED", "Relaxed mode",
                "Syntax Style");
//        consumer.showCustomOption(Xas99RCodeStyleSettings.class, "XAS99_SYNTAX", "Syntax mode",
//                "foo", SYNTAX_DESCRS, SYNTAX_VALUES);
    }

    @Override
    public String getCodeSample(@NotNull SettingsType settingsType) {
        return "* SAMPLE xdt99 ASSEMBLY PROGRAM\n\n" +
                "       IDT 'ASHELLO'\n" +
                "       DEF SLOAD,SFIRST,SLAST,START\n" +
                "       REF VSBW,VMBW,VWTR\n" +
                "WRKSP  EQU  >8300\n" +
                "MESSG  TEXT 'HELLO WORLD'\n" +
                "MESSGL EQU  $-MESSG\n\n" +
                "START  LIMI 0                       CLEAR SCREEN\n" +
                "       LWPI WRKSP\n" +
                "       PUSH R15\n" +
                "       CLR  R0\n" +
                "       LI   R1,'* '\n" +
                "       LI   R2,24*32\n" +
                "CLS    BLWP @VSBW\n" +
                "       INC  R0\n" +
                "       DEC  R2\n" +
                "       JNE  CLS\n\n" +
                "       LI   R0,2*32+3               WRITE WELCOME MESSAGE\n" +
                "       LI   R1,MESSG\n" +
                "       LI   R2,MESSGL\n" +
                "       BLWP @VMBW\n\n" +
                "SLAST  END";
    }

}
