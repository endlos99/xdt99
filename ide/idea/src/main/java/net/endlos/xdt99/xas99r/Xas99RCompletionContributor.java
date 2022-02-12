package net.endlos.xdt99.xas99r;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.psi.PsiElement;
import com.intellij.util.ProcessingContext;
import net.endlos.xdt99.xas99r.psi.Xas99RFile;
import net.endlos.xdt99.xas99r.psi.Xas99RLabeldef;
import net.endlos.xdt99.xas99r.psi.Xas99ROpLabel;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xas99RCompletionContributor extends CompletionContributor {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();

    public Xas99RCompletionContributor() {
        extend(CompletionType.BASIC, PlatformPatterns.psiElement(Xas99RTypes.IDENT),
                new CompletionProvider<CompletionParameters>() {
                    @Override
                    protected void addCompletions(@NotNull CompletionParameters parameters,
                                                  @NotNull ProcessingContext context,
                                                  @NotNull CompletionResultSet resultSet) {
                        PsiElement parent = parameters.getPosition().getParent();
                        if (parent instanceof Xas99ROpLabel ||
                                (parent instanceof Xas99RFile &&
                                        parameters.getPosition().getPrevSibling().getNode().getElementType() == Xas99RTypes.OP_AT)) {
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
        List<Xas99RLabeldef> labeldefs = Xas99RUtil.findLabels(project, label, 0, element, 0, true);
        for (final Xas99RLabeldef labeldef : labeldefs) {
            if (labeldef.getName() != null && labeldef.getName().length() > 0) {
                resultSet.addElement(LookupElementBuilder.create(labeldef).
                        withIcon(Xas99RIcons.FILE).
                        withTypeText(labeldef.getContainingFile().getName())
                );
            }
        }
    }

}
