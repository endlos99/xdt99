package net.endlos.xdt99.xas99;

import com.intellij.application.options.CodeStyleAbstractConfigurable;
import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.application.options.TabbedLanguageCodeStylePanel;
import com.intellij.psi.codeStyle.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99CodeStyleSettingsProvider extends CodeStyleSettingsProvider {

    @Override
    public CustomCodeStyleSettings createCustomSettings(CodeStyleSettings settings) {
        return new Xas99CodeStyleSettings(settings);
    }

    @Override
    @Nullable
    public String getConfigurableDisplayName() {
        return "xdt99 Assembly";
    }

    @NotNull
    public CodeStyleConfigurable createConfigurable(@NotNull CodeStyleSettings settings, @NotNull CodeStyleSettings modelSettings) {
        return new CodeStyleAbstractConfigurable(settings, modelSettings, this.getConfigurableDisplayName()) {
            @Override
            protected CodeStyleAbstractPanel createPanel(CodeStyleSettings settings) {
                return new Xas99CodeStyleMainPanel(getCurrentSettings(), settings);
            }
        };
    }

    private static class Xas99CodeStyleMainPanel extends TabbedLanguageCodeStylePanel {

        public Xas99CodeStyleMainPanel(CodeStyleSettings currentSettings, CodeStyleSettings settings) {
            super(Xas99Language.INSTANCE, currentSettings, settings);
        }

        @Override
        protected void initTabs(CodeStyleSettings settings) {
            addTab(new Xas99CodeStyleSettingsPanel(settings));
        }

    }

}
