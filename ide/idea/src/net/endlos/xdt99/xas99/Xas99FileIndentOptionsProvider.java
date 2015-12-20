package net.endlos.xdt99.xas99;

import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CommonCodeStyleSettings;
import com.intellij.psi.codeStyle.FileIndentOptionsProvider;
import net.endlos.xdt99.xas99.psi.Xas99File;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99FileIndentOptionsProvider extends FileIndentOptionsProvider {
    @Nullable
    @Override
    public CommonCodeStyleSettings.IndentOptions getIndentOptions(@NotNull CodeStyleSettings codeStyleSettings,
                                                                  @NotNull PsiFile psiFile) {
        if (psiFile instanceof Xas99File) {
            CommonCodeStyleSettings.IndentOptions options = new CommonCodeStyleSettings.IndentOptions();
            Xas99CodeStyleSettings customSettings = codeStyleSettings.getCustomSettings(Xas99CodeStyleSettings.class);
            options.INDENT_SIZE = options.CONTINUATION_INDENT_SIZE =
                    customSettings != null ? customSettings.XAS99_MNEMONIC_TAB_STOP - 1 : Xas99CodeStyleSettings.XAS99_INDENT;
            return options;
        }
        return null;
    }
}
