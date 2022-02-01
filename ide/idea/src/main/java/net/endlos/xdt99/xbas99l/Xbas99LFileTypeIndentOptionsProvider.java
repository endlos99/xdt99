//package net.endlos.xdt99.xbas99l;
//
//import com.intellij.application.options.CodeStyle;
//import com.intellij.application.options.IndentOptionsEditor;
//import com.intellij.openapi.fileTypes.FileType;
//import com.intellij.psi.PsiFile;
//import com.intellij.psi.codeStyle.CommonCodeStyleSettings;
//import com.intellij.psi.codeStyle.FileTypeIndentOptionsProvider;
//import net.endlos.xdt99.xbas99.Xbas99FileType;
//import org.jetbrains.annotations.NonNls;
//import org.jetbrains.annotations.NotNull;
//
//public class Xbas99LFileTypeIndentOptionsProvider implements FileTypeIndentOptionsProvider {
//
//    @Override
//    public CommonCodeStyleSettings.IndentOptions createIndentOptions() {
//        CommonCodeStyleSettings.IndentOptions options = new CommonCodeStyleSettings.IndentOptions();
//        options.INDENT_SIZE = Xbas99LCodeStyleSettings.XBAS99_INDENT;
//        options.CONTINUATION_INDENT_SIZE = 0;
//        return options;
//    }
//
//    @Override
//    public FileType getFileType() {
//        return Xbas99FileType.INSTANCE;
//    }
//
//    public IndentOptionsEditor createOptionsEditor() {
//        return new IndentOptionsEditor(null);
//    }
//
//    @NonNls
//    public String getPreviewText() {
//        return " REM SAMPLE xdt99 EXTENDED BASIC PROGRAM\n" +
//                " CALL CLEAR :: CALL MYSUB(9)\n" +
//                " FOR I=1 TO 9 :: CALL SPRITE(#I,48+I,3+I*0.8,RND*100,RND*200):: NEXT I\n" +
//                "ASKNAME:\n" +
//                " INPUT \"WHAT IS YOUR NAME?\":NAME$\n" +
//                " PRINT \"HELLO \";NAME$\n" +
//                " GO SUB SOUND ! PLAY SOUND EFFECT\n" +
//                " IF NAME$<>\"BYE\" THEN ASKNAME\n" +
//                " END\n" +
//                "SOUND:\n" +
//                " REM SUBROUTINES\n" +
//                " LET LEN=LEN$(NAME$)+1\n" +
//                " IF LEN>5 THEN LEN=5\n" +
//                " FOR J=1 TO LEN :: CALL SOUND(200,110*J,J):: NEXT J\n" +
//                " RETURN\n" +
//                " SUB MYSUB(X) :: CALL SCREEN(X) :: SUBEND\n";
//    }
//
//    public void prepareForReformat(final PsiFile psiFile) {
//    }
//
//}
