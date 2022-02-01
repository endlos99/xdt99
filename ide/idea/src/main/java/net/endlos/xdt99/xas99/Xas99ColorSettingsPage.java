package net.endlos.xdt99.xas99;

import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.options.colors.AttributesDescriptor;
import com.intellij.openapi.options.colors.ColorDescriptor;
import com.intellij.openapi.options.colors.ColorSettingsPage;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.util.Map;

public class Xas99ColorSettingsPage implements ColorSettingsPage {
    private static final AttributesDescriptor[] DESCRIPTORS = new AttributesDescriptor[]{
            new AttributesDescriptor("Instruction", Xas99SyntaxHighlighter.INSTRUCTION),
            new AttributesDescriptor("Directive", Xas99SyntaxHighlighter.DIRECTIVE),
            //new AttributesDescriptor("Instruction extension", Xas99SyntaxHighlighter.XINSTRUCTION),
            new AttributesDescriptor("Preprocessor command", Xas99SyntaxHighlighter.PREPROCESSOR),
            new AttributesDescriptor("Label", Xas99SyntaxHighlighter.IDENT),
            new AttributesDescriptor("Value", Xas99SyntaxHighlighter.VALUE),
            new AttributesDescriptor("Text literal", Xas99SyntaxHighlighter.TEXT),
            new AttributesDescriptor("Register", Xas99SyntaxHighlighter.REGISTER),
            new AttributesDescriptor("Operator", Xas99SyntaxHighlighter.OPERATOR),
            new AttributesDescriptor("Argument separator", Xas99SyntaxHighlighter.SEPARATOR),
            new AttributesDescriptor("Comment", Xas99SyntaxHighlighter.COMMENT),
    };

    @Override
    @Nullable
    public Icon getIcon() {
        return Xas99Icons.FILE;
    }

    @Override
    @NotNull
    public SyntaxHighlighter getHighlighter() {
        return new Xas99SyntaxHighlighter();
    }

    @Override
    @NotNull
    public String getDemoText() {
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
        return "xdt99 Assembly";
    }

}
