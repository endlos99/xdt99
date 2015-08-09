package net.endlos.xdt99.xas99;

import com.intellij.application.options.CodeStyleAbstractConfigurable;
import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.openapi.options.Configurable;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsProvider;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99CodeStyleSettingsProvider extends CodeStyleSettingsProvider {
    @Nullable
    @Override
    public CustomCodeStyleSettings createCustomSettings(CodeStyleSettings settings) {
        return new Xas99CodeStyleSettings(settings);
    }

    @Nullable
    @Override
    public String getConfigurableDisplayName() {
        return "xdt99 Assembly";
    }

    @NotNull
    @Override
    public Configurable createSettingsPage(CodeStyleSettings settings, CodeStyleSettings originalSettings) {
        return new CodeStyleAbstractConfigurable(settings, originalSettings, "Xas99") {
            @Nullable
            @Override
            public String getHelpTopic() {
                return null;
            }

            @Override
            protected CodeStyleAbstractPanel createPanel(CodeStyleSettings settings) {
                return new Xas99CodeStyleSettingsPanel(settings);
            }
        };
    }
}
