package net.endlos.xdt99.xas99;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99FormattingModelBuilder implements FormattingModelBuilder {

    @Override
    @NotNull
    public FormattingModel createModel(@NotNull FormattingContext formattingContext) {
        final CodeStyleSettings codeStyleSettings = formattingContext.getCodeStyleSettings();
        return FormattingModelProvider.createFormattingModelForPsiFile(formattingContext.getContainingFile(),
                    new Xas99Block(formattingContext.getNode()), codeStyleSettings);
    }

}
