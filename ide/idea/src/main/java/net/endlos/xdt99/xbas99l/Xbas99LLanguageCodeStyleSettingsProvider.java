package net.endlos.xdt99.xbas99l;

import com.intellij.lang.Language;
import com.intellij.psi.codeStyle.CodeStyleSettingsCustomizable;
import com.intellij.psi.codeStyle.LanguageCodeStyleSettingsProvider;
import org.jetbrains.annotations.NotNull;

public class Xbas99LLanguageCodeStyleSettingsProvider extends LanguageCodeStyleSettingsProvider {

    @NotNull
    @Override
    public Language getLanguage() {
        return Xbas99LLanguage.INSTANCE;
    }

    @Override
    public void customizeSettings(@NotNull CodeStyleSettingsCustomizable consumer, @NotNull SettingsType settingsType) {
    }

    @Override
    public String getCodeSample(@NotNull SettingsType settingsType) {
        return " REM SAMPLE xdt99 EXTENDED BASIC PROGRAM\n" +
               " CALL CLEAR :: CALL MYSUB(9)\n" +
               " FOR I=1 TO 9 :: CALL SPRITE(#I,48+I,3+I*0.8,RND*100,RND*200):: NEXT I\n" +
               "ASKNAME:\n" +
               " INPUT \"WHAT IS YOUR NAME?\":NAME$\n" +
               " PRINT \"HELLO \";NAME$\n" +
               " GO SUB SOUND ! PLAY SOUND EFFECT\n" +
               " IF NAME$<>\"BYE\" THEN ASKNAME\n" +
               " END\n" +
               "SOUND:\n" +
               " REM SUBROUTINES\n" +
               " LET LEN=LEN$(NAME$)+1\n" +
               " IF LEN>5 THEN LEN=5\n" +
               " FOR J=1 TO LEN :: CALL SOUND(200,110*J,J):: NEXT J\n" +
               " RETURN\n" +
               " SUB MYSUB(X) :: CALL SCREEN(X) :: SUBEND\n";
    }

}
