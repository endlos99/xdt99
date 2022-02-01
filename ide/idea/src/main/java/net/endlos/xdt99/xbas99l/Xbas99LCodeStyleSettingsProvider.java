package net.endlos.xdt99.xbas99l;

import com.intellij.application.options.CodeStyleAbstractConfigurable;
import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.application.options.TabbedLanguageCodeStylePanel;
import com.intellij.psi.codeStyle.CodeStyleConfigurable;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsProvider;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xbas99LCodeStyleSettingsProvider extends CodeStyleSettingsProvider {

    @Override
    public CustomCodeStyleSettings createCustomSettings(CodeStyleSettings settings) {
        return new Xbas99LCodeStyleSettings(settings);
    }

    @Nullable
    @Override
    public String getConfigurableDisplayName() {
        return "xdt99 BASIC (labels)";
    }

    @NotNull
    public CodeStyleConfigurable createConfigurable(@NotNull CodeStyleSettings settings, @NotNull CodeStyleSettings modelSettings) {
        return new CodeStyleAbstractConfigurable(settings, modelSettings, this.getConfigurableDisplayName()) {
            @Override
            protected CodeStyleAbstractPanel createPanel(CodeStyleSettings settings) {
                return new Xbas99LCodeStyleMainPanel(getCurrentSettings(), settings);
            }
        };
    }

    private static class Xbas99LCodeStyleMainPanel extends TabbedLanguageCodeStylePanel {

        public Xbas99LCodeStyleMainPanel(CodeStyleSettings currentSettings, CodeStyleSettings settings) {
            super(Xbas99LLanguage.INSTANCE, currentSettings, settings);
        }

        @Override
        protected void initTabs(CodeStyleSettings settings) {
            addTab(new Xbas99LCodeStyleSettingsPanel(settings));
        }

    }

}
