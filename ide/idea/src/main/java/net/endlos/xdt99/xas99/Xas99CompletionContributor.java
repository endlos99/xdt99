package net.endlos.xdt99.xas99;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.psi.PsiElement;
import com.intellij.util.ProcessingContext;
import net.endlos.xdt99.xas99.psi.Xas99File;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99OpLabel;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xas99CompletionContributor extends CompletionContributor {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();

    public Xas99CompletionContributor() {
        extend(CompletionType.BASIC, PlatformPatterns.psiElement(Xas99Types.IDENT),
                new CompletionProvider<CompletionParameters>() {
                    @Override
                    protected void addCompletions(@NotNull CompletionParameters parameters,
                                                  @NotNull ProcessingContext context,
                                                  @NotNull CompletionResultSet resultSet) {
                        PsiElement parent = parameters.getPosition().getParent();
                        if (parent instanceof Xas99OpLabel ||
                                (parent instanceof Xas99File &&
                                        parameters.getPosition().getPrevSibling().getNode().getElementType() == Xas99Types.OP_AT)) {
                            getCompletions(parameters.getPosition(), resultSet);
                        }
                    }
                }
        );
    }

    private void getCompletions(@NotNull PsiElement element, @NotNull CompletionResultSet resultSet) {
        Project project = element.getProject();
        String label = element.getText().toUpperCase();
        if (label.endsWith(dummy)) {
            label = label.substring(0, label.length() - dummy.length());
        }
        List<Xas99Labeldef> labeldefs = Xas99Util.findLabels(project, label, 0, element, 0, true);
        for (final Xas99Labeldef labeldef : labeldefs) {
            if (labeldef.getName() != null && labeldef.getName().length() > 0) {
                resultSet.addElement(LookupElementBuilder.create(labeldef).
                        withIcon(Xas99Icons.FILE).
                        withTypeText(labeldef.getContainingFile().getName())
                );
            }
        }
    }

}
