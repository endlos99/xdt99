package net.endlos.xdt99.xas99r;

import com.intellij.application.options.CodeStyleAbstractConfigurable;
import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.application.options.TabbedLanguageCodeStylePanel;
import com.intellij.psi.codeStyle.CodeStyleConfigurable;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsProvider;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99RCodeStyleSettingsProvider extends CodeStyleSettingsProvider {

    @Override
    public CustomCodeStyleSettings createCustomSettings(CodeStyleSettings settings) {
        return new Xas99RCodeStyleSettings(settings);
    }

    @Nullable
    @Override
    public String getConfigurableDisplayName() {
        return "xdt99 Assembly (relaxed)";
    }

    @NotNull
    public CodeStyleConfigurable createConfigurable(@NotNull CodeStyleSettings settings, @NotNull CodeStyleSettings modelSettings) {
        return new CodeStyleAbstractConfigurable(settings, modelSettings, this.getConfigurableDisplayName()) {
            @Override
            protected CodeStyleAbstractPanel createPanel(CodeStyleSettings settings) {
                return new Xas99RCodeStyleMainPanel(getCurrentSettings(), settings);
            }
        };
    }

    private static class Xas99RCodeStyleMainPanel extends TabbedLanguageCodeStylePanel {

        public Xas99RCodeStyleMainPanel(CodeStyleSettings currentSettings, CodeStyleSettings settings) {
            super(Xas99RLanguage.INSTANCE, currentSettings, settings);
        }

        @Override
        protected void initTabs(CodeStyleSettings settings) {
            addTab(new Xas99RCodeStyleSettingsPanel(settings));
        }

    }

//    @NotNull
//    @Override
//    public Configurable createSettingsPage(CodeStyleSettings settings, CodeStyleSettings originalSettings) {
//        return new CodeStyleAbstractConfigurable(settings, originalSettings, "Xas99R") {
//            @Nullable
//            @Override
//            public String getHelpTopic() {
//                return null;
//            }
//
//            @Override
//            protected CodeStyleAbstractPanel createPanel(CodeStyleSettings settings) {
//                return new Xas99RCodeStyleSettingsPanel(settings);
//            }
//        };
//    }

}
