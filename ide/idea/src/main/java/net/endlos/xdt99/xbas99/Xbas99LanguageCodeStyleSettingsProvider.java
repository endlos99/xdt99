package net.endlos.xdt99.xbas99;

import com.intellij.lang.Language;
import com.intellij.psi.codeStyle.CodeStyleSettingsCustomizable;
import com.intellij.psi.codeStyle.LanguageCodeStyleSettingsProvider;
import org.jetbrains.annotations.NotNull;

public class Xbas99LanguageCodeStyleSettingsProvider extends LanguageCodeStyleSettingsProvider {

    @NotNull
    @Override
    public Language getLanguage() {
        return Xbas99Language.INSTANCE;
    }

    @Override
    public void customizeSettings(@NotNull CodeStyleSettingsCustomizable consumer, @NotNull SettingsType settingsType) {
    }

    @Override
    public String getCodeSample(@NotNull SettingsType settingsType) {
        return "10 REM SAMPLE xdt99 EXTENDED BASIC PROGRAM\n" +
                "20 CALL CLEAR :: CALL MYSUB(9)\n" +
                "30 FOR I=1 TO 9 :: CALL SPRITE(#I,48+I,3+I*0.8,RND*100,RND*200):: NEXT I\n" +
                "40 LINPUT \"WHAT IS YOUR NAME?\":NAME$\n" +
                "50 PRINT \"HELLO \";NAME$\n" +
                "60 GO SUB 100 ! PLAY SOUND EFFECT\n" +
                "70 IF NAME$<>\"BYE\" THEN 40\n" +
                "80 END\n" +
                "100 REM SUBROUTINES\n" +
                "110 LET LEN=LEN$(NAME$)+1\n" +
                "120 IF LEN>5 THEN LEN=5\n" +
                "130 FOR J=1 TO LEN :: CALL SOUND(200,110*J,J):: NEXT J\n" +
                "140 RETURN\n" +
                "200 SUB MYSUB(X) :: CALL SCREEN(X) :: SUBEND\n";
    }

}
