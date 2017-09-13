package net.endlos.xdt99.xga99;

import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.options.colors.AttributesDescriptor;
import com.intellij.openapi.options.colors.ColorDescriptor;
import com.intellij.openapi.options.colors.ColorSettingsPage;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.util.Map;

public class Xga99ColorSettingsPage implements ColorSettingsPage {
    private static final AttributesDescriptor[] DESCRIPTORS = new AttributesDescriptor[]{
            new AttributesDescriptor("Instruction", Xga99SyntaxHighlighter.INSTRUCTION),
            new AttributesDescriptor("FMT Instruction", Xga99SyntaxHighlighter.FINSTRUCTION),
            new AttributesDescriptor("Directive", Xga99SyntaxHighlighter.DIRECTIVE),
            new AttributesDescriptor("Preprocessor command", Xga99SyntaxHighlighter.PREPROCESSOR),
            new AttributesDescriptor("Value", Xga99SyntaxHighlighter.VALUE),
            new AttributesDescriptor("Text literal", Xga99SyntaxHighlighter.TEXT),
            new AttributesDescriptor("Operator", Xga99SyntaxHighlighter.OPERATOR),
            new AttributesDescriptor("Argument separator", Xga99SyntaxHighlighter.SEPARATOR),
            new AttributesDescriptor("Comment", Xga99SyntaxHighlighter.COMMENT),
    };

    @Nullable
    @Override
    public Icon getIcon() {
        return Xga99Icons.FILE;
    }

    @NotNull
    @Override
    public SyntaxHighlighter getHighlighter() {
        return new Xga99SyntaxHighlighter();
    }

    @NotNull
    @Override
    public String getDemoText() {
        return "* SAMPLE xdt99 GPL PROGRAM\n\n" +
                "       GROM  >6000\n" +
                "COUNT  EQU   >8302\n\n" +
                "START  ALL   '*'\n" +
                "       BACK  >02\n" +
                "       FMT\n" +
                "       ROW   10\n" +
                "       COL   5\n" +
                "       HTEXT 'HELLO WORLD'\n" +
                "       FEND\n" +
                "       DST   768,@COUNT\n" +
                "LOOP   ST    '+',V@0(COUNT)\n" +
                "       DDEC  @COUNT\n" +
                "       BR    LOOP\n\n" +
                "       .ifdef TEST" +
                "       MOVE  20,G@LOOP-4,V@320" +
                "       .endif\n\n" +
                "       HCF\n  ; not an actual instruction" +
                "SLAST  END";
    }

    @Nullable
    @Override
    public Map<String, TextAttributesKey> getAdditionalHighlightingTagToDescriptorMap() {
        return null;
    }

    @NotNull
    @Override
    public AttributesDescriptor[] getAttributeDescriptors() {
        return DESCRIPTORS;
    }

    @NotNull
    @Override
    public ColorDescriptor[] getColorDescriptors() {
        return ColorDescriptor.EMPTY_ARRAY;
    }

    @NotNull
    @Override
    public String getDisplayName() {
        return "xdt99 GPL";
    }
}
