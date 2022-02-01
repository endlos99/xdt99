package net.endlos.xdt99.xbas99l;

import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.options.colors.AttributesDescriptor;
import com.intellij.openapi.options.colors.ColorDescriptor;
import com.intellij.openapi.options.colors.ColorSettingsPage;
import net.endlos.xdt99.xbas99.Xbas99SyntaxHighlighter;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.util.Map;

public class Xbas99LColorSettingsPage implements ColorSettingsPage {
    private static final AttributesDescriptor[] DESCRIPTORS = new AttributesDescriptor[]{
            new AttributesDescriptor("Statement", Xbas99LSyntaxHighlighter.STATEMENT),
            new AttributesDescriptor("Function", Xbas99LSyntaxHighlighter.FUNCTION),
            new AttributesDescriptor("Numeric Variable", Xbas99LSyntaxHighlighter.NVAR),
            new AttributesDescriptor("String Variable", Xbas99LSyntaxHighlighter.SVAR),
            new AttributesDescriptor("Value", Xbas99LSyntaxHighlighter.VALUE),
            new AttributesDescriptor("String", Xbas99LSyntaxHighlighter.QSTRING),
            new AttributesDescriptor("Operator", Xbas99LSyntaxHighlighter.OPERATOR),
            new AttributesDescriptor("Label", Xbas99LSyntaxHighlighter.LABEL),
            new AttributesDescriptor("Statement Separator", Xbas99LSyntaxHighlighter.SEPARATOR),
            new AttributesDescriptor("Comment", Xbas99LSyntaxHighlighter.COMMENT),
    };

    @Override
    @Nullable
    public Icon getIcon() {
        return Xbas99LIcons.FILE;
    }

    @Override
    @NotNull
    public SyntaxHighlighter getHighlighter() {
        return new Xbas99LSyntaxHighlighter();
    }

    @Override
    @NotNull
    public String getDemoText() {
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

    @Override
    @Nullable
    public Map<String, TextAttributesKey> getAdditionalHighlightingTagToDescriptorMap() {
        return null;
    }

    @Override
    public AttributesDescriptor @NotNull [] getAttributeDescriptors() {
        return DESCRIPTORS;
    }

    @Override
    public ColorDescriptor @NotNull [] getColorDescriptors() {
        return ColorDescriptor.EMPTY_ARRAY;
    }

    @Override
    @NotNull
    public String getDisplayName() {
        return "xdt99 BASIC (labels)";
    }
}
