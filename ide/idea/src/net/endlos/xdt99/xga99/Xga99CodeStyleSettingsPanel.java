package net.endlos.xdt99.xga99;

import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.openapi.editor.colors.EditorColorsScheme;
import com.intellij.openapi.editor.highlighter.EditorHighlighter;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.awt.*;
import java.util.Arrays;
import java.util.Enumeration;

public class Xga99CodeStyleSettingsPanel extends CodeStyleAbstractPanel {
    private static final String[] caseOptions = new String[]{"Lower", "Upper", "As-is"};
    private JPanel myPanel;
    private JTextField myMnemonicTabStop;
    private JTextField myOperandsTabStop;
    private JTextField myCommentsTabStop;
    private ButtonGroup myCharCase;
    private JCheckBox myIncrIndent;
    private JCheckBox myRelaxedSpacing;
    private JCheckBox myColonLabels;

    public Xga99CodeStyleSettingsPanel(CodeStyleSettings settings) {
        super(settings);
        createUIComponents();
    }

    public void apply(CodeStyleSettings settings) {
        Xga99CodeStyleSettings xgaSettings = settings.getCustomSettings(Xga99CodeStyleSettings.class);
        xgaSettings.XGA99_MNEMONIC_TAB_STOP = getIntValue(myMnemonicTabStop);
        xgaSettings.XGA99_OPERANDS_TAB_STOP = getIntValue(myOperandsTabStop);
        xgaSettings.XGA99_COMMENT_TAB_STOP = getIntValue(myCommentsTabStop);
        xgaSettings.XGA99_CHAR_CASE = getRadioValue(myCharCase, caseOptions);
        xgaSettings.XGA99_INCR_INDENT = myIncrIndent.isSelected();
        xgaSettings.XGA99_RELAXED = myRelaxedSpacing.isSelected();
        xgaSettings.XGA99_COLONLABELS = myColonLabels.isSelected();
    }

    private int getIntValue(JTextField field) {
        try {
            return Integer.parseInt(field.getText());
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    private int getRadioValue(ButtonGroup group, String[] values) {
        for (Enumeration<AbstractButton> radios = group.getElements(); radios.hasMoreElements();) {
            AbstractButton radio = radios.nextElement();
            if (radio.isSelected()) {
                return Arrays.asList(values).indexOf(radio.getText());
            }
        }
        return -1;
    }

    protected void resetImpl(CodeStyleSettings settings) {
        Xga99CodeStyleSettings xgaSettings = settings.getCustomSettings(Xga99CodeStyleSettings.class);
        this.myMnemonicTabStop.setText(String.valueOf(xgaSettings.XGA99_MNEMONIC_TAB_STOP));
        this.myOperandsTabStop.setText(String.valueOf(xgaSettings.XGA99_OPERANDS_TAB_STOP));
        this.myCommentsTabStop.setText(String.valueOf(xgaSettings.XGA99_COMMENT_TAB_STOP));
        for (Enumeration<AbstractButton> radios = myCharCase.getElements(); radios.hasMoreElements();) {
            AbstractButton radio = radios.nextElement();
            if (radio.getText().equals(caseOptions[xgaSettings.XGA99_CHAR_CASE])) {
                radio.setSelected(true);
                break;
            }
        }
        this.myIncrIndent.setSelected(xgaSettings.XGA99_INCR_INDENT);
        this.myRelaxedSpacing.setSelected(xgaSettings.XGA99_RELAXED);
        this.myColonLabels.setSelected(xgaSettings.XGA99_COLONLABELS);
    }

    public boolean isModified(CodeStyleSettings settings) {
        Xga99CodeStyleSettings xgaSettings = settings.getCustomSettings(Xga99CodeStyleSettings.class);
        return xgaSettings.XGA99_MNEMONIC_TAB_STOP != getIntValue(myMnemonicTabStop) ||
                xgaSettings.XGA99_OPERANDS_TAB_STOP != getIntValue(myOperandsTabStop) ||
                xgaSettings.XGA99_COMMENT_TAB_STOP != getIntValue(myCommentsTabStop) ||
                xgaSettings.XGA99_CHAR_CASE != getRadioValue(myCharCase, caseOptions) ||
                xgaSettings.XGA99_INCR_INDENT != myIncrIndent.isSelected() ||
                xgaSettings.XGA99_RELAXED != myRelaxedSpacing.isSelected() ||
                xgaSettings.XGA99_COLONLABELS != myColonLabels.isSelected();
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
        return Xga99FileType.INSTANCE;
    }

    private void createUIComponents() {
        // tab stops
        myMnemonicTabStop = new JTextField();
        myOperandsTabStop = new JTextField();
        myCommentsTabStop = new JTextField();

        // character case radio buttons
        JPanel myCharCasePanel = new JPanel();
        myCharCase = new ButtonGroup();
        for (String caseOption : caseOptions) {
            JRadioButton b = new JRadioButton(caseOption);
            myCharCasePanel.add(b);
            myCharCase.add(b);
        }

        // options check boxes
        myIncrIndent = new JCheckBox();
        myRelaxedSpacing = new JCheckBox();
        myColonLabels = new JCheckBox();

        // dialog
        JPanel inner = new JPanel(new GridLayout(0, 2, 10, 0));
        inner.add(new JLabel("Mnemonic column"));
        inner.add(myMnemonicTabStop);
        inner.add(new JLabel("Operands column"));
        inner.add(myOperandsTabStop);
        inner.add(new JLabel("Comments column"));
        inner.add(myCommentsTabStop);
        inner.add(new JLabel("Character case"));
        inner.add(myCharCasePanel);
        inner.add(new JLabel("Relaxed spacing"));
        inner.add(myRelaxedSpacing);
        inner.add(new JLabel("Increase indent after RETURN"));
        inner.add(myIncrIndent);
//        inner.add(new JLabel("Labels with colons"));  // TODO
//        inner.add(myColonLabels);
        myPanel = new JPanel(new FlowLayout(FlowLayout.LEADING));
        myPanel.add(inner);
    }
}
