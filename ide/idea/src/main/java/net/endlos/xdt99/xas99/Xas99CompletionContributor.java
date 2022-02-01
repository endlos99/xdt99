package net.endlos.xdt99.xas99;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.util.ProcessingContext;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;

public class Xas99CompletionContributor extends CompletionContributor {

    public Xas99CompletionContributor() {
        extend(CompletionType.BASIC, PlatformPatterns.psiElement(Xas99Types.OP_LABEL),
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
