package net.endlos.xdt99.xga99;

import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.openapi.editor.colors.EditorColorsScheme;
import com.intellij.openapi.editor.highlighter.EditorHighlighter;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import net.endlos.xdt99.common.Xdt99CharCase;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.awt.*;
import java.util.Enumeration;
import java.util.Map;

public class Xga99CodeStyleSettingsPanel extends CodeStyleAbstractPanel {
    private static final Map<String, Xdt99CharCase> caseOptions =
            Map.of("As-is", Xdt99CharCase.ASIS,
                   "Lower", Xdt99CharCase.LOWER,
                   "Upper", Xdt99CharCase.UPPER);
    private JPanel myPanel;
    private JTextField myMnemonicTabStop;
    private JTextField myOperandsTabStop;
    private JTextField myCommentsTabStop;
    private ButtonGroup myCharCase;
    private JCheckBox myCaseComments;
    private JCheckBox myIncrIndent;
    private JCheckBox myStrictMode;
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
        xgaSettings.XGA99_CHAR_CASE = getCharRadioValue(myCharCase);
        xgaSettings.XGA99_CASE_COMMENTS = myCaseComments.isSelected();
        xgaSettings.XGA99_INCR_INDENT = myIncrIndent.isSelected();
        xgaSettings.XGA99_STRICT = myStrictMode.isSelected();
    }

    private int getIntValue(JTextField field) {
        try {
            return Integer.parseInt(field.getText());
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    private Xdt99CharCase getCharRadioValue(ButtonGroup group) {
        for (Enumeration<AbstractButton> radios = group.getElements(); radios.hasMoreElements();) {
            AbstractButton radio = radios.nextElement();
            if (radio.isSelected()) {
                return caseOptions.get(radio.getText());
            }
        }
        return Xdt99CharCase.ASIS;
    }

    protected void resetImpl(CodeStyleSettings settings) {
        Xga99CodeStyleSettings xgaSettings = settings.getCustomSettings(Xga99CodeStyleSettings.class);
        this.myMnemonicTabStop.setText(String.valueOf(xgaSettings.XGA99_MNEMONIC_TAB_STOP));
        this.myOperandsTabStop.setText(String.valueOf(xgaSettings.XGA99_OPERANDS_TAB_STOP));
        this.myCommentsTabStop.setText(String.valueOf(xgaSettings.XGA99_COMMENT_TAB_STOP));
        for (Enumeration<AbstractButton> radios = myCharCase.getElements(); radios.hasMoreElements();) {
            AbstractButton radio = radios.nextElement();
            if (caseOptions.get(radio.getText()) == xgaSettings.XGA99_CHAR_CASE) {
                radio.setSelected(true);
                break;
            }
        }
        this.myCaseComments.setSelected(xgaSettings.XGA99_CASE_COMMENTS);
        this.myIncrIndent.setSelected(xgaSettings.XGA99_INCR_INDENT);
        this.myStrictMode.setSelected(xgaSettings.XGA99_STRICT);
    }

    public boolean isModified(CodeStyleSettings settings) {
        Xga99CodeStyleSettings xgaSettings = settings.getCustomSettings(Xga99CodeStyleSettings.class);
        return xgaSettings.XGA99_MNEMONIC_TAB_STOP != getIntValue(myMnemonicTabStop) ||
                xgaSettings.XGA99_OPERANDS_TAB_STOP != getIntValue(myOperandsTabStop) ||
                xgaSettings.XGA99_COMMENT_TAB_STOP != getIntValue(myCommentsTabStop) ||
                xgaSettings.XGA99_CHAR_CASE != getCharRadioValue(myCharCase) ||
                xgaSettings.XGA99_CASE_COMMENTS != myCaseComments.isSelected() ||
                xgaSettings.XGA99_INCR_INDENT != myIncrIndent.isSelected() ||
                xgaSettings.XGA99_STRICT != myStrictMode.isSelected();
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
        for (String caseOption : caseOptions.keySet()) {
            JRadioButton b = new JRadioButton(caseOption);
            myCharCasePanel.add(b);
            myCharCase.add(b);
        }

        // options check boxes
        myIncrIndent = new JCheckBox();
        myStrictMode = new JCheckBox();
        myCaseComments = new JCheckBox();

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
        inner.add(new JLabel("Change case of comments"));
        inner.add(myCaseComments);
        inner.add(new JLabel("Strict mode"));
        inner.add(myStrictMode);
        inner.add(new JLabel("Increase indent after RETURN"));
        inner.add(myIncrIndent);
        myPanel = new JPanel(new FlowLayout(FlowLayout.LEADING));
        myPanel.add(inner);
    }

}
