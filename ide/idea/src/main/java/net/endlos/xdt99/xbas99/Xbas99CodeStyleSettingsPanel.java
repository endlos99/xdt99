package net.endlos.xdt99.xbas99;

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

public class Xbas99CodeStyleSettingsPanel extends CodeStyleAbstractPanel {
    private static final Map<String, Xdt99CharCase> caseOptions =
            Map.of("As-is", Xdt99CharCase.ASIS,
                   "Lower", Xdt99CharCase.LOWER,
                   "Upper", Xdt99CharCase.UPPER);
    private JPanel myPanel;
    private ButtonGroup myCharCase;
    private JCheckBox myCaseComments;
    private JCheckBox myExtendedBasic;

    public Xbas99CodeStyleSettingsPanel(CodeStyleSettings settings) {
        super(settings);
        createUIComponents();
    }

    public void apply(CodeStyleSettings settings) {
        Xbas99CodeStyleSettings xbasSettings = settings.getCustomSettings(Xbas99CodeStyleSettings.class);
        xbasSettings.XBAS99_CHAR_CASE = getCharRadioValue(myCharCase);
        xbasSettings.XBAS99_CASE_COMMENTS = myCaseComments.isSelected();
        xbasSettings.XBAS99_EXTENDEDBASIC = myExtendedBasic.isSelected();
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
        Xbas99CodeStyleSettings xbasSettings = settings.getCustomSettings(Xbas99CodeStyleSettings.class);
        for (Enumeration<AbstractButton> radios = myCharCase.getElements(); radios.hasMoreElements();) {
            AbstractButton radio = radios.nextElement();
            if (caseOptions.get(radio.getText()) == xbasSettings.XBAS99_CHAR_CASE) {
                radio.setSelected(true);
                break;
            }
        }
        this.myCaseComments.setSelected(xbasSettings.XBAS99_CASE_COMMENTS);
        this.myExtendedBasic.setSelected(xbasSettings.XBAS99_EXTENDEDBASIC);
    }

    public boolean isModified(CodeStyleSettings settings) {
        Xbas99CodeStyleSettings xbasSettings = settings.getCustomSettings(Xbas99CodeStyleSettings.class);
        return xbasSettings.XBAS99_CHAR_CASE != getCharRadioValue(myCharCase) ||
               xbasSettings.XBAS99_CASE_COMMENTS != myCaseComments.isSelected() ||
               xbasSettings.XBAS99_EXTENDEDBASIC != myExtendedBasic.isSelected();
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
        return Xbas99FileType.INSTANCE;
    }

    private void createUIComponents() {
        // character case radio buttons
        JPanel myCharCasePanel = new JPanel();
        myCharCase = new ButtonGroup();
        for (String caseOption : caseOptions.keySet()) {
            JRadioButton b = new JRadioButton(caseOption);
            myCharCasePanel.add(b);
            myCharCase.add(b);
        }

        // options check boxes
        myExtendedBasic = new JCheckBox();
        myCaseComments = new JCheckBox();

        // dialog
        JPanel inner = new JPanel(new GridLayout(0, 2, 10, 0));
        inner.add(new JLabel("Character case"));
        inner.add(myCharCasePanel);
        inner.add(new JLabel("Change case of comments"));
        inner.add(myCaseComments);
        inner.add(new JLabel("TI Extended BASIC"));
        inner.add(myExtendedBasic);
        myPanel = new JPanel(new FlowLayout(FlowLayout.LEADING));
        myPanel.add(inner);
    }

}
