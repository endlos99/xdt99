package net.endlos.xdt99.xas99;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.psi.PsiElement;
import com.intellij.util.ProcessingContext;
import net.endlos.xdt99.xas99.psi.*;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xas99CompletionContributor extends CompletionContributor {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();
    private final String localLabelPrefix = "!";

    public Xas99CompletionContributor() {
        extend(CompletionType.BASIC, PlatformPatterns.psiElement(Xas99Types.IDENT),
                new CompletionProvider<>() {
                    @Override
                    protected void addCompletions(@NotNull CompletionParameters parameters,
                                                  @NotNull ProcessingContext context,
                                                  @NotNull CompletionResultSet resultSet) {
                        PsiElement parent = parameters.getPosition().getParent();
                        if (parent instanceof Xas99OpLabel ||
                                parent instanceof Xas99OpAlias ||
                                (parent instanceof Xas99File && parameters.getPosition().getPrevSibling().getNode()
                                                .getElementType() == Xas99Types.OP_AT)) {
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
        if (element.getParent() instanceof Xas99OpAlias) {
            List<Xas99Labeldef> aliasdefs = Xas99Util.findAliases(project, label, true);
            for (final Xas99Labeldef aliasdef : aliasdefs) {
                if (aliasdef.getName() != null && aliasdef.getName().length() > 0) {
                    resultSet.addElement(LookupElementBuilder.create(aliasdef).
                            withIcon(Xas99Icons.FILE).
                            withTypeText(aliasdef.getContainingFile().getName())
                    );
                }
            }
        } else {
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

}
