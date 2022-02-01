package net.endlos.xdt99.xas99r;

import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CommonCodeStyleSettings;
import com.intellij.psi.codeStyle.FileIndentOptionsProvider;
import net.endlos.xdt99.xas99r.psi.Xas99RFile;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99RFileIndentOptionsProvider extends FileIndentOptionsProvider {

    @Override
    @Nullable
    public CommonCodeStyleSettings.IndentOptions getIndentOptions(@NotNull CodeStyleSettings codeStyleSettings,
                                                                  @NotNull PsiFile psiFile) {
        if (psiFile instanceof Xas99RFile) {
            CommonCodeStyleSettings.IndentOptions options = new CommonCodeStyleSettings.IndentOptions();
            Xas99RCodeStyleSettings customSettings = codeStyleSettings.getCustomSettings(Xas99RCodeStyleSettings.class);
            options.INDENT_SIZE = customSettings.XAS99_MNEMONIC_TAB_STOP - 1;
            // sometimes, CONT_IDENT_SIZE is added on top of INDENT_SIZE (IDEA), sometimes not (PyCharm)
            options.CONTINUATION_INDENT_SIZE = customSettings.XAS99_INCR_IDENT ? options.INDENT_SIZE : 0;
            return options;
        }
        return null;
    }

}
