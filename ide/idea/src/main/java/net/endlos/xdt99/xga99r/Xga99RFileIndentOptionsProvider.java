package net.endlos.xdt99.xga99r;

import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CommonCodeStyleSettings;
import com.intellij.psi.codeStyle.FileIndentOptionsProvider;
import net.endlos.xdt99.xga99r.psi.Xga99RFile;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xga99RFileIndentOptionsProvider extends FileIndentOptionsProvider {

    @Nullable
    @Override
    public CommonCodeStyleSettings.IndentOptions getIndentOptions(@NotNull CodeStyleSettings codeStyleSettings,
                                                                  @NotNull PsiFile psiFile) {
        if (psiFile instanceof Xga99RFile) {
            CommonCodeStyleSettings.IndentOptions options = new CommonCodeStyleSettings.IndentOptions();
            Xga99RCodeStyleSettings customSettings = codeStyleSettings.getCustomSettings(Xga99RCodeStyleSettings.class);
            options.INDENT_SIZE = options.CONTINUATION_INDENT_SIZE = customSettings.XGA99_MNEMONIC_TAB_STOP - 1;
            return options;
        }
        return null;
    }

}
