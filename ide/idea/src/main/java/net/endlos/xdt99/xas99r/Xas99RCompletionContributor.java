package net.endlos.xdt99.xas99r;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.util.ProcessingContext;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import org.jetbrains.annotations.NotNull;

public class Xas99RCompletionContributor extends CompletionContributor {

    public Xas99RCompletionContributor() {
        extend(CompletionType.BASIC, PlatformPatterns.psiElement(Xas99RTypes.OP_LABEL),
                new CompletionProvider<>() {
                    public void addCompletions(@NotNull CompletionParameters parameters,
                                               @NotNull ProcessingContext context,
                                               @NotNull CompletionResultSet resultSet) {
                        resultSet.addElement(LookupElementBuilder.create("Hello"));
                        //TODO
                    }
                }
        );
    }

}
