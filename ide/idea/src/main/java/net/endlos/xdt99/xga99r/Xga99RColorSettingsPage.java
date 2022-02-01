package net.endlos.xdt99.xga99r;

import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.options.colors.AttributesDescriptor;
import com.intellij.openapi.options.colors.ColorDescriptor;
import com.intellij.openapi.options.colors.ColorSettingsPage;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.util.Map;

public class Xga99RColorSettingsPage implements ColorSettingsPage {
    private static final AttributesDescriptor[] DESCRIPTORS = new AttributesDescriptor[]{
            new AttributesDescriptor("Instruction", Xga99RSyntaxHighlighter.INSTRUCTION),
            new AttributesDescriptor("FMT Instruction", Xga99RSyntaxHighlighter.FINSTRUCTION),
            new AttributesDescriptor("Directive", Xga99RSyntaxHighlighter.DIRECTIVE),
            new AttributesDescriptor("Preprocessor command", Xga99RSyntaxHighlighter.PREPROCESSOR),
            new AttributesDescriptor("Value", Xga99RSyntaxHighlighter.VALUE),
            new AttributesDescriptor("Text literal", Xga99RSyntaxHighlighter.TEXT),
            new AttributesDescriptor("Operator", Xga99RSyntaxHighlighter.OPERATOR),
            new AttributesDescriptor("Argument separator", Xga99RSyntaxHighlighter.SEPARATOR),
            new AttributesDescriptor("Comment", Xga99RSyntaxHighlighter.COMMENT),
    };

    @Nullable
    @Override
    public Icon getIcon() {
        return Xga99RIcons.FILE;
    }

    @NotNull
    @Override
    public SyntaxHighlighter getHighlighter() {
        return new Xga99RSyntaxHighlighter();
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

    @Override
    public AttributesDescriptor @NotNull [] getAttributeDescriptors() {
        return DESCRIPTORS;
    }

    @Override
    public ColorDescriptor @NotNull [] getColorDescriptors() {
        return ColorDescriptor.EMPTY_ARRAY;
    }

    @NotNull
    @Override
    public String getDisplayName() {
        return "xdt99 GPL";
    }

}
