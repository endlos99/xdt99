package net.endlos.xdt99.xas99;

import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.openapi.editor.colors.EditorColorsScheme;
import com.intellij.openapi.editor.highlighter.EditorHighlighter;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.awt.*;

public class Xas99CodeStyleSettingsPanel extends CodeStyleAbstractPanel {
    private JPanel myPanel;
    private JTextField myMnemonicTabStop;
    private JTextField myOperandsTabStop;
    private JTextField myCommentsTabStop;

    public Xas99CodeStyleSettingsPanel(CodeStyleSettings settings) {
        super(settings);
        createUIComponents();
    }

    public void apply(CodeStyleSettings settings) {
        Xas99CodeStyleSettings xasSettings = settings.getCustomSettings(Xas99CodeStyleSettings.class);
        xasSettings.XAS99_MNEMONIC_TAB_STOP = getIntValue(myMnemonicTabStop);
        xasSettings.XAS99_OPERANDS_TAB_STOP = getIntValue(myOperandsTabStop);
        xasSettings.XAS99_COMMENT_TAB_STOP = getIntValue(myCommentsTabStop);
    }

    private int getIntValue(JTextField field) {
        try {
            return Integer.parseInt(field.getText());
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    protected void resetImpl(CodeStyleSettings settings) {
        Xas99CodeStyleSettings xasSettings = settings.getCustomSettings(Xas99CodeStyleSettings.class);
        this.myMnemonicTabStop.setText(String.valueOf(xasSettings.XAS99_MNEMONIC_TAB_STOP));
        this.myOperandsTabStop.setText(String.valueOf(xasSettings.XAS99_OPERANDS_TAB_STOP));
        this.myCommentsTabStop.setText(String.valueOf(xasSettings.XAS99_COMMENT_TAB_STOP));
    }

    public boolean isModified(CodeStyleSettings settings) {
        Xas99CodeStyleSettings xasSettings = settings.getCustomSettings(Xas99CodeStyleSettings.class);
        return xasSettings.XAS99_MNEMONIC_TAB_STOP != getIntValue(myMnemonicTabStop) ||
                xasSettings.XAS99_OPERANDS_TAB_STOP != getIntValue(myOperandsTabStop) ||
                xasSettings.XAS99_COMMENT_TAB_STOP != getIntValue(myCommentsTabStop);
    }

    @Override
    protected int getRightMargin() {
        return 0;
    }

    @Nullable
    @Override
    protected EditorHighlighter createHighlighter(EditorColorsScheme scheme) {
        return null;
    }

    @Nullable
    @Override
    public JComponent getPanel() {
        return myPanel;
    }

    @Nullable
    @Override
    protected String getPreviewText() {
        return null;
    }

    @NotNull
    protected FileType getFileType() {
        return Xas99FileType.INSTANCE;
    }

    private void createUIComponents() {
        myPanel = new JPanel(new FlowLayout(FlowLayout.LEADING));
        myMnemonicTabStop = new JTextField();
        myOperandsTabStop = new JTextField();
        myCommentsTabStop = new JTextField();

        JPanel inner = new JPanel(new GridLayout(0, 2, 10, 10));
        inner.add(new JLabel("Mnemonic column"));
        inner.add(myMnemonicTabStop);
        inner.add(new JLabel("Operands column"));
        inner.add(myOperandsTabStop);
        inner.add(new JLabel("Comments column"));
        inner.add(myCommentsTabStop);
        myPanel.add(inner);
    }
}
