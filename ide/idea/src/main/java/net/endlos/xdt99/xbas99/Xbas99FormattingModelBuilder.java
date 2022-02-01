package net.endlos.xdt99.xbas99;

import com.intellij.formatting.FormattingContext;
import com.intellij.formatting.FormattingModel;
import com.intellij.formatting.FormattingModelBuilder;
import com.intellij.formatting.FormattingModelProvider;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import org.jetbrains.annotations.NotNull;

public class Xbas99FormattingModelBuilder implements FormattingModelBuilder {

    @Override
    @NotNull
    public FormattingModel createModel(@NotNull FormattingContext formattingContext) {
        final CodeStyleSettings codeStyleSettings = formattingContext.getCodeStyleSettings();
        return FormattingModelProvider.createFormattingModelForPsiFile(formattingContext.getContainingFile(),
                new Xbas99Block(formattingContext.getNode()), codeStyleSettings);
    }

}
