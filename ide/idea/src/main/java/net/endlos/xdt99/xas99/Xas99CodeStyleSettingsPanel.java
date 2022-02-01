package net.endlos.xdt99.xas99;

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
import java.util.Arrays;
import java.util.Enumeration;
import java.util.Map;

public class Xas99CodeStyleSettingsPanel extends CodeStyleAbstractPanel {
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
    private JCheckBox myStrictSpacing;
    private JCheckBox myColonLabels;

    public Xas99CodeStyleSettingsPanel(CodeStyleSettings settings) {
        super(settings);
        createUIComponents();
    }

    public void apply(CodeStyleSettings settings) {
        Xas99CodeStyleSettings xasSettings = settings.getCustomSettings(Xas99CodeStyleSettings.class);
        xasSettings.XAS99_MNEMONIC_TAB_STOP = getIntValue(myMnemonicTabStop);
        xasSettings.XAS99_OPERANDS_TAB_STOP = getIntValue(myOperandsTabStop);
        xasSettings.XAS99_COMMENT_TAB_STOP = getIntValue(myCommentsTabStop);
        xasSettings.XAS99_CHAR_CASE = getCharRadioValue(myCharCase);
        xasSettings.XAS99_CASE_COMMENTS = myCaseComments.isSelected();
        xasSettings.XAS99_INCR_IDENT = myIncrIndent.isSelected();
        xasSettings.XAS99_STRICT = myStrictSpacing.isSelected();
        xasSettings.XAS99_COLONLABELS = myColonLabels.isSelected();
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
        Xas99CodeStyleSettings xasSettings = settings.getCustomSettings(Xas99CodeStyleSettings.class);
        this.myMnemonicTabStop.setText(String.valueOf(xasSettings.XAS99_MNEMONIC_TAB_STOP));
        this.myOperandsTabStop.setText(String.valueOf(xasSettings.XAS99_OPERANDS_TAB_STOP));
        this.myCommentsTabStop.setText(String.valueOf(xasSettings.XAS99_COMMENT_TAB_STOP));
        for (Enumeration<AbstractButton> radios = myCharCase.getElements(); radios.hasMoreElements();) {
            AbstractButton radio = radios.nextElement();
            if (caseOptions.get(radio.getText()) == xasSettings.XAS99_CHAR_CASE) {
                radio.setSelected(true);
                break;
            }
        }
        this.myCaseComments.setSelected(xasSettings.XAS99_CASE_COMMENTS);
        this.myIncrIndent.setSelected(xasSettings.XAS99_INCR_IDENT);
        this.myStrictSpacing.setSelected(xasSettings.XAS99_STRICT);
        this.myColonLabels.setSelected(xasSettings.XAS99_COLONLABELS);
    }

    public boolean isModified(CodeStyleSettings settings) {
        Xas99CodeStyleSettings xasSettings = settings.getCustomSettings(Xas99CodeStyleSettings.class);
        return xasSettings.XAS99_MNEMONIC_TAB_STOP != getIntValue(myMnemonicTabStop) ||
                xasSettings.XAS99_OPERANDS_TAB_STOP != getIntValue(myOperandsTabStop) ||
                xasSettings.XAS99_COMMENT_TAB_STOP != getIntValue(myCommentsTabStop) ||
                xasSettings.XAS99_CHAR_CASE != getCharRadioValue(myCharCase) ||
                xasSettings.XAS99_CASE_COMMENTS != myCaseComments.isSelected() ||
                xasSettings.XAS99_INCR_IDENT != myIncrIndent.isSelected() ||
                xasSettings.XAS99_STRICT != myStrictSpacing.isSelected() ||
                xasSettings.XAS99_COLONLABELS != myColonLabels.isSelected();
    }

    @Override
    protected int getRightMargin() {
        return 0;
    }

    @Override
    @Nullable
    protected EditorHighlighter createHighlighter(EditorColorsScheme scheme) {
        return null;
    }

    @Override
    @Nullable
    public JComponent getPanel() {
        return myPanel;
    }

    @Override
    @Nullable
    protected String getPreviewText() {
        return null;
    }

    @NotNull
    protected FileType getFileType() {
        return Xas99FileType.INSTANCE;
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
        myStrictSpacing = new JCheckBox();
        myColonLabels = new JCheckBox();
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
        inner.add(new JLabel("Strict spacing"));
        inner.add(myStrictSpacing);
        inner.add(new JLabel("Increase indent after RETURN"));
        inner.add(myIncrIndent);
        myPanel = new JPanel(new FlowLayout(FlowLayout.LEADING));
        myPanel.add(inner);
    }

}
